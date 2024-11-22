from workday.workday_api_generator_call import *
from workday.workday_implement_api import *
from workday.workday_raas_implementation_api import *


def main_master_data(input):
    """
    Use this main function for master data integrations
    :param input:
    :return:
    """
    # Replace with actual credentials and details
    workday = input['workday_server']
    tenant = input['workday_tenant']
    client_id = input['workday_client_id']
    client_secret = input['workday_client_secret']
    refresh_token = input['workday_refresh_token']
    integration_scope = int(input.get("integration_scope")) if input.get("integration_scope") else None
    is_test = False if (input.get("is_test") or "") == "false" else True
    # Optional  argument
    generate_all = is_test
    IS_PROD = not is_test
    _DEFAULT_WORKDAY_API_VERSION = input.get("api_version") or DEFAULT_WORKDAY_API_VERSION

    connector = WorkdayConnector(workday, tenant, client_id, client_secret, refresh_token)
    connector.acquire_token()

    """CURRENCY CATEGORY"""
    if generate_all or CURRENCY == integration_scope:
        currency_service = GetCurrencies(
            base_url=connector.base_uri,
            token=connector.access_token,
            tenant=tenant,
            api_version=_DEFAULT_WORKDAY_API_VERSION,
        )

        eur_cur = currency_service.search_entity('EUR', './/wd:Currency_Data')
        print(eur_cur)
        all_currencies = currency_service.get_all_entities('.//wd:Currency_Data')
        csv_content: str = currency_service.generate_csv(
            list(all_currencies),
            [
                ("wid", lambda o: o.wid if o else None),
                ("currency_description", lambda o: o.currency_description if o else None),
                ("currency_numeric_code", lambda o: o.currency_numeric_code if o else None),
                ("currency_id", lambda o: o.currency_id if o else None),
                ("currency_id", lambda o: o.currency_id if o else None),
            ],
            filename='CSVs/all_currencies',
            prod=IS_PROD
        )
        if IS_PROD:
            return {"master_data_csv": csv_content}

    """Companies WD CATEGORY"""
    if generate_all or COMPANIES_WD == integration_scope:
        cp_wd_service = GetWDCompanies(
            base_url=connector.base_uri,
            token=connector.access_token,
            tenant=tenant,
        )
        companies: Dict[str, WorkdayCompanies] = cp_wd_service.get_entity_dic()
        print(companies.get("LE107"))
        csv_content: str = cp_wd_service.generate_csv(
            list(companies.values()),
            [
                ("wid", lambda o: o.wid if o else None),
                ("organization_reference_id", lambda o: o.organization_reference_id if o else None),
                ("company_reference_id", lambda o: o.company_reference_id if o else None),
                ("name", lambda o: o.descriptor if o else None)
            ],
            filename='CSVs/workday_companies',
            prod=IS_PROD
        )
        if IS_PROD:
            return {"master_data_csv": csv_content}

    """SPEND CATEGORY"""
    if generate_all or SPEND_CATEGORIES == integration_scope:
        spend_category_service = GetResourceCategories(
            base_url=connector.base_uri,
            token=connector.access_token,
            tenant=tenant,
            api_version=_DEFAULT_WORKDAY_API_VERSION,
        )

        # spend_cat = spend_category_service.get_entity('MAR_2_6', './/wd:Resource_Category_Data')
        spend_categories = spend_category_service.get_all_entities('.//wd:Resource_Category_Data')
        csv_content: str = spend_category_service.generate_csv(
            list(spend_categories),
            [
                ("code", lambda o: o.code if o else None),
                ("name", lambda o: o.name if o else None),
            ],
            filename='CSVs/spend_categories',
            prod=IS_PROD
        )
        if IS_PROD:
            return {"master_data_csv": csv_content}

    """CUSTOMER CONTRACT CATEGORY"""
    if generate_all or CUSTOMER_CONTRACT == integration_scope:
        deal_service = GetCustomerContracts(
            base_url=connector.base_uri,
            token=connector.access_token,
            tenant=tenant,
            api_version=_DEFAULT_WORKDAY_API_VERSION
        )
        # deal = deal_service.get_entity(object_id='CUSTOMER_CONTRACT-6-1', data_entity_path='.//wd:Customer_Contract_Data')
        customer_contracts = deal_service.get_all_entities('.//wd:Customer_Contract_Data')
        csv_content: str = deal_service.generate_csv(
            customer_contracts,
            [
                ("id", lambda o: o.customer_contract_id if o else None),
                ("name", lambda o: o.contract_name if o else None),
                ("po_number", lambda o: o.po_number if o else None),
                ("on_hold", lambda o: o.on_hold if o else None),
                ("contract_type", lambda o: o.contract_type if o else None),
            ],
            filename='CSVs/customer_contracts',
            prod=IS_PROD
        )
        if IS_PROD:
            return {"master_data_csv": csv_content}

    """REGION CATEGORIES"""
    if generate_all or REGION_CATEGORIES == integration_scope:
        regions_service = Region(
            base_url=connector.base_uri,
            token=connector.access_token,
            tenant=tenant,
            api_version=_DEFAULT_WORKDAY_API_VERSION
        )
        # region = regions_service.get_entity(object_id='GTM_24', data_entity_path='.//wd:Organization_Data')
        regions = regions_service.get_all_entities('.//wd:Organization_Data')
        csv_content: str = regions_service.generate_csv(
            regions,
            [
                ("code", lambda o: o.code if o else None),
                ("name", lambda o: o.name if o else None),
            ],
            filename='CSVs/regions_GTM',
            prod=IS_PROD
        )
        if IS_PROD:
            return {"master_data_csv": csv_content}

    """COMPANIES/SUPPLIERS CATEGORIES"""
    if generate_all or COMPANIES_CATEGORIES == integration_scope:
        companies_service = GetRAASSuppliers(
            base_url=connector.base_uri,
            token=connector.access_token,
            tenant=tenant,
            api_version=_DEFAULT_WORKDAY_API_VERSION
        )
        # supplier = companies_service.get_entity(
        #     object_id='SUP-691', data_entity_path='.//wd:Supplier_Data',
        #     as_of_effective_date=None, as_of_entry_datetime=None
        # )
        suppliers = companies_service.get_all_entities(
            './/wd:Supplier_Data',
            # can use effective and entry date
            # as_of_effective_date="2024-09-05", as_of_entry_datetime="2024-09-05"
        )
        csv_content: str = companies_service.generate_csv(
            suppliers,
            [
                ("vendor_ref_id", lambda o: o.vendor_ref_id if o else None),
                ("id", lambda o: o.vendor_code if o else None),
                ("company_name", lambda o: o.company_name if o else None),
                ("approval_status", lambda o: o.approval_status if o else None),
                ("supplier_category", lambda o: o.supplier_category if o else None),
                ("supplier_group_category", lambda o: o.supplier_group_category if o else None),
                ("worktag_only", lambda o: o.worktag_only if o else None),
                ("submit", lambda o: o.submit if o else None),
                ("disable_change_order", lambda o: o.disable_change_order if o else None),
                ("acknowledgement_expected", lambda o: o.acknowledgement_expected if o else None),
                ("enable_global_location_number", lambda o: o.enable_global_location_number if o else None),
                ("enable_asn", lambda o: o.enable_asn if o else None),
                ("edit_port_taxes", lambda o: o.edit_port_taxes if o else None),
                ("payment_terms_reference", lambda o: o.payment_terms_reference if o else None),
                ("default_payment_type_reference", lambda o: o.default_payment_type_reference if o else None),
                ("fatca", lambda o: o.fatca if o else None),
                ("irs_1099_supplier", lambda o: o.irs_1099_supplier if o else None),
                ("invoice_any_supplier", lambda o: o.invoice_any_supplier if o else None),
                ("supplier_minimum_order_amount", lambda o: o.supplier_minimum_order_amount if o else None),
                ("asn_due_in_days", lambda o: o.asn_due_in_days if o else None),
            ],
            filename='CSVs/vendors_suppliers',
            prod=IS_PROD
        )
        if IS_PROD:
            return {"master_data_csv": csv_content}

    """PAYMENT METHOD CATEGORIES"""
    if generate_all or PAY_METH_CATEGORIES == integration_scope:
        pay_meth_service = GetPaymentMethod(
            base_url=connector.base_uri,
            token=connector.access_token,
            tenant=tenant,
            api_version=_DEFAULT_WORKDAY_API_VERSION
        )
        # payment_meth = pay_meth_service.get_entity(object_id='Immediate', data_entity_path='.//wd:Payment_Term_Data')
        payment_methods = pay_meth_service.get_all_entities(
            './/wd:Payment_Term_Data', as_of_effective_date=None, as_of_entry_datetime=None
        )
        csv_content: str = pay_meth_service.generate_csv(
            payment_methods,
            [
                ("payment_term_id", lambda o: o.payment_term_id if o else None),
                ("name", lambda o: o.name if o else None),
                ("cut_off_day", lambda o: o.cut_off_day if o else None),
                ("grace_days", lambda o: o.grace_days if o else None),
                ("payment_discount_days", lambda o: o.payment_discount_days if o else None),
                ("payment_discount_percent", lambda o: o.payment_discount_percent if o else None),
            ],
            filename='CSVs/payment_methods',
            prod=IS_PROD
        )
        if IS_PROD:
            return {"master_data_csv": csv_content}

    """SUBSIDIARIES aka Comnpanies CATEGORIES"""
    if generate_all or SUBSIDIARIES_CATEGORIES == integration_scope:
        subsidiaries_service = GetRAASCompanies(
            base_url=connector.base_uri,
            token=connector.access_token,
            tenant=tenant
        )
        subsidiaries = subsidiaries_service.get_entity_dic()
        csv_content: str = subsidiaries_service.generate_csv(
            list(subsidiaries.values()),
            [
                ("id", lambda o: o.internal_id if o else None),
                ("name", lambda o: o.name if o else None),
            ],
            filename='CSVs/companies_aka_subsidiaries',
            prod=IS_PROD
        )
        if IS_PROD:
            return {"master_data_csv": csv_content}

    """BOOK CODE CATEGORIES"""
    if generate_all or BOOK_CODE_CATEGORIES == integration_scope:
        book_code_service = GetRAASBookCodes(
            base_url=connector.base_uri,
            token=connector.access_token,
            tenant=tenant,
        )
        book_codes = book_code_service.get_entity_dic()
        print(book_codes)
        csv_content: str = book_code_service.generate_csv(
            list(book_codes.values()),
            [
                ("book_code", lambda o: o.book_code_id if o else None),
                ("book_code_name", lambda o: o.name if o else None),
            ],
            filename='CSVs/book_codes',
            prod=IS_PROD
        )
        if IS_PROD:
            return {"master_data_csv": csv_content}

    """COST CENTER CATEGORIES"""
    if generate_all or COST_CENTER_CATEGORIES == integration_scope:
        cost_center_service = GetRAASCostCenter(
            base_url=connector.base_uri,
            token=connector.access_token,
            tenant=tenant,
        )
        cost_centers = cost_center_service.get_entity_dic()
        print(cost_centers)
        cost_centers_list: List[CostCenterInfo] = list(cost_centers.values())
        filtered_active_cost_center = [cc for cc in cost_centers_list if cc.isActive]
        csv_content: str = cost_center_service.generate_csv(
            filtered_active_cost_center,
            [
                ("referenceID", lambda o: o.referenceID if o else None),
                ("name", lambda o: o.name if o else None),
                ("code", lambda o: o.code if o else None),
                ("isActive", lambda o: o.isActive if o else None),
                # Manager
                ("manager_employee_id", lambda o: o.manager.manager_employee_id if o.manager else None),
                ("manager_name", lambda o: o.manager.manager_name if o.manager else None),
                ("manager_email", lambda o: o.manager.manager_email if o.manager else None),
            ],
            filename='CSVs/cost_centers',
            prod=IS_PROD
        )
        if IS_PROD:
            return {"master_data_csv": csv_content}

    """LEDGER ACCOUNT"""
    if generate_all or LEDGER_ACCOUNT == integration_scope:
        ledger_account_service = GetRAASLedgerAccount(
            base_url=connector.base_uri,
            token=connector.access_token,
            tenant=tenant,
        )
        ledger_accounts: Dict[str, LedgerAccount] = ledger_account_service.get_entity_dic()
        print(ledger_accounts)
        ledger_accounts_list: List[LedgerAccount] = list(ledger_accounts.values())
        # @Omer asked `take only the "Corporate COA || Corporate COA Child" in the column Ledger_Account_Account_Sets`
        # From: https://docs.google.com/spreadsheets/d/1ObsDQllv46CPfaSjAKfFPYa2x2IYZ3uFeqvAq8rtEVI
        filtered_ledger_account = [la for la in ledger_accounts_list if 'Corporate COA' in la.Account_Sets and 'Corporate COA Child' in la.Account_Sets]
        csv_content: str = ledger_account_service.generate_csv(
            filtered_ledger_account,
            [
                ("Ledger_Account_ID", lambda o: o.Ledger_Account_ID if o else None),
                ("Ledger_Account_Name", lambda o: o.Ledger_Account_Name if o else None),
                ("Ledger_Account_Types", lambda o: o.Types if o else None),
                ("Ledger_Account_Account_Sets", lambda o: "||".join(o.Account_Sets or []) if o else None),
            ],
            filename='CSVs/ledger_account',
            prod=IS_PROD
        )
        if IS_PROD:
            return {"master_data_csv": csv_content}

    """SITES"""
    if generate_all or SITES == integration_scope:
        sites_service = GetRAASSites(
            base_url=connector.base_uri,
            token=connector.access_token,
            tenant=tenant,
        )
        sites: Dict[str, SiteInfo] = sites_service.get_entity_dic()
        print(sites)
        csv_content: str = sites_service.generate_csv(
            list(sites.values()),
            [
                ("site_id", lambda o: o.site_id if o else None),
                ("inactive", lambda o: o.inactive if o else None),
                ("location_name", lambda o: o.location_name if o else None),
                ("location_address", lambda o: o.location_address if o else None),
                ("location_type", lambda o: o.location_type if o else None),
                ("location_usage", lambda o: o.location_usage if o else None),
                ("country_name", lambda o: o.country_name if o else None),
                ("country_digit_code", lambda o: o.country_digit_code if o else None),
                ("country_alpha_code", lambda o: o.country_alpha_code if o else None),
                ("location_hierarchies", lambda o: o.location_hierarchies if o else None),
            ],
            filename='CSVs/sites',
            prod=IS_PROD
        )
        if IS_PROD:
            return {"master_data_csv": csv_content}

    """Employees"""
    if generate_all or EMPLOYEES == integration_scope:
        employees_service = GetRAASEmployees(
            base_url=connector.base_uri,
            token=connector.access_token,
            tenant=tenant,
            worker_types='d588c334446c11de98360015c5e6daf6!d588c41a446c11de98360015c5e6daf6'
        )
        employees: Dict[str, EmployeeInfo] = employees_service.get_entity_dic()
        print(list(employees.items())[:5])
        csv_content: str = employees_service.generate_csv(
            list(employees.values()),
            [
                ("employee_id", lambda o: o.employee_id if o else None),
                ("full_legal_name", lambda o: o.full_legal_name if o else None),
                ("employee_contract_type", lambda o: o.employee_contract_type if o else None),
                ("primary_work_email", lambda o: o.primary_work_email if o else None),
                ("manager_employee_id", lambda o: o.manager.manager_employee_id if o.manager else None),
                ("manager_name", lambda o: o.manager.manager_name if o.manager else None),
                ("manager_email", lambda o: o.manager.manager_email if o.manager else None),
                ("primary_work_address", lambda o: o.primary_work_address if o else None),
                ("country_name",
                 lambda o: o.primary_work_country_address.country_name if o.primary_work_country_address else None),
                ("country_digit_code", lambda
                    o: o.primary_work_country_address.country_digit_code if o.primary_work_country_address else None),
                ("country_alpha_code", lambda
                    o: o.primary_work_country_address.country_alpha_code if o.primary_work_country_address else None),
            ],
            filename='CSVs/employees',
            prod=IS_PROD
        )
        if IS_PROD:
            return {"master_data_csv": csv_content}

    """ASSETS"""
    if generate_all or ASSETS == integration_scope:
        asset_cat_service = GetRAASAssetCategories(
            base_url=connector.base_uri,
            token=connector.access_token,
            tenant=tenant,
        )
        asset_cat: Dict[str, AssetCategories] = asset_cat_service.get_entity_dic()
        print(asset_cat)
        csv_content: str = asset_cat_service.generate_csv(
            list(asset_cat.values()),
            [
                ("asset_class_id", lambda o: o.asset_class_id if o else None),
                ("asset_class_name", lambda o: o.asset_class_name if o else None),
            ],
            filename='CSVs/asset_categories',
            prod=IS_PROD
        )
        if IS_PROD:
            return {"master_data_csv": csv_content}

    """GTM ORGANIZATION"""
    if generate_all or GTM_ORG == integration_scope:
        gtm_org_service = GetRAASGeoSales(
            base_url=connector.base_uri,
            token=connector.access_token,
            tenant=tenant
        )

        gtm_orgs: Dict[str, GeoSales] = gtm_org_service.get_entity_dic()
        print(gtm_orgs)
        csv_content: str = gtm_org_service.generate_csv(
            list(gtm_orgs.values()),
            [
                ("dimension_id", lambda o: o.dimension_id if o else None),
                ("name", lambda o: o.name if o else None),
                ("organization_active", lambda o: o.organization_active if o else None),
                ("dimension_name", lambda o: o.dimension_name if o else None),
            ],
            filename='CSVs/GTM_organizations',
            prod=IS_PROD
        )
        if IS_PROD:
            return {"master_data_csv": csv_content}


if __name__ == '__main__':
    workday = 'workday_url.com'
    tenant = 'company'
    client_id = 'xxxxxx'
    client_secret = 'xxxxxxxxx-xxxxx-xxxx'
    refresh_token = 'xxxxxxxxxxxx-xxx'

    main_master_data({
        "workday_server": workday,
        "workday_tenant": tenant,
        "workday_client_id": client_id,
        "workday_client_secret": client_secret,
        "workday_refresh_token": refresh_token,
        "is_test": "true",
        "integration_scope": "8",
        "api_version": "v42.1"
    })
