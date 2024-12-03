from abc import ABC
import xml.etree.ElementTree as ET
from typing import Tuple

from workday.models import *
from workday_api_generator_call import WorkdayRAASService


class GetRAASCompanies(WorkdayRAASService, ABC):
    """ Get all companies aka Subsidiaries """

    def __init__(
            self, base_url: str,
            tenant: str, token: str,
    ):
        # Initialize the parent class (ADNService)
        self._url = f'{base_url}/ccx/service/customreport2/{tenant}/ISU%20Workato/INT-UPD-001_MasterData_Companies'

        super().__init__(
            self._url, tenant, token,
            'urn:com.workday.report/INT-UPD-001_MasterData_Companies',
        )

    def parse_raas_element(self, entry: ET.Element) -> Tuple[str, T]:
        namespace = self.raas_ns

        # Find the CC reference ID
        reference_id_element = entry.find('wd:referenceID', namespace)
        reference_id = reference_id_element.text if reference_id_element is not None else None

        # Extract Descriptor of Company Element with null safety
        company_element = entry.find('wd:Company', namespace)
        company_name = company_element.attrib.get(
            self.get_raas_att_path('Descriptor')) if company_element is not None else None

        # convert into Mapped Object
        subsidiary = SubsidiaryInfo(internal_id=reference_id, name=company_name)

        return reference_id, subsidiary


class GetWDCompanies(WorkdayRAASService, ABC):
    """ Get all companies aka Subsidiaries with Workday element for Zuora inbound"""

    def __init__(
            self, base_url: str,
            tenant: str, token: str,
    ):
        # Initialize the parent class (ADNService)
        self._url = f'{base_url}/ccx/service/customreport2/{tenant}/ISU%20Workato/INT-UPD-001_MasterData_Companies'

        super().__init__(
            self._url, tenant, token,
            'urn:com.workday.report/INT-UPD-001_MasterData_Companies',
        )

    def parse_raas_element(self, entry: ET.Element) -> Tuple[str, T]:
        namespace = self.raas_ns

        wid: str = self.xml_helper.get_single_tag_nested_value(
            entry, 'wd:Company', 'wd:ID[@wd:type="WID"]', str
        )
        organization_ref_id: str = self.xml_helper.get_single_tag_nested_value(
            entry, 'wd:Company', 'wd:ID[@wd:type="Organization_Reference_ID"]', str
        )
        company_ref_id: str = self.xml_helper.get_single_tag_nested_value(
            entry, 'wd:Company', 'wd:ID[@wd:type="Company_Reference_ID"]', str
        )
        # Extract Descriptor of Company Element with null safety
        company_entry = entry.find('wd:Company', namespace)
        descriptor = company_entry.attrib.get(
            self.get_raas_att_path('Descriptor')) if company_entry is not None else None

        # convert into Mapped Object
        cmp = WorkdayCompanies(
            wid=wid,
            organization_reference_id=organization_ref_id,
            company_reference_id=company_ref_id,
            descriptor=descriptor
        )

        return company_ref_id, cmp


class GetRAASBookCodes(WorkdayRAASService, ABC):
    """ Get all Book Codes """

    def __init__(self, base_url: str, tenant: str, token: str):
        # Initialize the parent class (ADNService)
        self._url = f'{base_url}/ccx/service/customreport2/{tenant}/ISU%20Workato/INT-AUTO-001_MasterData_BookCodes'

        super().__init__(
            self._url, tenant, token,
            'urn:com.workday.report/INT-AUTO-001_MasterData_BookCodes',
        )

    def parse_raas_element(self, entry: ET.Element) -> Tuple[str, BookCodeInfo]:
        namespace = self.raas_ns

        # Find the reference ID
        book_code_id = self.xml_helper.get_single_tag_line_value(entry, 'wd:Book_Code_ID', str)

        # Extract Descriptor of the Book_Code_Name
        book_code_name_element = entry.find('wd:Book_Code_Name', namespace)
        book_code = book_code_name_element.attrib.get(
            self.get_raas_att_path('Descriptor')) if book_code_name_element is not None else None

        # convert into Mapped Object
        book_code = BookCodeInfo(book_code_id=book_code_id, name=book_code)

        return book_code_id, book_code


