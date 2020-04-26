import sys

from excel_magic import splitter
import xlrd
import os

__all__ = ['Document']

class Document:

    def __init__(self, path: str):
        self.docPath = path

    def split_sheets(self, out: str = '', out_prefix: str = ''):
        splitter.split_sheets(self.docPath, out, out_prefix)

    def split_rows(self, row_count: int, out: str = '', out_prefix: str = ''):
        splitter.split_rows(self.docPath, row_count, out, out_prefix)

    def to_html(self) -> str:
        html = '<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.15.2/xlsx.min.js"></script>\n<table border>\n'

        workbook = xlrd.open_workbook(self.docPath)
        for row in workbook.sheet_by_index(0).get_rows():
            html += '<tr>\n'
            for cell in row:
                html += f'<td>{cell.value}</td>\n'
            html += '</tr>\n'

        html += '</table>'
        return html

    def to_pdf(self, out = 'out.pdf', config = ''):
        if not (os.path.isfile('render-pea') or os.path.isfile('render-pea.exe')):
            raise FileNotFoundError('render-pea plugin is not present')

        if sys.platform.startswith('win'):
            cmd = f'render-pea.exe "{self.docPath}" --out "{out}"'
        else:
            cmd = f'./render-pea "{self.docPath}" --out "{out}"'
        if config != '':
            cmd += f' --config "{config}"'
        print(cmd)
        a = os.popen(cmd)
        print(a)
