# Amount assigned for type of scholarships
## Description
> Funding budgets for scholarships obtained are difficult to calculate due to different characteristics or items. For this reason, it is desired to calculate an equitable formula that allows a methodology for liquidating amounts assigned for a scholarship obtained based on a Machine Learning model.


## Data (data/senescyt_becas_2022febrero.zip)
> An education database with assigned amounts is used [link](https://www.datosabiertos.gob.ec/group/edu).
> From 2001 to 2021 

## Overview Notebook
> Data download (process/notebook.ipynb)
- It allows for verifying the data available for analysis.
> EDA
- Filter columns
- Variable standardization
- Types and features
- Data missing
- Missing data
- Change variables types
- Feature enginering
> Model Selection (and Parameter Tuning)
- Linear Regression
- RidgeRegression
- Decision Tree
- Random Forest
- XGBoost
> Final MOdel
- Random Forest

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
- https://www.datosabiertos.gob.ec/dataset/becas
- https://github.com/alexeygrigorev/mlbookcamp-code/tree/master/course-zoomcamp/projects
- https://github.com/alexeygrigorev/mlbookcamp-code/blob/master/course-zoomcamp/cohorts/2022/projects.md#capstone-2
- https://docs.google.com/spreadsheets/d/e/2PACX-1vQCwqAtkjl07MTW-SxWUK9GUvMQ3Pv_fF8UadcuIYLgHa0PlNu9BRWtfLgivI8xSCncQs82HDwGXSm3/pubhtml
