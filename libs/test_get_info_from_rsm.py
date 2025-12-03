import pytest
import requests

headers = {
    'Content-Type': 'application/json; charset=utf-8'
}


def get_token():
    url = 'https://api.rsm.promenergo.local/api/Auth/Login'
    body = {
        "id": "1003",
        "password": "123"
    }
    response = requests.post(url, json=body, headers=headers, verify=False)

    token = response.cookies

    return token


def get_stand(cookies):
    base = 'https://api.rsm.promenergo.local'
    ext = '/api/Stand/Get'
    response = requests.get(
        base + ext,
        verify=False, headers=headers, cookies=cookies)
    res = {}
    for i in response.json()['value']:
        res[i['name']] = i['id']
    return res


@pytest.mark.asd
def test_123():
    cookies = get_token()

    stands = get_stand(cookies)

    response = requests.get(f'https://api.rsm.promenergo.local/api/Cell/Get/ByStandId/{stands['1Ф Стенд ЛП']}',
                            verify=False, headers=headers, cookies=cookies)

    assert response.status_code == 200

    res = [''.join(i['meter']['serialNumber'][-4:]) for i in response.json()['value']]

    res = [num.lstrip('0') or '0' for num in res]
    print(res)
