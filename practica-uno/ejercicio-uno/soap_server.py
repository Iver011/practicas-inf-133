from http.server import HTTPServer
from pysimplesoap.server import SoapDispatcher,SOAPHandler

def suma(n1,n2):
    return n1+n2

def resta(n1,n2):
    return n1-n2

def multiplicacion(n1,n2):
    return n1*n2

def division(n1,n2):
    return n1//n2
    

dispatcher=SoapDispatcher(
    "ejercicio-uno-soap-server",
    location="http://localhost:8000/",
    action="http://localhost:8000/",
    namespace="http://localhost:8000/",
    trace=True,
    ns=True,

)
dispatcher.register_function(
    "Sumar",
    suma,
    returns={"result":int},
    args={"n1":int,"n2":int},
)
dispatcher.register_function(
    "Restar",
    resta,
    returns={"result":int},
    args={"n1":int,"n2":int},
)
dispatcher.register_function(
    "Multiplicar",
    multiplicacion,
    returns={"result":int},
    args={"n1":int,"n2":int},
)
dispatcher.register_function(
    "Dividir",
    division,
    returns={"result":int},
    args={"n1":int,"n2":int},
)
server = HTTPServer(("0.0.0.0", 8000), SOAPHandler)
server.dispatcher = dispatcher
print("Servidor SOAP iniciado en http://localhost:8000/")
server.serve_forever()
