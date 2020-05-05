'''
Bot should read the configuration and create this activity:

● signup users (number provided in config)

● each user creates random number of posts with any content (up to

max_posts_per_user)

● After creating the signup and posting activity, posts should be liked randomly, posts

can be liked multiple times
'''

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
        self.token = ''
        self.refresh = ''

    def authorize(self, username=None, password=None):
        data = {
            "username": username,
            "password": password
        }
        response = requests.post(f'{self.address}/api/token/', json=data)
        resp_dict = response.json()
        self.token = resp_dict['access']
        self.header = {'Authorization': 'Bearer ' + self.token}
        self.refresh = resp_dict['refresh']

        return response.status_code

    def update_token(self):
        data = {'refresh': self.refresh}
        response = requests.post(f'{self.address}/api/token/refresh', json=data)
        resp_dict = response.json()
        self.token = resp_dict['access']
        return resp_dict['access']

    def create_user(self, username, password, email=None, first_name=None, last_name=None):
        data = {"username": username,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
                "email": email
                }

        response = requests.post(f'{self.address}/users/', json=data, header=self.header)
        return response.status_code

    def create_post(self, title, text):
        data = {
            'title': title,
            'text': text
        }
        response = requests.post(f'{self.address}/posts/', json=data, headers=self.header)
        return response.status_code

    def create_like(self, post_id):
        data = {
            'publications': post_id
        }
        response = requests.post(f'{self.address}/likes/', json=data, headers=self.header)
        return response.status_code

    def get_service_information(self):
        response = requests.get(f'{self.address}/service/', headers=self.header)
        return response.status_code

    def get_user_activity(self):
        response = requests.get(f'{self.address}/user_activity/', headers=self.header)
        print(response.json())
        


if '__main__' == __name__:
    r = Request('http://127.0.0.1:8000')
    r.authorize('admin', 'admin')
    r.get_user_activity()
