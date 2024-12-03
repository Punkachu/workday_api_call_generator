"""
Generate merged python file from the whole project to fit in Workato python action.
"""

DOUBLE_RETURN_LINES = '\n'


def copy_lines_from_file(source_file, start_line, end_line) -> str:
    """
    Copies content from a specific range of lines in the source file to the destination file.

    :param source_file: Name of the source file.
    :param start_line: Starting line number (inclusive).
    :param end_line: Ending line number (inclusive).
    :return: Content of the copied file
    """
    try:
        copied_content: str = ""
        with open(source_file, 'r') as src:
            for current_line_number, line_content in enumerate(src, start=1):
                if start_line <= current_line_number <= end_line:
                    copied_content += line_content
        return copied_content
    except FileNotFoundError:
        print(f"Error: The file '{source_file}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


def write_content_to_file(content: str, destination_file: str):
    try:
        with open(destination_file, 'w') as dest:
            dest.write(content)
    except Exception as e:
        print(f"An error occurred: {e}")

def load_mandatory_dependencies() -> str:
    import_lines = """from abc import ABC, abstractmethod
import datetime
import csv
import io
from dataclasses import dataclass, field
from typing import TypeVar, Dict, Optional, List, Union, Tuple, Callable, Type, Any
import xml.etree.ElementTree as ET
from functools import wraps

import requests

import time

# TypeVar for generic type T
T = TypeVar('T')

"""
    models_py_path = 'workday/models.py'
    content_models_py = copy_lines_from_file(models_py_path, 7, 400)

    utils_py_path = "workday/utils.py"
    content_utils_py = copy_lines_from_file(utils_py_path, 8, 40)

    csv_helpers_py_path = "workday/csv_helpers.py"
    content_csv_helpers_py = copy_lines_from_file(csv_helpers_py_path, 8, 145)

    xml_helpers_py_path = "workday/xml_helper.py"
    content_xml_helpers_py = copy_lines_from_file(xml_helpers_py_path, 6, 129)

    api_generator_py_path = "workday/workday_api_generator_call.py"
    content_main_macro_py = copy_lines_from_file(api_generator_py_path, 21, 42)
    content_main_wd_classes_py = copy_lines_from_file(api_generator_py_path, 43, 532)

    api_workday_impl_py_path = "workday/workday_implement_api.py"
    content_api_workday_py = copy_lines_from_file(api_workday_impl_py_path, 7, 909)

    api_raas_impl_py_path = "workday/workday_raas_implementation_api.py"
    content_api_raas_py = copy_lines_from_file(api_raas_impl_py_path, 8, 426)

    return f"""{import_lines}
    {content_main_macro_py}
    {DOUBLE_RETURN_LINES}
    {content_models_py}
    {DOUBLE_RETURN_LINES}
    {content_utils_py}
    {DOUBLE_RETURN_LINES}
    {content_csv_helpers_py}
    {DOUBLE_RETURN_LINES}
    {content_xml_helpers_py}
    {DOUBLE_RETURN_LINES}
    {content_main_wd_classes_py}
    {DOUBLE_RETURN_LINES}
    {content_api_workday_py}
    {DOUBLE_RETURN_LINES}
    {content_api_raas_py}
    {DOUBLE_RETURN_LINES}
    """


def generate_file():
    mandatory_dep = load_mandatory_dependencies()

    journ_gen_py_path = "workday_accounting_journal_generator.py"
    content_journal_gen = copy_lines_from_file(journ_gen_py_path, 8, 108)

    content = f"{mandatory_dep}\n{content_journal_gen}"
    write_content_to_file(content, "workato_journal_script.py")

    raas_gen_py_path = "workday_all_report_generator.py"
    content_raas_gen = copy_lines_from_file(raas_gen_py_path, 5, 428)
    content = f"{mandatory_dep}\n{content_raas_gen}"
    write_content_to_file(content, "workato_raas_script.py")


if __name__ == '__main__':
    generate_file()




