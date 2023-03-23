import json
from _datetime import datetime


class BoardSync:
    """The class is used for methods for board sync logic"""

    def __init__(self, pp_api_client, ap_api_client):
        self.pp_api_client = pp_api_client
        self.ap_api_client = ap_api_client

    def get_pp_board_data(self, board_id):
        """Method to get the boards and cards data from the Project Place API using the board ID"""

        boards_raw_data = self.pp_api_client.get_board_data(board_id)

        cards_raw_data = self.pp_api_client.get_cards_data(board_id)

        tags_data = self.pp_api_client.get_tags_data(board_id)

        boards_raw_data = json.loads(boards_raw_data)
        cards_raw_data = json.loads(cards_raw_data)
        tags_data = json.loads(tags_data)

        columns = boards_raw_data['progresses']

        columns_data = dict()
        cards_data = list()

        for column in columns:
            columns_data[column['id']] = {
                "column_id": column['id'],
                "display_order": column['display_order'],
                "name": column['name'],
                "wip_limit": column['wip_limit']
            }

        for raw_card in cards_raw_data:
            card = dict()
            card['id'] = raw_card['local_id']
            card['assignee_id'] = raw_card['assignee_id']
            card['comment_count'] = raw_card['comment_count']
            card['creator'] = raw_card['creator']
            card['custom_fields'] = raw_card['custom_fields']
            card['description'] = raw_card['description']
            card['due_date'] = raw_card['due_date']
            card['estimated_time'] = raw_card['estimated_time']
            card['is_blocked'] = raw_card['is_blocked']
            card['is_blocked_reason'] = raw_card['is_blocked_reason']
            card['label_id'] = raw_card['local_id']
            card['column'] = columns_data[raw_card['progress']['id']]
            card['title'] = raw_card['title']
            card['start_date'] = raw_card['start_date']
            card['start_date_offset'] = raw_card['start_date_offset']
            assignee = list()
            assignee.append(raw_card['assignee'])
            assignee.append(raw_card['contributors'])
            card['assignee'] = assignee
            card['activity'] = raw_card['planlet']
            card['direct_url'] = raw_card['direct_url']
            card['tags'] = tags_data.get(str(raw_card['id']), None)

            cards_data.append(card)

        return cards_data

    @staticmethod
    def convert_date_time(date_time_str):
        return str(datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S').date())

    def populate_agile_place_board(self, project_place_data, agile_place_board_id):
        """Method used to populate the Agile Place board using the data got from the Project Place"""

        for card in project_place_data:

            tags = []
            if card['tags']:
                for tag in card['tags']:
                    tags.append(tag['name'])

            project_place_progress_mapping = {
                0: "New Requests",
                1: "Doing Now",
                2: "Recently Finished"
            }

            lanes = json.loads(self.ap_api_client.get_board_details(agile_place_board_id))

            lanes_data = lanes.get('lanes')

            lane_id_map = dict()

            for lane in lanes_data:
                lane_id_map[lane['name']] = lane['id']

            create_card_request = {
                "boardId": agile_place_board_id,
                "title": card['title'],
                "assignedUserids": [],
                "blockReason": card['is_blocked_reason'],
                "customFields": [],
                "description": card['description'],
                "isBlocked": card['is_blocked'],
                "tags": tags,
                "laneId": lane_id_map[project_place_progress_mapping[card['column']['column_id']]],
                "plannedStart": BoardSync.convert_date_time(card['start_date']) if card['start_date'] else None,
                "plannedFinish": BoardSync.convert_date_time(card['due_date']) if card['due_date'] else None,
                "externalLink": {
                    "label": "The link",
                    "url": card['direct_url']
                }
            }

            response = self.ap_api_client.create_new_card_with_properties(create_card_request)
            return response
