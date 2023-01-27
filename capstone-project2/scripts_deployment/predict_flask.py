import pickle
import math
import pandas as pd
from flask import Flask, request, jsonify

## suppress warnings 
import warnings
warnings.filterwarnings("ignore")

#@ Import pickle model
input_file = 'model_appr.bin'

with open(input_file, 'rb') as f_in: 
    model_predict = pickle.load(f_in)
f_in.close()

app = Flask('scolarship-amount')

@app.route('/predict', methods=['POST'])
def predict():
    predict_data = request.get_json()
    print('predict_moths', predict_data)
    months_to_predict = predict_data['steps']
    y_pred = model_predict.predict(months_to_predict)
    frame = { 
            'date': y_pred.index.strftime("%Y-%m-%d"), 
            'forecasting': y_pred.values 
            }
    result = pd.DataFrame(frame).to_dict(orient='records')
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
