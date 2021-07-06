import requests


def add_mesage(data):

    r = requests.post('https://gukly.com/clients/lionpost/', data)
    print(r.text)
    return r