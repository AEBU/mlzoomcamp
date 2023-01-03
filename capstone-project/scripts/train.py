#@ Import libraries
import pandas as pd
import numpy as np
import os
import pickle

from sklearn.metrics import mutual_info_score
from datetime import datetime
from datetime import date
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import RandomForestRegressor

#TODO: Verificar Estas líneas de código.
from IPython.display import display
get_ipython().run_line_magic('matplotlib', 'inline')



#@ Download Data
data_download = 'https://raw.githubusercontent.com/AEBU/mlzoomcamp/main/capstone-project/senescyt_becas_2022febrero.zip'
data_output_zip = 'scolarships_ec.zip'
filename = 'senescyt_becas_2022febrero.csv'

#TODO: Verificar estas líneas de código
os.system('wget $data_download -O $data_output_zip')
os.system('unzip $data_output_zip')

#@Define functions

def calculate_age(date_age, type_calculate = 1):
    """Allows to calculate the age of an individual
    Keyword arguments:

        date_age Date birthday
        type_calculate type of calculation 
            1   age
            2   only change format
    """
    try: 
        if type_calculate == 1:
            birth_day = pd.to_datetime(date_age, format='%d/%m/%Y')
            today = date.today()
            return today.year - birth_day.year - ((today.month, today.day) < (birth_day.month, birth_day.day))
        elif type_calculate == 2:
            return pd.to_datetime(date_age, format='%d/%m/%Y')
    except Exception as e:
        print(e)
        return np.nan


def change_replace(str_replace, str_input_replace, str_out_replace):
    """ Allow replace string of strings
    Keyword arguments:
        str_replace string to replace
        str_input_replace String in replace 
        str_out_replace String out replace
    """
    try: 
        return str_replace.replace(str_input_replace,str_out_replace )
    except Exception as e:
        return str_replace
        

def mutual_info_amount_score(series, target_variable):
    """ Allow calculate the mutual information of a target variable
    Keyword arguments:
        series Information in series of variable to compare
        target_variable Target variable to compare
    """
    return mutual_info_score(series, target_variable)        

def rmse(y, y_pred):
    """ Allow calculate RMSE of values predict and real
        Keyword arguments:
            y Real values of target variable.
            y_pred Predicted values of 
    """
    se = (y - y_pred) ** 2
    mse = se.mean()
    return np.sqrt(mse)    
    


#@ Data Preparation
##@ Read document
df_scolaships = pd.read_csv(filename, encoding='latin-1', sep=';', skiprows=1, dtype=str)
##@ FILTER ONLY NECCESARY FEATURES
df_scolaships = df_scolaships.iloc[: , 0:38].dropna(subset=['ID UNICO','ETNIA','GENERO'])
##@ Variable standardization
df_scolaships.columns = df_scolaships.columns.str.lower().str.strip().str.replace(' ', '_')
string_columns = list(df_scolaships.dtypes[df_scolaships.dtypes == 'object'].index)

for col in string_columns:
    df_scolaships[col] = df_scolaships[col].str.lower().str.strip()\
                            .replace('no registrado', np.nan)\
                            .replace('%', '')\
                            .replace('-', None)

#@ Data Cleaning - Missing data
##@ Data Imputation of target variable
df_scolaships.dropna(subset=['monto_contratado'], inplace=True)
##@ Cleaning variables
df_scolaships.monto_contratado =df_scolaships.monto_contratado.apply(lambda x: change_replace(x,'.',''))
df_scolaships['tipo_discapacidad'] = df_scolaships['tipo_discapacidad'].replace('-', 'ninguna').replace('0', 'ninguna').fillna('ninguna')
df_scolaships['porcentaje_discapacidad'] = df_scolaships['porcentaje_discapacidad'].str.replace('%', '').str.replace('-', '0').fillna('0')
df_scolaships['etnia'] = df_scolaships['etnia'].fillna('no_definida')
df_scolaships['discapacidad'] = df_scolaships['discapacidad'].fillna('no')
df_scolaships['provincia_nacimiento_homologada'] = df_scolaships['provincia_nacimiento_homologada'].fillna('pichincha') # Se reemplaza con la moda

