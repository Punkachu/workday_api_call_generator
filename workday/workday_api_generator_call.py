"""
    Make the parent abstract class for calling ADN services
    and make calling endpoints easier to create, maintainable and testable
"""

from abc import ABC, abstractmethod

from models import *
from utils import retry_on_500

from datetime import datetime
from typing import Dict, Optional, List, Union, Tuple, Callable
import xml.etree.ElementTree as ET

import requests

from workday_new.workday.csv_helpers import CSVExportHelper
from workday_new.workday.xml_helper import XMLHelper



DEFAULT_NUM_ROW_LIMIT = 40000
DEFAULT_WORKDAY_API_VERSION = 'v43.1'
DEFAULT_WORKDAY_COUNT_PAGINATION = 999

"""Master Data Scope """
ASSET_CATEGORIES = 0
SPEND_CATEGORIES = 1
CUSTOMER_CONTRACT = 2
REGION_CATEGORIES = 3
COMPANIES_CATEGORIES = 4  # Suppliers
COMPANIES_WD = 44
PAY_METH_CATEGORIES = 5
SUBSIDIARIES_CATEGORIES = 6
BOOK_CODE_CATEGORIES = 7
COST_CENTER_CATEGORIES = 8
LEDGER_ACCOUNT = 9
SITES = 10
EMPLOYEES = 11
ASSETS = 12
GTM_ORG = 13
CURRENCY = 14
CUSTOMERS = 15
LEDGER_ACCOUNT_HIERARCHY = 16


class ProcessException(Exception):
    pass


