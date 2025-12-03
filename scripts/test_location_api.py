from fastapi.testclient import TestClient
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import app


def main():
    client = TestClient(app)

    r_dep = client.post('/departamentos/', json={'nombreDepartamento': 'Lima'})
    print('DEP', r_dep.status_code, r_dep.json())
    dep_id = r_dep.json()['id']

    r_prov = client.post('/provincias/', json={'nombreProvincia': 'Lima', 'departamento_id': dep_id})
    print('PROV', r_prov.status_code, r_prov.json())
    prov_id = r_prov.json()['id']

    r_dist = client.post('/distritos/', json={'nombreDistrito': 'Lima Centro', 'provincia_id': prov_id})
    print('DIST', r_dist.status_code, r_dist.json())
    dist_id = r_dist.json()['id']

    r_col = client.post('/colegios/', json={'nombreColegio': 'Colegio 1', 'distrito_id': dist_id})
    print('COL', r_col.status_code, r_col.json())

    print('GET departamentos ->', client.get('/departamentos/').json())
    print('GET provincias ->', client.get('/provincias/').json())
    print('GET distritos ->', client.get('/distritos/').json())
    print('GET colegios ->', client.get('/colegios/').json())


if __name__ == '__main__':
    main()
