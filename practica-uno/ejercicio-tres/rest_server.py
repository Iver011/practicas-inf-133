from http.server import HTTPServer,BaseHTTPRequestHandler
import json

from urllib.parse import urlparse,parse_qs

pacientes = [
    {
        'ci':4512456,
        'nombre':'Carlos',
        'apellido':'Sanchez',
        'edad':45,
        'genero':'M',
        'diagnostico':'diabetes',
        'doctor':'Garcia',
    },
]
class pacientesService:
    @staticmethod
    def add_paciente(data):
        id=len(pacientes)+1
        pacientes.append(data)
        return pacientes

    @staticmethod
    def buscar_paciente(ci):
        return next(
            (paciente for paciente in pacientes if paciente["ci"]==ci),
            None,
        )
    
    @staticmethod
    def filtrar_diagnostico(diagnostico):
        return [
            paciente for paciente in pacientes if paciente["diagnostico"]==diagnostico
        ]

    @staticmethod
    def filtrar_doctor(doctor):
        return[
            paciente for paciente in pacientes if paciente["doctor"]==doctor
        ]
    
    @staticmethod
    def update_paciente(ci,data):
        paciente=pacientesService.buscar_paciente(ci)
        if paciente:
            paciente.update(data)
            return pacientes
        else:
            return None
        
    @staticmethod
    def delete_paciente(ci):
        paciente = pacientesService.buscar_paciente(ci)
        if paciente:
            paciente_index = pacientes.index(paciente)
            pacientes.pop(paciente_index)
            return pacientes
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
        if parsed_path.path=='/pacientes':
            if 'ci' in query_params:
                ci=int(query_params['ci'][0])
                pacientes_buscado=pacientesService.buscar_paciente(ci)
                if pacientes_buscado:
                    HTTPResponseHandler.handle_response(self,200,pacientes_buscado)
                else:
                    HTTPResponseHandler.handle_response(self,204,"")
            elif 'diagnostico' in query_params:
                diagnostico=query_params['diagnostico'][0]
                pacientes_filtrados=pacientesService.filtrar_diagnostico(diagnostico)
                if pacientes_filtrados!=[]:
                    HTTPResponseHandler.handle_response(self,200,pacientes_filtrados)
                else:
                    HTTPResponseHandler.handle_response(self,204,[])
            
            elif 'doctor' in query_params:
                doctor=query_params['doctor'][0]
                pacientes_filtrados=pacientesService.filtrar_doctor(doctor)
                if pacientes_filtrados!=[]:
                    HTTPResponseHandler.handle_response(self,200,pacientes_filtrados)
                else:
                    HTTPResponseHandler.handle_response(self,204,[])
            else:
                HTTPResponseHandler.handle_response(self,200,pacientes)

    def do_POST(self):
        if self.path == "/pacientes":
            data=self.read_data()
            pacientes=pacientesService.add_paciente(data)
            HTTPResponseHandler.handle_response(self,201,pacientes)
        else:
            HTTPResponseHandler.handle_response(self,404,{'Error':'Ruta no Existente'})

    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            ci=int(self.path.split("/")[-1])
            data=self.read_data()
            pacientes=pacientesService.update_paciente(ci,data)
            if pacientes:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "Estudiante no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )
    def do_DELETE(self):
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            pacientes = pacientesService.delete_paciente(ci)
            if pacientes:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "Paciente no encontrado"}
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