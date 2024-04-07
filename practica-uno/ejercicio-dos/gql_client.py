import requests

url = 'http://localhost:8000/graphql'
query_lista = """
{
        plantas{
            id
            nombre
            especie
            edad
            altura
            frutos
        }
    }
"""
response = requests.post(url, json={'query': query_lista})
print(response.text)


query_crear="""
    mutation{
        crearPlanta(nombre:"Girasol",especie:"Heliannatus",edad:14,altura:124){
        planta{
            id
            nombre
            especie
            edad
            altura
            frutos
        }
        }
    }


"""
response_mutation=requests.post(url,json={'query':query_crear})
print(response_mutation.text)

response = requests.post(url, json={'query': query_lista})
print(response.text)
query="""
{
    plantaPorEspecie(especie:"Heliannatus"){
        id
        nombre

    }
}"""
response = requests.post(url, json={'query': query})
print(response.text)



query_eliminar= """
mutation{
    deletePlanta(id: 2){
    planta{
        id
        nombre
        especie
        edad
        altura
        frutos
    }
    }
}
"""
response_mutation=requests.post(url,json={'query':query_eliminar})
print(response_mutation.text)



response=requests.post(url,json={'query':query_lista})
print(response.text)