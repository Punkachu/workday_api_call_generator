from workday_generator_api import *
from abc import ABC
import xml.etree.ElementTree as ET

from models import *


class GetResourceCategories(WorkdayService, ABC):
    """ Get Resource Categories with resource management endpoint """

    def __init__(self, base_url: str, tenant: str, token: str, api_version: str = 'v42.1'):
        # Initialize the parent class (WorkdayService)
        self._url = f'{base_url}/ccx/service/{tenant}/Resource_Management/{api_version}'
        self.namespace = {'wd': 'urn:com.workday/bsvc'}

        super().__init__(self._url, tenant, token, self.namespace)

    def _generate_payload_pagination(self, next_page: int, **kwargs) -> str:
        payload = f"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<env:Envelope\r\n    xmlns:env=\"http://schemas.xmlsoap.org/soap/envelope/\"\r\n    xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\">\r\n    <env:Body>\r\n        <wd:Get_Resource_Categories_Request\r\n            xmlns:wd=\"urn:com.workday/bsvc\"\r\n            wd:version=\"v42.2\">\r\n            \r\n            <wd:Response_Filter>\r\n                <wd:Page>{next_page}</wd:Page>\r\n                <wd:Count>999</wd:Count>\r\n            </wd:Response_Filter>\r\n           \r\n            <wd:Response_Group>\r\n                <wd:Include_Reference>true</wd:Include_Reference>\r\n            </wd:Response_Group>\r\n        </wd:Get_Resource_Categories_Request>\r\n    </env:Body>\r\n</env:Envelope>"
        return payload

    def _get_entity_id(self, entry: ET.Element) -> Optional[str]:
        spend_category_id: str = self.xml_helper.get_single_tag_line_value(entry, 'wd:Resource_Category_ID', str)
        return spend_category_id

    def _generate_payload(self, entity_id: str, **kwargs):
        """generate the body request payload"""
        payload = f"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<env:Envelope\r\n    xmlns:env=\"http://schemas.xmlsoap.org/soap/envelope/\"\r\n    xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\">\r\n    <env:Body>\r\n        <wd:Get_Resource_Categories_Request\r\n            xmlns:wd=\"urn:com.workday/bsvc\"\r\n            wd:version=\"v42.2\">\r\n            \r\n            <wd:Request_References>\r\n                <wd:Resource_Category_Reference>\r\n                    <wd:ID wd:type=\"Spend_Category_ID\">{entity_id}</wd:ID>\r\n                </wd:Resource_Category_Reference>\r\n            </wd:Request_References>\r\n           \r\n            <wd:Response_Group>\r\n                <wd:Include_Reference>true</wd:Include_Reference>\r\n            </wd:Response_Group>\r\n        </wd:Get_Resource_Categories_Request>\r\n    </env:Body>\r\n</env:Envelope>"
        return payload

    def _parse_entity_element(self, entry: ET.Element) -> SpendCategory:
        """Parses an XML element and returns a Type T object"""
        # Find the Supplier ID
        spend_category_id: str = self.xml_helper.get_single_tag_line_value(entry, 'wd:Resource_Category_ID', str)
        # Get the Supplier_Name
        spend_category_name = self.xml_helper.get_single_tag_line_value(entry, 'wd:Resource_Category_Name', str)

        return SpendCategory(code=spend_category_id, name=spend_category_name)

    def _update_cache(self, spend_category: SpendCategory):
        self.cache.update({spend_category.code: spend_category})

    # def get_spend_category_by_id(self, spend_cat_id: str) -> SpendCategory:
    #     return self._get_entity(spend_cat_id, self.resource_xml_path, method='POST')


class GetCustomerContracts(WorkdayService, ABC):
    """ Get Customer Contract aka Deals with the Revenue Management endpoint """

    def __init__(self, base_url: str, tenant: str, token: str, api_version: str = 'v42.1'):
        # Initialize the parent class (WorkdayService)
        self._url = f'{base_url}/ccx/service/{tenant}/Revenue_Management/{api_version}'
        self.namespace = {'wd': 'urn:com.workday/bsvc'}

        super().__init__(self._url, tenant, token, self.namespace)

    def _generate_payload_pagination(self, next_page: int, **kwargs) -> str:
        payload = f"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<env:Envelope\r\n    xmlns:env=\"http://schemas.xmlsoap.org/soap/envelope/\"\r\n    xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\">\r\n    <env:Body>\r\n        <wd:Get_Customer_Contracts_Request\r\n            xmlns:wd=\"urn:com.workday/bsvc\"\r\n            wd:version=\"v42.2\">\r\n            \r\n            <wd:Response_Filter>\r\n                <wd:Page>{next_page}</wd:Page>\r\n                <wd:Count>999</wd:Count>\r\n            </wd:Response_Filter>\r\n           \r\n            <wd:Response_Group>\r\n                <wd:Include_Reference>true</wd:Include_Reference>\r\n                <wd:Include_Customer_Contract_Data>true</wd:Include_Customer_Contract_Data>\r\n            </wd:Response_Group>\r\n        </wd:Get_Customer_Contracts_Request>\r\n    </env:Body>\r\n</env:Envelope>"
        return payload

    def _get_entity_id(self, entry: ET.Element) -> Optional[str]:
        customer_contract_id: str = self.xml_helper.get_single_tag_line_value(entry, 'wd:Customer_Contract_ID', str)
        return customer_contract_id

    def _generate_payload(self, entity_id: str, **kwargs):
        """generate the body request payload"""
        payload = f"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<env:Envelope\r\n    xmlns:env=\"http://schemas.xmlsoap.org/soap/envelope/\"\r\n    xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\">\r\n    <env:Body>\r\n        <wd:Get_Customer_Contracts_Request\r\n            xmlns:wd=\"urn:com.workday/bsvc\"\r\n            wd:version=\"v42.2\">\r\n            \r\n            <wd:Request_References>\r\n                <wd:Customer_Contract_Reference>\r\n                    <wd:ID wd:type=\"Customer_Contract_Reference_ID\">{entity_id}</wd:ID>\r\n                </wd:Customer_Contract_Reference>\r\n            </wd:Request_References>\r\n           \r\n            <wd:Response_Group>\r\n                <wd:Include_Reference>true</wd:Include_Reference>\r\n                <wd:Include_Customer_Contract_Data>true</wd:Include_Customer_Contract_Data>\r\n            </wd:Response_Group>\r\n        </wd:Get_Customer_Contracts_Request>\r\n    </env:Body>\r\n</env:Envelope>"
        return payload

    def _parse_entity_element(self, entry: ET.Element) -> DealInfo:
        """Parses an XML element and returns a Type T object"""
        # Find the Customer_Contract_ID
        customer_contract_id: str = self.xml_helper.get_single_tag_line_value(entry, 'wd:Customer_Contract_ID', str)
        # Get the Contract_Name
        contract_name = self.xml_helper.get_single_tag_line_value(entry, 'wd:Contract_Name', str)
        # Get PO_Number
        po_number = self.xml_helper.get_single_tag_line_value(entry, 'wd:PO_Number', str)
        # Get On_Hold
        on_hold = bool(self.xml_helper.get_single_tag_line_value(entry, 'wd:On_Hold', int))
        # Get Customer_Contract_Type_Reference
        contract_type = self.xml_helper.get_single_tag_nested_value(entry, 'wd:Customer_Contract_Type_Reference',
                                                                    'wd:ID[@wd:type="Contract_Type_ID"]', str)
        return DealInfo(
            customer_contract_id=customer_contract_id,
            contract_name=contract_name,
            po_number=po_number,
            on_hold=on_hold,
            contract_type=contract_type,
        )

    def _update_cache(self, deal: DealInfo):
        self.cache.update({deal.customer_contract_id: deal})


