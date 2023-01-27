#@ Import libraries
import pandas as pd
import numpy as np
import pickle

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Lasso

from skforecast.ForecasterAutoregDirect import ForecasterAutoregDirect
from skforecast.model_selection import grid_search_forecaster

# # Functions

def rmse(y_true, y_pred ):
    se = (y_true - y_pred) ** 2
    mse = se.mean()
    return np.sqrt(mse)


def prepare_date_format(months_request, sucursal, fechas_date_month, steps):
    months_request_analyze = months_request.loc[:,[fechas_date_month, sucursal]]
    months_request_analyze = months_request_analyze.set_index(fechas_date_month)
    months_request_analyze = months_request_analyze.rename(columns={sucursal: 'y'})
    months_request_analyze = months_request_analyze.asfreq('MS')
    months_request_analyze = months_request_analyze.sort_index()
    datos_train = months_request_analyze[:-steps]
    datos_test  = months_request_analyze[-steps:]
    #months_request_analyze.reset_index()
    return datos_train, datos_test

def prepare_date_format_exog(months_request, sucursal, fechas_date_month, steps, exog):
    months_request_analyze = months_request.loc[:,[fechas_date_month, sucursal, exog]]
    months_request_analyze = months_request_analyze.set_index(fechas_date_month)
    months_request_analyze = months_request_analyze.rename(columns={sucursal: 'y'})
    months_request_analyze = months_request_analyze.asfreq('MS')
    months_request_analyze = months_request_analyze.sort_index()
    datos_train = months_request_analyze[:-steps]
    datos_test  = months_request_analyze[-steps:]
    #months_request_analyze.reset_index()
    return datos_train, datos_test


def scaler_months(months_request,col ):
    values = months_request[col].values
    values = values.reshape((len(values), 1))
    scaler = StandardScaler()
    scaler = scaler.fit(values)
    normalized = scaler.transform(values)
    return scaler, normalized


#@ Create variable exogen
def create_exogen_variable(date_data):
    # date_data = df.fechas_date_month
    if (date_data < pd.to_datetime('2020-03-01')):
        return 0
    elif(date_data >=  pd.to_datetime( '2020-03-01')) and (date_data <=  pd.to_datetime('2020-08-01') ):
        return 1
    else:
        return 0.80


data_download = 'https://raw.githubusercontent.com/AEBU/mlzoomcamp/main/capstone-project2/data/appraisal_data.csv'
data_output = 'appraisal_data.csv'
#@ Import dataset
request_equipments = pd.read_csv(data_download)
#@ FILTER ONLY NECCESARY FEATURES
request_appr = request_equipments[['appraisal','fechas_date_month']]
request_appr.head().T

# # Data Cleaning
request_appr['fechas_date_month'] = pd.to_datetime(request_appr['fechas_date_month'], format='%Y-%m-%d')
#@ Create exogen variable with perception of covid 
request_appr['exog_1'] = request_appr.fechas_date_month.apply(create_exogen_variable)

# ## Split Train-Test
data_train, data_test  = prepare_date_format(request_appr, 'appraisal', 'fechas_date_month', 12)
steps = 12 
# ### Forecaster Standar
# Grid search de hiperparámetros
# ==============================================================================
forecaster = ForecasterAutoregDirect(
                regressor     = Lasso(random_state=123),
                transformer_y = StandardScaler(),
                steps         = steps,
                lags          = 6 # Este valor será remplazado en el grid search
             )

param_grid = {'alpha': np.logspace(-5, 5, 10)}
lags_grid = [5, 12, 20]
resultados_grid = grid_search_forecaster(
                    forecaster         = forecaster,
                    y                  = data_train['y'],
                    param_grid         = param_grid,
                    lags_grid          = lags_grid,
                    steps              = steps,
                    refit              = True,
                    metric             = rmse,
                    initial_train_size = int(len(data_train)*0.9),
                    fixed_train_size   = False,
                    return_best        = True,
                    verbose            = False
                )
# Predicciones
# ==============================================================================
predicciones = forecaster.predict()
output_file = f'model_appr.bin'
f_out = open(output_file, 'wb') 
pickle.dump(forecaster, f_out)
f_out.close()