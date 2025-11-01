from datetime import date

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def run():
    # Crear cadena de ubicación mínima
    dep = client.post("/departamentos/", json={"nombreDepartamento": "Cusco"}).json()
    prov = client.post("/provincias/", json={"nombreProvincia": "Cusco", "departamento_id": dep["id"]}).json()
    dist = client.post("/distritos/", json={"nombreDistrito": "Centro", "provincia_id": prov["id"]}).json()
    col = client.post("/colegios/", json={"nombreColegio": "Colegio Central", "distrito_id": dist["id"]}).json()

    # Crear ciclo y programa
    ciclo = client.post("/ciclos/", json={
        "nombreCiclo": "2025-A",
        "fechaInicio": "2025-01-10",
        "fechaFin": "2025-03-30",
        "estado": True
    }).json()
    prog = client.post("/programas/", json={"nombrePrograma": "Contabilidad"}).json()

    # Crear grupo y clase
    grupo = client.post("/grupos/", json={
        "nombreGrupo": "G1",
        "aforo": 30,
        "estado": True,
        "ciclo_id": ciclo["id"]
    }).json()
    clase = client.post("/clases/", json={
        "codigoClase": "CL-001",
        "grupo_id": grupo["id"]
    }).json()

    # Crear alumno
    alumno = client.post("/alumnos/", json={
        "nombreAlumno": "Luis",
        "aMaterno": "Quispe",
        "aPaterno": "Huaman",
        "sexo": "M",
        "telefonoEstudiante": "999111222",
        "telefonoApoderado": "988777666",
        "fechaNacimiento": "2007-05-05",
        "email": "luis.alumno@example.com",
        "anoCulminado": 2024,
        "Direccion": "Av. Principal 123",
        "nroDocumento": "12345678",
        "idColegio": col["id"]
    }).json()

    # Crear inscripción
    ins = client.post("/inscripciones/", json={
        "turno": "mañana",
        "fecha": str(date.today()),
        "Estado": True,
        "idAlumno": alumno["id"],
        "idPrograma": prog["id"],
        "idCiclo": ciclo["id"],
        "idClase": clase["id"],
        "Codigo": "INS-0001",
        "EstadoPago": "pendiente",
        "TipoPago": "contado"
    }).json()

    # Crear pago
    pago = client.post("/pagos/", json={
        "nroVoucher": "VCH-100",
        "medioPago": "transferencia",
        "monto": 150.5,
        "fecha": str(date.today()),
        "idInscripcion": ins["id"],
        "foto": None,
        "Estado": True
    }).json()

    # Listar
    alumnos = client.get("/alumnos/").json()
    inscs = client.get("/inscripciones/").json()
    pagos = client.get("/pagos/").json()

    print("Alumno creado:", alumno)
    print("Inscripcion creada:", ins)
    print("Pago creado:", pago)
    print("Alumnos:", alumnos)
    print("Inscripciones:", inscs)
    print("Pagos:", pagos)


if __name__ == "__main__":
    run()
