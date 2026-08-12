from openpyxl import load_workbook
from openpyxl.utils.cell import range_boundaries
from shutil import copyfile
from io import BytesIO

from pathlib import Path

import gc

TEMPLATE_PATH = Path(__file__).parent / 'sender_template.xlsm'

def create_sendfile(output_data=None):
  if not output_data:
    return None

  # ====================================================
  # ЧТЕНИЕ ШАБЛОНА
  # ====================================================

  # this_file_path = Path(__file__).parent
  # template = this_file_path / 'sender_template.xlsm'
  # xl_output = this_file_path / 'new_file.xlsm'
  # copyfile(template, xl_output)

  with open(TEMPLATE_PATH, 'rb') as f:
    template_bytes = f.read()

  # ====================================================
  # ОТКРЫТИЕ ФАЙЛА, ПОДГОТОВКА ПЕРЕМЕННЫХ И ОБЪЕКТОВ
  # ====================================================

  buffer = BytesIO(template_bytes)
  wb = load_workbook(buffer, keep_vba=True)
  ws = wb["Рассылка"]

  lo = ws.tables

  table = lo["Рассылка"]
  table_adr = table.ref

  min_col, min_row, max_col, max_row = range_boundaries(table_adr)

  # ====================================================
  # СОХРАНЕНИЕ СТИЛЕЙ СТРОКИ
  # ====================================================

  row_style = {}

  for col in range(min_col, max_col + 1):
    row_style[col] = ws.cell(min_row + 1, col)._style

  # ====================================================
  # ПРОСТАВЛЕНИЕ ЗАЧЕНИЙ
  # ====================================================

  start_row = min_row + 1

  for i, row_values in enumerate(output_data):
    current_row = start_row + i
    for col_idx, value in enumerate(row_values, start=min_col):
      cell = ws.cell(current_row, col_idx)
      cell.value = value
      cell._style = row_style.get(col_idx, row_style[min_col])

    # # ЗНАЧЕНИЯ
    # ws.cell(i, 2).value = "ТЕСТ"

    # ПРОТЯГИВАНИЕ ТАБЛИЦЫ
    # table.ref = f"A1:N{ws.max_row}"
  table.ref = (
    f"{ws.cell(min_row, min_col).coordinate}:"
    f"{ws.cell(ws.max_row, max_col).coordinate}"
  )

    # # ПРОСТАВЛЕНИЕ СТИЛЕЙ В СТРОКЕ
    # for col in range(min_col, max_col + 1):
    #   ws.cell(i, col)._style = row_style[col]

  # ====================================================
  # СОХРАНЕНИЕ И ЗАКРЫТИЕ ФАЙЛА
  # ====================================================

  output_buffer = BytesIO()
  wb.save(output_buffer)
  wb.close()
  # gc.collect()
  output_buffer.seek(0)

  return output_buffer
