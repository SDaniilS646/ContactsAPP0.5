import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import joblib

import sys
from pathlib import Path

this_file_path = Path(__file__).parent
project_path = this_file_path.parent
sys.path.append(str(this_file_path.parent))

from .helpers import printLabel, read_json, long_text, update_json, append_json, delete_from_json, get_values_from_json

from .models import TrainingExample, ModelVersion, ModelFile

import io
import joblib

from django.conf import settings
from django.core.files.base import ContentFile
from django.utils import timezone
from django.core.files.storage import FileSystemStorage

from collections import Counter
from backend.ai.ai_service import AiService

from apps.crm.services.model_services.company_service import CompanyService
from apps.crm.services.model_services.material_service import MaterialService

def find_contact(input_data):
  companies = CompanyService.get_companies()
  company_materials = []
  for company in companies:
    company_materials.append(
      {
        'id': company.id,
        'name': company.name,
        'materials': [material.id for material in company.materials.all()]
      }
    )
  total_materials = MaterialService.get_materials()
  materials = []
  for material in total_materials:
    materials.append(
      {
        'id': material.id,
        'name': material.name,
        'parent': material.parent.name if material.parent else None
      }
    )

  payload = {
    'material_request': input_data['user_request'],
    'candidates': materials, 
    'companies': company_materials
  }
  user_query = json.dumps(payload, ensure_ascii=False)
  system_query = 'Подбери материалы из списка <candidates>, с учетом иерархии материалов <candidates.parent>, который наиболее соответствуют запросу из <material_request>. Ответ предстваь в формате списка словарей <[{"id":material_id, "name":material_name, "parent":material_parent}]>'
  # system_query = 'Подбери материалы из списка <candidates>, с учетом иерархии материалов <candidates.parent>, который наиболее соответствуют запросу из <material_request> и найди компании работающие с этим материалом, сопоставив <candidates.material.id> с <companies.materials>. Ответ предстваь в формате списка словарей <[{"id":company_id, "name":company_name, "material_id":material_id, "material_name":material_name, "parent":material_parent}]>'
  # system_query = 'Подбери компании, из списка <candidates> по <candidates.materials.name>, которым можно направить запрос на материал из <material_request>. Учитывай категорию материала <candidates.materials.parent>. Ответ предоставь в формате списка словарей <[{"id":company_id, "name":company_name, "confidence":<float от 0 до 1>}, {"id":company_id, "name":company_name, "confidence":<float от 0 до 1>}]>. Если подходящая компания не найдена, верни пустой список: []'
  response = AiService.execute_ai_query(user_query=user_query, system_query=system_query)
  print(f'output - {response}')
  temp = [item['id'] for item in json.loads(response)]
  print(f'temp - {temp}')
  response_list = [{'id':item['id'], 'name':item['name']} for item in company_materials if any(mat in temp for mat in item['materials'])]
  print(response_list)
  result = {
    'user_request': input_data['user_request'],
    'promt_template': system_query,
    'output': response_list
  }
  return result


def get_version(model_type):
  active_version = ModelVersion.objects.filter(model_type=model_type, is_active=True).first()
  
  if not active_version:
    active_version = ModelVersion.objects.filter(model_type=model_type).order_by('-version').first()

  return active_version

def create_version(model_type, metrics=None, training_examples_count=0, trained_by=None):
  latest_version = ModelVersion.objects.filter(model_type=model_type).order_by('-version').first()
  new_version_number = (latest_version.version or 0) + 1

  return set_new_version(model_type, new_version_number, metrics, training_examples_count, trained_by)

def set_new_version(model_type, new_version, metrics=None, training_examples_count=0, trained_by=None):
  return ModelVersion.objects.create(
    version = new_version,
    model_type = model_type,
    trained_at = timezone.now(),
    trained_by = trained_by,
    Training_examples_count = training_examples_count,
    metrics = metrics,
    is_active = False,
  )

def set_model_file(latest_version, file, file_path, created_by=None):
  ModelFile.objects.create(
    model_version = latest_version,
    file = file,
    file_path = file_path,
    created_at = timezone.now(),
    created_by = created_by
  )

def work_classifier():

  text_output = ''

  x, y = load_labeled_data()
  text_output = f'\nx size: {len(x)} \ny size: {len(y)}'

  x_train, x_test, y_train, y_test, temp_output = split_dataset(x, y)

  text_output = text_output + f'\n{temp_output}'

  x_train_vec, x_test_vec, vectorizer, temp_output = create_vectorizer(x_train, x_test)

  text_output = text_output + f'\n{temp_output}'

  model = train_model(x_train_vec, y_train)

  training_results, metrics = evaluate_model(model, x_test_vec, y_test, y)
  text_output = text_output + f'\n{training_results}'

  model_name = 'work_classifier'
  model_version = create_version(model_name, metrics, len(x), None)

  current_dir = settings.ML_MODELS_DIR / model_name / f'v{model_version.version}'

  storage = FileSystemStorage(location=str(current_dir))
  
  text_output = text_output + save_model(model, vectorizer, storage)
  set_model_file(model_version, 'vectorizer', f'{model_name}/v{model_version.version}/vectorizer.joblib')
  set_model_file(model_version, 'model', f'{model_name}/v{model_version.version}/model.joblib')


  return text_output

def load_labeled_data():
    
  data = TrainingExample.objects.filter(status__in=['labeled', 'reviewed'])
  works = []

  for work in data:
    if work.text is not None and work.text is not None:
      works.append({
        'name': work.text,
        'category': work.label
      })

  x = [item['name'] for item in works]
  y = [item['category'] for item in works]

  return x, y

