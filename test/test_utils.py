import csv
from typing import Type, Dict, Optional, Any, List, TypeVar
from dataclasses import dataclass, fields, is_dataclass

T = TypeVar('T')


class TestCSVHelper:

    @classmethod
    def __dataclass_from_dict(
            cls,
            klass,
            d: Dict[str, Any],
            field_mapping: Optional[Dict[str, str]] = None,
            headers: Optional[List[str]] = None
    ) -> T:
        """

        :param klass: Class Object to deserialize
        :param d: Dict to deserialize from
        :param field_mapping: mapping between the appearing order of the object field and CSV headers
        :param headers: Header field of the CSV
        :return: Serialized object T
        """
        fieldtypes = {f.name: f.type for f in fields(klass)}

        if field_mapping is None and headers is None:
            # Map as an identical dict representation of the object [klass]
            return klass(**d)

        if field_mapping and headers:
            # custom csv from dict klass representation
            # Get class fields in order of declaration
            class_fields = [f.name for f in fields(klass)]
            # Automatically generate the field_mapping by pairing class fields with CSV headers
            field_mapping = {class_field: csv_header for class_field, csv_header in zip(class_fields, headers)}

            # Create an object using the mapped fields
            return klass(**{
                f: cls.__dataclass_from_dict(fieldtypes[f], d[field_mapping[f]], field_mapping, headers)
                if is_dataclass(fieldtypes[f]) else d[field_mapping[f]]
                for f in fieldtypes if field_mapping[f] in d
            })

        raise ValueError('Parameters are not valid, please provide either all arguments or only class and data')

    def csv_to_object_dict(
            self,
            path: str,
            id_field: str,
            object_type: Type[T],
            field_mapping: Optional[Dict[str, str]] = None
    ) -> Dict[str, T]:
        """
        Load a CSV , and simulate ADNService and return a dict of id: Object
        :param path:
        :param id_field: field to be the value of the ID
        :param object_type: Type Object T
        :param field_mapping: In case the csv headers does not match the object T field name , provide this dict
        :return: Dict of id and object,
        e.g: {'Computers_equipment': SpendCategory(asset_class_id='Computers_equipment', asset_class_name='Asset Class')}
        """
        result = {}

        # Open and read the CSV file
        with open(path, mode='r') as csvfile:
            reader = csv.DictReader(csvfile)

            # For each row, create an object and populate the dictionary
            for row in reader:
                field_value_id = row[id_field]
                # Deserializing the row into the given object type
                if field_mapping is not None:
                    headers = reader.fieldnames
                    obj = self.__dataclass_from_dict(object_type, row, field_mapping, headers)
                else:
                    obj = self.__dataclass_from_dict(object_type, row)
                result[field_value_id] = obj

        return result


"""
    Example:
"""
if __name__ == "__main__":
    @dataclass(frozen=True, eq=True)
    class SpendCategory:
        asset_class_id: Optional[str] = None
        asset_class_name: Optional[str] = None


    @dataclass(frozen=True, eq=True)
    class SpendCategory2:
        code: Optional[str] = None
        name: Optional[str] = None

    field_mapping = {
        "code": "asset_class_id",  # CSV field -> Object field mapping
        "name": "asset_class_name"
    }
    csv_helper = TestCSVHelper()

    result1 = csv_helper.csv_to_object_dict('../generated_csv/asset_categories.csv', 'asset_class_id', SpendCategory2, field_mapping)
    result2 = csv_helper.csv_to_object_dict('../generated_csv/asset_categories.csv', 'asset_class_id', SpendCategory, None)

    print(result1)
    print(result2)
