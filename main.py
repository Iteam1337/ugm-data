from datetime import datetime
from json import dumps
from pathlib import Path
from sys import argv

from xlrd import (XL_CELL_DATE, xldate_as_tuple, open_workbook)

def camelcase(string):
    output = ''.join(s for s in string.title() if s.isalnum())
    return output[0].lower() + output[1:]

def get_col_names(sheet):
    row_size = sheet.row_len(0)
    col_values = sheet.row_values(0, 0, row_size)
    column_names = []

    for value in col_values:
        column_names.append(value)

    return column_names

def get_row_data(row, column_names):
    row_data = {}
    counter = 0

    for cell in row:
        if cell.ctype == XL_CELL_DATE:
            row_data[
                camelcase(column_names[counter])
            ] = datetime(* xldate_as_tuple(cell.value, 0)).isoformat()
        else:
            row_data[
                camelcase(column_names[counter])
            ] = cell.value
        counter += 1

    return row_data

def get_sheet_data(sheet, column_names):
    n_rows = sheet.nrows
    sheet_data = []

    for idx in range(1, n_rows):
        row = sheet.row(idx)
        row_data = get_row_data(row, column_names)
        sheet_data.append(row_data)

    return sheet_data

def get_workbook_data(workbook):
    nsheets = workbook.nsheets
    workbookdata = {}

    for idx in range(0, nsheets):
        worksheet = workbook.sheet_by_index(idx)
        column_names = get_col_names(worksheet)
        sheetdata = get_sheet_data(worksheet, column_names)
        workbookdata[
            camelcase(worksheet.name)
        ] = sheetdata

    return workbookdata

def main():

    filename = Path(argv[1] if len(argv) > 1 else r'data/spreadsheet.xlsx')
    out_file = open(filename.with_suffix('.json'), 'w+')
    workbook = open_workbook(filename)
    workbookdata = get_workbook_data(workbook)

    out_file.write(dumps(
        workbookdata,
        indent=2,
        separators=(',', ': '),
        ensure_ascii=False,
    ))

    out_file.close()

    print('wrote to file', filename.with_suffix('.json'))

if __name__ == '__main__':
    main()
