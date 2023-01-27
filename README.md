# Apuntes DataScience

## Isolation
- environments
    - virtual env
    - pipenv conda
    - pipenv poetry
- Docker
    - Dependencias de sistema
- Cloud
    - Subida de contenedores Docker
    - Subida de Kubernetes
- Conda:
    - conda create --name <name_env> python=<version_package>
    - conda activate <name_env>
    - conda deactivate
## Deployar un modelo
- Pasos
    - pip install pipenv
    - pipenv install dependencies
    This create two files (Pipfile and Pipfile.lock)
- [Pip install](https://www.freecodecamp.org/espanol/news/como-usar-pip-install-en-python/) -> Usamos como un gestor de dependencias que descarga de forma global por default, se puede usar pip2 para Python2 y pip3 para Python3.
- RUN vs (ENTRYPOINT y CMD)
    - RUN es para ejecutar en la creación o construcción de la imagen, por ejemplo paquetes dentro de la imagen y el CMD y ENTRYPOINT es para ejecutar cuando ya se tiene una imagen y se quiere ejecutar.

    - ENTRYPOINT y CMD los dos permiten ejecutar comandos cuando corremos el contenedor, y ya se tiene la imagen creada, sin embargo, CMD es para correr un comando por defecto que puede ser reemplazable por alguna configuración al realizar el exec. Usualmente para levantar servicios, servidores, servicios que se quedan activos mediante el server esté corriendo.    
    ENTRYPOINT, está pensado para usar el contenedor como si fuera un ejecutable, le pasamos argumentos o algún archivo y el contenedor lo ejecuta. 
    Al ejecutar comandso que no se deban sobreescribir (si se puede mediante argumentos pero no es ideal), es útil usarlo como si fuera un ejecutable.por ejemplo python, y al correrle mandarle a que ejecute nuestro archivo .py

- [Gunicorn](https://gunicorn.org/)
    - Se usa Gunicorn porque es un WSGI, que administra solicitudes y comunicación, reaccionar a muchas solicitudes y distribución de carga por eso es común usarla en producción.
    Se puede usar [FastAPI](https://fastapi.tiangolo.com/) que también cumple con este propósito.

- Escaling
    - Horizontal: Aumentar más equipos
        - Scaling UP: Aumentar equipos bajo demanda
        - Scaling Down: Disminuir equipos que no se usan.
    - Vertical: Aumentar recursos en el mismo equipo

- Pass notebook to .py
    jupyter nbconvert AlexisBautista_notebook.ipynb --to python