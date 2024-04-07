from zeep import Client

client = Client('http://localhost:8000')
result = client.service.Sumar(n1=100,n2=2)
print("Suma: ",result)
result = client.service.Restar(n1=100,n2=2)
print("Resta: ",result)
result = client.service.Multiplicar(n1=100,n2=2)
print("Multiplicacion: ",result)
result = client.service.Dividir(n1=100,n2=2)
print("Division: ",result)