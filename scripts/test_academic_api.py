from fastapi.testclient import TestClient
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import app


def main():
    client = TestClient(app)

    # Crear ciclo
    r_c = client.post('/ciclos/', json={
        'nombreCiclo': '2025-A', 'fechaInicio': '2025-02-01', 'fechaFin': '2025-07-15', 'estado': True
    })
    print('POST /ciclos ->', r_c.status_code, r_c.json())
    ciclo_id = r_c.json()['id']

    # PUT ciclo
    r_c_put = client.put(f'/ciclos/{ciclo_id}', json={
        'nombreCiclo': '2025-A-Edit', 'fechaInicio': '2025-02-05', 'fechaFin': '2025-07-20', 'estado': False
    })
    print('PUT /ciclos/{id} ->', r_c_put.status_code, r_c_put.json())

    # Crear grupo
    r_g = client.post('/grupos/', json={'nombreGrupo': 'G1', 'aforo': 25, 'estado': True, 'ciclo_id': ciclo_id})
    print('POST /grupos ->', r_g.status_code, r_g.json())
    grupo_id = r_g.json()['id']

    # PUT grupo
    r_g_put = client.put(f'/grupos/{grupo_id}', json={'nombreGrupo': 'G1-Edit', 'aforo': 28, 'estado': False, 'ciclo_id': ciclo_id})
    print('PUT /grupos/{id} ->', r_g_put.status_code, r_g_put.json())

    # Crear clase
    r_cl = client.post('/clases/', json={'codigoClase': 'MAT101', 'grupo_id': grupo_id})
    print('POST /clases ->', r_cl.status_code, r_cl.json())
    clase_id = r_cl.json()['id']

    # PUT clase
    r_cl_put = client.put(f'/clases/{clase_id}', json={'codigoClase': 'MAT101-EDIT', 'grupo_id': grupo_id})
    print('PUT /clases/{id} ->', r_cl_put.status_code, r_cl_put.json())

    # Listar
    print('GET /ciclos ->', client.get('/ciclos/').status_code, client.get('/ciclos/').json())
    print('GET /grupos ->', client.get('/grupos/').status_code, client.get('/grupos/').json())
    print('GET /clases ->', client.get('/clases/').status_code, client.get('/clases/').json())


if __name__ == '__main__':
    main()
