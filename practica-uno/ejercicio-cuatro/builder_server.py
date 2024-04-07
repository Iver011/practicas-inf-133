from http.server import BaseHTTPRequestHandler,HTTPServer
import json

class Paciente:
    def __init__(self):
        self.ci=None
        self.nombre=None
        self.apellido=None
        self.edad=None
        self.genero=None
        self.diagnostico=None
        self.doctor=None

    def __str__(self):
        return f"ci: {self.ci}, nombre: {self.nombre}, apellido: { self.apellido}, edad: {self.edad}, genero: {self.genero},diagnostico: {self.diagnostico}, doctor: {self.doctor}"
    

class PacienteBuilder:
    def __init__(self):
        self.paciente=Paciente()
    def set_ci(self,ci):
        self.paciente.ci=ci
    def set_nombre(self,nombre):
        self.paciente.nombre=nombre
    def set_apellido(self,apellido):
        self.paciente.apellido=apellido
    def set_edad(self,edad):
        self.paciente.edad=edad
    def set_genero(self,genero):
        self.paciente.genero=genero
    def set_diagnostico(self,diagnostico):
        self.paciente.diagnostico=diagnostico
    def set_doctor(self,doctor):
        self.paciente.doctor=doctor

    def get_paciente(self):
        return self.paciente
    


class Hospital:
    def __init__(self, builder):
        self.builder = builder

    def create_paciente(self, ci,nombre,apellido,edad,genero,diagnostico,doctor):
        self.builder.set_ci(ci)
        self.builder.set_nombre(nombre)
        self.builder.set_apellido(apellido)
        self.builder.set_genero(genero)
        self.builder.set_edad(edad)
        self.builder.set_diagnostico(diagnostico)
        self.builder.set_doctor(doctor)

        return self.builder.get_paciente()

class HospitalService:
    def __init__(self):
        self.builder = PacienteBuilder()
        self.hospital = Hospital(self.builder)

    def handle_post_request(self, post_data):
        ci=post_data.get('ci',None)
        nombre=post_data.get('nombre',None)
        apellido=post_data.get('apellido',None)
        edad=post_data.get('edad',None)
        genero=post_data.get('genero',None)
        diagnostico=post_data.get('diagnostico',None)
        doctor=post_data.get('doctor',None)


        paciente = self.hospital.create_paciente(ci,nombre,apellido,edad,genero,diagnostico,doctor)

        return {
            'ci':paciente.ci,
            'nombre':paciente.nombre,
            'apellido':paciente.apellido,
            'edad':paciente.edad,
            'genero':paciente.genero,
            'diagnostico':paciente.diagnostico,
            'doctor':paciente.doctor,
            
        }

class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers['Content-Length'])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode('utf-8'))

class PacienteHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.controller = HospitalService()
        super().__init__(*args, **kwargs)
        
    def do_POST(self):
        if self.path == '/paciente':
            
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.handle_post_request(data)
            
            HTTPDataHandler.handle_response(self, 201, response_data)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})


def run(server_class=HTTPServer, handler_class=PacienteHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Iniciando servidor HTTP en puerto {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()