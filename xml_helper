from typing import Optional, Type
import xml.etree.ElementTree as ET

from workday.models import T, WorktagsReference


class XMLHelper:

    def __init__(self, ns: Optional[dict[str, str]] = None, raas_ns=None):
        self.ns = ns if ns is not None else {
            'env': 'http://schemas.xmlsoap.org/soap/envelope/',
            'wd': 'urn:com.workday/bsvc'
        }
        self.raas_ns = raas_ns if raas_ns is not None else {
            'wd': 'urn:com.workday.report/Master_Data_-_Ledger_Accounts__MSA_'
        }

    def get_single_tag_line_value(self, entry: ET.Element, tag_name: str, return_type: Optional[Type[T]]):
        """
        Null safely search for a value of a tag name regarding its tag path

        :param entry: Entry element where you want to find the tag's value
        :param tag_name: String representing the path of the tag name, example: 'wd:Supplier_ID'
        :param return_type: The type to which the tag's value should be converted, e.g., int, str, bool
        :return: The tag's value converted to the specified type, or None if the element is not found or conversion fails
        """
        element = entry.find(tag_name, self.ns)
        if element is not None and element.text is not None:
            try:
                return return_type(element.text)
            except (ValueError, TypeError) as e:
                return None  # Return None if conversion fails
        return None

    def get_single_tag_nested_value(self, entry: ET.Element, tag_name: str, nested_tag_name: str,
                                    return_type: Optional[Type[T]]):
        """
        Null safely search for a value of a tag name regarding its tag path

        :param entry: Entry element where you want to find the tag's value
        :param tag_name: String representing the path of the tag name, example: 'wd:Supplier_ID'
        :param nested_tag_name: String representing the nested path of the tag name,
        example: 'wd:ID[@wd:type="Supplier_Category_ID"]'
        :param return_type: The type to which the tag's value should be converted, e.g., int, str, bool
        :return: The tag's value converted to the specified type, or None if the element is not found or conversion fails
        """
        element: Optional[ET.Element] = entry.find(tag_name, self.ns)
        if element is not None:
            text = self.safe_get_text(element, nested_tag_name)
            if text is not None:
                try:
                    return return_type(text)
                except (ValueError, TypeError):
                    return None  # Return None if conversion fails
        return None

    def get_raas_att_path(self, prpty: str):
        return '{' + self.raas_ns.get('wd') + '}' + prpty

    @staticmethod
    def bytes_to_utf8_string(xml_bytes: bytes) -> str:
        """
        Converts bytes XML input to a UTF-8 encoded string.
        """
        return xml_bytes.decode('utf-8')

    def safe_get_text(self, element, path):
        if element is not None:
            found_element = element.find(path, self.ns)
            return found_element.text if found_element is not None else None
        else:
            return None

    def safe_get_float(self, element, path):
        if element is not None:
            text = self.safe_get_text(element, path)
            return float(text) if text else None
        else:
            return None

    def safe_get_int(self, element, path):
        if element is not None:
            text = self.safe_get_text(element, path)
            return int(text) if text else None
        else:
            return None

    def create_worktags_object(self, worktag, wortakObj: WorktagsReference) -> WorktagsReference:
        # acquisition channel dimension usingGTM org
        custom_org_id = self.safe_get_text(worktag, './/wd:ID[@wd:type="Custom_Organization_Reference_ID"]')
        if custom_org_id:
            wortakObj.Custom_Organization_Reference_ID = custom_org_id

        cost_center_id = self.safe_get_text(worktag, './/wd:ID[@wd:type="Cost_Center_Reference_ID"]')
        if cost_center_id:
            wortakObj.Cost_Center_Reference_ID = cost_center_id

        supplier_id = self.safe_get_text(worktag, 'wd:ID[@wd:type="Supplier_ID"]')
        if supplier_id:
            wortakObj.Supplier_ID = supplier_id

        project_id = self.safe_get_text(worktag, 'wd:ID[@wd:type="Project_ID"]')
        if project_id:
            wortakObj.Project_ID = project_id

        spend_cat_id = self.safe_get_text(worktag, 'wd:ID[@wd:type="Spend_Category_ID"]')
        if spend_cat_id:
            wortakObj.Spend_Category_ID = spend_cat_id

        revenue_cat_id = self.safe_get_text(worktag, 'wd:ID[@wd:type="Revenue_Category_ID"]')
        if revenue_cat_id:
            wortakObj.Revenue_Category_ID = revenue_cat_id

        cust_contract_id = self.safe_get_text(worktag, 'wd:ID[@wd:type="Customer_Contract_Reference_ID"]')
        if cust_contract_id:
            wortakObj.Customer_Contract_Reference_ID = cust_contract_id

        # Cash Flow Code
        cash_flow_code = self.safe_get_text(worktag, 'wd:ID[@wd:type="Custom_Worktag_3_ID"]')
        if cash_flow_code:
            wortakObj.cash_flow_code = cash_flow_code

        # Customer ID
        customer_id = self.safe_get_text(worktag, 'wd:ID[@wd:type="Customer_ID"]')
        if customer_id:
            wortakObj.customer_id = customer_id

        return wortakObj
