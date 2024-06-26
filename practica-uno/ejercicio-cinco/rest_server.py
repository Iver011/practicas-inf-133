from http.server import HTTPServer,BaseHTTPRequestHandler
import json

from urllib.parse import urlparse,parse_qs

animales = [
    {
        'id':1,
        'nombre':'iguana',
        'especie':'iguana iguana',
        'genero': 'iguana',
        'edad':20,
        'peso':5,
    },
]
class animalesService:
    @staticmethod
    def add_animal(data):
        id=len(animales)+1
        animales.append(data)
        return animales

    @staticmethod
    def buscar_animal(id):
        return next(
            (animal for animal in animales if animal["id"]==id),
            None,
        )
 
    @staticmethod
    def buscar_genero(genero):
        return next(
            (animal for animal in animales if animal["genero"]==genero),
            None,
        )
    
    @staticmethod
    def buscar_especie(especie):
        return next(
            (animal for animal in animales if animal["especie"]==especie),
            None,
        )
    
    
    @staticmethod
    def update_animal(id,data):
        animal=animalesService.buscar_animal(id)
        if animal:
            animal.update(data)
            return animales
        else:
            return None
        
    @staticmethod
    def delete_animal(id):
        animal = animalesService.buscar_animal(id)
        if animal:
            animal_index = animales.index(animal)
            animales.pop(animal_index)
            return animales
        else:
            return None

        
class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler,status,data):
        handler.send_response(status)
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

class RESTRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path=urlparse(self.path)
        query_params=parse_qs(parsed_path.query)
        print("Query params:", query_params)
        if parsed_path.path=='/animales':
            
            if 'genero' in query_params:
                genero=query_params['genero'][0]
                animales_filtrados=animalesService.buscar_genero(genero)
                if animales_filtrados!=[]:
                    HTTPResponseHandler.handle_response(self,200,animales_filtrados)
                else:
                    HTTPResponseHandler.handle_response(self,204,[])
            
            elif 'especie' in query_params:
                especie=query_params['especie'][0]
                animales_filtrados=animalesService.buscar_especie(especie)
                if animales_filtrados!=[]:
                    HTTPResponseHandler.handle_response(self,200,animales_filtrados)
                else:
                    HTTPResponseHandler.handle_response(self,204,[])
            else:
                HTTPResponseHandler.handle_response(self,200,animales)

    def do_POST(self):
        if self.path == "/animales":
            data=self.read_data()
            animales=animalesService.add_animal(data)
            HTTPResponseHandler.handle_response(self,201,animales)
        else:
            HTTPResponseHandler.handle_response(self,404,{'Error':'Ruta no Existente'})

    def do_PUT(self):
        if self.path.startswith("/animales/"):
            id=int(self.path.split("/")[-1])
            data=self.read_data()
            animales=animalesService.update_animal(id,data)
            if animales:
                HTTPResponseHandler.handle_response(self, 200, animales)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "Animal no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )
    def do_DELETE(self):
        if self.path.startswith("/animales/"):
            id = int(self.path.split("/")[-1])
            animales = animalesService.delete_animal(id)
            if animales:
                HTTPResponseHandler.handle_response(self, 200, animales)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "Animal no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )




    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data
def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()