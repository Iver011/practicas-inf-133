import requests

# Consultando a un servidor RESTful
url = "http://localhost:8000/"
# GET obtener a todos los estudiantes por la ruta /estudiantes
ruta_get = url + "pacientes"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)

ruta_post=url+ 'pacientes'
nuevo_paciente={
    'ci':12454124,
    'nombre':'Daniel',
    'apellido':'Mendoza',
    'edad':60,
    'genero':'M',
    'diagnostico':'Problemas Cardiacos',
    'doctor':'Pedro Perez',
}

post_response=requests.request(method="POST",url=ruta_post,json=nuevo_paciente)
print(post_response)

get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)

ruta_get=url+'pacientes?ci=12454124'
get_response=requests.request(method='GET',url=ruta_get)
print("paciente por ci: ",get_response.text)

ruta_get=url+'pacientes?diagnostico=diabetes'
get_response=requests.request(method='GET',url=ruta_get)
print("Por Diagnostico: ", get_response.text)


ruta_get=url+'pacientes?doctor=Pedro Perez'
get_response=requests.request(method='GET',url=ruta_get)
print("Por Doctor: ", get_response.text)
ruta_put = url + 'pacientes/4512456'
datos_actualizados = {
    'nombre': 'Juan',
    'apellido': 'Garcia',
    'edad': 50,
    'diagnostico': 'Hipertension',
    'doctor': 'Lopez',
}
put_response = requests.request(method='PUT', url=ruta_put, json=datos_actualizados)
print("Respuesta del PUT:")
print(put_response.text)


ruta_delete = url + 'pacientes/4512456'
delete_response = requests.request(method='DELETE', url=ruta_delete)

ruta_get = url + "pacientes"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)