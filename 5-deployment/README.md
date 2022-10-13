# Gestor de dependencias
> Para este caso usaremos pipenv, pero se puede usar virtual env, conda, poetry.

    pip install pipenv
    pipenv install Scikit-Learn==1.0.2
    pipenv install flask
    pipenv install gunicorn

# Para activr el ambiente
    pipenv shell
    which flask

# Create enviroment with conda

    conda activate python3.9.12
    conda deactivate
    conda create -n "python3.9.12" python=3.9.12 

# Download files
    ipython

    PREFIX='https://raw.githubusercontent.com/alexeygrigorev/mlbookcamp-code/master/course-zoomcamp/cohorts/2022/05-deployment/homework'

    !wget $PREFIX/model1.bin
    !wget $PREFIX/dv.bin

## Predicción con local
python app-env/app.py
## Prediction with flask
- service-flask
- app.py
- request

## Docker
### Verificación
    docker exec -it ID_CONT sh
    ps fax # Comandas que está corriendo
### Construcción
    COPY . . # Copia todo el contenido
### Ejecución
    pull request 
    docker build -t credit-prediction .
    docker run  -it --rm --entrypoint=bash  credit-prediction 
    docker run -it -p 9696:9696 
    docker run -it credit-prediction sh #Para entrar al contenedor 
    credit-prediction:latest