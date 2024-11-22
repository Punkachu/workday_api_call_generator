import time

from workday.csv_helpers import CSVJournalHelper
from workday.workday_api_generator_call import *
from workday.workday_implement_api import *
from workday.workday_raas_implementation_api import *


def main(input):
    """
    Main call function for Workato Python Action
    :param input:
    :return:
    """
    # Replace with actual credentials and details
    workday = input['workday_server']
    tenant = input['workday_tenant']

    client_id = input['workday_client_id']
    client_secret = input['workday_client_secret']
    refresh_token = input['workday_refresh_token']

    accounting_from_date = input['accounting_from_date']
    accounting_to_date = input['accounting_to_date']

    is_test = False if (input.get("is_test") or "") == "false" else True
    _DEFAULT_WORKDAY_API_VERSION = input.get("api_version") or DEFAULT_WORKDAY_API_VERSION

    connector = WorkdayConnector(workday, tenant, client_id, client_secret, refresh_token)
    connector.acquire_token()

    # Get Raas Data
    raas_ledger_account = GetRAASLedgerAccount(base_url=connector.base_uri, token=connector.access_token, tenant=tenant)
    raas_cost_center = GetRAASCostCenter(base_url=connector.base_uri, token=connector.access_token, tenant=tenant)
    raas_book_code = GetRAASBookCodes(base_url=connector.base_uri, token=connector.access_token, tenant=tenant)
    raas_subsidiaries = GetRAASCompanies(base_url=connector.base_uri, token=connector.access_token, tenant=tenant)
    gtm_org_service = GetRAASGeoSales(base_url=connector.base_uri, token=connector.access_token, tenant=tenant)

    resource_category_service = GetResourceCategories(
        base_url=connector.base_uri, token=connector.access_token,
        tenant=tenant, api_version=_DEFAULT_WORKDAY_API_VERSION
    )

    customer_contract_service = GetCustomerContracts(
        base_url=connector.base_uri, token=connector.access_token,
        tenant=tenant, api_version=_DEFAULT_WORKDAY_API_VERSION
    )

    suppliers = GetRAASSuppliers(
        base_url=connector.base_uri, token=connector.access_token,
        tenant=tenant, api_version=_DEFAULT_WORKDAY_API_VERSION
    )

    # Call the RAAS Endpoint and get all the ledger accounts into a dict
    ledger_accounts: Dict[str, LedgerAccount] = raas_ledger_account.get_entity_dic()
    # Call RAAS Endpoint and get all the Cost Centers into a dict
    cost_centers: Dict[str, CostCenterInfo] = raas_cost_center.get_entity_dic()
    print(f'Cost center : {cost_centers}')
    # Book Code
    book_codes: Dict[str, BookCodeInfo] = raas_book_code.get_entity_dic()
    # Call RAAS Endpoint and get all the Companies (Subsidiaries) into a dict
    subsidiaries: Dict[str, SubsidiaryInfo] = raas_subsidiaries.get_entity_dic()
    # Use Geo Sales Raas to extract GTM ORG
    gtm_org: Dict[str, GeoSales] = gtm_org_service.get_entity_dic()

    # Init GetAllJournals with all the fetched data
    journal_lines = GetAllJournals(
        base_url=connector.base_uri,
        tenant=connector.tenant,
        token=connector.access_token,

        api_version=connector.version,

        ledger_accounts=ledger_accounts,
        cost_centers=cost_centers,
        book_codes=book_codes,
        gtm_org=gtm_org,
        subsidiaries=subsidiaries,

        raas_suppliers=suppliers,
        resource_category_service=resource_category_service,
        customer_contract_service=customer_contract_service,
    )

    journals: List[MappedJournal] = journal_lines.get_all_entities(
        './/wd:Journal_Entry_Data',
        accounting_from_date=accounting_from_date,
        accounting_to_date=accounting_to_date
    )

    scv_helper = CSVJournalHelper()
    if len(journals) > 0:
        csv_content = scv_helper.mapped_journals_to_csv(journals)
    else:
        csv_content = []  # nothing to do
    if is_test:
        scv_helper.export_to_csv(
            csv_content,
            f'accounting_journal_{accounting_from_date[0:10]}_to_{accounting_to_date[0:10]}'
        )

    return {
        "journals_csv_contents": csv_content,
        # return process errors and parse error
        "journals_error": [data for data in journal_lines.failed_journals]
    }


if __name__ == '__main__':
    workday = 'cmpny.workday.com'
    tenant = 'company'
    client_id = 'xxxxxxxxx'
    client_secret = 'xxxxxxxxxxxxxxxxxxxxxx'
    refresh_token = 'xxxxxxxxxxxxxxXXXXXXXxxxxxXXXXXXXXX'

    # Start the timer
    start_time = time.time()

    res = main({
      "accounting_from_date": "2024-10-01",
      "accounting_to_date": "2024-10-28",
      "workday_server": workday,
      "workday_tenant": "contentsquare3",
      "workday_client_id": client_id,
      "workday_client_secret": client_secret,
      "workday_refresh_token": refresh_token,
      "is_test": "false",
    })
    # End the timer
    end_time = time.time()
    # Calculate the duration13 November 2024
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
    print(res['journals_error'])
