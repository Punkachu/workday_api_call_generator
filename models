""" 
    Contains all the Models From Workday APIs.
    Use this file to add up as many models as you want.
"""
from dataclasses import dataclass, field
from typing import TypeVar, Optional, List, Any

# TypeVar for generic type T
T = TypeVar('T')


@dataclass
class BookCodeInfo:
    book_code_id: Optional[str] = None
    name: Optional[str] = None


@dataclass
class JournalEntryReference:
    WID: Optional[str] = None
    Accounting_Journal_ID: Optional[str] = None


@dataclass
class JournalStatusReference:
    WID: Optional[str] = None
    Journal_Entry_Status_ID: Optional[str] = None


@dataclass
class CompanyReference:
    Company_Reference_ID: Optional[str] = field(default=None, metadata={"alias": "Subsidiary_Internal_ID"})
    WID: Optional[str] = None
    Organization_Reference_ID: Optional[str] = None


@dataclass
class CurrencyReference:
    WID: Optional[str] = None
    Currency_ID: Optional[str] = None
    Currency_Numeric_Code: Optional[str] = None


@dataclass
class LedgerReference:
    WID: Optional[str] = None
    Ledger_Reference_ID: Optional[str] = field(default=None, metadata={"alias": "Account Code"})


@dataclass
class JournalSourceReference:
    Journal_Source_ID: Optional[str] = None


@dataclass
class LineCompanyReference:
    WID: Optional[str] = None
    Organization_Reference_ID: Optional[str] = None
    Company_Reference_ID: Optional[str] = None


@dataclass
class LedgerAccountReference:
    WID: Optional[str] = None
    Ledger_Account_ID: Optional[str] = None


@dataclass
class LedgerAccount:
    # Used to complete data
    Ledger_Account_ID: str
    Ledger_Account_Name: str
    Types: str
    # Ledger_Account_Summary: Optional[str]
    Account_Sets: Optional[list]


@dataclass
class LedgerPeriodReference:
    WID: Optional[str] = None


@dataclass
class CurrencyReference:
    WID: Optional[str] = None
    Currency_ID: Optional[str] = None
    Currency_Numeric_Code: Optional[str] = None


@dataclass(frozen=True, eq=True)
class SpendCategory:
    code: Optional[str] = None
    name: Optional[str] = None


@dataclass
class WorktagsReference:
    # Cost Center Code
    Cost_Center_Reference_ID: Optional[str] = None
    # Region ID (revenue)
    Custom_Organization_Reference_ID: Optional[str] = None
    # Vendor code
    Supplier_ID: Optional[str] = None
    # Project Code
    Project_ID: Optional[str] = None
    # Expense Type
    Spend_Category_ID: Optional[str] = None
    # Class Name
    Revenue_Category_ID: Optional[str] = None
    # Acquisition Channel dimension reference
    Customer_Contract_Reference_ID: Optional[str] = None
    # Cash Flow Code --> Custom Worktag 03
    cash_flow_code: Optional[str] = None
    # Customer ID
    customer_id: Optional[str] = None


@dataclass
class JournalEntryLine:
    lineCompanyReference: Optional[LineCompanyReference] = None
    ledgerAccountReference: Optional[LedgerAccountReference] = None
    currencyReference: Optional[CurrencyReference] = None
    worktagsReference: Optional[WorktagsReference] = None

    debit_Amount: Optional[float] = None
    credit_Amount: Optional[float] = None

    currency_Rate: Optional[float] = None

    ledger_Debit_Amount: Optional[float] = None
    ledger_Credit_Amount: Optional[float] = None

    exclude_from_spend_report: Optional[int] = None
    journal_line_number: Optional[int] = None

    memo: Optional[str] = None


@dataclass
class JournalEntry:
    journal_Number: Optional[str] = None
    journal_Sequence_Number: Optional[str] = None
    accounting_Date: Optional[str] = None
    record_Quantity: Optional[int] = None
    total_Ledger_Debits: Optional[float] = None
    total_ledger_credits: Optional[float] = None
    creation_Date: Optional[str] = None
    last_Updated_Date: Optional[str] = None
    description: Optional[str] = None
    # P& L Destination
    custom_Worktag_4_ID: Optional[str] = None

    book_code: Optional[BookCodeInfo] = None
    journalEntryReference: Optional[JournalEntryReference] = None
    journalStatusReference: Optional[JournalStatusReference] = None
    companyReference: Optional[CompanyReference] = None
    currencyReference: Optional[CurrencyReference] = None
    ledgerReference: Optional[LedgerReference] = None
    journalSourceReference: Optional[JournalSourceReference] = None
    ledgerPeriodReference: Optional[LedgerPeriodReference] = None

    journalEntryLines: Optional[List[JournalEntryLine]] = None



@dataclass
class SiteInfo:
    site_id: Optional[str] = None
    inactive: Optional[bool] = None

    location_name: Optional[str] = None
    location_address: Optional[str] = None
    location_type: Optional[str] = None
    location_usage: Optional[str] = None

    country_name: Optional[str] = None
    country_digit_code: Optional[int] = None
    country_alpha_code: Optional[str] = None

    location_hierarchies: Optional[str] = None


@dataclass
class ProjectCodeInfo:
    project_id: Optional[str] = None
    name: Optional[str] = None
    project_currency_id: Optional[str] = None
    project_currency_num_code: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    project_status: Optional[str] = None
    company: Optional[str] = None


@dataclass
class AssetCategories:
    asset_class_id: Optional[str] = None
    asset_class_name: Optional[str] = None