class GetRAASCostCenter(WorkdayRAASService, ABC):
    """ Get all Cost Center """

    def __init__(self, base_url: str, tenant: str, token: str):
        # Initialize the parent class (ADNService)
        self._url = f'{base_url}/ccx/service/customreport2/{tenant}/ISU%20Workato/INT-UPL-002_MasterData_CostCenters'

        super().__init__(
            self._url, tenant, token,
            'urn:com.workday.report/INT-UPL-002_MasterData_CostCenters',
        )

    def parse_raas_element(self, entry: ET.Element) -> Tuple[str, CostCenterInfo]:
        namespace = self.raas_ns

        # Extract Is Active with null safety
        is_active_element = entry.find('wd:Inactive', namespace)
        # use `NOT` because the header is 'is active'
        is_active = not bool(int(is_active_element.text)) if is_active_element is not None else None

        # Find the CC reference ID
        reference_id_element = entry.find('wd:referenceID', namespace)
        reference_id = reference_id_element.text if reference_id_element is not None else None

        # Extract Cost_Center_Code with null safety
        cost_center_code_element = entry.find('wd:Cost_Center_Code', namespace)
        cost_center_code = cost_center_code_element.text if cost_center_code_element is not None else None

        cost_center_mger_element = entry.find('.//wd:Cost_Center_Manager', namespace)
        cost_center_mng_name = cost_center_mger_element.attrib.get(
            self.get_raas_att_path('Descriptor')) if cost_center_mger_element is not None else None

        cost_center_mng_id = self.xml_helper.get_single_tag_nested_value(entry, 'wd:Cost_Center_Manager',
                                                                         'wd:ID[@wd:type="Employee_ID"]', str)

        manager = Manager(manager_employee_id=cost_center_mng_id, manager_name=cost_center_mng_name)

        # Extract Descriptor of Cost_Center Element with null safety
        cost_center_element = entry.find('wd:Cost_Center', namespace)
        cost_center_descriptor = cost_center_element.attrib.get(
            self.get_raas_att_path('Descriptor')) if cost_center_element is not None else None

        name = None
        if cost_center_descriptor:
            splitted_descriptor = cost_center_descriptor.split('-')
            if len(splitted_descriptor) > 1:
                name = ''.join(splitted_descriptor[1:]).strip()

        # convert into Mapped Object
        cc_info = CostCenterInfo(
            code=cost_center_code,
            name=name,
            manager=manager,
            isActive=is_active,
            referenceID=reference_id
        )

        return cc_info.code, cc_info


class GetRAASLedgerAccount(WorkdayRAASService, ABC):
    """ Get all Ledger Accounts """

    def __init__(self, base_url: str, tenant: str, token: str):
        # Initialize the parent class (ADNService)
        self._url = f'{base_url}/ccx/service/customreport2/{tenant}/ISU%20Workato/INT-UPL-001_MasterData_LedgerAccounts'

        super().__init__(
            self._url, tenant, token,
            'urn:com.workday.report/Master_Data_-_Ledger_Accounts__MSA_',
        )

    def parse_raas_element(self, entry: ET.Element) -> Tuple[str, LedgerAccount]:
        namespace = self.raas_ns

        ledger_account_id = entry.find('wd:Ledger_Account_ID', namespace).text

        # Correctly fetching the Ledger_Account_Name and Types using the Descriptor attribute
        ledger_account_name_elmt = entry.find('wd:Ledger_Account_Name', namespace)
        ledger_account_name = ledger_account_name_elmt.attrib.get(
            self.get_raas_att_path('Descriptor')) if ledger_account_name_elmt else None

        types_elmt = entry.find('wd:Types', namespace)
        types = types_elmt.attrib.get(self.get_raas_att_path('Descriptor')) if types_elmt else None

        # Fetching all Account_Sets descriptors and joining them
        account_sets = [
            account_set.attrib.get(self.get_raas_att_path('Descriptor'))
            for account_set in (entry.findall('wd:Account_Sets', namespace) or [])
        ]

        ledger_account = LedgerAccount(
            Ledger_Account_ID=ledger_account_id,
            Ledger_Account_Name=ledger_account_name,
            Types=types,
            Account_Sets=account_sets,
            WID="NA"
        )

        return ledger_account_id, ledger_account


