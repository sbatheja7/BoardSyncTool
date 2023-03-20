from boardssynctool.BoardsSync import BoardSync
from projectplaceapiclient.PPApiClient import PPApiClient
from agileplaceapiclient.APApiClient import APApiClient
import json


def read_config():
    with open("config/config.json", "r") as jsonfile:
        data = json.load(jsonfile)
    return data


if __name__ == '__main__':

    project_place_board_id = '1420409'
    agile_place_board_id = '1895181389'

    config = read_config()

    project_place_api_client = PPApiClient(config)
    agile_place_api_client = APApiClient(config)

    boards_sync = BoardSync(project_place_api_client)
    project_place_data = boards_sync.get_pp_board_data(project_place_board_id)

    print(json.dumps(project_place_data))

    for card in project_place_data:
        title = card['title']

        update_card_request = {
            "boardId": agile_place_board_id,
            "title": card['title'],
            # "typeId": str(card['label_id']),
            "assignedUserids": [],
            "blockReason": card['is_blocked_reason'],
            "customFields": [],
            "description": card['description'],
            "index": card['column'][0]['display_order'],
            "isBlocked": card['is_blocked'],
            # "tags": card['tags'],
            # "laneId": str(card['column'][0]['display_order'])
        }

        print(update_card_request)

        response = agile_place_api_client.create_new_card_with_properties(update_card_request)

        print(response)
