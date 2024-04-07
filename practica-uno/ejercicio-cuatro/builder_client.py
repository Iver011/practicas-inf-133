import requests

url = "http://localhost:8000/paciente"
headers = {'Content-type': 'application/json'}

paciente = {
    'nombre': 'Juan',
    'apellido': 'Garcia',
    'edad': 50,
    'diagnostico': 'Hipertension',
    'doctor': 'Lopez',
}

response = requests.post(url, json=paciente, headers=headers)
print(response.json())