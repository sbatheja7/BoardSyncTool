import http.client
import json


class APApiClient:
    """Class used to Agile Place API client"""

    def __init__(self, config):
        self.config = config

    def create_new_card(self, board_id, title):
        payload = json.dumps({
            "boardId": board_id,
            "title": title
        })
        data = self.get_connection("/io/card", payload)

        return data.decode("utf-8")

    def create_new_card_with_properties(self, card_json):
        card_json = json.dumps(card_json)
        data = self.get_connection("/io/card", card_json)

        return data.decode("utf-8")

    def get_board_details(self, board_id):
        data = self.get_connection('/io/board/' + board_id, '')
        return data.decode("utf-8")

    def get_connection(self, url, payload):
        conn = http.client.HTTPSConnection("planview.leankit.com")
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.config['ap_access_token']
        }
        request = "POST" if payload else "GET"
        conn.request(request, url, payload, headers)
        res = conn.getresponse()
        data = res.read()
        return data
