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

    boards_sync = BoardSync(project_place_api_client, agile_place_api_client)
    project_place_data = boards_sync.get_pp_board_data(project_place_board_id)

    print(json.dumps(project_place_data))

    boards_sync.populate_agile_place_board(project_place_data, agile_place_board_id)


