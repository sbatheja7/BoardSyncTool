import http.client


class PPApiClient:
    """Class used for Project Place API client methods"""

    def __init__(self, config):
        print(config)
        self.config = config

    def get_connection(self, url):
        access_token = self.config['pp_access_token']
        conn = http.client.HTTPSConnection("api.projectplace.com")
        payload = ''
        headers = {
            'Authorization': 'Bearer ' + access_token
        }
        conn.request("GET", url, payload, headers)
        return conn

    def get_cards_data(self, board_id):
        conn = self.get_connection("/1/boards/" + board_id + "/cards")
        res = conn.getresponse()
        data = res.read()

        return data.decode("utf-8")

    def get_board_data(self, board_id):
        conn = self.get_connection("/1/boards/" + board_id)

        res = conn.getresponse()
        data = res.read()

        return data.decode("utf-8")

    def get_tags_data(self, board_id):
        conn = self.get_connection("/1/tags/boards/" + board_id)

        res = conn.getresponse()
        data = res.read()

        return data.decode("utf-8")
