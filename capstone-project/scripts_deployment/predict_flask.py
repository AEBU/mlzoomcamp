import pickle
import math

from flask import Flask, request, jsonify

## suppress warnings 
import warnings
warnings.filterwarnings("ignore")

#@ Import pickle model
input_file = './../model/model_scolarship=0.4.bin'
with open(input_file, 'rb') as f_in: 
    dv, model = pickle.load(f_in)

app = Flask('scolarship-amount')

@app.route('/predict', methods=['POST'])
def predict():
    carreer_data = request.get_json()
    print('carreer_data', carreer_data)

    X = dv.transform([carreer_data])

    y_pred = model.predict(X)[0]
    y_pred_real = round(math.exp(y_pred),2)

    result = {
        'y_pred_log': y_pred,
        'y_pred_real': y_pred_real
    }
    return jsonify(result)



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
