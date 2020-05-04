import requests

auth_token = 'kbkcmbkcmbkcbc9ic9vixc9vixc9v'
hed = {'Authorization': 'Bearer ' + auth_token}
# data = {'app' : 'aaaaa'}

data = {
    "username": "admin",
    "password": "admin"
}
url = 'http://127.0.0.1:8000/api/token/'
response = requests.post(url, json=data, headers=hed)
print(response)
resp_dict = response.json()
print(resp_dict["access"])

data = {
    "username": "admin",
    "password": "admin"
}


class Request:

    def __init__(self, address):
        self.address = address

    def get_token(self, username=None, password=None):
        data = {
            "username": username,
            "password": password
        }
        response = requests.post(f'{self.address}/api/token/', json=data)
        resp_dict = response.json()
        return resp_dict["access"]

    def update_token(self, username=None, password=None):
        pass

    def create_user(self, token, name, surname, email, password):
        header = {'Authorization': 'Bearer ' + token}
        data = {

        }
        response = requests.post(f'{self.address}/posts/', json=data, header=header)
        return response.status_code