class Region(WorkdayService, ABC):
    """ Get GTM Organization Region data (For Revenue only) """

    def __init__(self, base_url: str, tenant: str, token: str, api_version: str = 'v42.1'):
        # Initialize the parent class (WorkdayService)
        self._url = f'{base_url}/ccx/service/{tenant}/Recruiting/{api_version}'
        self.namespace = {'wd': 'urn:com.workday/bsvc'}

        super().__init__(self._url, tenant, token, self.namespace)

    def _generate_payload_pagination(self, next_page: int, **kwargs) -> str:
        payload = f"<?xml version=\"1.0\" ?>\r\n<env:Envelope xmlns:env=\"http://schemas.xmlsoap.org/soap/envelope/\">\r\n    <env:Body>\r\n        <wd:Get_Organizations_Request xmlns:wd=\"urn:com.workday/bsvc\" wd:version=\"v42.2\">\r\n            <wd:Response_Filter>\r\n                <wd:Page>{next_page}</wd:Page>\r\n                <wd:Count>999</wd:Count>\r\n            </wd:Response_Filter>\r\n            <wd:Response_Group>\r\n                <wd:Include_Hierarchy_Data>true</wd:Include_Hierarchy_Data>\r\n            </wd:Response_Group>\r\n        </wd:Get_Organizations_Request>\r\n    </env:Body>\r\n</env:Envelope>"
        return payload

    def _get_entity_id(self, entry: ET.Element) -> Optional[str]:
        code: str = self.xml_helper.get_single_tag_line_value(entry, 'wd:Reference_ID', str)
        return code

    def _generate_payload(self, entity_id: str, **kwargs):
        """generate the body request payload"""
        payload = f"<?xml version=\"1.0\" ?>\r\n<env:Envelope xmlns:env=\"http://schemas.xmlsoap.org/soap/envelope/\">\r\n    <env:Body>\r\n        <wd:Get_Organizations_Request xmlns:wd=\"urn:com.workday/bsvc\" wd:version=\"v42.2\">\r\n            <wd:Request_References>\r\n                <wd:Organization_Reference>\r\n                    <wd:ID wd:type=\"Organization_Reference_ID\">{entity_id}</wd:ID>\r\n                </wd:Organization_Reference>\r\n            </wd:Request_References>\r\n            <wd:Response_Group>\r\n                <wd:Include_Hierarchy_Data>true</wd:Include_Hierarchy_Data>\r\n            </wd:Response_Group>\r\n        </wd:Get_Organizations_Request>\r\n    </env:Body>\r\n</env:Envelope>"
        return payload

    def _parse_entity_element(self, entry: ET.Element) -> RegionInfo:
        """
        Parse the Get Region Organization response paylaod
        :param entry: XML element from soap payload  response
        :return: [RegionInfo]
        """
        code: str = self.xml_helper.get_single_tag_line_value(entry, 'wd:Reference_ID', str)
        name = self.xml_helper.get_single_tag_line_value(entry, 'wd:Name', str)

        return RegionInfo(code=code, name=name)

    def _update_cache(self, region: RegionInfo):
        self.cache.update({region.code: region})

    # def get_region(self, region_id: str) -> DealInfo:
    #     return self._get_entity(region_id, self.resource_xml_path, method='POST')