class WorkdayConnector:
    """
    Access token generator class
    """
    def __init__(
            self, workday, tenant, client_id, client_secret, refresh_token,
            version=DEFAULT_WORKDAY_API_VERSION, xml_version='1.0'
    ):
        self.workday = workday
        self.tenant = tenant
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.version = version
        self.xml_version = xml_version
        self.access_token = None
        self.base_uri = f'https://{self.workday}'

    @retry_on_500()
    def acquire_token(self):
        refresh_url = f'{self.base_uri}/ccx/oauth2/{self.tenant}/token'
        payload = {
            'grant_type': 'refresh_token',  # constant value do not modify
            'refresh_token': self.refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(refresh_url, data=payload, headers=headers)

        if response.status_code == 200:
            tokens = response.json()
            self.access_token = tokens.get('access_token')
            self.refresh_token = tokens.get('refresh_token')
        else:
            response.raise_for_status()

    def apply_headers(self):
        if not self.access_token:
            raise ValueError("Access token is missing. Please acquire a token first.")
        return {
            'Authorization': f'Bearer {self.access_token}'
        }


class WorkdayService(ABC):
    """
    Generic  Workday API Call generator
    """
    def __init__(
            self,
            url: str,
            tenant: str,
            token: str,
            namespace: Dict[str, str],
            api_version: str = DEFAULT_WORKDAY_API_VERSION,
    ):
        self.url = url
        self.tenant = tenant
        self.token = token
        self.namespace = namespace
        self.api_version = api_version
        # XML Parameters
        self.xml_helper = XMLHelper(ns=namespace)
        # cache Dictionary
        self.cache: Dict[str, T] = {}

        # Pagination
        self.is_complete = False
        self.next_page = 1
        self.total_record = 0
        self.total_page = 0

        self.all_entity: List[T] = []
        self.failed_entity: List[FailedProcessedJournal] = []
        self.outdated_counter = 0

    # ABSTRACT METHODS
    @abstractmethod
    def _parse_entity_element(self, entry: ET.Element) -> Optional[T]:
        """
            Abstract method to parse an XML element data node and return an entity of type T
        :param entry: Entity Node element
        :return:
        """
        pass

    @abstractmethod
    def _update_cache(self, element: T):
        """Abstract method to update the cache dic with the object of type T and the identifier from the object T """
        pass

    @abstractmethod
    def _generate_payload(self, entity_id: str, **kwargs) -> str:
        """
            Abstract method to generate a payload string from the provided entity ID
        :param entity_id: ID needed to call the endpoint and get the data
        :param kwargs: other optional argument
        :return: String XML request payload
        """
        pass

    # ABSTRACT METHOD FOR PAGINATION
    @abstractmethod
    def _generate_payload_pagination(self, next_page: int, **kwargs) -> str:
        """
            Abstract method to generate a payload string from the provided argument
            to fetch all the entity available
        :param next_page: pagination number
        :param kwargs: other optional argument
        :return: String XML request payload
        """
        pass

    @abstractmethod
    def _get_entity_id(self, entry: ET.Element) -> Optional[str]:
        """
            Abstract method to Extract Entity ID from  the current entity node
        :param entry: ET entity from the response payload
        :return: String representation of the UID of the current entity, None in case of failure
        """
        pass

    @staticmethod
    def filter_objects(items: List[T], condition: Callable[[T], bool]) -> List[T]:
        """
        Filter a list of objects of type T based on a condition.

        Parameters:
            items (List[T]): The list of objects to filter.
            condition (Callable[[T], bool]): A function that defines the filter condition.

        Returns:
            List[T]: A list of objects that satisfy the condition.
        """
        return list(filter(condition, items))

    # Internal Methods
    @retry_on_500()
    def __call_endpoint(self, method: str, payload: Optional[str]) -> bytes:
        """
        Implemented method to call an API endpoint and return the raw response as bytes

        :payload: Provide the request payload needed to look for the supplier.
        :method: HTTP method [POST, GET, ...]
        :return: Bytes representation of response payload
        :raise: Raises :class:`HTTPError`
        """
        # Generate header
        headers = {
            'Content-Type': 'application/xml',
            'Authorization': f'Bearer {self.token}'
        }

        method = method.strip().upper()
        response = requests.request(method, self.url, headers=headers, data=payload)

        response.raise_for_status()  # Raise an error for bad status codes

        return response.content

    def get_entity(self, object_id: str, data_entity_path: str, method: Optional[str] = 'POST', **kwargs) -> Optional[
        T]:
        """
        Get the matching Entity regarding the provided ID

        :param object_id: Entity ID
        :param data_entity_path: The path of the data node tag to fetch, e.g: './/wd:Resource_Category_Data'
        :param method: HTTP Method to query with e.g: [POST, GET, PATCH, DELETE, ...]
        :return: Return T or None if not found
        """
        if object_id:
            # check whether the cache contains the requested OBJ
            obj = self.cache.get(object_id)
            if obj:
                return obj

            # Run Request otherwise
            # generate payload
            payload = self._generate_payload(object_id, **kwargs)

            # Call the Raas endpoint and get payload result
            xml_response_data = self.__call_endpoint(method, payload)

            root = ET.fromstring(xml_response_data)
            # Find all Supplier_Data elements
            entity_data_elements = root.findall(data_entity_path, self.namespace)

            entities: List[T] = []

            # Iterate and print each Supplier_Data element
            for entity in entity_data_elements:
                element: Optional[T] = self._parse_entity_element(entity)
                if element:
                    # add the entity
                    entities.append(element)
                    # update the cache with a new value
                    #self._update_cache(element)

            # Assert to check that the list contains only one element
            error_message = f"Expected list to contain exactly one element, but it has {len(entities)} elements."
            assert len(entities) == 1, error_message

            if len(entities) == 1:
                return entities[0]

        return None

    def search_entity(self, object_id: str, data_entity_path: str, method: Optional[str] = 'POST', **kwargs) -> Optional[
        T]:
        """
        Search the matching Entity regarding the provided ID in a one payload response
        eg: All currencies

        :param object_id: Entity ID
        :param data_entity_path: The path of the data node tag to fetch, e.g: './/wd:Resource_Category_Data'
        :param method: HTTP Method to query with e.g: [POST, GET, PATCH, DELETE, ...]
        :return: Return T or None if not found
        """
        if object_id:
            # check whether the cache contains the requested Object
            obj = self.cache.get(object_id)
            if obj:
                return obj

            # Run Request otherwise
            # generate payload
            payload = self._generate_payload(object_id, **kwargs)

            # Call the Raas endpoint and get payload result
            xml_response_data = self.__call_endpoint(method, payload)

            root = ET.fromstring(xml_response_data)
            # Find all Supplier_Data elements
            entity_data_elements = root.findall(data_entity_path, self.namespace)

            # Iterate and print each Supplier_Data element
            for entity in entity_data_elements:
                parsed_obj_id = self._get_entity_id(entity)
                element: Optional[T] = self._parse_entity_element(entity)
                if element and parsed_obj_id == object_id:
                    return element

        return None


    # METHOD FOR GETTING ALL THE ENTITIES FROM ALL THE PAGINATION
    def __parse_all_entities_page(self, xml_input: Union[str, bytes], entity_entry_data_path: str) -> List[T]:
        # Check if the input is bytes and convert to string if necessary
        if isinstance(xml_input, bytes):
            xml_input = self.xml_helper.bytes_to_utf8_string(xml_input)

        root = ET.fromstring(xml_input)
        ns = self.namespace

        root_entry_data = root.findall(entity_entry_data_path, ns)
        #print(len(root_entry_data))

        parsed_entities = []

        for entry_data_ in root_entry_data:
            try:
                parsed_entry: Optional[T] = self._parse_entity_element(entry_data_)
                if parsed_entry is not None:
                    parsed_entities.append(parsed_entry)
            except Exception as error:
                print(error)
                self.failed_entity.append(
                    FailedProcessedJournal(
                        journal_id=self._get_entity_id(entry_data_),
                        data=str(entry_data_),
                        error_message=str(error),
                        datetime=str(datetime.now()),
                        reason=
                        f'Could not extract data from XML payload in `parse_journals` at page {self.next_page - 1}'
                    )
                )

        return parsed_entities

    def __extract_response_results(self, xml_data: Union[str, bytes]) -> ResponseResults:
        """
            Extract the Response_Results node into object
        :param xml_data: XML answer payload
        :return: ResponseResults object
        """
        # Check if the input is bytes and convert to string if necessary
        if isinstance(xml_data, bytes):
            xml_data = self.xml_helper.bytes_to_utf8_string(xml_data)
        # Parse the XML data
        root = ET.fromstring(xml_data)
        # Namespace dictionary to help with the parsing
        ns = self.namespace
        # Find the Response_Filter element
        response_filter = root.find('.//wd:Response_Results', ns)
        if response_filter is not None:
            # Extract the fields from the Response_Results element
            total_results = response_filter.find('wd:Total_Results', ns).text if response_filter.find(
                'wd:Total_Results',
                ns
            ).text is not None else None
            print(f'total_results: {response_filter.find("wd:Total_Results", ns).text}')
            total_pages = response_filter.find('wd:Total_Pages', ns).text if response_filter.find(
                'wd:Total_Pages',
                ns
            ).text is not None else None
            page_results = response_filter.find('wd:Page_Results', ns).text if response_filter.find(
                'wd:Page_Results',
                ns
            ).text is not None else None

            page = response_filter.find('wd:Page', ns).text if response_filter.find('wd:Page',
                                                                                    ns) is not None else 1  # by default it must be 1, since 0 throw zero

            # Create and return a ResponseResults dataclass instance
            res = ResponseResults(
                total_results=int(total_results),
                total_pages=int(total_pages),
                page_results=int(page_results),
                page=int(page)
            )
            return res

        return ResponseResults(
                total_results=0,
                total_pages=1,
                page_results=0,
                page=1
            )

    def get_all_entities(self, entity_entry_data_path: str, **kwargs) -> List[T]:
        """
        Get all entities from all pages with the given [kwargs] argument
        :param entity_entry_data_path: The XML path element that holds the entry data e.g: './/wd:Journal_Entry_Data'
        :param kwargs: optional argument which might be used for forging the payload
        :return: List of converted entry into object type T
        """
        # Fetch all FX rates using pagination
        # First call, get the first page
        # init inner entities
        self.all_entity = []
        # generate payload
        payload = self._generate_payload_pagination(self.next_page, **kwargs)
        #print(f'payload: {payload}')
        response_content = self.__call_endpoint('POST', payload)

        # Check for the result page data in the response
        next_page_data = self.__extract_response_results(response_content)

        self.total_page = next_page_data.total_pages
        self.next_page = next_page_data.page
        self.total_record = next_page_data.total_results

        # get first results
        entities = self.__parse_all_entities_page(response_content, entity_entry_data_path)
        print(f'Found: {len(entities)} entities')
        # make sure only available lines ore kept
        self.all_entity.extend(entities)
        # get other page results
        if next_page_data.page >= 1:
            for page in range(2, self.total_page + 1):
                # call next page
                self.next_page = page
                # Generate payload for the next pagination
                payload = self._generate_payload_pagination(page, **kwargs)
                response_content = self.__call_endpoint('POST', payload)

                entities = self.__parse_all_entities_page(response_content, entity_entry_data_path)
                self.all_entity.extend(entities)

        # Now `all_fx_rates` contains all the FX rates retrieved across all pages
        print(f"Total Journals fetched: {len(self.all_entity)}")
        self.is_complete = (len(self.all_entity) + self.outdated_counter) == self.total_record
        print(f"Is Complete: {self.is_complete}")
        if not self.is_complete:
            print(f"The number found is {self.total_record}, but fetch {len(self.all_entity)} records.")
        print("OK")

        return self.all_entity

    def get_all_entities_by_page(
            self,
            entity_entry_data_path: str,
            page: int,
            entity_count: int = 999,
            **kwargs
    ) -> List[T]:
        """
        Get all entities by page (use in case of a huge workload)
        :param page: Page number to parse
        :param entity_count: entity to retrieve by page, default 999
        :param entity_entry_data_path: The XML path element that holds the entry data e.g: './/wd:Journal_Entry_Data'
        :param kwargs: optional argument which might be used for forging the payload
        :return: List of converted entry into object type T
        """
        # First call, get the first page
        # generate payload
        payload = self._generate_payload_pagination(page, count=entity_count, **kwargs)
        print(f'payload: {payload}')
        response_content = self.__call_endpoint('POST', payload)
        # Check for the result page data in the response
        next_page_data = self.__extract_response_results(response_content)
        self.total_page = next_page_data.total_pages
        self.total_record = next_page_data.total_results
        # get results
        entities = self.__parse_all_entities_page(response_content, entity_entry_data_path)
        print(f'Parsed: {len(entities)} entities over {self.total_page}')

        self.is_complete = len(entities) == entity_count or len(entities) == self.total_record % entity_count
        print(f"Is Complete: {self.is_complete}")
        if not self.is_complete:
            print(f"The number found {self.total_page}, but fetch {len(entities)} records.")
        else:
            print("OK")
        return entities

    @staticmethod
    def generate_csv(list_data: List[T], fields, filename: Optional[str], prod=True):
        csv_helper = CSVExportHelper(fields=fields)
        csv_content = csv_helper.generate_csv_content(list_data)

        if not prod and filename:
            csv_helper.export_to_csv(csv_content, filename)

        return csv_content


class WorkdayRAASService(ABC):
    """
    Generic Service to support RAAS endpoint
    (One export Payload answer)
    """
    def __init__(
            self,
            url: str,
            tenant: str,
            token: str,
            wd_ns_value: str,  # Ex: 'urn:com.workday.report/INT-UPD-001_MasterData_Companies'
    ):
        self.url = url
        self.tenant = tenant
        self.token = token
        # XML Parameters
        self.wd_ns_value = wd_ns_value
        self.raas_ns = {'wd': self.wd_ns_value}
        self.xml_helper = XMLHelper(ns=self.raas_ns)
        # cache Dictionary
        self.cache: Dict[str, T] = {}

    def get_raas_att_path(self, prpty: str):
        return '{' + self.raas_ns.get('wd') + '}' + prpty

    def get_tag_property_value(self, entry: ET.Element, tag_path: str, property_key: str):
        element = entry.find(tag_path, self.raas_ns)
        value = element.attrib.get(
            self.get_raas_att_path(property_key)) if element else None

        return value

    def generate_csv(self, list_data: List[T], fields, filename: Optional[str], prod=True):
        csv_helper = CSVExportHelper(fields=fields)
        csv_content = csv_helper.generate_csv_content(list_data)
        if not prod and filename:
            csv_helper.export_to_csv(csv_content, filename)

        return csv_content

    @abstractmethod
    def parse_raas_element(self, entry: ET.Element) -> Tuple[str, T]:
        """
        Convert XML node entry into Type T
        :param entry: XML element Node to convert
        :return: ID key to map the object T with its ID on the Dict
        """
        pass

    @retry_on_500()
    def __call_endpoint(self) -> bytes:
        """
        Implemented method to call an API GET endpoint and return the raw response as bytes

        :return: Bytes representation of response payload
        :raise: Raises :class:`HTTPError`
        """
        # Generate header
        headers = {
            'Content-Type': 'application/xml',
            'Authorization': f'Bearer {self.token}'
        }

        response = requests.get(self.url, headers=headers)

        response.raise_for_status()  # Raise an error for bad status codes

        return response.content

    def _parse_all_raas_element(self, element_entries_path: str = 'wd:Report_Entry') -> Dict[str, T]:
        """
        Parse the Raas Endpoint Answer

        :param element_entries_path: path of the element node entries to retrieve
        :return: Dict of key = Entity ID : T
        """
        # Call the Raas endpoint and get payload result
        xml_data = self.__call_endpoint()

        # Check if the input is bytes and convert to string if necessary
        if isinstance(xml_data, bytes):
            xml_data = self.xml_helper.bytes_to_utf8_string(xml_data)

        root = ET.fromstring(xml_data)
        namespace = self.raas_ns

        element_dict: Dict[str, T] = {}

        entries: List[ET.Element] = root.findall(element_entries_path, namespace)
        print(f'Found {len(entries)} entries.')
        for entry in entries:
            entity_key, mapped_object = self.parse_raas_element(entry)

            if entity_key:
                element_dict.update(
                    {
                        entity_key: mapped_object
                    }
                )

        return element_dict

    def get_entity_dic(self) -> Dict[str, T]:
        """
            Call the internal function to compute all the data and return it as a dictionary of UID and their matching
            object T
        :return: Dict of UID and Object T
        """
        data = self._parse_all_raas_element()

        return data

