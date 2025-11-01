from fastapi.testclient import TestClient
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import app


def main():
    client = TestClient(app)

    # Asegurar datos base: ciclo, programa y colegio
    r_ciclo = client.post('/ciclos/', json={
        'nombreCiclo': '2025-B', 'fechaInicio': '2025-08-01', 'fechaFin': '2025-12-15', 'estado': True
    })
    ciclo_id = r_ciclo.json()['id']

    r_prog = client.post('/programas/', json={'nombrePrograma': 'Administración'})
    programa_id = r_prog.json()['id']

    # Crear ubicación base para colegio: departamento/provincia/distrito
    dep = client.post('/departamentos/', json={'nombreDepartamento': 'Cusco'}).json()
    prov = client.post('/provincias/', json={'nombreProvincia': 'Cusco', 'departamento_id': dep['id']}).json()
    dist = client.post('/distritos/', json={'nombreDistrito': 'Cusco Centro', 'provincia_id': prov['id']}).json()
    col = client.post('/colegios/', json={'nombreColegio': 'Colegio Cusco', 'distrito_id': dist['id']}).json()

    # Crear PreInscripcion
    pre = client.post('/preinscripciones/', json={
        'nombreAlumno': 'Ana',
        'aMaterno': 'López',
        'aPaterno': 'García',
        'sexo': 'F',
        'telefonoEstudiante': '999111222',
        'telefonoApoderado': '988777666',
        'fechaNacimiento': '2007-05-10',
        'email': 'ana@example.com',
        'anoCulminado': 2024,
        'Direccion': 'Av. Siempre Viva 123',
        'nroDocumento': '12345678',
        'idColegio': col['id'],
        'idCiclo': ciclo_id,
        'idPrograma': programa_id
    })
    print('POST /preinscripciones ->', pre.status_code, pre.json())
    pre_id = pre.json()['id']

    # Crear PrePago asociado
    pago = client.post('/prepagos/', json={
        'nroVoucher': 'VCH-001',
        'medioPago': 'Yape',
        'monto': 50.0,
        'fecha': '2025-08-05',
        'idInscripcion': pre_id,
        'foto': 'voucher1.png',
        'TipoPago': 'Inscripción'
    })
    print('POST /prepagos ->', pago.status_code, pago.json())

    # Listar
    print('GET /preinscripciones ->', client.get('/preinscripciones/').status_code, client.get('/preinscripciones/').json())
    print('GET /prepagos ->', client.get('/prepagos/').status_code, client.get('/prepagos/').json())


if __name__ == '__main__':
    main()
