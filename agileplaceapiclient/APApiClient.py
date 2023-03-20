import http.client
import json


class APApiClient:

    def __init__(self, config):
        self.config = config

    def create_new_card(self, board_id, title):
        payload = json.dumps({
            "boardId": board_id,
            "title": title,
            "lane": 2
        })
        data = self.get_connection(payload)

        return data.decode("utf-8")

    def create_new_card_with_properties(self, card_json):
        card_json = json.dumps(card_json)
        data = self.get_connection(card_json)

        return data.decode("utf-8")

    def get_connection(self, payload):
        conn = http.client.HTTPSConnection("planview.leankit.com")
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.config['ap_access_token']
        }
        conn.request("POST", "/io/card", payload, headers)
        res = conn.getresponse()
        data = res.read()
        return data
