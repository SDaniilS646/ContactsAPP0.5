def printLabel(text):
  print('\n' +'=' * 60 + f'\n{text}\n' + '=' * 60 + '\n')

def read_json(json_path):
  import json
  with open(json_path, 'r', encoding='UTF-8') as file:
    return json.load(file)

def update_json(data, json_path):
  import json
  with open(json_path, 'w', encoding='UTF-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

def delete_from_json(key_criteria, crit_value, json_path):
  import json
  data = read_json(json_path)

  data = [record for record in data if record.get(key_criteria) != crit_value]

  update_json(data, json_path)

def append_json(new_data, json_path, is_index=False):
  data = read_json(json_path)

  if is_index:
    data_size = len(data)
    data_id = 0
    for i, record in enumerate(data):
      if 'id' in record:
        data_id = record['id'] if record['id'] > data_id else data_id

    new_ind = data_size + 1 if data_size > data_id else data_id + 1
    new_data['id'] = new_ind

  if isinstance(data, list):
    data.append(new_data)
  else:
    data = [data, new_data]
  
  update_json(data, json_path)

def long_text(text, max_size):
  if len(text) >= max_size:
    return f'{text[:max_size]} ...'
  else:
    return text

def get_values_from_json(file_path, item_key, unique=False):
  data = read_json(file_path)
  values = [item[item_key] for item in data]
  if unique:
    values = list(set(values))
  return values



def date_to_filename(input_date):
  file_name = input_date
  file_name = file_name.strftime("%Y-%m-%d")
  file_name = file_name.split("-")
  return f"{file_name[0][2:]}{file_name[1]}{file_name[2]}"