def split_dataset(x, y, test_size=0.2, random_state=42):
  
  try:
    x_train, x_test, y_train, y_test = train_test_split(
      x, y,
      test_size=test_size,
      random_state=random_state,
      stratify=y
    )
    split_output_text = "\n✅ Finished with stratification\n"
  except ValueError as e:
    split_output_text = f"\n⚠️ Stratification ERROR: {e}"
    x_train, x_test, y_train, y_test = train_test_split(
      x, y,
      test_size=test_size,
      random_state=random_state
    )
    split_output_text = split_output_text + "\nFinished with no stratification\n"

  split_output_text = split_output_text + f"\nTrain list: {len(x_train)} examples"
  split_output_text = split_output_text + f"\nTest list: {len(x_test)} examples"

  return x_train, x_test, y_train, y_test, split_output_text

def create_vectorizer(x_train, x_test):
  vectorizer = TfidfVectorizer(max_features=1000, lowercase=True, token_pattern=r'(?u)\b\w+\b')

  x_train_vectorized = vectorizer.fit_transform(x_train)
  x_test_vectorized = vectorizer.transform(x_test)
  
  vectorizer_output_text = f"\nx train size: {x_train_vectorized.shape[1]}"

  return x_train_vectorized, x_test_vectorized, vectorizer, vectorizer_output_text

def train_model(x_train_vectorized, y_train):
  model = LogisticRegression(
    max_iter=1000,
    random_state=42,
    C=1.0
  )
  model.fit(x_train_vectorized, y_train)

  return model

def analyze_class_distibution(y, y_test, y_pred):
  overall_counts = Counter(y)
  test_counts = Counter(y_test)
  predicted_counts = Counter(y_pred)

  lines = []
  lines.append('\n----------Распределение категорий---------')

  for label, count in sorted(overall_counts.items(), key=lambda x: x[1]):
    lines.append(f' {label}: {count} examples')

  never_predicted = [
    label for label in overall_counts
    if label in test_counts and predicted_counts.get(label, 0) == 0
  ]

  if never_predicted:
    lines.append('\n⚠️ Категории присутствующие в тесте но ни разу не предсказанные моделью:')
    for label in never_predicted:
      lines.append(
        f'  "{label}" — всего {overall_counts[label]} примеров в выборке, '
        f'{test_counts[label]} из них в тесте. '
        f'Precision для этой категории показан как 0.0 (недостатточно данных для обучения)'
      )
  else:
    lines.append('\n✅ Все категории из теста хотя бы раз предсказаны моделью')

  return '\n'.join(lines)

def evaluate_model(model, x_test_vectorized, y_test, y_full):
  y_pred = model.predict(x_test_vectorized)

  accuracy = accuracy_score(y_test, y_pred)

  report_text = classification_report(y_test, y_pred, zero_division=0)
  report_dict = classification_report(y_test, y_pred, zero_division=0, output_dict=True)

  distribution_report = analyze_class_distibution(y_full, y_test, y_pred)

  output = f'\nModel accuracy: {accuracy:.2%}\n'
  output += '\nDetailed classification report:\n'
  output += report_text
  output += distribution_report

  metrics = {
    'accuracy': accuracy,
    'report': report_dict
  }

  return output, metrics

def save_model(model, vectorizer, storage):
  model_buffer = io.BytesIO()
  joblib.dump(model, model_buffer)
  model_buffer.seek(0)

  vectorizer_buffer = io.BytesIO()
  joblib.dump(vectorizer, vectorizer_buffer)
  vectorizer_buffer.seek(0)

  model_path = storage.save('model.joblib', ContentFile(model_buffer.read()))
  vectorizer_path = storage.save('vectorizer.joblib', ContentFile(vectorizer_buffer.read()))

  temp_ouput = f"\n\nModel saved in {storage.base_location}/{model_path}"
  temp_ouput = temp_ouput + f"\nVectorizer saved in {storage.base_location}/{vectorizer_path}"
  return  temp_ouput

def load_model(model_version, files=[]):

  if len(files) == 0:
    return {}

  storage = FileSystemStorage(location=str(settings.ML_MODELS_DIR))

  output = {}
  for file_type in files:
    model_file = ModelFile.objects.filter(model_version=model_version, file=file_type).first()
    if model_file is None:
      raise ValueError(f'Файл типа "{file_type}" не найден для версии {model_version}')
    with storage.open(model_file.file_path, 'rb') as f:
      output[file_type] = joblib.load(f)
  return output

def predict_category(model, vectorizer, new_texts):
  texts_vectorized = vectorizer.transform(new_texts)
  predictions = model.predict(texts_vectorized)
  probabilities = model.predict_proba(texts_vectorized)

  return predictions, probabilities

def test_model(user_works):
  loaded = load_model(get_version('work_classifier'), ['model', 'vectorizer'])
  model = loaded['model']
  vectorizer = loaded['vectorizer']

  predictions, probabilities = predict_category(model, vectorizer, user_works)
  output = ''
  for example, pred, probs in zip(user_works,predictions, probabilities):
    output += f'\nЗапрос: {example};'
    output += f'\nПредсказание: {pred};'
    output += f'\nВероятность: {max(probs):.2%}'
    output += '\n'
    set_pending_data(example, pred, max(probs))

  return output

def set_pending_data(text, predicted_label=None, probability=None, created_by=None):
  if len(TrainingExample.objects.filter(text=text)) > 0:
    return
  TrainingExample.objects.create(
    text=text,
    predicted_label=predicted_label,
    uncertainity_score=probability,
    status='pending' if probability < 0.9 else 'labeled',
    label=None if probability < 0.9 else predicted_label,
    created_at=timezone.now(),
    created_by=created_by
  )
