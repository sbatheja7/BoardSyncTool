import json


class BoardSync:

    def __init__(self, pp_api_client, ap_api_client):
        self.pp_api_client = pp_api_client
        self.ap_api_client = ap_api_client

    def get_pp_board_data(self, board_id):

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

            card['tags'] = tags_data.get(str(raw_card['id']), None)

            cards_data.append(card)

        return cards_data

    def populate_agile_place_board(self, project_place_data, agile_place_board_id):

        for card in project_place_data:

            tags = []
            if card['tags']:
                for tag in card['tags']:
                    tags.append(tag['name'])

            lane = {
                "index": card['column']['column_id'],
                "orientation": "vertical",
                "laneClassType": "active",
                "laneType": "completed"
            }

            update_card_request = {
                "boardId": agile_place_board_id,
                "title": card['title'],
                "assignedUserids": [],
                "blockReason": card['is_blocked_reason'],
                "customFields": [],
                "description": card['description'],
                "index": card['column']['column_id'],
                "isBlocked": card['is_blocked'],
                "tags": tags,
                "lane": lane
            }

            print(update_card_request)

            response = self.ap_api_client.create_new_card_with_properties(update_card_request)

            print(response)
