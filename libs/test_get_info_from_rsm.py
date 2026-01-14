import pytest
import requests
import urllib3

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
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    cookies = get_token()
    stands = get_stand(cookies)
    id_stand = stands['(Авто)стенд №3 ']

    response = requests.get(f'https://api.rsm.promenergo.local/api/Cell/Get/ByStandId/{id_stand}',
                            verify=False, headers=headers, cookies=cookies)

    data = response.json()['value']
    res = [i['meter']['serialNumber'][-4:] for i in data if 'meter' in i]
    res = [num.lstrip('0') or '0' for num in res]
    return res


def get_ip():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    cookies = get_token()
    stands = get_stand(cookies)
    id_stand = stands['(Авто)стенд №3 ']

    response = requests.get(f'https://api.rsm.promenergo.local/api/Cell/Get/ByStandId/{id_stand}',
                            verify=False, headers=headers, cookies=cookies)

    data = response.json()['value']

    res = {i['meter']['serialNumber']: i['comModule']['ipAddress'] for i in data
           if 'comModule' in i and i['comModule']['ipAddress'] != '-'} # надо добавить проверку на соответствию формату ip вместо != '-'

    print(res)
    return res


@pytest.mark.asd
def test_get_serial_number_from_stand():
    # cookies = get_token()
    #
    # stands = get_stand(cookies)
    # print('\n', stands)
    #
    # id_stand = stands['(Авто)стенд №3 ']
    #
    # response = requests.get(f'https://api.rsm.promenergo.local/api/Cell/Get/ByStandId/{id_stand}',
    #                         verify=False, headers=headers, cookies=cookies)

    # print(response.json(), '\n')

    # data = response.json()['value']
    # for i in data:
    #     if 'comModule' in i.keys() and i['comModule']['ipAddress'] != '-':
    #         # print(i['comModule'])
    #         # print()
    #         print(i['comModule']['ipAddress'])

    # assert response.status_code == 200
    #
    # data = response.json()['value']
    # res = [i['meter']['serialNumber'][-4:] for i in data if 'meter' in i]
    # #
    # res = [num.lstrip('0') or '0' for num in res]
    # print(res)

    get_ip()
