import openpyxl

def read_test_data(file_path, sheet_name=None):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook[sheet_name] if sheet_name else workbook.active

    data = []
    headers = [cell.value for cell in sheet[1]]

    for row in sheet.iter_rows(min_row=2, values_only=True):
        row_data = dict(zip(headers, row))
        data.append(row_data)

    return data