class GetRAASSuppliers(WorkdayService, ABC):
    """
        Get all Vendors aka Suppliers
        ADN DOCUMENTATION LINK:
        https://community.workday.com/sites/default/files/file-hosting/productionapi/Resource_Management/v43.0/Get_Suppliers.html
    """

    def __init__(
            self, base_url: str,
            tenant: str, token: str,
            api_version: str = 'v42.1',
    ):
        # Initialize the parent class (WorkdayService)
        self._url = f'{base_url}/ccx/service/{tenant}/Resource_Management/{api_version}'
        self.namespace = {'wd': 'urn:com.workday/bsvc'}

        super().__init__(self._url, tenant, token, self.namespace)

    def _generate_payload_pagination(self, next_page: int, **kwargs) -> str:
        payload = f"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<env:Envelope\r\n    xmlns:env=\"http://schemas.xmlsoap.org/soap/envelope/\"\r\n    xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\">\r\n    <env:Body>\r\n        <wd:Get_Suppliers_Request xmlns:wd=\"urn:com.workday/bsvc\">\r\n            <wd:Response_Filter>\r\n                <wd:Page>{next_page}</wd:Page>\r\n                <wd:Count>999</wd:Count>\r\n            </wd:Response_Filter>\r\n            <wd:Response_Group>\r\n                <wd:Include_Reference>true</wd:Include_Reference>\r\n                <wd:Include_Attachment_Data>true</wd:Include_Attachment_Data>\r\n            </wd:Response_Group>\r\n        </wd:Get_Suppliers_Request>\r\n    </env:Body>\r\n</env:Envelope>"
        return payload

    def _get_entity_id(self, entry: ET.Element) -> Optional[str]:
        supplier_id: str = self.xml_helper.get_single_tag_line_value(entry, 'wd:Supplier_ID', str)
        return supplier_id

    def _generate_payload(self, entity_id: str, **kwargs):
        """generate the body request payload"""
        as_of_effective_date = None
        as_of_entry_datetime = None
        for key, value in kwargs.items():
            if key == 'as_of_effective_date':
                as_of_effective_date = value
            elif key == 'as_of_entry_datetime':
                as_of_entry_datetime = value

        _as_of_effective_date_filter: str = f"<wd:As_Of_Effective_Date>{as_of_effective_date}</wd:As_Of_Effective_Date>\r\n" if as_of_effective_date is not None else ""
        _as_of_entry_dateTime: Optional[
            str] = f"<wd:As_Of_Entry_DateTime>{as_of_entry_datetime}</wd:As_Of_Entry_DateTime>\r\n" if as_of_entry_datetime is not None else ""

        payload = f"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<env:Envelope\r\n    xmlns:env=\"http://schemas.xmlsoap.org/soap/envelope/\"\r\n    xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\">\r\n    <env:Body>\r\n        <wd:Get_Suppliers_Request xmlns:wd=\"urn:com.workday/bsvc\">\r\n        \r\n            <wd:Request_References>\r\n                <wd:Supplier_Reference>\r\n                    <wd:ID wd:type=\"Supplier_ID\">{entity_id}</wd:ID>\r\n                </wd:Supplier_Reference>\r\n            </wd:Request_References>\r\n           \r\n            <wd:Response_Filter>\r\n                {_as_of_effective_date_filter}                {_as_of_entry_dateTime}                <wd:Page>1</wd:Page>\r\n                <wd:Count>1</wd:Count>\r\n            </wd:Response_Filter>\r\n            <wd:Response_Group>\r\n                <wd:Include_Reference>true</wd:Include_Reference>\r\n                <wd:Include_Attachment_Data>true</wd:Include_Attachment_Data>\r\n            </wd:Response_Group>\r\n        </wd:Get_Suppliers_Request>\r\n    </env:Body>\r\n</env:Envelope>"

        return payload

    def _parse_entity_element(self, entry: ET.Element) -> VendorInfo:
        """
        Parse the Get supplier response paylaod

        :param entry: XML element node
        :return: [VendorInfo]
        """
        # Find the Supplier ID
        supplier_id: str = self.xml_helper.get_single_tag_line_value(entry, 'wd:Supplier_ID', str)
        supplier_ref_id: str = self.xml_helper.get_single_tag_line_value(entry, 'wd:Supplier_Reference_ID', str)
        supplier_name = self.xml_helper.get_single_tag_line_value(entry, 'wd:Supplier_Name', str)
        worktag_only = bool(self.xml_helper.get_single_tag_line_value(entry, 'wd:Worktag_Only', int))
        submit: Optional[bool] = bool(self.xml_helper.get_single_tag_line_value(entry, 'wd:Submit', int))

        app_status = self.xml_helper.get_single_tag_nested_value(entry, 'wd:Approval_Status_Reference',
                                                                 'wd:ID[@wd:type="Document_Status_ID"]', str)
        supplier_category = self.xml_helper.get_single_tag_nested_value(
            entry, 'wd:Supplier_Category_Reference', 'wd:ID[@wd:type="Supplier_Category_ID"]', str
        )
        supplier_group_category = self.xml_helper.get_single_tag_nested_value(
            entry, 'wd:Supplier_Group_Reference', 'wd:ID[@wd:type="Supplier_Group_ID"]', str
        )
        fatca: Optional[bool] = bool(self.xml_helper.get_single_tag_line_value(entry, 'wd:FATCA', int))
        disable_change_order: Optional[bool] = bool(
            self.xml_helper.get_single_tag_line_value(entry, 'wd:Disable_Change_Order', int))
        acknowledgement_expected: Optional[bool] = bool(
            self.xml_helper.get_single_tag_line_value(entry, 'wd:Acknowledgement_Expected', int))
        payment_terms_reference = self.xml_helper.get_single_tag_nested_value(
            entry, 'wd:Payment_Terms_Reference', 'wd:ID[@wd:type="Payment_Terms_ID"]', str
        )
        default_payment_type_reference = self.xml_helper.get_single_tag_nested_value(
            entry, 'wd:Default_Payment_Type_Reference', 'wd:ID[@wd:type="Payment_Type_ID"]', str
        )
        invoice_any_supplier: Optional[int] = self.xml_helper.get_single_tag_line_value(
            entry, 'wd:Invoice_Any_Supplier', int
        )
        supplier_minimum_order_amount: Optional[int] = self.xml_helper.get_single_tag_line_value(
            entry, 'wd:Supplier_Minimum_Order_Amount', int
        )
        edit_port_taxes: Optional[bool] = bool(
            self.xml_helper.get_single_tag_line_value(entry, 'wd:Edit_Portal_Taxes', int))
        irs_1099_supplier: Optional[bool] = bool(
            self.xml_helper.get_single_tag_line_value(entry, 'wd:IRS_1099_Supplier', int))
        asn_due_in_days: Optional[int] = self.xml_helper.get_single_tag_line_value(entry, 'wd:ASN_Due_In_Days', int)
        enable_asn: Optional[bool] = bool(self.xml_helper.get_single_tag_line_value(entry, 'wd:Enable_ASN', int))
        enable_global_location_number: Optional[bool] = bool(
            self.xml_helper.get_single_tag_line_value(entry, 'wd:Enable_Global_Location_Number', int)
        )

        return VendorInfo(
            company_name=supplier_name,
            vendor_code=supplier_id,
            irs_1099_supplier=irs_1099_supplier,
            supplier_category=supplier_category,
            invoice_any_supplier=invoice_any_supplier,
            supplier_group_category=supplier_group_category,
            supplier_minimum_order_amount=supplier_minimum_order_amount,
            submit=submit,
            enable_asn=enable_asn,
            worktag_only=worktag_only,
            enable_global_location_number=enable_global_location_number,
            approval_status=app_status,
            vendor_ref_id=supplier_ref_id,
            asn_due_in_days=asn_due_in_days,
            edit_port_taxes=edit_port_taxes,
            default_payment_type_reference=default_payment_type_reference,
            disable_change_order=disable_change_order,
            acknowledgement_expected=acknowledgement_expected,
            payment_terms_reference=payment_terms_reference,
            fatca=fatca,
        )

    def _update_cache(self, vendor: VendorInfo):
        self.cache.update({vendor.vendor_code: vendor})


