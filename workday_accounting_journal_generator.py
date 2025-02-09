import time

from workday.csv_helpers import CSVJournalHelper
from workday.workday_api_generator_call import *
from workday.workday_implement_api import *
from workday.workday_raas_implementation_api import *
from workday_new.workday.utils import *


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
    # in order to make sure we retrieve all the journals for the required date
    as_of_effective_date = f"{str(transform_and_adjust_date(accounting_from_date, days=-1))}T00:00:00.000"

    # filter_by_creation_date = input.get('filter_by_creation_date', True)
    filter_by_creation_date = str(input.get('filter_by_creation_date', "true")) == "true"

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

        creation_date=accounting_from_date,
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

    journals: List[MappedJournal] = get_all_journals.get_all_entities(
        './/wd:Journal_Entry_Data',
        accounting_from_date=accounting_from_date,
        accounting_to_date=accounting_to_date,
        as_of_effective_date=as_of_effective_date,
    )

    scv_helper = CSVJournalHelper()
    total_journals = len(journals)
    print(f"journals transformed: {total_journals}")

    if total_journals > 0:
        # 🔎🕵🏽 filter Journals, check override `callable_condition` function in [workday_implementation_api.py]
        journals = get_all_journals.filter_objects(journals, get_all_journals.callable_condition)
        print(f"journals Filtered: {len(journals)}")
        csv_content = scv_helper.mapped_journals_to_csv(journals)

        if is_test:
            scv_helper.export_to_csv(
                csv_content,
                f'accounting_journal_{accounting_from_date[0:10]}_to_{accounting_to_date[0:10]}'
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
            "journals_error": [data for data in get_all_journals.failed_journals]
        }
    else:
        return {
            "journals_csv_contents": [],  # empty list when nothing is found
            # return process errors and parse error
            "journals_error": [data for data in get_all_journals.failed_journals]
        }



if __name__ == '__main__':
    workday = 'workday.com'
    tenant = 'Tenant'
    client_id = 'XXXXXXXXX'
    client_secret = 'CXXXXXXXXX-XXXXXXX-XXXXXXX'
    refresh_token = 'XXXXXXX-XXXXXX-XXXXXXXX-XXXXX'

    filter_by_creation_date = "true"
    accounting_from_date = "2025-01-20"
    accounting_to_date = ""
    days = 4  # Number of days to loop

    # Start the timer
    start_time = time.time()

    if filter_by_creation_date == "true":

        start_date = accounting_from_date
        dates = loop_over_date(start_date, days)

        print("Dates:")
        csv_files = []
        for date in dates:
            print(f"🚀 Parsing for: {date}")

            csv_files.append(f"accounting_journal_{date}_to_{date}_journal_entries.csv")

            res = main({
                "accounting_from_date": date,
                "accounting_to_date": date,
                "workday_server": workday,
                "workday_tenant": tenant,
                "workday_client_id": client_id,
                "workday_client_secret": client_secret,
                "workday_refresh_token": refresh_token,
                "is_test": "true",
                "num_row_limit": 40000,
                "filter_by_creation_date": filter_by_creation_date,
            })

            print(res['journals_error'])

            if len(dates):
                output_file = f"accounting_journal_{dates[0]}_to_{dates[-1]}_journal_entries.csv"
                merge_csv_files(csv_files, output_file)
    else:
        res = main({
            "accounting_from_date": accounting_from_date,
            "accounting_to_date": accounting_to_date,
            "workday_server": workday,
            "workday_tenant": tenant,
            "workday_client_id": client_id,
            "workday_client_secret": client_secret,
            "workday_refresh_token": refresh_token,
            "is_test": "true",
            "filter_by_creation_date": filter_by_creation_date,
        })
        print(res['journals_error'])

    # End the timer
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
