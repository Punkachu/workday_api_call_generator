# Workday Projects
This project has initially been created to fit into [WORKATO](https://www.workato.com/) `python` actions.
Thus the use of `Built-in` only libraries.
You can easily improve the whole architecture and optimize the program with better external libraries.

## This is the repository made for all the Workday integrations. You will find the code for:
## - **Workday APIs** (documentation [here](https://community.workday.com/sites/default/files/file-hosting/productionapi/versions/v42.2/index.html))


# Workday API :

### 1. You must use `WorkdayConnector` to fetch the `access token` as follow:

```python
from adn_service import WorkdayConnector
workday = 'wd3-impl-services1'
tenant = 'company'  # You can change from cs1 to 4
client_id = 'XXXXXX_client_id_XXXXXX'
client_secret = 'XXXXXX_client_secret_XXXXXX'
refresh_token = 'XXXXXX_refresh_token_XXXXXX'
    
worday_connector = WorkdayConnector(workday, tenant, client_id, client_secret, refresh_token)
# generate the refresh token
worday_connector.acquire_token()
# use it 
token = worday_connector.access_token
```

### 2. Implementing New Endpoints Faster with `ADNService`
To simplify and speed up the process of creating new endpoints, you can leverage the ADNService class. This class provides an abstraction layer designed specifically for interacting with **Workday** endpoints.

#### **Key Features:**
- Endpoint Integration: The class is tailored to handle any Workday endpoint. 
- Basic Methods: It includes core methods to interact with these endpoints, fetch data, and handle pagination seamlessly. 
- CSV Export: Built-in support for exporting data as CSV files.

### How to Implement my own new WD service?:
You must implement **`5`** methods
- `__parse_entity_element(self, entry: ET.Element) -> T` Defines the behaviour to extract data from XML node
- `_update_cache(self, element: T)` Defines how to store entity, must be ID which is representing the object as a key and the whole object as a value.
- `_generate_payload(self, entity_id: str, **kwargs) -> str` Generate the request payload.
- `_generate_payload_pagination(self, next_page: int, **kwargs) -> str` Generate the request payload for pagination.

### How to Use:
You can quickly build new services to connect with the Workday API by extending the `ADNServicez` class. It streamlines the development process, allowing you to focus on the specific endpoint logic.
- Use `get_all_entities` method to fetch all the available entities through **pagination**
- Use `get_entity` method to fetch a specific resource with a given `object_id`
- Use `search_entity` method to fetch a specific resource with a given `object_id` from response large payload.
- Use `generate_csv` to extract fetched entities into an external `CSV`. You can easily define the order and format the data to display with the second arguments `fields: Any` 
which is a List of Tuple , first row is containing the header label and the second row is containing a lambda function specifying which data to display on your behalf.
- Use `get_entity_dic`, for `ADN RAAS` services **only** to extract entities as a dic, jey will be the entity's ID 

You can instantiate any service regarding its constructor. 
- Specify the supported [Version](https://community.workday.com/sites/default/files/file-hosting/productionapi/versions/)
- Use the `entity_entry_data_path` argument from the XML response payload to fetch the right node
- Use the `kwargs` arguments to pass any extra argument that will be fetched by the inner functions `_generate_payload` and `_generate_payload_pagination`
  And thus being able to **forge** any request payload.

### Example:
Get a specific supplier with a given `object_id` and `all` the suppliers from workday using a specific **effective date** and **entry date**.

```python
# Instantiate the service  
companies_service = GetRAASSuppliers(
        base_url=worday_connector.base_uri,
        token=worday_connector.access_token,
        tenant=tenant,
        api_version='v42.1'  # supported version https://community.workday.com/sites/default/files/file-hosting/productionapi/versions/ 
    )

# Get a specific company
supplier = companies_service.get_entity(
        object_id='SUP-691', 
        data_entity_path='.//wd:Supplier_Data',
        # kwargs arguments for specifying request payload
        as_of_effective_date=None, 
        as_of_entry_datetime=None
    )

# Get a specific company from a response payload
supplier = companies_service.search_entity(
        object_id='SUP-691', 
        data_entity_path='.//wd:Supplier_Data',
    )

# Get all companies
suppliers = companies_service.get_all_entities(
        './/wd:Supplier_Data',
        # kwargs arguments for specifying request payload
        as_of_effective_date="2024-09-05", 
        as_of_entry_datetime="2024-09-05"
    )

# Extract fetched data as CSV
companies_service.generate_csv(
        suppliers,  # provide the list of entities 
        [
            ("vendor_ref_id", lambda o: o.vendor_ref_id if o else None),
            ("id", lambda o: o.vendor_code if o else None),
            ("company_name", lambda o: o.company_name if o else None),
            ("approval_status", lambda o: o.approval_status if o else None),
            ("supplier_category", lambda o: o.supplier_category if o else None),
            ("supplier_group_category", lambda o: o.supplier_group_category if o else None),
            ("worktag_only", lambda o: o.worktag_only if o else None),
            ...
        ],
        filename='CSVs/vendors_suppliers'
    )
```

For the ADN RAAS service please refer to `ADNRAASService` parent class.
It requires the workday namespace to work (`wd_ns_value`). you can find it in the second line of the response payload:

Workday Namespace:
```xml
<?xml version='1.0' encoding='UTF-8'?>
<wd:Report_Data xmlns:wd="urn:com.workday.report/XXXX_WD_NS">
.....
```


```python
# Init Service
cost_center_service = GetRAASCostCenter(
        base_url=connector.base_uri,
        token=connector.access_token,
        tenant=tenant,
    )

# Get all the resource as a dic
cost_centers = cost_center_service.get_entity_dic()

# Export as CSV
cost_center_service.generate_csv(
        list(cost_centers.values()),
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
        filename='CSVs/cost_centers'
    )
```


`integration_scope` is the integer that match which scope you want to retrieve, please refer to the GLOBAL env:

```python
ASSET_CATEGORIES = 0
SPEND_CATEGORIES = 1
CUSTOMER_CONTRACT = 2
REGION_CATEGORIES = 3
COMPANIES_CATEGORIES = 4  # aka Suppliers
PAY_METH_CATEGORIES = 5
SUBSIDIARIES_CATEGORIES = 6
BOOK_CODE_CATEGORIES = 7
COST_CENTER_CATEGORIES = 8
LEDGER_ACCOUNT = 9
SITES = 10
EMPLOYEES = 11
ASSETS = 12
GTM_ORG = 13
CURRENCY = 14  # All Currencies fromn the tenant
```

## Implemented Services:

- #### Resource Categories `GetResourceCategories` You can use it to fetch `Spend categories` ([doc](https://community.workday.com/sites/default/files/file-hosting/productionapi/Resource_Management/v42.2/Get_Resource_Categories.html))
- #### Customer contract `GetCustomerContracts` You can use it to fetch `Deals` ([doc](https://community.workday.com/sites/default/files/file-hosting/productionapi/Revenue_Management/v42.2/Get_Customer_Contracts.html#Response))
- #### Suppliers `GetRAASSuppliers` You can use it to fetch `Companies` ([doc](https://community.workday.com/sites/default/files/file-hosting/productionapi/Resource_Management/v42.2/Get_Suppliers.html))
- #### Journals `GetAllJournals` ([doc](https://community.workday.com/sites/default/files/file-hosting/productionapi/Financial_Management/v43.0/Get_Journals.html))
- #### Payment Method `GetPaymentMethod` Payment method type ([doc](https://community.workday.com/sites/default/files/file-hosting/productionapi/Financial_Management/v42.0/Get_Payment_Types.html))


## How to run tests ?

Run the `test_suite.py` under the `tests` folder, it will run all the tests from the `Workato` folder.

