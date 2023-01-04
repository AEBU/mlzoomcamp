import requests


url = 'http://localhost:9696/predict'

customer_id = 'xyz-123'
scolarship = {
  "etnia": "mestizo",
  "genero": "femenino",
  "discapacidad": "no",
  "tipo_discapacidad": "intelectual",
  "estado_civil": "soltero(a)",
  "provincia_nacimiento_homologada": "el oro",
  "canton_nacimiento": "balsas",
  "provincia_residencia_homologada": "el oro",
  "programa_general": "programa de becas senescyt",
  "destino": "nacional",
  "financiamiento": "senescyt",
  "pais_de_estudios": "ecuador",
  "ies_de_estudios_homologada": "universidad tecnica de machala",
  "nivel_detallado": "pregrado",
  "carrera": "educacion inicial",
  "area_de_estudio": "educacion",
  "age": 23.0
}

response = requests.post(url, json=scolarship).json()
print(response)
print('Value to disburse %s' % response.get('y_pred_real'))