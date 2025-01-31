import requests
import xml.etree.ElementTree as ET
from dataclasses import dataclass, asdict
from typing import List, Union, Dict, Any, Optional
import time
from functools import wraps
from datetime import datetime


# Global variable
FROM_CURRENCY_CODE = "USD"
WD_EFFECTIVE_TIMESTAMP_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'
KYRIBA_CURRENCY_RATE_TYPE_ID = 'Current'
PIGMENT_CURRENCY_RATE_TYPE_ID = 'Monthly_Average'


# DATACLASS OBJECTS
@dataclass
class CurrencyReference:
    Currency_ID: str
    Currency_Numeric_Code: str

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}


@dataclass
class CurrencyConversionRate:
    Effective_Timestamp: str
    Currency_Rate: float
    Currency_Rate_Type_ID: str
    From_Currency: CurrencyReference
    Target_Currency: CurrencyReference

    def dict(self):
        # Use dict() method from CurrencyReference for nested objects
        return {
            "Effective_Timestamp": self.Effective_Timestamp,
            "Currency_Rate": str(self.Currency_Rate),
            "Currency_Rate_Type_ID": self.Currency_Rate_Type_ID,
            "From_Currency": self.From_Currency.dict(),
            "Target_Currency": self.Target_Currency.dict(),
        }


@dataclass
class ResponseResults:
    total_results: int
    total_pages: int
    page_results: int
    page: int


class ProcessException(Exception):
    pass


