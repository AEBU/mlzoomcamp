# Equipment Assessment Request Forecast
## Description
> There is a demand for requests to evaluate electronics equipments that arrive to the company on a monthly basis, for this reason a model is needed that allows knowing the number of requests that can arrive in the month to better allocate resources.


## Data
> Request data for revision of different electronic equipment 
> From 2019 to 2021 

## Overview Notebook
> Data download (data/appraisal_data.csv)
- It allows for verifying the data available for analysis.
> EDA
- Filter columns
- Change variables types
- Verify Estacionary
> Model Selection (and Parameter Tuning)
- ForecasterAutoreg  (RandomForestRegressor)
- backtesting_forecaster
- ForecasterAutoregDirect (Lasso)
- Random Forest
- XGBoost
> Final MOdel
- ForecasterAutoregDirect

## Exporting notebook to script
- View *scripts_deployment/train.py*

## Reproducibly
-   Execute */process/AlexisBautista_notebook.ipynb*

## Model Deployment
- Steps
    - execute python script */scripts_deployment/predict_flask.py*
    - execute python script */scripts_deployment/predict_test.py*
        - To get the score of career of scholarship
            - y_pred_log: value logarithm
            - y_pred_real: value with out logarithm (real)

## Dependency and environment Managment
- Steps
    - Below *scripts_deployment* we have a environment with pipenv
    - Localize in folder and execute this commands:
        - *pipenv shell* # To install and create virtual environment
        - *gunicorn --bind 0.0.0.0:9696 predict_flask:ap* # *gunicorn --bind 0.0.0.0:9696 <file_to_run>:<name_app>* Execute app with gunicorn

## Containerization (Pending)
## Cloud deployment	 (Pending)

# References
- https://www.cienciadedatos.net/documentos/py27-forecasting-series-temporales-python-scikitlearn.html
