import csv
import io
from typing import List

from workday.models import T, Any
from workday.models import MappedJournal, MappedEntryJournal


class CSVJournalHelper:
    """ Define a specific easy maintainable class to generate CSV report """

    def __init__(self):
        # you can reorganize header by switching index here
        self.fields = [
            ("journal_id", lambda j: j.journal_id if j else None),
            ("document_number", lambda j: j.document_info.document_number if j and j.document_info else None),
            ("accounting_period_name", lambda j: j.accounting_period_name if j else None),
            ("document_description", lambda j: j.document_info.description if j and j.document_info else None),
            ("book_code_id", lambda j: j.book_code_info.book_code_id if j and j.book_code_info else None),
            ("book_code_name", lambda j: j.book_code_info.name if j and j.book_code_info else None),
            ("ledger_code", lambda j: j.account_info.code if j and j.account_info else None),
            ("pl_info_destination", lambda j: j.pl_info_destination if j else None),
            ("journal_source", lambda j: j.journal_source if j else None)
        ]

        self.entry_line_fields = [
            ("number", lambda j: j),

            ("cash_flow_code", lambda j: j.cash_flow_code),

            ("customer_id", lambda j: j.customer_id),

            ("ledger_account_code", lambda j: j.ledger_account.Ledger_Account_ID if j.ledger_account else None),
            ("ledger_account_name", lambda j: j.ledger_account.Ledger_Account_Name if j.ledger_account else None),
            ("ledger_account_type", lambda j: j.ledger_account.Types if j.ledger_account else None),

            ("subsidiary_internal_id", lambda j: j.subsidiary_info.internal_id if j.subsidiary_info else None),
            ("subsidiary_name", lambda j: j.subsidiary_info.name if j.subsidiary_info else None),

            ("debit", lambda j: j.amount_info.debit if j.amount_info else None),
            ("credit", lambda j: j.amount_info.credit if j.amount_info else None),
            ("ledger_debit", lambda j: j.amount_info.ledger_debit if j.amount_info else None),
            ("ledger_credit", lambda j: j.amount_info.ledger_credit if j.amount_info else None),
            ("currency_symbol", lambda j: j.amount_info.currency_symbol if j.amount_info else None),
            ("amount_net_usd", lambda j: j.amount_info.amount_net_usd if j.amount_info else None),

            ("cost_center_code", lambda j: j.cost_center_info.code if j.cost_center_info else None),
            ("cost_center_name", lambda j: j.cost_center_info.name if j.cost_center_info else None),

            ("revenue_name", lambda j: j.revenue_info.revenue_name if j.revenue_info else None),

            ("acquisition_channel_dim_id",
             lambda j: j.revenue_info.gtm_org.dimension_id if j.revenue_info.gtm_org else None),
            ("acquisition_channel_name", lambda j: j.revenue_info.gtm_org.name if j.revenue_info.gtm_org else None),
            ("acquisition_channel_dim_name",
             lambda j: j.revenue_info.gtm_org.dimension_name if j.revenue_info.gtm_org else None),

            ("vendor_code", lambda j: j.revenue_info.deal.customer_contract_id if j.revenue_info.deal else None),
            ("vendor_company_name", lambda j: j.revenue_info.deal.contract_name if j.revenue_info.deal else None),
            ("vendor_po", lambda j: j.revenue_info.deal.po_number if j.revenue_info.deal else None),
            ("vendor_on_hold", lambda j: j.revenue_info.deal.on_hold if j.revenue_info.deal else None),
            ("vendor_contract_type", lambda j: j.revenue_info.deal.contract_type if j.revenue_info.deal else None),

            ("project_code", lambda j: j.project_code),

            ("expense_type_code", lambda j: j.expense_type.code if j.expense_type else None),
            ("expense_type_name", lambda j: j.expense_type.name if j.expense_type else None),

            ("memo", lambda j: j.memo),
        ]

        self.entries_prefix = "entry_line"

    @staticmethod
    def export_to_csv(csv_content: str, base_filename: str):
        with open(f'{base_filename}_journal_entries.csv', 'w', newline='') as file:
            file.write(csv_content)

    def _mapped_entry_journals_to_csv(self, mapped_entries: List[MappedEntryJournal]) -> List[List[Any]]:
        # Write each MappedEntryJournal object to the CSV row format
        row = []
        for index, entry in enumerate(mapped_entries):
            data = [(index + 1)] + [_field[1](entry) for _field in self.entry_line_fields[1:]]
            row.append(data)
        return row

    def mapped_journals_to_csv(self, mapped_journals: List[MappedJournal]) -> str:
        # Define the output buffer for the CSV
        output = io.StringIO()
        writer = csv.writer(output)
        # Extract headers
        headers = [field[0] for field in self.fields]
        # Write the header to the CS
        entries_header = [f'{self.entries_prefix}_{field_[0]}' for field_ in self.entry_line_fields]
        writer.writerow(headers + entries_header)

        # Write each MappedJournal object to the CSV
        for journal in mapped_journals:
            if journal:
                journal_row = [_field[1](journal) for _field in self.fields]
                entity_line_rows = self._mapped_entry_journals_to_csv(journal.mapped_entries)

                for entry_line_row in entity_line_rows:
                    writer.writerow(journal_row + entry_line_row)

        # Get the CSV string from the output buffer
        csv_text = output.getvalue()
        output.close()

        return csv_text


class CSVExportHelper:
    """
        Export Generic Object as CSV
    """

    def __init__(self, fields):
        # you can reorganize header by switching index here
        self.fields = fields

    @staticmethod
    def export_to_csv(csv_content: str, filename: str):
        with open(f'{filename}.csv', 'w', newline='') as file:
            file.write(csv_content)

    def generate_csv_content(self, data_list: List[T]) -> str:
        # Define the output buffer for the CSV
        output = io.StringIO()
        writer = csv.writer(output)
        # Extract headers
        headers = [field[0] for field in self.fields]
        writer.writerow(headers)

        # Write each MappedJournal object to the CSV
        for data in data_list:
            data_row = [_field[1](data) for _field in self.fields]
            writer.writerow(data_row)

        # Get the CSV string from the output buffer
        csv_text = output.getvalue()
        output.close()

        return csv_text
