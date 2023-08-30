from openpyxl import Workbook, load_workbook
from os.path import join
from models.enums import Column, ColumnName


# 创建一个模板
class MakeTemplate:
    def __init__(self, name, columns, save_path):
        self.name = name
        self.columns = columns
        self.save_path = save_path


    def make(self):
        with Workbook() as wb:
            ws = wb.active
            ws.append(self.columns)
            wb.save(join(self.save_path, f'{self.name}_template.xlsx'))

class ReadTemplate:
    def read(self, columns, file_path):
        column_len = len(columns)
        with load_workbook(file_path) as wb:
            ws = wb[wb.sheetnames[0]]
            dataList = []
            # 查看ws_Excel的第一列
            first_column =  ws[0]
            if (first_column != columns):
                raise Exception(f'列名不匹配，请检查模板')

            for row in ws.iter_rows(min_row = 2, values_only = True):  # 跳过列名
                data = list(row)
                if len(data) != column_len:
                    raise Exception(f'列数不匹配，请检查模板')
                data.append(data)
            return dataList