class GetPaymentMethod(WorkdayService, ABC):
    """
    Get PAYMENT METHODS
    DOCUMENTATION LINK:
    https://community.workday.com/sites/default/files/file-hosting/productionapi/Financial_Management/v43.0/Get_Payment_Terms.html
     """

    def __init__(self, base_url: str, tenant: str, token: str, api_version: str = 'v42.1'):
        # Initialize the parent class (WorkdayService)
        self._url = f'{base_url}/ccx/service/{tenant}/Financial_Management/{api_version}'
        self.namespace = {'wd': 'urn:com.workday/bsvc'}

        super().__init__(self._url, tenant, token, self.namespace)

    def _generate_payload_pagination(self, next_page: int, **kwargs) -> str:
        """generate the body request payload"""
        as_of_effective_date = None
        as_of_entry_datetime = None
        for key, value in kwargs.items():
            if key == 'as_of_effective_date':
                as_of_effective_date = value
            elif key == 'as_of_entry_datetime':
                as_of_entry_datetime = value

        _as_of_effective_date_filter: str = f"<wd:As_Of_Effective_Date>{as_of_effective_date}</wd:As_Of_Effective_Date>\r\n" if as_of_effective_date is not None else ""
        _as_of_entry_dateTime: Optional[
            str] = f"<wd:As_Of_Entry_DateTime>{as_of_entry_datetime}</wd:As_Of_Entry_DateTime>\r\n" if as_of_entry_datetime is not None else ""

        payload = f"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<env:Envelope\r\n    xmlns:env=\"http://schemas.xmlsoap.org/soap/envelope/\"\r\n    xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\">\r\n    <env:Body>\r\n        <wd:Get_Payment_Terms_Request xmlns:wd=\"urn:com.workday/bsvc\" wd:version=\"v42.0\">\r\n            <wd:Response_Filter>\r\n                {as_of_effective_date}                {_as_of_entry_dateTime}                <wd:Page>{next_page}</wd:Page>\r\n                <wd:Count>999</wd:Count>\r\n            </wd:Response_Filter>\r\n            <wd:Response_Group>\r\n                <wd:Include_Reference>true</wd:Include_Reference>\r\n            </wd:Response_Group>\r\n        </wd:Get_Payment_Terms_Request>\r\n    </env:Body>\r\n</env:Envelope>"
        return payload

    def _get_entity_id(self, entry: ET.Element) -> Optional[str]:
        payment_term_id: str = self.xml_helper.get_single_tag_line_value(entry, 'wd:Payment_Terms_ID', str)
        return payment_term_id

    def _generate_payload(self, entity_id: str, **kwargs):
        """generate the body request payload"""
        payload = f"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<env:Envelope\r\n    xmlns:env=\"http://schemas.xmlsoap.org/soap/envelope/\"\r\n    xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\">\r\n    <env:Body>\r\n        <wd:Get_Payment_Terms_Request xmlns:wd=\"urn:com.workday/bsvc\" wd:version=\"v42.0\">\r\n            <wd:Request_References>\r\n                <wd:Payment_Term_Reference>\r\n                    <wd:ID wd:type=\"Payment_Terms_ID\">{entity_id}</wd:ID>\r\n                </wd:Payment_Term_Reference>\r\n            </wd:Request_References>  \r\n            <wd:Response_Group>\r\n                <wd:Include_Reference>true</wd:Include_Reference>\r\n            </wd:Response_Group>\r\n        </wd:Get_Payment_Terms_Request>\r\n    </env:Body>\r\n</env:Envelope>"
        return payload

    def _parse_entity_element(self, entry: ET.Element) -> PaymentMethod:
        """Parses an XML element and returns a Type T object"""
        payment_term_id: str = self.xml_helper.get_single_tag_line_value(entry, 'wd:Payment_Terms_ID', str)
        name = self.xml_helper.get_single_tag_line_value(entry, 'wd:Payment_Terms_Name', str)

        cut_off_day = self.xml_helper.get_single_tag_line_value(entry, 'wd:Cut-Off_Day', int)
        grace_days = self.xml_helper.get_single_tag_line_value(entry, 'wd:Grace_Days', int)
        payment_discount_days = self.xml_helper.get_single_tag_line_value(entry, 'wd:Payment_Discount_Days', int)
        payment_discount_percent = self.xml_helper.get_single_tag_line_value(entry, 'wd:Payment_Discount_Percent', int)

        return PaymentMethod(
            payment_term_id=payment_term_id,
            name=name,
            cut_off_day=cut_off_day,
            payment_discount_days=payment_discount_days,
            payment_discount_percent=payment_discount_percent,
            grace_days=grace_days
        )

    def _update_cache(self, obj: PaymentMethod):
        self.cache.update({obj.payment_term_id: obj})


