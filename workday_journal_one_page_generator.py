"""
This entry point must be used for the Busy workload process only
When you hit the maximum amount
"""

import time
from workday.csv_helpers import CSVJournalHelper
from workday.workday_implement_api import *
from workday.workday_raas_implementation_api import *
from workday.utils import *


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

    # Get the query Argument
    accounting_date = input['date']
    page = int(input['page'])
    count = int(input['count'])

    filter_by_creation_date = str(input.get('filter_by_creation_date', "true")) == "true"
    # in order to make sure we retrieve all the journals for the required date
    as_of_effective_date = f"{str(transform_and_adjust_date(accounting_date, days=-1))}T00:00:00.000"

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
    # Book Code
    book_codes: Dict[str, BookCodeInfo] = raas_book_code.get_entity_dic()
    # Call RAAS Endpoint and get all the Companies (Subsidiaries) into a dict
    subsidiaries: Dict[str, SubsidiaryInfo] = raas_subsidiaries.get_entity_dic()
    # Use Geo Sales Raas to extract GTM ORG
    gtm_org: Dict[str, GeoSales] = gtm_org_service.get_entity_dic()

    # Init GetAllJournals with all the fetched data
    get_all_journals = GetAllJournals(
        base_url=connector.base_uri,
        tenant=connector.tenant,
        token=connector.access_token,

        creation_date=accounting_date,
        filter_by_creation_date=filter_by_creation_date,

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

    journals: List[MappedJournal] = get_all_journals.get_all_entities_by_page(
        './/wd:Journal_Entry_Data',
        page=page,
        entity_count=count,
        accounting_from_date=accounting_date,
        accounting_to_date=accounting_date,
        as_of_effective_date=as_of_effective_date,
    )

    scv_helper = CSVJournalHelper()
    total_journals = len(journals)

    if total_journals > 0:
        # 🔎🕵🏽 filter Journals, check override `callable_condition` function in [workday_implementation_api.py]
        journals = get_all_journals.filter_objects(journals, get_all_journals.callable_condition)
        csv_content = scv_helper.mapped_journals_to_csv(journals)

        if is_test:
            scv_helper.export_to_csv(
                csv_content,
                f'accounting_journal_{accounting_date[0:10]}'
            )

        # Split up csv into several chunks
        line_number = input.get('num_row_limit')
        if line_number:
            line_number = int(line_number)
        else:
            line_number = 40000

        csvs: List[str] = get_all_journals.split_csv_content(csv_content, line_number=line_number)
        print(f"Generated {len(csvs)} chunks for {len(journals)} journals")

        return {
            "journals_csv_contents": csvs,
            # return process errors and parse error
            "journals_error": [data for data in get_all_journals.failed_journals],
            "has_end": total_journals == 0
        }
    else:
        return {
            "journals_csv_contents": [],  # empty list when nothing is found
            # return process errors and parse error
            "journals_error": [data for data in get_all_journals.failed_journals],
            "has_end": True
        }


if __name__ == '__main__':
    workday = 'cmpny.workday.com'
    tenant = 'company'
    client_id = 'xxxxxxxxx'
    client_secret = 'xxxxxxxxxxxxxxxxxxxxxx'
    refresh_token = 'xxxxxxxxxxxxxxXXXXXXXxxxxxXXXXXXXXX'

    filter_by_creation_date = "true"

    # Start the timer
    start_time = time.time()

    res = main({
      "date": "2025-01-01",
      "page": 1,
      "count": 999,
      "num_row_limit": 40000,
      "filter_by_creation_date": filter_by_creation_date,

      "workday_server": workday,
      "workday_tenant": tenant,
      "workday_client_id": client_id,
      "workday_client_secret": client_secret,
      "workday_refresh_token": refresh_token,

      "is_test": "true",
    })
    # End the timer
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
    print(res['journals_error'])