##@ Change variables types 
df_scolaships['age'] = df_scolaships.fecha_de_nacimiento.apply(lambda x: calculate_age(x))
df_scolaships['fecha_inicio_estudios_rec'] =  pd.to_datetime(df_scolaships['fecha_inicio_financiamiento'], format='%d/%m/%Y') 
df_scolaships['anio_inicio_estudios'] =  pd.DatetimeIndex(df_scolaships['fecha_inicio_estudios_rec']).year
df_scolaships['age'] = df_scolaships.age.astype('float32')
df_scolaships.monto_contratado = df_scolaships.monto_contratado.astype('float32')

#@Filter Data
##@ Filter year to analyze
minimum_year_filter = 2014
##@ Filter only data greater than minimum year
df_scolaships = df_scolaships[df_scolaships.fecha_inicio_estudios_rec.dt.year > minimum_year_filter]

#@ Choose only important features
categorical = [
    'etnia', 'genero', 'discapacidad', 'tipo_discapacidad',
    'estado_civil',  'provincia_nacimiento_homologada', 
    'canton_nacimiento', 'provincia_residencia_homologada', 
    'programa_general', 
    'destino', 'financiamiento',
    'pais_de_estudios', 'ies_de_estudios_homologada',
    'nivel_detallado', 'carrera', 'area_de_estudio',
    ########################## Elminados por no relevancia ##########################
    # 'id_unico',  
    # 'estado_estudiante', 'estado_beca',
    # 'ies_de_estudios_homologada'
    # convocatoria -- Porque es el año en el que fue generado laconvocatoria
    # porcentaje_discapacidad REVISAR
    ########################## Elminados por que ya se tiene su derivado ##########################
    #'fecha_de_nacimiento', 'fecha_fin_estudios','fecha_inicio_estudios_rec',
    #'fecha_inicio_estudios', 'fecha_de_suscripcion',
    #'fecha_inicio_financiamiento', 'fecha_fin_financiamiento', 
    # 'provincia_nacimiento',  'zona_senplades_lugar_nacimiento', 
    # 'provincia_residencia', 'canton_residencia', 
    # 'subprograma',
    # 'nivel_de_estudios'
    #  'subarea_de_estudio', 'area_estudio_detallado'
    # Componente => Se elimina porque deberíamos tener algo que las agrupe
    # centro_estudios_beca Se tiene la homoloagada
]
numerical = ['monto_contratado', 'age']
#@Split train-test
df_full_train, df_test = train_test_split(df_scolaships[categorical + numerical], test_size=0.2, random_state=1)
df_train, df_val = train_test_split(df_full_train, test_size=0.25, random_state=1)
df_train = df_train.reset_index(drop=True)
df_val = df_val.reset_index(drop=True)
df_test = df_test.reset_index(drop=True)
y_train = np.log1p(df_train.monto_contratado.values)
y_val = np.log1p(df_val.monto_contratado.values)
y_test = np.log1p(df_test.monto_contratado.values)
del df_train['monto_contratado']
del df_val['monto_contratado']
del df_test['monto_contratado']

#@Choose columns
columns = categorical+ [ 'age']
#@One hot encoding
dv = DictVectorizer(sparse=False)
train_dict = df_train[columns].to_dict(orient='records')
X_train = dv.fit_transform(train_dict)
val_dict = df_val[columns].to_dict(orient='records')
X_val = dv.transform(val_dict)

#@Training Model
max_depth = 15
min_samples_leaf = 1
n_estimators = 200
rf = RandomForestRegressor(n_estimators=n_estimators,
                            max_depth=max_depth,
                            min_samples_leaf=min_samples_leaf,
                            random_state=1)
rf.fit(X_train, y_train)

#@Save the model to pickle
output_file = './model/model_scolarship=0.4.bin'

f_out = open(output_file, 'wb') 
pickle.dump((dv, rf), f_out)
f_out.close()

