import requests


class DataManager():
    # This class is responsible for talking to the Google Sheet.
    def __init__(self, endpoint, token):
        self.endpoint = endpoint
        self.token = token
        self.destination_data = {}

    def get_destination_data(self):
        bearer_headers = {
            'Content-Type': 'application/json',
            "Authorization": f'Bearer {self.token}'
        }

        response = requests.get(self.endpoint, headers=bearer_headers)
        response.raise_for_status()
        self.destination_data = response.json()['prices']
        return self.destination_data

    def update_destination_data(self):
        for city in self.destination_data:
            bearer_headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.token}'
            }

            body = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }

            response = requests.put(f'{self.endpoint}/{city["id"]}', json=body, headers=bearer_headers)
            response.raise_for_status()

