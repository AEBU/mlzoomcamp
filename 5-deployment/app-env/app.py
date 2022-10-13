import pickle

client = {"reports": 0, "share": 0.001694, "expenditure": 0.12, "owner": "yes"}

print('********', 'Abriendo vectorizar')
# Open the file with Vectorizer
with open('./../models/dv.bin', 'rb') as f_in:
    dv = pickle.load(f_in)
f_in.close()
print('********', 'Asignando vectorizar')

# Open the model prediction
print('********', 'Abriendo modelo')
with open('./../models/model1.bin', 'rb') as f_in:
    model = pickle.load(f_in)
f_in.close()
print('********', 'asignando modelo')

# Create the prediction
X = dv.transform([client])
y_pred = model.predict_proba(X)[0,1]

print('******************')
print('Predicción', str(y_pred.round(3)))
print('******************')
