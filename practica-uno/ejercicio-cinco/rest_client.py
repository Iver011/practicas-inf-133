import requests

url = "http://localhost:8000/"
ruta_post=url+ 'animales'
nuevo_animal={
    'id':2,
    'nombre':'Leopardo',
    'especie':'Leopardo',
    'genero': 'Felidae',
    'edad':20,
    'peso':50,
}

post_response=requests.request(method="POST",url=ruta_post,json=nuevo_animal)
print(post_response)

ruta_get=url+'animales'
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)

ruta_get=url+'animales?especie=Leopardo'
get_response=requests.request(method='GET',url=ruta_get)
print("por especie: ",get_response.text)

ruta_get=url+'animales?genero=Felidae'
get_response=requests.request(method='GET',url=ruta_get)
print("Por genero: ", get_response.text)



ruta_put = url + 'animales/1'
datos_actualizados = {
    'nombre':'Varano',
    'especie':'Sauropsido',
    'genero': 'Chrorata',
    'edad':26,
    'peso':2,
}
put_response = requests.request(method='PUT', url=ruta_put, json=datos_actualizados)
print("Respuesta del PUT:")
print(put_response.text)


ruta_delete = url + 'animales/2'
delete_response = requests.request(method='DELETE', url=ruta_delete)

ruta_get = url + "animales"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)