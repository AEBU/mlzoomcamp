# Bentoml
[Documentation](https://docs.bentoml.org/en/latest/): Hace facil la creacioń de servicios de predicción basados en ML que están listos para implementar y escalar.
- Acelear y estandarice los proesos tomando ML models a producción.
- Cree servicios de predicción escalables y de alto rendimiento
- Implemente, suprevise y opoere continuamente servicios de predicción en producción.


## Commands

- bentoml.xlgeboost.save_model
Permite guardar el modelo, y obtenrá un tag asociado al modelo que está creando.

Model(tag="credit_risk_model:fp4tfjkrwkbjvzar", path="/home/lex/bentoml/models/credit_risk_model/fp4tfjkrwkbjvzar/")
> Para obtener el modelo actual 
-tag_model:latest 

> Para recargar cada vez que cambiamos algo al server
- bentoml serve service.py:svc --reload 
- Opcional el puerto: --port=3001
> Para guardar objetos adicionales que el modelo necesite
- ..save_model(....,
                custom_objects= {
                    "dictVectorizer":dv
                })

> Permite correr el servidor
- bentoml serve name_file:variable_servicio
- Pagína que describe las APIs creadas
    - http://localhost:3000

> Para listar modelos generados
- bentoml models list
- Tag- Marco usado - Size y fecha creación
> Para importar modelo generado
- bentoml models import nameModel.bentoml

> Para metadata del modelo
- bentoml models get TAG
- Metadata , nombre etiqueta, versión del framework, versión BentoML, versión python
- Se debe tener la misma versión del framework_versions,  porque puede obtener resultados diferentes si este cambia, lo mismo con la versión del Python. Estas versiones en diferente de pip env es que determina automáticamente estas versiones.
y lo coloca automáticamente como dependencias al modelo.

> Para construir un bentoml, podemos usar un file bentoml.yaml

````yaml
service: file.py:name_service
labels: #Clave valor etiquetas de importancia o negocio
    owner: bentoml-team
    project: gallery
    # Cosas necesarias para recorddarle al negocio lo que se está realizando.
include: 
- "*.py" # Que files necesitamos en el  servicio bentoml, especialmente si su bentoml es parte de un repositorio más grande donde no necesitemos todos los files.
python: 
    packages: #Paquetes de python que estamos uasndo.
    - xgboost
    - sklearn
    - ""package==2"
    - "torchvision>=2, <0,.3"
    requirements: "path" # pip install options
# No solo genera datos de las librerías sino también del entorno que se ejecutará
docker:
    distro: debian
    cuda_version: "12,2" # Si la máquina tiene habilitado una GPU

````

> COnstruir una imagen bentoml
- bentoml build  # Toma por default el file bentofile.yaml
- TOma todas las dependencias correctas y crea un único desplegable, 
Esto hará ver su archivo de servicio y extraer los modelos y tomar todas las dependencias y crear un solo file.
> Directorio para verificar la imagen construída
- cd 
- cd bentoml/bentos
- cd tag.split(":")[0]
- cd tag.split(":")[1]
- tree # Para ver los files dentro de cada carpeta
> Files encontrados
- openapi.yaml # Permite tener las interfaces de usuario que están expuestas swagger-
- Se crea automáticamente un dockerfile, para luego se edite
- en la folder models, crea todo sus modelos y versiones con sus custom_objects

- La idea detrás de una estructura personalizada es proporcionalr una forma estandarizada de rear todo lo que un SERVICIO de machine learning podría requerir, por loq ue necesiteamos que todas esas cosas estén dentro de un mismo contenedor.                              
> Necesito construir el contenedor
- bentoml containerize credit_risk_classifier:6vlz2rssx6tyfzar
- En este contenedor coiene la imgaen docker creada, y nos da el paso para poder ejecutarlo con docker run.
El tiempo dependerá de la cantidad de veces que ejecutó y se almacenó en la caché de docker.

> Para listar las imágenes
- docker images
> Para ejecutar la imagen
- docker run -it --rm -p 3000:3000 ID IMGAE
- docker run -it --rm -p 3000:3000 credit_risk_classifier:6vlz2rssx6tyfzar serve --production
- localhost:3000

#### Commands Linux
- top: Ver un explorador de tareas
- udo ss -lptn 'sport = :3000: Que datos se está ejecutando en ese puerto
- kill PID: Eliminar un proceso
## Validation Data

Es Necesario validar los datos que entran ya que puede haber el caso que se envía nulos, o datos erróneos pero el modelo predice de igual manera. Lo cual puede ser perjudicial para el negocio.
Para esto usamos **pydantinc**.

Es muy útil validar los tipos de datos, ya que puede existir casos que no se sabe que envían.

> Tipos de datos.
- Se puede enviar varios tipos de datos:
    - CSV
    - JSON
    - Images
    - Dataframes
    - Numpy Arrays
        ```python
        @svc.api(input=NumpyNdarray(shape = (-1,29), enforce_shape=True), output=JSON())
        #shape (-1) quiere decir muchas fmatrices negativas en la primera dimensión
        # shape (29) quiere decir 29 matrices en la segunda matriz
        # enforce.dtype = True, dtype= np.float32
        ```

## High-Performance Serving
Configuración por defecto para una falla en bentoml es de 1 segundo (cambiable).

- Locus:
    - Número de usuarios
    - Que tán rápido debo inciarlos 
    - Podemos verificar cuantas veces por segundo se hace un request.
    - Latencia de solicitud promedio
    - Percentil 90 y 99
    - Máximo en general

- Ejemplo:
    - Concurrencia: 50
        - usuarios concurrentes
    - Spawn rate (usuarios iniicados / segundo)
        - 10 (low) , 50 (high)
    - Metrics
        - Percentiles, maximum, request.latencia
- Optimization (async- await)
    - Sin async esperabamos a atender la solicitud una a una, es decir, esperamos a que se ejecute un request realizado.Pero con async esto permite realizar en paralelo. Esto permite realizar bentoml o FastAPI

    > En algunas pruebas se tendrá fallas pero es porque el servidor arraca en frío, y es porque un servidor cuando arranca por primera vez necesita almacenar algunas cosas en caché, para que funcione realmente al máximo.

- Optimización
    - Cuando se crea un servicio en la máquina se está creando un proceso y las CPUs de la máquina trabajan en ese proceso, el proceso es cuando se tiene solo un proceso solo una CPU puede trabajar en ese proceso a la vez (es decir, solo consume una CPU) , por lo que si deseamos usar todas las CPUs debemos tener varios procesos trabajando en paralelo.


    - Problemas:
        - Que el modelo sea demaisado grando y cuando se creaen las réplicas sean demasiado grandes, por lo que al estar en memoria se pueden quedar sin espacio
        - QUe enviemos todas las solicitudes una a la vez, 
            - Podemos combinar en lotes las predicciones que estamos enviando al modelo y enviarlas a la vez, podemos tener un aumento de la eficiencia.
            [**Micro batches**](https://docs.bentoml.org/en/0.13-lts/guides/micro_batching.html): feature de bentoml, se puede dispersar a los trabajadores de transformación y luego cuando se llama a la predicción en realidad se agrupan en lotes más pequeños para su respectiva predicción. 
            [Pasos](https://docs.bentoml.org/en/latest/guides/batching.html):
                - 1 volver a guardar el modelo con la característica signatures: predict, batchable and dimension of batch. Con ello concatenamos en una matriz, los inputs.
                - Ejecutar *bentoml serve --production*, con --production tenemos a más de un proceso para nuestros workers web(servicios).
                - Podemos ajustar el tamaño de los lotes (Max batch size -  no superar un cierto tamaño antes de enviar estas entradas) en función de de los últimos lotes que hemos ejecutado. Tomar en cuenta que no espera más de un tiempo específico (Max Latency - no espera más de 5 milisegundos anes de enviar al lote) que lleguen las solicitudes.
                - Se puede configurar estos parámetros usando un archivo de configuración. *bentoconfiguration.yaml*
                - Tomar en cuenta que podemos tener múltiples runners en la misma predicción. [Concurrencia de modelos](https://docs.bentoml.org/en/latest/concepts/runner.html)
