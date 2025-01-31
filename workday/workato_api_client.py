from typing import Dict, List, Any, Tuple

import requests

"""
This class will fetch the data table data containing the journal entries 
which are already processed, in order to filter out only the current generated journals

The list of ids will be: Journal_id#journal_doc_number
"""


class WorkatoAPIClient:

    def __init__(self, url, api_token, limit: int = 2):
        self.url: str = url
        self.api_token: str = api_token
        self.limit: int = limit

    def __call_end_point(self, url: str, limit: int, next_page_token) -> Tuple[List[str], str]:
        """

        :param url: Url to query
        :param limit: Number of journal Ids to retrieve
        :param next_page_token: Generated Next page token
        :return: list of journal Ids, generated next page token
        """
        # init query parameter
        headers = {
            'api-token': self.api_token
        }
        params = {
            "limit": limit,
            "next_page_token": next_page_token,
        }
        response = requests.request("GET", url, headers=headers, params=params)
        data: Dict[str, str] = response.json()

        print(data)

        journal_ids: List[str] = data.get('journal_ids', [])
        next_page_token: str = data.get('next_page_token', "")

        return journal_ids, next_page_token

    def get_all_journal_ids_by_iteration(self) -> List[str]:
        """
        Use it to avoid bottleneck network bandwidth and limitations
        :return: list of journal ids
        """
        url = f"{self.url}/get/all_journals_ids"
        # init parameters
        journal_ids: List[str] = []
        next_page_token = ""

        # Make the first call to the Workato API
        _journal_ids, next_page_token = self.__call_end_point(url, self.limit, next_page_token)
        # Add the returned data into the main return list
        journal_ids.extend(_journal_ids)

        # Make the loop and stop when the next_page_token returns is empty
        while next_page_token:
            # Make the first call to the Workato API
            _journal_ids, next_page_token = self.__call_end_point(url, self.limit, next_page_token)
            # Add the returned data into the main return list
            journal_ids.extend(_journal_ids)

        return journal_ids

    def get_all_journal_ids(self) -> List[str]:
        url = f"{self.url}/get/all_journals_ids"
        headers = {
            'api-token': self.api_token
        }

        response = requests.request("GET", url, headers=headers)
        data: Dict[str, str] = response.json()
        print(data)
        journal_ids: List[str] = data.get('journal_ids', [])

        return journal_ids


if __name__ == '__main__':
    workato_client: WorkatoAPIClient = WorkatoAPIClient(
        url="https://apim.eu.workato.com/contentsquare/pigment-trigger-button-endpoint-v1",
        api_token="XXX",
        limit=2
    )

    print(workato_client.get_all_journal_ids_by_iteration())