class GetRAASSites(WorkdayRAASService, ABC):
    """ Get all Site Locations """

    def __init__(self, base_url: str, tenant: str, token: str):
        # Initialize the parent class (ADNService)
        self._url = f'{base_url}/ccx/service/customreport2/{tenant}/ISU%20Workato/INT-UPD-002_MasterData_Sites'

        super().__init__(
            self._url, tenant, token,
            'urn:com.workday.report/INT-UPD-002_MasterData_Sites',
        )

    def parse_raas_element(self, entry: ET.Element) -> Tuple[str, SiteInfo]:
        namespace = self.raas_ns

        site_id = self.xml_helper.get_single_tag_line_value(entry, 'wd:Location_ID', str)

        inactive = bool(self.xml_helper.get_single_tag_line_value(entry, 'wd:Inactive', int))

        location_arch_elmt = entry.find('wd:Location_Hierarchies', namespace)
        location_arch = location_arch_elmt.attrib.get(
            self.get_raas_att_path('Descriptor')) if location_arch_elmt else None

        location_elmt = entry.find('wd:Location', namespace)
        location_name = location_elmt.attrib.get(self.get_raas_att_path('Descriptor')) if location_elmt else None

        address_elmt = entry.find('wd:Addresses', namespace)
        address = address_elmt.attrib.get(self.get_raas_att_path('Descriptor')) if address_elmt else None

        country_elmt = entry.find('wd:country', namespace)
        country_name = country_elmt.attrib.get(
            self.get_raas_att_path('Descriptor')) if country_elmt else None

        country_alpha = self.xml_helper.get_single_tag_nested_value(entry, 'wd:country',
                                                                    'wd:ID[@wd:type="ISO_3166-1_Alpha-3_Code"]', str)
        country_digit = self.xml_helper.get_single_tag_nested_value(entry, 'wd:country',
                                                                    'wd:ID[@wd:type="ISO_3166-1_Numeric-3_Code"]', int)

        location_type = self.xml_helper.get_single_tag_nested_value(entry, 'wd:Location_Type',
                                                                    'wd:ID[@wd:type="Location_Type_ID"]', str)

        location_usage = self.xml_helper.get_single_tag_nested_value(entry, 'wd:locationUsage',
                                                                     'wd:ID[@wd:type="Location_Usage_ID"]', str)

        sites = SiteInfo(
            site_id=site_id,
            inactive=inactive,
            country_name=country_name,
            location_usage=location_usage,
            location_name=location_name,
            location_type=location_type,
            location_address=address,
            location_hierarchies=location_arch,
            country_alpha_code=country_alpha,
            country_digit_code=country_digit,
        )

        return site_id, sites


class GetRAASProjectCodes(WorkdayRAASService, ABC):
    """ Get all Project Codes ⚠️ Depreciated """

    def __init__(self, base_url: str, tenant: str, token: str, projects_and_project_hierarchies_id: str):
        # Initialize the parent class (ADNService)
        self._url = f'{base_url}/ccx/service/customreport2/{tenant}/ISU%20Workato/INT-AUTO-022_MasterData_Projects?Projects_and_Project_Hierarchies!WID={projects_and_project_hierarchies_id}'

        super().__init__(
            self._url, tenant, token,
            'urn:com.workday.report/INT-AUTO-022_MasterData_Projects',
        )

    def parse_raas_element(self, entry: ET.Element) -> Tuple[str, ProjectCodeInfo]:
        reference_id = self.xml_helper.get_single_tag_line_value(entry, 'wd:referenceID', str)

        start_date = self.xml_helper.get_single_tag_line_value(entry, 'wd:Start_Date', str)
        end_date = self.xml_helper.get_single_tag_line_value(entry, 'wd:End_Date', str)
        project_status = self.xml_helper.get_single_tag_line_value(entry, 'wd:Project_Status', str)
        company = self.xml_helper.get_single_tag_line_value(entry, 'wd:Company', str)

        project_currency_id = self.xml_helper.get_single_tag_nested_value(entry, 'wd:Project_Currency',
                                                                          'wd:ID[@wd:type="Currency_ID"]', str)

        project_currency_num_code = self.xml_helper.get_single_tag_nested_value(entry, 'wd:Project_Currency',
                                                                                'wd:ID[@wd:type="Currency_Numeric_Code"]',
                                                                                str)

        project_name = self.xml_helper.get_single_tag_nested_value(entry, 'wd:Project',
                                                                   'wd:ID[@wd:type="Project_ID"]', str)

        project_code = ProjectCodeInfo(
            project_id=reference_id,
            name=project_name,
            project_currency_id=project_currency_id,
            project_currency_num_code=project_currency_num_code,
            start_date=start_date,
            end_date=end_date,
            project_status=project_status,
            company=company
        )

        return reference_id, project_code


