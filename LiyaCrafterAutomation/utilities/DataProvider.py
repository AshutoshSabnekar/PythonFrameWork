from configparser import ConfigParser
from excelReader import ExcelUtils

class DataProvider:
    def __init__(self, properties_file='LIYA-Crafter-Test-Details.ini'):
        self.config = ConfigParser()
        self.config.read(properties_file)
        self.excel_reader_cache = {}

    #Returns ExcelReader instance for given file key from properties. Caches instances to avoid reopening multiple times.
    def getExcelReader(self, file_key):
        excel_file = self.config.get('EXCEL DETAILS', file_key)
        if excel_file not in self.excel_reader_cache:
            self.excel_reader_cache[excel_file] = ExcelUtils(excel_file)
        return self.excel_reader_cache[excel_file]

    # Returns list of test data dictionaries read from the Excel sheet.
    def getTestDataList(self, file_key, sheet_key):
        sheet_name = self.config.get('EXCEL DETAILS', sheet_key)
        excel_reader = self.getExcelReader(file_key)
        return excel_reader.read_data(sheet_name)