class GetCurrencies(WorkdayService, ABC):
    """
        Get all Currencies and find a specific currency
        ADN DOCUMENTATION LINK:
        https://community.workday.com/sites/default/files/file-hosting/productionapi/Financial_Management/v42.1/GetAll_Currencies.html
    """

    def __init__(
            self, base_url: str,
            tenant: str, token: str,
            api_version: str = DEFAULT_WORKDAY_API_VERSION,
    ):
        # Initialize the parent class (WorkdayService)
        self._url = f'{base_url}/ccx/service/{tenant}/Financial_Management/{api_version}'
        self.namespace = {'wd': 'urn:com.workday/bsvc'}

        super().__init__(self._url, tenant, token, self.namespace)

    def _generate_payload_pagination(self, next_page: int, **kwargs) -> str:
        payload = """<?xml version="1.0" encoding="UTF-8"?>
        <env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
            <env:Body>
                <wd:Currency_GetAll xmlns:wd="urn:com.workday/bsvc">
                </wd:Currency_GetAll>
            </env:Body>
        </env:Envelope>"""
        return payload

    def _get_entity_id(self, entry: ET.Element) -> Optional[str]:
        currency_id: str = self.xml_helper.get_single_tag_line_value(entry, 'wd:Currency_ID', str)
        return currency_id

    def _generate_payload(self, entity_id: str, **kwargs):
        """generate the body request payload"""
        payload = """<?xml version="1.0" encoding="UTF-8"?>
        <env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
        	<env:Body>
        		<wd:Currency_GetAll xmlns:wd="urn:com.workday/bsvc">
        		</wd:Currency_GetAll>
        	</env:Body>
        </env:Envelope>"""
        return payload

    def _parse_entity_element(self, entry: ET.Element) -> WORKDAYCurrency:
        """
        Parse the Get currency response paylaod

        :param entry: XML element node
        :return: [WORKDAYCurrency]
        """
        # Find the Supplier ID
        currency_id: str = self.xml_helper.get_single_tag_line_value(entry, 'wd:Currency_ID', str)
        currency_description: str = self.xml_helper.get_single_tag_line_value(entry, 'wd:Currency_Description', str)
        currency_numeric_code = self.xml_helper.get_single_tag_line_value(entry, 'wd:Currency_Numeric_Code', str)
        wid = self.xml_helper.get_single_tag_line_value(entry, 'wd:WID', str)

        return WORKDAYCurrency(
            wid=wid,
            currency_id=currency_id,
            currency_description=currency_description,
            currency_numeric_code=currency_numeric_code,
        )

    def _update_cache(self, currency: WORKDAYCurrency):
        self.cache.update({currency.currency_id: currency})