class GetRAASEmployees(WorkdayRAASService, ABC):
    """ Get all Employees """

    def __init__(self, base_url: str, tenant: str, token: str, worker_types: str):
        # Initialize the parent class (ADNService)
        self._url = f'{base_url}/ccx/service/customreport2/{tenant}/ISU%20Workato/INT-UPL-003_MasterData_Employees?Worker_Types!WID={worker_types}'
        namespace = 'urn:com.workday.report/Master_Data_-_Employees'

        super().__init__(self._url, tenant, token, namespace)

    def parse_raas_element(self, entry: ET.Element) -> Tuple[str, EmployeeInfo]:
        employee_id = self.xml_helper.get_single_tag_line_value(entry, 'wd:Employee_ID', str)
        full_name = self.xml_helper.get_single_tag_line_value(entry, 'wd:Full_Legal_Name', str)
        contract_type = self.xml_helper.get_single_tag_line_value(entry, 'wd:CF_Employee_Type_Contract_Type', str)
        primary_work_email = self.xml_helper.get_single_tag_line_value(entry, 'wd:primaryWorkEmail', str)

        manager_email = self.xml_helper.get_single_tag_line_value(entry, 'wd:Manager_Email', str)
        manager_element = entry.find('wd:Manager', self.raas_ns)
        manager_name = manager_element.attrib.get(self.get_raas_att_path('Descriptor')) if manager_element else None
        manager_employee_id = self.xml_helper.get_single_tag_nested_value(
            entry, 'wd:Manager', 'wd:ID[@wd:type="Employee_ID"]', str
        )

        primary_address = self.get_tag_property_value(entry, 'wd:Primary_Work_Address', 'Descriptor')

        work_address_country = self.get_tag_property_value(entry, 'wd:Primary_Work_Address_-_Country', 'Descriptor')
        work_address_country_code = self.xml_helper.get_single_tag_nested_value(
            entry, 'wd:Primary_Work_Address_-_Country', 'wd:ID[@wd:type="ISO_3166-1_Alpha-3_Code"]', str
        )
        work_address_country_num = self.xml_helper.get_single_tag_nested_value(
            entry, 'wd:Primary_Work_Address_-_Country', 'wd:ID[@wd:type="ISO_3166-1_Numeric-3_Code"]', str
        )

        primary_country_address = Country(
            country_name=work_address_country,
            country_digit_code=work_address_country_num,
            country_alpha_code=work_address_country_code
        )

        manager = Manager(manager_employee_id=manager_employee_id, manager_name=manager_name,
                          manager_email=manager_email)

        employee = EmployeeInfo(
            employee_id=employee_id,
            full_legal_name=full_name,
            employee_contract_type=contract_type,
            primary_work_email=primary_work_email,
            primary_work_address=primary_address,
            primary_work_country_address=primary_country_address,
            manager=manager
        )

        return employee_id, employee


class GetRAASAssetCategories(WorkdayRAASService, ABC):
    """ Get all Asset Categories """

    def __init__(self, base_url: str, tenant: str, token: str):
        # Initialize the parent class (ADNService)
        self._url = f'{base_url}/ccx/service/customreport2/{tenant}/ISU%20Workato/INT-UPL-004_MasterData_AssetCategories'
        namespace = 'urn:com.workday.report/INT-UPL-004_MasterData_AssetCategories'

        super().__init__(self._url, tenant, token, namespace)

    def parse_raas_element(self, entry: ET.Element) -> Tuple[str, AssetCategories]:
        asset_id = self.xml_helper.get_single_tag_line_value(entry, 'wd:Reference_ID_Value', str)

        asset_class_name = self.xml_helper.get_single_tag_nested_value(
            entry, 'wd:Class_of_Instance_group', 'wd:Name', str
        )

        asset = AssetCategories(asset_class_id=asset_id, asset_class_name=asset_class_name)

        return asset_id, asset


class GetRAASGeoSales(WorkdayRAASService, ABC):
    """ Get all Geo Sales aka GTM Organization """

    def __init__(self, base_url: str, tenant: str, token: str):
        # Initialize the parent class (ADNService)
        self._url = f'{base_url}/ccx/service/customreport2/{tenant}/ISU%20Workato/INT-AUTO-014_MasterData_GeoSales'
        namespace = 'urn:com.workday.report/INT-AUTO-014_MasterData_GeoSales'

        super().__init__(self._url, tenant, token, namespace)

    def parse_raas_element(self, entry: ET.Element) -> Tuple[Optional[str], Optional[GeoSales]]:
        dimension_id = self.xml_helper.get_single_tag_line_value(entry, 'wd:Dimension_Reference_ID', str)
        name = self.xml_helper.get_single_tag_line_value(entry, 'wd:name', str)
        organization_active = bool(
            self.xml_helper.get_single_tag_line_value(entry, 'wd:RPT_TF_Organization_Active', int))
        dimension_name = self.get_tag_property_value(entry, 'wd:Dimension', 'Descriptor')

        # return Active only:
        if organization_active:
            geosales = GeoSales(
                dimension_id=dimension_id,
                name=name,
                dimension_name=dimension_name,
                organization_active=organization_active
            )
            return dimension_id, geosales
        else:
            # will not be processed
            return None, None