@dataclass
class GeoSales:
    dimension_id: Optional[str] = None
    name: Optional[str] = None
    organization_active: Optional[bool] = None
    dimension_name: Optional[str] = None


@dataclass
class Manager:
    manager_employee_id: Optional[str] = None
    manager_name: Optional[str] = None
    manager_email: Optional[str] = None


@dataclass
class Country:
    country_name: Optional[str] = None
    country_digit_code: Optional[str] = None
    country_alpha_code: Optional[str] = None


@dataclass
class EmployeeInfo:
    employee_id: Optional[str] = None
    full_legal_name: Optional[str] = None
    employee_contract_type: Optional[str] = None
    primary_work_email: Optional[str] = None
    manager: Optional[Manager] = None
    primary_work_address: Optional[str] = None
    primary_work_country_address: Optional[Country] = None


@dataclass
class SubsidiaryInfo:
    internal_id: Optional[str] = None
    name: Optional[str] = None



@dataclass
class AccountInfo:
    code: Optional[str] = None
    name: Optional[str] = None
    account_type: Optional[str] = None


@dataclass
class AmountInfo:
    # In Foreign Currency
    debit: Optional[float] = None
    credit: Optional[float] = None
    ledger_debit: Optional[float] = None
    ledger_credit: Optional[float] = None

    currency_symbol: Optional[str] = None
    # 🚨 coming soon , not in test, do not convert
    amount_net_usd: Optional[float] = None


@dataclass
class DocumentInfo:
    document_number: Optional[str] = None
    description: Optional[str] = None


@dataclass
class PaymentMethod:
    payment_term_id: Optional[str] = None
    name: Optional[str] = None
    cut_off_day: Optional[int] = None
    grace_days: Optional[int] = None
    payment_discount_days: Optional[int] = None
    payment_discount_percent: Optional[int] = None


@dataclass
class CostCenterInfo:
    referenceID: Optional[str] = None
    name: Optional[str] = None
    code: Optional[str] = None
    isActive: Optional[bool] = None
    manager: Optional[Manager] = None


@dataclass
class VendorInfo:
    vendor_code: Optional[str] = None
    vendor_ref_id: Optional[str] = None
    company_name: Optional[str] = None

    worktag_only: Optional[bool] = None
    submit: Optional[bool] = None
    disable_change_order: Optional[bool] = None
    acknowledgement_expected: Optional[bool] = None
    enable_global_location_number: Optional[bool] = None
    enable_asn: Optional[bool] = None
    edit_port_taxes: Optional[bool] = None

    approval_status: Optional[str] = None
    supplier_category: Optional[str] = None
    supplier_group_category: Optional[str] = None
    payment_terms_reference: Optional[str] = None
    default_payment_type_reference: Optional[str] = None

    fatca: Optional[int] = None
    irs_1099_supplier: Optional[bool] = None
    invoice_any_supplier: Optional[int] = None
    supplier_minimum_order_amount: Optional[int] = None
    asn_due_in_days: Optional[int] = None


@dataclass
class RegionInfo:
    code: Optional[str] = None
    name: Optional[str] = None


@dataclass(frozen=True, eq=True)
class DealInfo:
    customer_contract_id: Optional[str] = None
    contract_name: Optional[str] = None
    po_number: Optional[str] = None
    on_hold: Optional[bool] = None
    contract_type: Optional[str] = None


@dataclass
class RevenueInfo:
    gtm_org: Optional[GeoSales] = None
    deal: Optional[DealInfo] = None
    revenue_name: Optional[str] = None
    # revenue_org_region: Optional[RegionInfo] = None
    deal_commission_by_deal_code: Optional[float] = None


@dataclass
class MappedEntryJournal:
    ledger_account: Optional[LedgerAccount] = None
    subsidiary_info: Optional[SubsidiaryInfo] = None
    amount_info: Optional[AmountInfo] = None
    cost_center_info: Optional[CostCenterInfo] = None
    revenue_info: Optional[RevenueInfo] = None
    vendor_info: Optional[VendorInfo] = None
    expense_type: Optional[SpendCategory] = None
    # Fields
    project_code: Optional[str] = None
    memo: Optional[str] = None
    cash_flow_code: Optional[str] = None
    customer_id: Optional[str] = None


@dataclass
class MappedJournal:
    account_info: Optional[AccountInfo] = None
    document_info: Optional[DocumentInfo] = None
    book_code_info: Optional[BookCodeInfo] = None
    mapped_entries: Optional[List[MappedEntryJournal]] = None

    journal_id: Optional[str] = None
    pl_info_destination: Optional[str] = None
    accounting_period_name: Optional[str] = None
    # Is Allocation
    journal_source: Optional[str] = None


@dataclass
class ResponseResults:
    total_results: int
    total_pages: int
    page_results: int
    page: int


@dataclass(frozen=True)
class FailedProcessedJournal:
    """ class used to track any error on fetching and converting journals data """
    journal_id: str
    error_message: str
    reason: str
    datetime: str
    data: Optional[Any] = None


###  ORKDAY DATA CLASS

@dataclass
class WORKDAYCurrency:
    wid: Optional[str] = None
    currency_description: Optional[str] = None
    currency_id: Optional[str] = None
    currency_numeric_code: Optional[str] = None

@dataclass
class WorkdayCompanies:
    wid: Optional[str] = None
    organization_reference_id: Optional[str] = None
    company_reference_id: Optional[str] = None
    descriptor: Optional[str] = None