class GetAllJournals(WorkdayService, ABC):

    def __init__(
            self, base_url: str,
            tenant: str,
            token: str,
            ledger_accounts: Dict[str, LedgerAccount],
            cost_centers: Dict[str, CostCenterInfo],
            subsidiaries: Dict[str, SubsidiaryInfo],
            book_codes: Dict[str, BookCodeInfo],
            gtm_org: Dict[str, GeoSales],
            raas_suppliers: GetRAASSuppliers,
            resource_category_service: GetResourceCategories,
            customer_contract_service: GetCustomerContracts,
            api_version: str = DEFAULT_WORKDAY_API_VERSION,
    ):
        # Initialize the parent class (WorkdayService)
        self._url = f'{base_url}/ccx/service/{tenant}/Financial_Management/{api_version}'
        self.api_version = api_version
        self.namespace = {'wd': 'urn:com.workday/bsvc'}

        # Initialize the external data resources
        self.resource_category_service = resource_category_service
        self.customer_contract_service = customer_contract_service
        # Dict Data
        self.ledger_accounts = ledger_accounts
        self.cost_centers = cost_centers
        self.subsidiaries = subsidiaries
        self.book_codes = book_codes
        self.raas_suppliers = raas_suppliers
        self.gtm_org = gtm_org

        # Will be updated within `parse_journals` and `map_workday_journal_to_pigment_data` functions
        self.failed_journals: List[FailedProcessedJournal] = []

        super().__init__(self._url, tenant, token, self.namespace)

    """ Override """

    def _generate_payload_pagination(self, next_page: int, **kwargs) -> str:
        as_of_effective_date = None
        as_of_entry_datetime = None
        accounting_from_date = None
        accounting_to_date = None
        for key, value in kwargs.items():
            if key == 'as_of_effective_date':
                as_of_effective_date = value
            elif key == 'as_of_entry_datetime':
                as_of_entry_datetime = value
            # Mandatory fields
            elif key == 'accounting_from_date':
                accounting_from_date = value
            elif key == 'accounting_to_date':
                accounting_to_date = value

        _as_of_effective_date_filter: str = f"<wd:As_Of_Effective_Date>{as_of_effective_date}</wd:As_Of_Effective_Date>\r\n" if as_of_effective_date is not None else ""
        _as_of_entry_dateTime: Optional[
            str] = f"<wd:As_Of_Entry_DateTime>{as_of_entry_datetime}</wd:As_Of_Entry_DateTime>\r\n" if as_of_entry_datetime is not None else ""

        payload = f"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<env:Envelope\r\n    " \
                  f"xmlns:env=\"http://schemas.xmlsoap.org/soap/envelope/\"\r\n    " \
                  f"xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\">\r\n    <env:Body>\r\n        " \
                  f"<wd:Get_Journals_Request xmlns:wd=\"urn:com.workday/bsvc\" " \
                  f"wd:version=\"{self.api_version}\">\r\n\t\t\t<wd:Request_Criteria>\r\n\t\t\t\t<wd:Accounting_From_Date>" \
                  f"{accounting_from_date}</wd:Accounting_From_Date>\r\n\t\t\t\t<wd:Accounting_To_Date >" \
                  f"{accounting_to_date}</wd:Accounting_To_Date>\r\n\t\t\t</wd:Request_Criteria>\r\n            " \
                  f"<wd:Response_Filter>\r\n                {_as_of_entry_dateTime}                " \
                  f"{_as_of_effective_date_filter}                <wd:Page>{next_page}</wd:Page>\r\n                " \
                  f"<wd:Count>999</wd:Count>\r\n            </wd:Response_Filter>\r\n            " \
                  f"<wd:Response_Group>\r\n                " \
                  f"<wd:Include_Attachment_Data>true</wd:Include_Attachment_Data>\r\n            " \
                  f"</wd:Response_Group>\r\n        </wd:Get_Journals_Request>\r\n    </env:Body>\r\n</env:Envelope> "
        return payload

    """ Override """

    def _get_entity_id(self, entry: ET.Element) -> Optional[str]:
        supplier_id: str = self.xml_helper.get_single_tag_nested_value(
            entry,
            'wd:Journal_Entry_Reference',
            'wd:ID[@wd:type="Accounting_Journal_ID"]',
            str
        )
        return supplier_id

    """ Override """

    def _generate_payload(self, entity_id: str, **kwargs):
        """generate the body request payload"""
        payload = f"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<env:Envelope\r\n    " \
                  f"xmlns:env=\"http://schemas.xmlsoap.org/soap/envelope/\"\r\n    " \
                  f"xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\">\r\n    <env:Body>\r\n        " \
                  f"<wd:Get_Journals_Request xmlns:wd=\"urn:com.workday/bsvc\" wd:version=\"{self.api_version}\">\r\n            " \
                  f"<wd:Request_References>\r\n                <wd:JournalEntryReference>\r\n                    " \
                  f"<wd:ID wd:type=\"Accounting_Journal_ID\">{entity_id}</wd:ID>\r\n                " \
                  f"</wd:JournalEntryReference>\r\n            </wd:Request_References>\r\n            " \
                  f"<wd:Response_Filter>\r\n                <wd:Page>1</wd:Page>\r\n                " \
                  f"<wd:Count>999</wd:Count>\r\n            </wd:Response_Filter>\r\n            " \
                  f"<wd:Response_Group>\r\n                " \
                  f"<wd:Include_Attachment_Data>true</wd:Include_Attachment_Data>\r\n            " \
                  f"</wd:Response_Group>\r\n        </wd:Get_Journals_Request>\r\n    </env:Body>\r\n</env:Envelope> "
        return payload

    """ Override """

    def _parse_entity_element(self, entry: ET.Element) -> MappedJournal:
        """
        Parse the Get supplier response payload

        :param entry: XML element node
        :return: [MappedJournal]
        """
        journal: Optional[JournalEntry] = self._parse_journals(entry)
        # start converting data into Pigment Data
        converted_journal: Optional[MappedJournal] = self._convert_all_journals_into_pigment_journals(
            journal,
            self.ledger_accounts,
            self.cost_centers,
            self.subsidiaries
        )

        return converted_journal

    """ Override """

    def _update_cache(self, journal: JournalEntry):
        if journal and journal.journalEntryReference and journal.journalEntryReference.Accounting_Journal_ID:
            # check if it's necessary to update the dic since there is a heavy process to convert data
            if journal.journalEntryReference.Accounting_Journal_ID in self.cache.keys():
                # start converting data into Pigment Data
                converted_journal: Optional[MappedJournal] = self._convert_all_journals_into_pigment_journals(
                    journal,
                    self.ledger_accounts,
                    self.cost_centers,
                    self.subsidiaries
                )
                if converted_journal:
                    self.cache.update({journal.journalEntryReference.Accounting_Journal_ID: converted_journal})

    def _map_workday_journal_to_pigment_data(
            self, journal: JournalEntry,
            ledger_accounts: Dict[str, LedgerAccount],
            cost_centers: Dict[str, CostCenterInfo],
            subsidiaries: Dict[str, SubsidiaryInfo],
    ) -> MappedJournal:
        """
            Prepare the mapping object before filling detailesd field with WD APIs
            :return MappedEntryJournalData
            :raise ProcessException
        """
        try:
            entry_journals: List[MappedEntryJournal] = []
            # Create Base Account Object
            account = AccountInfo(code=journal.ledgerReference.Ledger_Reference_ID)
            # document info
            document = DocumentInfo(
                description=journal.description,
                document_number=journal.journal_Sequence_Number
            )
            # P & L Destination
            pl_info_destination = journal.custom_Worktag_4_ID
            # Accounting Period Name
            accounting_period = journal.accounting_Date
            # Is Journal Source
            journal_source = journal.journalSourceReference.Journal_Source_ID

            for entry in journal.journalEntryLines:
                # Expense type (Account)
                expense_type: SpendCategory = self.resource_category_service.get_entity(
                    object_id=entry.worktagsReference.Spend_Category_ID,
                    data_entity_path='.//wd:Resource_Category_Data'
                )
                # Create SubsidiaryInfo Object
                subsidiary = subsidiaries.get(entry.lineCompanyReference.Company_Reference_ID)
                # Amount
                amount = AmountInfo(
                    debit=entry.debit_Amount,
                    credit=entry.credit_Amount,
                    ledger_debit=entry.ledger_Debit_Amount,
                    ledger_credit=entry.ledger_Credit_Amount,
                    currency_symbol=entry.currencyReference.Currency_ID,
                    amount_net_usd=None,  # TODO: check with the finance team
                )
                # Cost center
                cost_center_info = cost_centers.get(entry.worktagsReference.Cost_Center_Reference_ID)
                # Revenue Line
                # region_id: Optional[str] = entry.worktagsReference.Custom_Organization_Reference_ID

                # Acquisition Channel dimension
                custom_org_ref = entry.worktagsReference.Custom_Organization_Reference_ID
                gtm_org = None
                if custom_org_ref:
                    gtm_org = self.gtm_org.get(custom_org_ref)

                customer_contract_ref = entry.worktagsReference.Customer_Contract_Reference_ID
                deal = None
                if customer_contract_ref:
                    deal: Optional[DealInfo] = self.customer_contract_service.get_entity(
                        object_id=customer_contract_ref,
                        data_entity_path='.//wd:Customer_Contract_Data',
                    )

                revenue_line = RevenueInfo(
                    # revenue_org_region=revenue_org_region,
                    deal=deal,
                    revenue_name=entry.worktagsReference.Revenue_Category_ID,
                    gtm_org=gtm_org
                )
                # Vendor
                vendor_line = self.raas_suppliers.get_entity(
                    object_id=entry.worktagsReference.Supplier_ID,
                    data_entity_path='.//wd:Supplier_Data'
                )
                # Memo
                memo = entry.memo
                # Project Code
                project_code = entry.worktagsReference.Project_ID
                # Ledger Account
                ledger_account = ledger_accounts.get(entry.ledgerAccountReference.Ledger_Account_ID)
                # Cash Flow Code
                cash_flow_code = entry.worktagsReference.cash_flow_code

                entry_line = MappedEntryJournal(
                    ledger_account=ledger_account,
                    expense_type=expense_type,
                    subsidiary_info=subsidiary,
                    amount_info=amount,
                    cost_center_info=cost_center_info,
                    revenue_info=revenue_line,
                    vendor_info=vendor_line,
                    project_code=project_code,
                    memo=memo,
                    cash_flow_code=cash_flow_code,
                    customer_id=entry.worktagsReference.customer_id
                )
                entry_journals.append(entry_line)

            return MappedJournal(
                journal_id=journal.journalEntryReference.Accounting_Journal_ID,
                account_info=account,
                book_code_info=journal.book_code,
                document_info=document,
                pl_info_destination=pl_info_destination,
                accounting_period_name=accounting_period,
                journal_source=journal_source,
                mapped_entries=entry_journals
            )
        except ProcessException as error:
            print(error)
            raise ProcessException(
                f"Mapping error for WD Accounting_Journal_ID {journal.journalEntryReference.Accounting_Journal_ID} with error: {error}."
            )
        except Exception as error:
            print(error)

    def _convert_all_journals_into_pigment_journals(
            self,
            journal: JournalEntry,
            ledger_accounts: Dict[str, LedgerAccount],
            cost_centers: Dict[str, CostCenterInfo],
            subsidiaries: Dict[str, SubsidiaryInfo]
    ) -> Optional[MappedJournal]:
        try:
            mapped_journal = self._map_workday_journal_to_pigment_data(
                journal,
                ledger_accounts,
                cost_centers,
                subsidiaries
            )
            if mapped_journal:
                return mapped_journal
        except ProcessException as perror:
            print(perror)
            self.failed_journals.append(
                FailedProcessedJournal(
                    journal_id=journal.journalEntryReference.Accounting_Journal_ID,
                    error_message=str(perror),
                    datetime=str(datetime.datetime.now()),
                    reason=
                    f'Could not concert XML data in `convert_all_journals_into_pigment_journals` at page {self.next_page - 1}'
                )
            )
        except Exception as error:
            print(error)
            self.failed_journals.append(
                FailedProcessedJournal(
                    journal_id=journal.journalEntryReference.Accounting_Journal_ID,
                    error_message=str(error),
                    datetime=str(datetime.datetime.now()),
                    reason=
                    f'Could not extract data from XML payload in `parse_journals` at page {self.next_page - 1}'
                )
            )

    # Function to parse the XML response and extract journals
    def _parse_journals(self, journal_data: ET.Element) -> Optional[JournalEntry]:
        ns = self.namespace
        entry_lines = []

        # Extract the Journal Entry reference
        journal_entry_ref = journal_data.find('.//wd:Journal_Entry_Reference', ns)
        journal_id = self.xml_helper.safe_get_text(journal_entry_ref, 'wd:ID[@wd:type="Accounting_Journal_ID"]')
        journal_entry = JournalEntryReference(Accounting_Journal_ID=journal_id)

        try:
            # P & L Destination
            custom_Worktag_4_ref = journal_data.find('.//wd:Worktags_Reference', ns)
            custom_Worktag_4_ID = self.xml_helper.safe_get_text(custom_Worktag_4_ref,
                                                                'wd:ID[@wd:type="Custom_Worktag_4_ID"]')

            # Extract Journal Number
            # journal_number = self.xml_helper.safe_get_text(journal_data, 'wd:Journal_Number')
            journal_number = self.xml_helper.get_single_tag_line_value(journal_data, './/wd:Journal_Number', str)

            # Get Description if present
            journal_description = self.xml_helper.safe_get_text(journal_data, './/wd:Memo')

            # Extract Accounting_Date
            accounting_date = self.xml_helper.safe_get_text(journal_data, './/wd:Accounting_Date')

            # Extract Creation_Date
            creation_date = self.xml_helper.safe_get_text(journal_data, './/wd:Creation_Date')

            # Extract Last_Updated_Date
            last_updated_date = self.xml_helper.safe_get_text(journal_data, './/wd:Last_Updated_Date')

            # Get Record_Quantity
            record_quantity = self.xml_helper.safe_get_int(journal_data, './/wd:Record_Quantity')

            # Get Total_Ledger_Debits
            total_ledger_debits = self.xml_helper.safe_get_float(journal_data, './/wd:Total_Ledger_Debits')

            # Get Total_Ledger_Credits
            total_ledger_credits = self.xml_helper.safe_get_float(journal_data, './/wd:Total_Ledger_Credits')

            # Extract Journal_Sequence_Number
            journal_sequence_number = self.xml_helper.safe_get_text(journal_data, './/wd:Journal_Sequence_Number')

            # Extract the Journal Status reference
            journal_status_ref = journal_data.find('.//wd:Journal_Status_Reference', ns)
            journal_status = JournalStatusReference(
                WID=self.xml_helper.safe_get_text(journal_status_ref, 'wd:ID[@wd:type="WID"]'),
                Journal_Entry_Status_ID=self.xml_helper.safe_get_text(journal_status_ref,
                                                                      'wd:ID[@wd:type="Journal_Entry_Status_ID"]')
            )

            # Extract the Journal Book Code
            journal_bookcode_ref = journal_data.find('.//wd:Book_Code_Reference', ns)
            book_code_id = self.xml_helper.safe_get_text(journal_bookcode_ref, 'wd:ID[@wd:type="Book_Code_ID"]')
            book_code = self.book_codes.get(book_code_id)

            # Extract Company_Reference
            journal_comp_ref = journal_data.find('.//wd:Company_Reference', ns)
            company_ref = CompanyReference(
                WID=self.xml_helper.safe_get_text(journal_comp_ref, 'wd:ID[@wd:type="WID"]'),
                Organization_Reference_ID=self.xml_helper.safe_get_text(journal_comp_ref,
                                                                        'wd:ID[@wd:type="Organization_Reference_ID"]'),
                Company_Reference_ID=self.xml_helper.safe_get_text(journal_comp_ref,
                                                                   'wd:ID[@wd:type="Company_Reference_ID"]')
            )

            # Extract Currency_Reference
            currency_ref = journal_data.find('.//wd:Currency_Reference', ns)
            currency = CurrencyReference(
                WID=self.xml_helper.safe_get_text(currency_ref, 'wd:ID[@wd:type="WID"]'),
                Currency_ID=self.xml_helper.safe_get_text(currency_ref, 'wd:ID[@wd:type="Currency_ID"]'),
                Currency_Numeric_Code=self.xml_helper.safe_get_text(currency_ref,
                                                                    'wd:ID[@wd:type="Currency_Numeric_Code"]')
            )

            # Extract Ledger_Reference
            ledger_ref = journal_data.find('.//wd:Ledger_Reference', ns)
            ledger = LedgerReference(
                WID=self.xml_helper.safe_get_text(ledger_ref, 'wd:ID[@wd:type="WID"]'),
                Ledger_Reference_ID=self.xml_helper.safe_get_text(ledger_ref,
                                                                  'wd:ID[@wd:type="Ledger_Reference_ID"]')
            )

            # Extract Journal_Source_Reference
            source_ref = journal_data.find('.//wd:Journal_Source_Reference', ns)
            journal_source = JournalSourceReference(
                Journal_Source_ID=self.xml_helper.safe_get_text(source_ref,
                                                                'wd:ID[@wd:type="Journal_Source_ID"]')
            )

            # Extract Ledger_Period_Reference
            ledger_per_ref = journal_data.find('.//wd:Ledger_Period_Reference', ns)
            ledger_period = LedgerPeriodReference(
                WID=self.xml_helper.safe_get_text(ledger_per_ref, 'wd:ID[@wd:type="WID"]')
            )

            # Get All Journal Entry Lines
            journal_entry_lines = journal_data.findall('.//wd:Journal_Entry_Line_Data', ns)
            for journal_entry_line_data in journal_entry_lines:

                # Extract Line_Company_Reference
                line_company_ref = journal_entry_line_data.find('wd:Line_Company_Reference', ns)
                line_company = LineCompanyReference(
                    WID=self.xml_helper.safe_get_text(line_company_ref, 'wd:ID[@wd:type="WID"]'),
                    Organization_Reference_ID=self.xml_helper.safe_get_text(line_company_ref,
                                                                            'wd:ID[@wd:type="Organization_Reference_ID"]'),
                    Company_Reference_ID=self.xml_helper.safe_get_text(line_company_ref,
                                                                       'wd:ID[@wd:type="Company_Reference_ID"]')
                )

                # Extract Ledger_Account_Reference
                ledger_acc_ref = journal_entry_line_data.find('wd:Ledger_Account_Reference', ns)
                ledger_account = LedgerAccountReference(
                    WID=self.xml_helper.safe_get_text(ledger_acc_ref, 'wd:ID[@wd:type="WID"]'),
                    Ledger_Account_ID=self.xml_helper.safe_get_text(ledger_acc_ref,
                                                                    'wd:ID[@wd:type="Ledger_Account_ID"]')
                )
                # Extract the Worktags_Reference with Organization_Reference_ID
                worktags = WorktagsReference()
                worktags_references = journal_entry_line_data.findall('.//wd:Worktags_Reference', ns)

                for worktag in worktags_references:
                    # Fill the work tags within a unique objects
                    worktags = self.xml_helper.create_worktags_object(worktag, worktags)

                # Extract Debit_Amount
                debit_amount = self.xml_helper.safe_get_float(journal_entry_line_data, 'wd:Debit_Amount')

                # Extract Credit_Amount
                credit_amount = self.xml_helper.safe_get_float(journal_entry_line_data, 'wd:Credit_Amount')

                # Extract Currency_Rate
                currency_rate = self.xml_helper.safe_get_float(journal_entry_line_data, 'wd:Currency_Rate')

                # Extract Ledger_Credit_Amount
                ledger_Credit_Amount = self.xml_helper.safe_get_float(journal_entry_line_data,
                                                                      'wd:Ledger_Credit_Amount')

                # Extract Ledger_Debit_Amount
                ledger_Debit_Amount = self.xml_helper.safe_get_float(journal_entry_line_data,
                                                                     'wd:Ledger_Debit_Amount')

                # Extract Exclude_from_Spend_Report
                exclude_from_report = self.xml_helper.safe_get_int(journal_entry_line_data,
                                                                   'wd:Exclude_from_Spend_Report')

                # Extract Journal_Line_Number
                journal_line_number = self.xml_helper.safe_get_int(journal_entry_line_data,
                                                                   'wd:Journal_Line_Number')

                # Extract Memo
                memo = self.xml_helper.safe_get_text(journal_entry_line_data, 'wd:Memo')

                # Create the JournalEntryLine object
                journal_entry_line = JournalEntryLine(
                    currencyReference=currency,
                    debit_Amount=debit_amount,
                    credit_Amount=credit_amount,
                    lineCompanyReference=line_company,
                    ledgerAccountReference=ledger_account,
                    currency_Rate=currency_rate,
                    ledger_Debit_Amount=ledger_Debit_Amount,
                    ledger_Credit_Amount=ledger_Credit_Amount,
                    worktagsReference=worktags,
                    exclude_from_spend_report=exclude_from_report,
                    journal_line_number=journal_line_number,
                    memo=memo
                )

                # Add the entry line to the list
                entry_lines.append(journal_entry_line)

            # Create a JournalEntry object and append it to the list
            journal = JournalEntry(
                journalEntryReference=journal_entry,
                accounting_Date=accounting_date,
                book_code=book_code,
                description=journal_description,
                custom_Worktag_4_ID=custom_Worktag_4_ID,  # Todo Test 🧪
                journal_Number=journal_number,
                currencyReference=currency,
                ledgerReference=ledger,
                companyReference=company_ref,
                journalStatusReference=journal_status,
                journal_Sequence_Number=journal_sequence_number,
                record_Quantity=record_quantity,
                journalSourceReference=journal_source,
                total_Ledger_Debits=total_ledger_debits,
                total_ledger_credits=total_ledger_credits,
                creation_Date=creation_date,
                last_Updated_Date=last_updated_date,
                ledgerPeriodReference=ledger_period,
                journalEntryLines=entry_lines
            )
            return journal
        except Exception as error:
            self.failed_journals.append(
                FailedProcessedJournal(
                    journal_id=journal_entry.Accounting_Journal_ID,
                    error_message=str(error),
                    datetime=str(datetime.datetime.now()),
                    reason=
                    f'Could not extract data from XML payload in `parse_journals` at page {self.next_page - 1}'
                )
            )

    @staticmethod
    def split_csv_content(csv_content: str, line_number: int, with_header: bool = False) -> List[str]:
        """
        Split up the csv content when the file is `large`
        :param csv_content: Full CSV size
        :param line_number: Number of line you want to start splitting up the file
        :param with_header: Variable to keep headers or not
        :return: List of CSV chunks
        """
        # Split the CSV content into lines
        lines = csv_content.strip().split('\n')
        # Extract the header (the first line of the CSV)
        header = lines[0]
        # Split the lines into chunks of 'line_number' size
        chunks = [lines[i:i + line_number] for i in range(0 if with_header else 1, len(lines), line_number)]
        # Join each chunk back into a CSV string
        if with_header:
            csv_chunks = ['\n'.join([header] + chunk) for chunk in chunks]
        else:
            csv_chunks = ['\n'.join(chunk) for chunk in chunks]

        return csv_chunks

