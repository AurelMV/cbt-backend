from fastapi.testclient import TestClient
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import app


def main():
    client = TestClient(app)

    r = client.post('/programas/', json={'nombrePrograma': 'Ingeniería de Sistemas'})
    print('POST /programas ->', r.status_code, r.json())
    pid = r.json()['id']

    # Update via PUT
    r_put = client.put(f'/programas/{pid}', json={'nombrePrograma': 'Ing. Sistemas y Cómputo'})
    print('PUT /programas/{id} ->', r_put.status_code, r_put.json())

    r2 = client.get('/programas/')
    print('GET /programas ->', r2.status_code, r2.json())


if __name__ == '__main__':
    main()
