"""Module """
import re
import json

from datetime import datetime, timezone
from freezegun import freeze_time
from uc3m_consulting.enterprise_project import EnterpriseProject
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.enterprise_manager_config import (PROJECTS_STORE_FILE,
                                                       TEST_DOCUMENTS_STORE_FILE,
                                                       TEST_NUMDOCS_STORE_FILE)
from uc3m_consulting.project_document import ProjectDocument

class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    @staticmethod
    def validate_cif(cif: str):
        """validates a cif number """
        if not isinstance(cif, str):
            raise EnterpriseManagementException("CIF code must be a string")
        cif_patrón = re.compile(r"^[ABCDEFGHJKNPQRSUVW]\d{7}[0-9A-J]$")
        if not cif_patrón.fullmatch(cif):
            raise EnterpriseManagementException("Invalid CIF format")

        cif_letra_inicial = cif[0]
        cif_intermedio = cif[1:8]
        cif_control = cif[8]

        cif_sum_impar = 0
        cif_sum_par = 0

        for i in range(len(cif_intermedio)):
            if i % 2 == 0:
                x = int(cif_intermedio[i]) * 2
                if x > 9:
                    cif_sum_impar = cif_sum_impar + (x // 10) + (x % 10)
                else:
                    cif_sum_impar = cif_sum_impar + x
            else:
                cif_sum_par = cif_sum_par + int(cif_intermedio[i])

        cif_suma_total = cif_sum_impar + cif_sum_par
        cif_resta = cif_suma_total % 10
        cif_resta_control = 10 - cif_resta

        if cif_resta_control == 10:
            cif_resta_control = 0

        cif_diccionario = "JABCDEFGHI"

        if cif_letra_inicial in ('A', 'B', 'E', 'H'):
            if str(cif_resta_control) != cif_control:
                raise EnterpriseManagementException("Invalid CIF character control number")
        elif cif_letra_inicial in ('P', 'Q', 'S', 'K'):
            if cif_diccionario[cif_resta_control] != cif_control:
                raise EnterpriseManagementException("Invalid CIF character control letter")
        else:
            raise EnterpriseManagementException("CIF type not supported")
        return True

    def validate_starting_date(self, fecha):
        """validates the  date format  using regex"""
        fecha_patrón = re.compile(r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$")
        fecha_valida = fecha_patrón.fullmatch(fecha)
        if not fecha_valida:
            raise EnterpriseManagementException("Invalid date format")

        try:
            my_date = datetime.strptime(fecha, "%d/%m/%Y").date()
        except ValueError as ex:
            raise EnterpriseManagementException("Invalid date format") from ex

        if my_date < datetime.now(timezone.utc).date():
            raise EnterpriseManagementException("Project's date must be today or later.")

        if my_date.year < 2025 or my_date.year > 2050:
            raise EnterpriseManagementException("Invalid date format")
        return fecha
    #pylint: disable=too-many-arguments, too-many-positional-arguments
    def register_project(self,
                         company_cif: str,
                         project_acronym: str,
                         project_description: str,
                         department: str,
                         date: str,
                         budget: str):
        """registers a new project"""
        self.validate_cif(company_cif)
        proy_acro_patrón = re.compile(r"^[a-zA-Z0-9]{5,10}")
        proy_acro_valida = proy_acro_patrón.fullmatch(project_acronym)
        if not proy_acro_valida:
            raise EnterpriseManagementException("Invalid acronym")
        proy_desc_patrón = re.compile(r"^.{10,30}$")
        proy_desc_valida = proy_desc_patrón.fullmatch(project_description)
        if not proy_desc_valida:
            raise EnterpriseManagementException("Invalid description format")

        proy_dept = re.compile(r"(HR|FINANCE|LEGAL|LOGISTICS)")
        proy_dept_valida = proy_dept.fullmatch(department)
        if not proy_dept_valida:
            raise EnterpriseManagementException("Invalid department")

        self.validate_starting_date(date)

        try:
            bdgt_as_float  = float(budget)
        except ValueError as exc:
            raise EnterpriseManagementException("Invalid budget amount") from exc

        bdgt_as_str = str(bdgt_as_float)
        if '.' in bdgt_as_str:
            decimales = len(bdgt_as_str.split('.')[1])
            if decimales > 2:
                raise EnterpriseManagementException("Invalid budget amount")

        if bdgt_as_float < 50000 or bdgt_as_float > 1000000:
            raise EnterpriseManagementException("Invalid budget amount")


        new_project = EnterpriseProject(company_cif=company_cif,
                                        project_acronym=project_acronym,
                                        project_description=project_description,
                                        department=department,
                                        starting_date=date,
                                        project_budget=budget)

        try:
            with open(PROJECTS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                proy_list = json.load(file)
        except FileNotFoundError:
            proy_list = []
        except json.JSONDecodeError as ex:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from ex

        for proy_existente in proy_list:
            if proy_existente == new_project.to_json():
                raise EnterpriseManagementException("Duplicated project in projects list")

        proy_list.append(new_project.to_json())

        try:
            with open(PROJECTS_STORE_FILE, "w", encoding="utf-8", newline="") as file:
                json.dump(proy_list, file, indent=2)
        except FileNotFoundError as ex:
            raise EnterpriseManagementException("Wrong file  or file path") from ex
        except json.JSONDecodeError as ex:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return new_project.project_id


    def find_docs(self, date_str):
        """
        Generates a JSON report counting valid documents for a specific date.

        Checks cryptographic hashes and timestamps to ensure historical data integrity.
        Saves the output to 'resultado.json'.

        Args:
            date_str (str): date to query.

        Returns:
            number of documents found if report is successfully generated and saved.

        Raises:
            EnterpriseManagementException: On invalid date, file IO errors,
                missing data, or cryptographic integrity failure.
        """
        fecha_patrón = re.compile(r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$")
        fecha_valida = fecha_patrón.fullmatch(date_str)
        if not fecha_valida:
            raise EnterpriseManagementException("Invalid date format")

        try:
            my_date = datetime.strptime(date_str, "%d/%m/%Y").date()
        except ValueError as ex:
            raise EnterpriseManagementException("Invalid date format") from ex


        # open documents
        try:
            with open(TEST_DOCUMENTS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                doc_list = json.load(file)
        except FileNotFoundError as ex:
            raise EnterpriseManagementException("Wrong file  or file path") from ex


        doc_valida_counter = 0

        # loop to find
        for el in doc_list:
            time_val = el["register_date"]

            # string conversion for easy match
            doc_date_str = datetime.fromtimestamp(time_val).strftime("%d/%m/%Y")

            if doc_date_str == date_str:
                d_obj = datetime.fromtimestamp(time_val, tz=timezone.utc)
                with freeze_time(d_obj):
                    # check the project id (thanks to freezetime)
                    # if project_id are different then the data has been
                    #manipulated
                    p = ProjectDocument(el["project_id"], el["file_name"])
                    if p.document_signature == el["document_signature"]:
                        doc_valida_counter = doc_valida_counter + 1
                    else:
                        raise EnterpriseManagementException("Inconsistent document signature")

        if doc_valida_counter == 0:
            raise EnterpriseManagementException("No documents found")
        # prepare json text
        now_str = datetime.now(timezone.utc).timestamp()
        s = {"Querydate":  date_str,
             "ReportDate": now_str,
             "Numfiles": doc_valida_counter
             }

        try:
            with open(TEST_NUMDOCS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                dl = json.load(file)
        except FileNotFoundError:
            dl = []
        except json.JSONDecodeError as ex:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from ex
        dl.append(s)
        try:
            with open(TEST_NUMDOCS_STORE_FILE, "w", encoding="utf-8", newline="") as file:
                json.dump(dl, file, indent=2)
        except FileNotFoundError as ex:
            raise EnterpriseManagementException("Wrong file  or file path") from ex
        return doc_valida_counter
