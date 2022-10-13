import pickle

from flask import request
from flask import Flask


app = Flask('webService')

print('Cargando Files ....')
with open('./../models/dv.bin', 'rb') as f_in:
    dv = pickle.load(f_in)
f_in.close()

with open('./../models/model1.bin', 'rb') as f_in:
    model = pickle.load(f_in)
f_in.close()


@app.route('/predict',methods=['POST'])
def predict():
    customer = request.get_json()
    X = dv.transform([customer])
    y_pred = model.predict_proba(X)[0,1]

    return str(y_pred.round(3))

if __name__=='__main__':
   app.run(debug=True, host='0.0.0.0', port=9696)