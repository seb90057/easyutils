from sdeutils.file.csv_file import CsvFile
import os
import pkg_resources


path = pkg_resources.resource_filename(__name__, "../../data/test_csv.csv")

path = os.path.abspath(path)
csv_file = CsvFile(path)
