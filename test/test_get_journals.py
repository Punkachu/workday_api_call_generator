import unittest
import os
from typing import Type, Dict

from test_utils import TestCSVHelper
from workday.workday_implement_api import *

T = TypeVar('T')


def load_csvs_as_dic(filename: str, obj: Type[T], field_id: str, field_mapping: Optional[Dict[str, str]]):
    # Define the path to the XML file in the data directory
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'CSVs')
    file_path = os.path.join(data_dir, filename)
    csv_helper = TestCSVHelper()

    result = csv_helper.csv_to_object_dict(file_path, field_id, obj, field_mapping)

    return result


# Define the test class
class TestXMLJournalParsing(unittest.TestCase):

    def setUp(self):
        # Define the path to the XML file in the data directory
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.', 'data')
        file_path = os.path.join(data_dir, 'mock_journal_entry.xml')

        # Load the XML data from the file
        with open(file_path, 'r') as file:
            self.xml_data = file.read()

        # Set the XML namespace
        self.xml_namespace = {'wd': 'urn:com.workday/bsvc'}

        cc_field_mapping = {
            "referenceID": "referenceID",
            "name": "name",
            "code": "code",
            "isActive": "isActive",
            "manager": "name"
        }
        self.cost_centers_dic = load_csvs_as_dic('cost_centers.csv', CostCenterInfo, 'code', cc_field_mapping)
        bc_field_mapping = {
            "book_code_id": "book_code",
            "name": "book_code_name"
        }
        book_code_dic = load_csvs_as_dic('book_codes.csv', BookCodeInfo, 'book_code', bc_field_mapping)

        la_field_mapping = {
            "Ledger_Account_ID": "Ledger_Account_ID",
            "Ledger_Account_Name": "Ledger_Account_Name",
            "Types": "Ledger_Account_Types",
        }
        self.ledger_accounts_dic = load_csvs_as_dic('ledger_account.csv', LedgerAccount, 'Ledger_Account_ID',
                                               la_field_mapping)

        sub_field_mapping = {
            "internal_id": "id",
            "name": "name"
        }
        self.subsidiaries_dic = load_csvs_as_dic('companies_aka_subsidiaries.csv', SubsidiaryInfo, 'id', sub_field_mapping)

        gtm_org_dic = load_csvs_as_dic('GTM_organizations.csv', GeoSales, 'dimension_id', None)

        base_url = 'test_base_url'
        tenant = 'cs3'
        version = 'v42.1'
        token = 'test'

        suppliers = GetRAASSuppliers(base_url=base_url, token=token, tenant=tenant, api_version='v42.1')

        resource_category_service = GetResourceCategories(base_url=base_url, token=token, tenant=tenant, api_version=version)

        customer_contract_service = GetCustomerContracts(base_url=base_url, token=token, tenant=tenant, api_version=version)

        self.get_all_journals = GetAllJournals(
            base_url=base_url,
            tenant=tenant,
            api_version=version,
            token=token,
            ledger_accounts=self.ledger_accounts_dic,
            cost_centers=self.cost_centers_dic,
            subsidiaries=self.subsidiaries_dic,
            book_codes=book_code_dic,
            gtm_org=gtm_org_dic,

            raas_suppliers=suppliers,
            resource_category_service=resource_category_service,
            customer_contract_service=customer_contract_service,
        )

        root = ET.fromstring(self.xml_data)
        # Find all Supplier_Data elements
        entity_data_elements = root.findall('.//wd:Journal_Entry', self.xml_namespace)
        self.journals: List[JournalEntry] = []
        for entry in entity_data_elements:
            # Parse the XML data
            journal = self.get_all_journals._parse_journals(entry)
            self.journals.append(journal)

    # Test Journal 1 from XML

    def test_parse_first_journal_entry_data(self):
        journal = self.journals[0]

        # Check if description is not found
        self.assertIsNone(journal.description)

        # Check Journal Entry Reference
        self.assertEqual(journal.journalEntryReference.Accounting_Journal_ID, "JOURNALHJHLDGS54")

        # Check Journal Number
        self.assertEqual(journal.journal_Number, "LE111 JRNL 2024 000002")

        # Check Accounting Date
        self.assertEqual(journal.accounting_Date, "2024-02-01")

        # Check Creation Date
        self.assertEqual(journal.creation_Date, "2024-05-22T06:34:08.883-07:00")

        # Check Last Updated Date
        self.assertEqual(journal.last_Updated_Date, "2024-05-22T23:13:04.206-07:00")

        # Check Record Quantity
        self.assertEqual(journal.record_Quantity, 0)

        # Check Total Ledger Debits
        self.assertEqual(journal.total_Ledger_Debits, 1750)

        # Check Total Ledger Credits
        self.assertEqual(journal.total_ledger_credits, 1750)

        # Check Journal Sequence Number
        self.assertEqual(journal.journal_Sequence_Number, "JRNL-2024-2")

        # Check Journal Status Reference
        self.assertEqual(journal.journalStatusReference.WID, "6f8e52d2376e4c899463020db034c87c")
        self.assertEqual(journal.journalStatusReference.Journal_Entry_Status_ID, "POSTED")

        # Check Company Reference
        self.assertEqual(journal.companyReference.WID, "12e1c4b8f4ed10167fc2cefddc590000")
        self.assertEqual(journal.companyReference.Organization_Reference_ID, "LE111")
        self.assertEqual(journal.companyReference.Company_Reference_ID, "LE111")

        # Check Currency Reference
        self.assertEqual(journal.currencyReference.WID, "eae312fc5152410cb4c8b452c26320a6")
        self.assertEqual(journal.currencyReference.Currency_ID, "EUR")
        self.assertEqual(journal.currencyReference.Currency_Numeric_Code, "978")

        # Check Ledger Reference
        self.assertEqual(journal.ledgerReference.WID, "b48857ec51c110194db3aea09f930000")
        self.assertEqual(journal.ledgerReference.Ledger_Reference_ID, "LEDGER-6-22")

        # Check Journal Source Reference
        self.assertEqual(journal.journalSourceReference.Journal_Source_ID, "Manual_Journal")

        # Check Ledger Period Reference
        self.assertEqual(journal.ledgerPeriodReference.WID, "b48857ec51c110194db3b23a37e40000")

    def test_parse_first_journal_entry_lines_1(self):
        journal = self.journals[0]

        # Check Journal Entry Lines
        self.assertEqual(len(journal.journalEntryLines), 2)
        line = journal.journalEntryLines[0]

        # Check Line Company Reference
        self.assertEqual(line.lineCompanyReference.WID, "12e1c4b8f4ed10167fc2cefddc590000")
        self.assertEqual(line.lineCompanyReference.Organization_Reference_ID, "LE111")
        self.assertEqual(line.lineCompanyReference.Company_Reference_ID, "LE111")

        # Check Ledger Account Reference
        self.assertEqual(line.ledgerAccountReference.WID, "12e1c4b8f4ed10168b6bd53ed5f20000")
        self.assertEqual(line.ledgerAccountReference.Ledger_Account_ID, "40800000")

        # Check Worktags Reference
        self.assertIsNone(line.worktagsReference.Spend_Category_ID)
        self.assertIsNone(line.worktagsReference.Supplier_ID)
        self.assertIsNone(line.worktagsReference.Customer_Contract_Reference_ID)
        self.assertEqual(line.worktagsReference.Cost_Center_Reference_ID, "CC_520")

        # Check Debit Amount
        self.assertEqual(line.debit_Amount, 1750)

        # Check Credit Amount
        self.assertEqual(line.credit_Amount, 0)

        # Check Currency Rate
        self.assertEqual(line.currency_Rate, 1)

        # Check Ledger Credit Amount
        self.assertEqual(line.ledger_Credit_Amount, 0)

        # Check Ledger Debit Amount
        self.assertEqual(line.ledger_Debit_Amount, 1750)

        # Check Exclude from Spend Report
        self.assertEqual(line.exclude_from_spend_report, 0)

        # Check Journal Line Number
        self.assertEqual(line.journal_line_number, 0)

    def test_parse_first_journal_entry_lines_2(self):
        journal = self.journals[0]

        # Check Journal Entry Lines
        self.assertEqual(len(journal.journalEntryLines), 2)
        line = journal.journalEntryLines[1]

        # Check Line Company Reference
        self.assertEqual(line.lineCompanyReference.WID, "12e1c4b8f4ed10167fc2cefddc590000")
        self.assertEqual(line.lineCompanyReference.Organization_Reference_ID, "LE111")
        self.assertEqual(line.lineCompanyReference.Company_Reference_ID, "LE111")

        # Check Ledger Account Reference
        self.assertEqual(line.ledgerAccountReference.WID, "12e1c4b8f4ed10168b6be7d4059d0004")
        self.assertEqual(line.ledgerAccountReference.Ledger_Account_ID, "62260000")

        # Check Worktags Reference
        self.assertIsNone(line.worktagsReference.Spend_Category_ID)
        self.assertIsNone(line.worktagsReference.Supplier_ID)
        self.assertIsNone(line.worktagsReference.Customer_Contract_Reference_ID)
        self.assertEqual(line.worktagsReference.Cost_Center_Reference_ID, "CC_520")

        # Check Debit Amount
        self.assertEqual(line.debit_Amount, 0)

        # Check Credit Amount
        self.assertEqual(line.credit_Amount, 1750)

        # Check Currency Rate
        self.assertEqual(line.currency_Rate, 1)

        # Check Ledger Credit Amount
        self.assertEqual(line.ledger_Credit_Amount, 1750)

        # Check Ledger Debit Amount
        self.assertEqual(line.ledger_Debit_Amount, 0)

        # Check Exclude from Spend Report
        self.assertEqual(line.exclude_from_spend_report, 0)

        # Check Journal Line Number
        self.assertEqual(line.journal_line_number, 0)

    # Test Journal 2 from XML

    def test_parse_journal_entry_data_2(self):
        journal = self.journals[1]

        # Check if description is not found
        self.assertIsNone(journal.description)

        # Check Journal Entry Reference
        self.assertEqual(journal.journalEntryReference.Accounting_Journal_ID, "FXREVALKO34")

        # Check Journal Number
        self.assertEqual(journal.journal_Number, "LE503 JRNL 2024 000000")

        # Check Accounting Date
        self.assertEqual(journal.accounting_Date, "2024-02-01")

        # Check Creation Date
        self.assertEqual(journal.creation_Date, "2024-05-22T23:20:47.602-07:00")

        # Check Last Updated Date
        self.assertEqual(journal.last_Updated_Date, "2024-05-22T23:20:47.602-07:00")

        # Check Record Quantity
        self.assertEqual(journal.record_Quantity, 0)

        # Check Total Ledger Debits
        self.assertEqual(journal.total_Ledger_Debits, 7832796)

        # Check Total Ledger Credits
        self.assertEqual(journal.total_ledger_credits, 7832796)

        # Check Journal Sequence Number
        self.assertEqual(journal.journal_Sequence_Number, "JRNL-2024-2")

        # Check Journal Status Reference
        self.assertEqual(journal.journalStatusReference.WID, "6f8e52d2376e4c899463020db034c87c")
        self.assertEqual(journal.journalStatusReference.Journal_Entry_Status_ID, "POSTED")

        # Check Company Reference
        self.assertEqual(journal.companyReference.Organization_Reference_ID, "COMPANY-3-22")
        self.assertEqual(journal.companyReference.Company_Reference_ID, "COMPANY-3-22")

        # Check Currency Reference
        self.assertEqual(journal.currencyReference.WID, "e5c5d283917f4e21a622d94fbf956dc1")
        self.assertEqual(journal.currencyReference.Currency_ID, "KRW")
        self.assertEqual(journal.currencyReference.Currency_Numeric_Code, "410")

        # Check Ledger Reference
        self.assertEqual(journal.ledgerReference.WID, "b48857ec51c110194db360a0b9770000")
        self.assertEqual(journal.ledgerReference.Ledger_Reference_ID, "LEDGER-6-9")

        # Check Journal Source Reference
        self.assertEqual(journal.journalSourceReference.Journal_Source_ID, "Manual_Journal")

        # Check Ledger Period Reference
        self.assertEqual(journal.ledgerPeriodReference.WID, "b48857ec51c110194db363a0af470006")

    def test_parse_second_journal_entry_lines_1(self):
        journal = self.journals[1]

        # Check Journal Entry Lines
        self.assertEqual(len(journal.journalEntryLines), 2)
        line = journal.journalEntryLines[0]

        # Check Line Company Reference
        self.assertEqual(line.lineCompanyReference.WID, "642fbcf9220e1001e5305039a2a60000")
        self.assertEqual(line.lineCompanyReference.Organization_Reference_ID, "COMPANY-3-22")
        self.assertEqual(line.lineCompanyReference.Company_Reference_ID, "COMPANY-3-22")

        # Check Ledger Account Reference
        self.assertEqual(line.ledgerAccountReference.Ledger_Account_ID, "45500009")

        # Check Worktags Reference
        self.assertIsNone(line.worktagsReference.Spend_Category_ID)
        self.assertIsNone(line.worktagsReference.Supplier_ID)
        self.assertIsNone(line.worktagsReference.Customer_Contract_Reference_ID)
        self.assertEqual(line.worktagsReference.Cost_Center_Reference_ID, "TBC_8")

        # Check Debit Amount
        self.assertEqual(line.debit_Amount, 7832796)

        # Check Credit Amount
        self.assertEqual(line.credit_Amount, 0)

        # Check Currency Rate
        self.assertEqual(line.currency_Rate, 1)

        # Check Ledger Credit Amount
        self.assertEqual(line.ledger_Credit_Amount, 0)

        # Check Ledger Debit Amount
        self.assertEqual(line.ledger_Debit_Amount, 7832796)

        # Check Exclude from Spend Report
        self.assertEqual(line.exclude_from_spend_report, 0)

        # Check Journal Line Number
        self.assertEqual(line.journal_line_number, 0)

    def test_parse_second_journal_entry_lines_2(self):
        journal = self.journals[1]

        # Check Journal Entry Lines
        self.assertEqual(len(journal.journalEntryLines), 2)
        line = journal.journalEntryLines[1]

        # Check Line Company Reference
        self.assertEqual(line.lineCompanyReference.WID, "642fbcf9220e1001e5305039a2a60000")
        self.assertEqual(line.lineCompanyReference.Organization_Reference_ID, "COMPANY-3-22")
        self.assertEqual(line.lineCompanyReference.Company_Reference_ID, "COMPANY-3-22")

        # Check Ledger Account Reference
        self.assertEqual(line.ledgerAccountReference.Ledger_Account_ID, "66600100")

        # Check Worktags Reference
        self.assertIsNone(line.worktagsReference.Spend_Category_ID)
        self.assertIsNone(line.worktagsReference.Supplier_ID)
        self.assertIsNone(line.worktagsReference.Customer_Contract_Reference_ID)
        self.assertEqual(line.worktagsReference.Cost_Center_Reference_ID, "TBC_8")

        # Check Debit Amount
        self.assertEqual(line.debit_Amount, 0)

        # Check Credit Amount
        self.assertEqual(line.credit_Amount, 7832796)

        # Check Currency Rate
        self.assertEqual(line.currency_Rate, 1)

        # Check Ledger Credit Amount
        self.assertEqual(line.ledger_Credit_Amount, 7832796)

        # Check Ledger Debit Amount
        self.assertEqual(line.ledger_Debit_Amount, 0)

        # Check Exclude from Spend Report
        self.assertEqual(line.exclude_from_spend_report, 0)

        # Check Journal Line Number
        self.assertEqual(line.journal_line_number, 0)

    # TEST CONVERTOR FUNCTIONS INTO PIGMENT DATA
    def test_convert_all_journals_into_pigment_journals(self):
        converted_journal1: MappedJournal = self.get_all_journals._convert_all_journals_into_pigment_journals(
            self.journals[0],
            ledger_accounts=self.ledger_accounts_dic,
            cost_centers=self.cost_centers_dic,
            subsidiaries=self.subsidiaries_dic
        )

        converted_journal2: MappedJournal = self.get_all_journals._convert_all_journals_into_pigment_journals(
            self.journals[1],
            ledger_accounts=self.ledger_accounts_dic,
            cost_centers=self.cost_centers_dic,
            subsidiaries=self.subsidiaries_dic
        )

        mapped_journal_1 = converted_journal1
        mapped_journal_2 = converted_journal2

        # check matching amount of MappedEntryJournal objects
        self.assertEqual(len(mapped_journal_1.mapped_entries), 2)
        self.assertEqual(len(mapped_journal_2.mapped_entries), 2)

        # Check Account information
        self.assertEqual(mapped_journal_1.account_info.code, 'LEDGER-6-22')
        self.assertEqual(mapped_journal_2.account_info.code, 'LEDGER-6-9')

        # check Document Information
        self.assertIsNone(mapped_journal_1.document_info.description)
        self.assertIsNone(mapped_journal_2.document_info.description)

        self.assertEqual(mapped_journal_1.document_info.document_number, 'JRNL-2024-2')
        self.assertEqual(mapped_journal_2.document_info.document_number, 'JRNL-2024-2')

        # Check fields is_allocation
        self.assertEqual(mapped_journal_1.journal_source, 'Manual_Journal')
        self.assertEqual(mapped_journal_2.journal_source, 'Manual_Journal')

        # Check fields pl_info_destination
        self.assertIsNone(mapped_journal_1.pl_info_destination)
        self.assertIsNone(mapped_journal_2.pl_info_destination)

        # Check accounting_period_name
        self.assertEqual(mapped_journal_1.accounting_period_name, '2024-02-01')
        self.assertEqual(mapped_journal_2.accounting_period_name, '2024-02-01')

        # Check mapped_entries Entries
        entries_1 = mapped_journal_1.mapped_entries
        entries_2 = mapped_journal_2.mapped_entries
        self.assertEqual(len(entries_1), 2)
        self.assertEqual(len(entries_2), 2)

        entries_1_1, entries_1_2 = entries_1[0], entries_1[1]
        entries_2_1, entries_2_2 = entries_2[0], entries_2[1]

        # Check Entry: memo
        self.assertIsNone(entries_1_1.memo)
        self.assertIsNone(entries_1_2.memo)
        self.assertIsNone(entries_2_1.memo)
        self.assertIsNone(entries_2_1.memo)

        # Check Entity project_code
        self.assertIsNone(entries_1_1.project_code)
        self.assertIsNone(entries_1_2.project_code)
        self.assertIsNone(entries_2_1.project_code)
        self.assertIsNone(entries_2_1.project_code)

        # Check Entity expense_type
        self.assertIsNone(entries_1_1.expense_type)
        self.assertIsNone(entries_1_2.expense_type)
        self.assertIsNone(entries_2_1.expense_type)
        self.assertIsNone(entries_2_1.expense_type)

        # Check Entity Vendor
        self.assertIsNone(entries_1_1.vendor_info)




# Run the tests
if __name__ == '__main__':
    unittest.main()
