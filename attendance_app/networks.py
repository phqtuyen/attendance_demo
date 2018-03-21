import requests

# Instructions on using requests: http://docs.python-requests.org/en/latest/user/quickstart/

class RocketUsersAPI:
    def __init__(self, url, authToken, userID):
        self.url = url or "http://localhost:3000/api/v1/"
        self.authToken = authToken or 'pl59Z7F1S7c5MGIMi8ZtQ6d1XAtvafqwCoc1VFoyRCN'
        self.userID = userID or 'KEPvCAsPtzniBTdYB'
    def getUsers(self):
        headers = {'X-Auth-Token' : self.authToken, 'X-User-Id' : self.userID}
        getUsersUrl = self.url + "users.list"
        r = requests.get(getUsersUrl, headers=headers)
        return r.text