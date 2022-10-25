import numpy as np
from pydantic import BaseModel
from bentoml.io import NumpyNdarray

import bentoml
from bentoml.io import JSON


class UserProfile(BaseModel) :
    name: str
    age: int
    country: str
    rating: float

model_ref = bentoml.sklearn.get("mlzoomcamp_homework:jsi67fslz6txydu5")
#dv = model_ref.custom_objects['dictVectorizer']

model_runner = model_ref.to_runner()

svc = bentoml.Service("credit_risk_classifier", runners=[model_runner])

"""
@svc.api(input=JSON(), output=JSON())
async def classify(application_data):
    vector = dv.transform(application_data)
    prediction = await model_runner.predict.async_run(vector)
    print(prediction)
    result = prediction[0]

    if result > 0.5:
        return {
            "status": "DECLINED"
        }
    elif result > 0.25:
        return {
            "status": "MAYBE"
        }
    else:
        return {
            "status": "APPROVED"
        }
"""


@svc.api(input=NumpyNdarray(), output=NumpyNdarray())
async def classify_numpy(vector):
    prediction = await model_runner.predict.async_run(vector)
    print(prediction)
    result = prediction[0]
    return result
    
