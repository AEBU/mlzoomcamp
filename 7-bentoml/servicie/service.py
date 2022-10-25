import bentoml
from bentoml.io import JSON
# Validación de datos 
from pydantic import BaseModel
from bentoml.io import NumpyNdarray


class CreditApplication(BaseModel) :
    seniority: int
    home: str
    time: int
    age: int
    marital: str
    records: str
    job: str
    expenses: int
    income: float
    assets: float
    debt: float
    amount: int
    price: int


# extraer el modelo con todos sus metadatos 
#model_ref = bentoml.xgboost.get("credit_risk_model:fp4tfjkrwkbjvzar")
model_ref = bentoml.xgboost.get("credit_risk_model:latest")#:latest -- para el último subido
dv = model_ref.custom_objects['dictVectorizer']


# Runner es la abstracción del bentoml para modelo en sí.
# Permite crear una capa de abstracción que hace escalar el modelo por separado del resto
# Accede al modelo y realiza la predicción
model_runner = model_ref.to_runner()

svc = bentoml.Service("credit_risk_classifier", runners=[model_runner])

# POdemos pasar images, vector, matrix, files
@svc.api(input=JSON(), output=JSON())
def classify_init(application_data):
    print('init')
    prediction = model_runner.predict.run(application_data)
    return "Approved"

@svc.api(input=JSON(), output=JSON())
def classify_vector(application_data):
    #Usualmente acá es donde se hace data cleaning a la data
    vector = dv.transform(application_data)    
    prediction = model_runner.predict.run(vector)

    ## Extra logica con business logic (BANCK, ISSUES, etc)
    result = prediction[0]
    if result > 0.5:
        return {
            'status': 'DECLINED'
        }
    elif  result > 0.25:
        return {
            'status': 'MAYVE'
        }
    else:
        return {
            'status': 'APPROVED'
        }

@svc.api(input=JSON(pydantic_model= CreditApplication), output=JSON())
def classify_vector_validate(credit_aplication):
    application_data = credit_aplication.dict()
    #Usualmente acá es donde se hace data cleaning a la data
    vector = dv.transform(application_data)    
    prediction = model_runner.predict.run(vector)

    ## Extra logica con business logic (BANCK, ISSUES, etc)
    result = prediction[0]
    if result > 0.5:
        return {
            'status': 'DECLINED'
        }
    elif  result > 0.25:
        return {
            'status': 'MAYVE'
        }
    else:
        return {
            'status': 'APPROVED'
        }        

@svc.api(input=NumpyNdarray(), output=JSON())
def classify_vector_numpy(vector):
    prediction = model_runner.predict.run(vector)
    ## Extra logica con business logic (BANCK, ISSUES, etc)
    result = prediction[0]
    if result > 0.5:
        return {
            'status': 'DECLINED'
        }
    elif  result > 0.25:
        return {
            'status': 'MAYVE'
        }
    else:
        return {
            'status': 'APPROVED'
        }                

    
@svc.api(input=NumpyNdarray(shape = (-1,29), enforce_shape=True), output=JSON())
def classify_vector_numpy_shape(vector):
    prediction = model_runner.predict.run(vector)
    ## Extra logica con business logic (BANCK, ISSUES, etc)
    result = prediction[0]
    if result > 0.5:
        return {
            'status': 'DECLINED'
        }
    elif  result > 0.25:
        return {
            'status': 'MAYVE'
        }
    else:
        return {
            'status': 'APPROVED'
        }      

@svc.api(input=NumpyNdarray(shape = (-1,29), enforce_shape=True), output=JSON())
async def classify_vector_numpy_shape_async(vector):
    prediction = await model_runner.predict.async_run(vector)
    ## Extra logica con business logic (BANCK, ISSUES, etc)
    result = prediction[0]
    if result > 0.5:
        return {
            'status': 'DECLINED'
        }
    elif  result > 0.25:
        return {
            'status': 'MAYVE'
        }
    else:
        return {
            'status': 'APPROVED'
        }            