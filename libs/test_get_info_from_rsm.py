import pytest
import requests

headers = {
    'Content-Type': 'application/json; charset=utf-8'
}

base_url = 'https://api.rsm.promenergo.local'


def get_token():
    ext = '/api/Auth/Login'
    body = {
        "id": "1003",
        "password": "123"
    }
    response = requests.post(base_url + ext, json=body, headers=headers, verify=False)

    token = response.cookies

    return token


def get_stand(cookies):
    ext = '/api/Stand/Get'
    response = requests.get(
        base_url + ext,
        verify=False, headers=headers, cookies=cookies)
    res = {}
    for i in response.json()['value']:
        res[i['name']] = i['id']
    return res


def get_serial_numbers():
    cookies = get_token()
    stands = get_stand(cookies)
    id_stand = stands['Стенд №3']

    response = requests.get(f'https://api.rsm.promenergo.local/api/Cell/Get/ByStandId/{id_stand}',
                            verify=False, headers=headers, cookies=cookies)

    data = response.json()['value']
    res = [i['meter']['serialNumber'][-4:] for i in data if 'meter' in i]
    res = [num.lstrip('0') or '0' for num in res]
    return res


@pytest.mark.asd
def test_get_serial_number_from_stand():
    cookies = get_token()

    stands = get_stand(cookies)

    id_stand = stands['Стенд №3']

    response = requests.get(f'https://api.rsm.promenergo.local/api/Cell/Get/ByStandId/{id_stand}',
                            verify=False, headers=headers, cookies=cookies)

    assert response.status_code == 200

    data = response.json()['value']
    res = [i['meter']['serialNumber'][-4:] for i in data if 'meter' in i]
    #
    res = [num.lstrip('0') or '0' for num in res]
    print(res)