def retry_on_500(retries=3, delay=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    # Call the original function
                    return func(*args, **kwargs)
                except requests.HTTPError as e:
                    # Check if the status code is 500
                    if e.response.status_code == 500:
                        attempt += 1
                        print(f"Attempt {attempt} failed with status 500. Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        # If it's not a 500 error, raise it immediately
                        raise
            # If we reach here, it means all retries have failed
            print("All retries failed.")
            raise
        return wrapper
    return decorator


class WorkdayConnector:
    def __init__(self, workday, tenant, client_id, client_secret, refresh_token, version='v42.1', xml_version='1.0'):
        self.workday = workday
        self.tenant = tenant
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.version = version
        self.xml_version = xml_version
        self.access_token = None
        self.base_uri = f'https://{self.workday}'

    @retry_on_500(retries=3, delay=2)
    def acquire_token(self):
        refresh_url = f'{self.base_uri}/ccx/oauth2/{self.tenant}/token'
        print(refresh_url)
        payload = {
            'grant_type': 'refresh_token',
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


class XMLHelper:
    @staticmethod
    def bytes_to_utf8_string(xml_bytes: bytes) -> str:
        """
        Converts bytes XML input to a UTF-8 encoded string.
        """
        return xml_bytes.decode('utf-8')

    @staticmethod
    def parse_xml_to_dict(xml_string):
        def _element_to_dict(element):
            # Recursively convert XML elements and their children to dictionary
            node = {}
            for child in element:
                child_tag = child.tag.split('}', 1)[-1]  # Remove namespace if present
                child_dict = _element_to_dict(child)
                if child_tag in node:
                    # Handle multiple children with the same tag
                    if not isinstance(node[child_tag], list):
                        node[child_tag] = [node[child_tag]]
                    node[child_tag].append(child_dict)
                else:
                    node[child_tag] = child_dict
            if element.text and element.text.strip():
                node['text'] = element.text.strip()
            if element.attrib:
                node['attributes'] = element.attrib
            return node

        root = ET.fromstring(xml_string)
        return {root.tag.split('}', 1)[-1]: _element_to_dict(root)}


class GetAllFXRates:

    def __init__(
            self,
            base_url,
            service_path,
            token,
            version,
            pigment_currency_rate_type_id=PIGMENT_CURRENCY_RATE_TYPE_ID,
            kyriba_currency_rate_type_id=KYRIBA_CURRENCY_RATE_TYPE_ID
    ):
        self.base_url = base_url
        self.token = token
        self.api_version = version
        self.url = f'{base_url}/ccx/service/{service_path}/Financial_Management/{version}'

        self.pigmt_currency_rate_type_id = pigment_currency_rate_type_id
        self.kyr_currency_rate_type_id = kyriba_currency_rate_type_id

        # Initialize variables for pagination
        self.xml_format = XMLHelper()
        self.xml_namespace = {
            'env': 'http://schemas.xmlsoap.org/soap/envelope/',
            'wd': 'urn:com.workday/bsvc'
        }

        self.is_complete = False
        self.next_page = 1
        self.total_record = 0
        self.total_page = 0

        self.all_fx_rates: List[CurrencyConversionRate] = []

    def parse_currency_conversion_rates(self, xml_input: Union[str, bytes]) -> List[CurrencyConversionRate]:
        """
        Parse the XML response and extract FX rates
        :param xml_input: Response payload
        :return: List of CurrencyConversionRate
        """
        # Check if the input is bytes and convert to string if necessary
        if isinstance(xml_input, bytes):
            xml_input = self.xml_format.bytes_to_utf8_string(xml_input)

        root = ET.fromstring(xml_input)
        ns = self.xml_namespace
        response_data = root.find('.//wd:Response_Data', ns)
        conversion_rates = []

        for rate in response_data.findall('wd:Currency_Conversion_Rate', ns):
            rate_data = rate.find('wd:Currency_Conversion_Rate_Data', ns)

            # Extract the Currency Rate
            currency_rate = float(rate_data.find('wd:Currency_Rate', ns).text)

            # Extract the Currency Rate Type ID
            rate_type_reference = rate_data.find('wd:Currency_Rate_Type_Reference', ns)
            currency_rate_type_id = rate_type_reference.find('wd:ID[@wd:type="Currency_Rate_Type_ID"]', ns).text

            # Extract effective timestamp date
            effective_timestamp = rate_data.find('wd:Effective_Timestamp', ns).text

            # Extract From Currency Information
            from_currency_ref = rate_data.find('wd:From_Currency_Reference', ns)
            from_currency = CurrencyReference(
                Currency_ID=from_currency_ref.find('wd:ID[@wd:type="Currency_ID"]', ns).text,
                Currency_Numeric_Code=from_currency_ref.find('wd:ID[@wd:type="Currency_Numeric_Code"]', ns).text
            )

            # Extract Target Currency Information
            target_currency_ref = rate_data.find('wd:Target_Currency_Reference', ns)
            target_currency = CurrencyReference(
                Currency_ID=target_currency_ref.find('wd:ID[@wd:type="Currency_ID"]', ns).text,
                Currency_Numeric_Code=target_currency_ref.find('wd:ID[@wd:type="Currency_Numeric_Code"]', ns).text
            )

            # Create a CurrencyConversionRate object and append it to the list
            conversion_rate = CurrencyConversionRate(
                Effective_Timestamp=effective_timestamp,
                Currency_Rate=currency_rate,
                Currency_Rate_Type_ID=currency_rate_type_id,
                From_Currency=from_currency,
                Target_Currency=target_currency
            )

            conversion_rates.append(conversion_rate)

        return conversion_rates

    def extract_response_results(self, xml_data: Union[str, bytes]) -> Optional[ResponseResults]:
        # Check if the input is bytes and convert to string if necessary
        if isinstance(xml_data, bytes):
            xml_data = self.xml_format.bytes_to_utf8_string(xml_data)
        # Parse the XML data
        root = ET.fromstring(xml_data)

        # Namespace dictionary to help with the parsing
        ns = self.xml_namespace

        # Find the Response_Filter element
        response_filter = root.find('.//wd:Response_Results', ns)

        try:
            # Extract the fields from the Response_Results element
            total_results = response_filter.find('wd:Total_Results', ns).text if response_filter.find(
                'wd:Total_Results',
                ns
            ).text is not None else None
            total_pages = response_filter.find('wd:Total_Pages', ns).text if response_filter.find(
                'wd:Total_Pages',
                ns
            ).text is not None else None
            page_results = response_filter.find('wd:Page_Results', ns).text if response_filter.find(
                'wd:Page_Results',
                ns
            ).text is not None else None

            page = response_filter.find('wd:Page', ns).text if response_filter.find('wd:Page', ns) is not None else None

            # Create and return a ResponseResults dataclass instance
            return ResponseResults(
                total_results=int(total_results),
                total_pages=int(total_pages),
                page_results=int(page_results),
                page=int(page)
            )
        except AttributeError as error:
            print(error)
            #raise ProcessException(f'No result found in that page with given param.')
            return None

    # @retry_on_500(retries=3, delay=2)
    def fetch_fx_rates(self, effective_timestamp: str, rates_type: str, next_page: int = None) -> bytes:
        """
        Call the FX rates Endpoint
        :param effective_timestamp: effective timestamp
        :param rates_type: Type of FX rates
        :param next_page: Next page number
        :return: response SOAP payload in bytes
        """
        headers = {
            'Content-Type': 'application/xml',
            'Authorization': f'Bearer {self.token}'
        }

        # If paginating, include the next page token in the request
        if next_page:
            payload = f'''<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<env:Envelope\r\n    xmlns:env=\"http://schemas.xmlsoap.org/soap/envelope/\"\r\n    xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\">\r\n    <env:Body>\r\n        <wd:Get_Currency_Conversion_Rates_Request\r\n            xmlns:wd=\"urn:com.workday/bsvc\"\r\n            wd:version=\"{self.api_version}\">\r\n            <wd:Request_Criteria>\r\n                \r\n\t\t\t\t<wd:Effective_Timestamp>{effective_timestamp}</wd:Effective_Timestamp>\r\n\r\n                <wd:Currency_Rate_Type_Reference> \r\n                    <wd:ID wd:type=\"Currency_Rate_Type_ID\">{rates_type}</wd:ID>\r\n                </wd:Currency_Rate_Type_Reference>\r\n            </wd:Request_Criteria>\r\n\r\n            <wd:Response_Filter>\r\n                <wd:Page>{next_page}</wd:Page>\r\n                <wd:Count>999</wd:Count>\r\n            </wd:Response_Filter>\r\n            <wd:Response_Group>\r\n                <wd:Include_Reference>true</wd:Include_Reference>\r\n            </wd:Response_Group>\r\n        </wd:Get_Currency_Conversion_Rates_Request>\r\n    </env:Body>\r\n</env:Envelope>'''
        else:
            payload = f'''<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<env:Envelope\r\n    xmlns:env=\"http://schemas.xmlsoap.org/soap/envelope/\"\r\n    xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\">\r\n    <env:Body>\r\n        <wd:Get_Currency_Conversion_Rates_Request\r\n            xmlns:wd=\"urn:com.workday/bsvc\"\r\n            wd:version=\"{self.api_version}\">\r\n            <wd:Request_Criteria>\r\n                \r\n\t\t\t\t<wd:Effective_Timestamp>{effective_timestamp}</wd:Effective_Timestamp>\r\n\r\n                <wd:Currency_Rate_Type_Reference> \r\n                    <wd:ID wd:type=\"Currency_Rate_Type_ID\">{rates_type}</wd:ID>\r\n                </wd:Currency_Rate_Type_Reference>\r\n            </wd:Request_Criteria>\r\n\r\n            <wd:Response_Filter>\r\n                <wd:Page>1</wd:Page>\r\n                <wd:Count>999</wd:Count>\r\n            </wd:Response_Filter>\r\n            <wd:Response_Group>\r\n                <wd:Include_Reference>true</wd:Include_Reference>\r\n            </wd:Response_Group>\r\n        </wd:Get_Currency_Conversion_Rates_Request>\r\n    </env:Body>\r\n</env:Envelope>'''

        response = requests.post(self.url, headers=headers, data=payload)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.content

    def fetch_currency_conversion_rates(self, effective_timestamp: str, rates_type: str) -> List[CurrencyConversionRate]:
        """
        Parse the FX rates response payload
        :param effective_timestamp:
        :param rates_type: Type : Current / Average_month / Average_YTD / End_of_ Month / Singapore / Israel / Egypte
        :return: List of extracted FX Rates
        """
        # Fetch all FX rates using pagination
        all_fx_rates = []
        # First call, get the first page
        response_content = self.fetch_fx_rates(effective_timestamp, rates_type, None)

        # Check for the result page data in the response
        next_page_data = self.extract_response_results(response_content)

        if next_page_data is not None:
            self.total_page = next_page_data.total_pages
            self.next_page = next_page_data.page
            self.total_record = next_page_data.total_results

            # get first results
            fx_rates = self.parse_currency_conversion_rates(response_content)
            print(f'Found: {len(fx_rates)} rates')
            all_fx_rates.extend(fx_rates)

            if next_page_data.page >= 1:
                for page in range(2, self.total_page + 1):
                    # call next page
                    self.next_page = page
                    response_content = self.fetch_fx_rates(effective_timestamp, rates_type, self.next_page)
                    fx_rates = self.parse_currency_conversion_rates(response_content)
                    all_fx_rates.extend(fx_rates)

            # Now `all_fx_rates` contains all the FX rates retrieved across all pages
            print(f"Total FX rates fetched: {len(all_fx_rates)}")
            self.is_complete = len(all_fx_rates) == self.total_record

            print(f"Is Complete: {self.is_complete}")
            if not self.is_complete:
                raise ProcessException(
                    f"The number found is {self.total_record}, but fetch {len(all_fx_rates)} records."
                )

        return all_fx_rates

    def filter_data_by_rate_types(self, rate_type: str) -> List[CurrencyConversionRate]:
        return [data for data in self.all_fx_rates if data.Currency_Rate_Type_ID == rate_type]


def convert_datetime_string(datetime_str, current_format, target_format) -> str:
    """
    Convert the input string to a datetime object using the current format
    :param datetime_str: date time string value to convert
    :param current_format: current date time format from the string to convert
    :param target_format: Targeted format
    :return: Converted string datime with the targeted format
    """
    dt = datetime.strptime(datetime_str, current_format)

    # Return the datetime object as a string in the target format
    return dt.strftime(target_format)


def is_same_date(current_date: str, last_day_date: str):
    return current_date.startswith(last_day_date)


def create_export_fx_rates(
        fx_rates: List[CurrencyConversionRate],
        target_format: str,
        last_day_date: str
) -> List[Dict[str, Any]]:
    """
        In Exported Systems.  All rates must be USD against currencies (for example USD/AED or USD/EUR).
        target_format: the date format you want to convert the date for the targeted System, e.g: %Y-%m-%d
        :return List of Dict with converted Effective_Timestamp as date , Currency Code and Exchange rate
    """
    exported_rates: List[Dict[str, Any]] = []
    wanted_target_ccy = FROM_CURRENCY_CODE.strip().lower()
    print(f'{len(fx_rates)} Fx Rates found')
    for rates in fx_rates:
        current_from_ccy = rates.From_Currency.Currency_ID.strip().lower()
        #print(rates.Effective_Timestamp)
        if current_from_ccy == wanted_target_ccy and is_same_date(rates.Effective_Timestamp, last_day_date):
            data = {
                # convert Effective_Timestamp
                "Date": convert_datetime_string(
                    rates.Effective_Timestamp,
                    WD_EFFECTIVE_TIMESTAMP_DATE_FORMAT,
                    target_format
                ),
                "Currency": rates.Target_Currency.Currency_ID,
                "Exchange_Rate": rates.Currency_Rate
            }
            exported_rates.append(data)

    print(f'Found {len(exported_rates)} FX Rates USD/<XXX> pairs.')
    return exported_rates


def main(input):
    # Replace with actual credentials and details
    workday = input['workday_server']
    tenant = input['workday_tenant']
    client_id = input['workday_client_id']
    client_secret = input['workday_client_secret']
    refresh_token = input['workday_refresh_token']
    effective_timestamp = input['effective_timestamp']  # Supposed to be the last day of the previous month
    pigment_currency_rate_type_id = input['pigment_currency_rate_type_id']
    kyriba_currency_rate_type_id = input['kyriba_currency_rate_type_id']

    connector = WorkdayConnector(workday, tenant, client_id, client_secret, refresh_token)
    connector.acquire_token()

    fx_rates = GetAllFXRates(
        base_url=connector.base_uri,
        service_path=connector.tenant,
        token=connector.access_token,
        version=connector.version,
        pigment_currency_rate_type_id=pigment_currency_rate_type_id,
        kyriba_currency_rate_type_id=kyriba_currency_rate_type_id
    )

    kyr_all_fx_rates = fx_rates.fetch_currency_conversion_rates(effective_timestamp, kyriba_currency_rate_type_id)
    # effective date Should be the last day of the month for average
    pgm_all_fx_rates = fx_rates.fetch_currency_conversion_rates(effective_timestamp, pigment_currency_rate_type_id)
    last_day_date = effective_timestamp[:10]  # take only the start of the US date e.g: 2024-07-26
    print(last_day_date)
    try:
        pass

        return {
            "kyriba_fx_rates": create_export_fx_rates(kyr_all_fx_rates, '%d/%m/%Y', last_day_date),
            "pigment_fx_rates": create_export_fx_rates(pgm_all_fx_rates, '%Y-%m-%d', last_day_date),
            #"zuora_fx_rates": create_export_fx_rates(fx_rates.all_fx_rates, '%d-%m-%Y', last_day_date),
            #"fx_rates": [data.dict() for data in fx_rates.all_fx_rates],
        }
    except requests.HTTPError as error:
        return {"error": error, "fx_rates": [], "kyriba_fx_rates": [], "pigment_fx_rates": [], "zuora_fx_rates": []}
    except Exception as error:
        return {"error": error, "fx_rates": [], "kyriba_fx_rates": [], "pigment_fx_rates": [], "zuora_fx_rates": []}

