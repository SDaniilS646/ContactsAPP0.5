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

from .models import TrainingExample

import io
import joblib

from django.conf import settings
from django.core.files.base import ContentFile

from django.core.files.storage import FileSystemStorage

from collections import Counter

def work_classifier():

  text_output = ''

  x, y = load_labeled_data()
  text_output = f'\nx size: {len(x)} \ny size: {len(y)}'

  x_train, x_test, y_train, y_test, temp_output = split_dataset(x, y)

  text_output = text_output + f'\n{temp_output}'

  x_train_vec, x_test_vec, vectorizer, temp_output = create_vectorizer(x_train, x_test)

  text_output = text_output + f'\n{temp_output}'

  model = train_model(x_train_vec, y_train)

  training_results = evaluate_model(model, x_test_vec, y_test, y)
  text_output = text_output + f'\n{training_results}'

  storage = FileSystemStorage(location=str(settings.ML_MODELS_DIR))
  
  text_output = text_output + save_model(model, vectorizer, storage)

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

  distribution_report = analyze_class_distibution(y_full, y_test, y_pred)

  output = f'\nModel accuracy: {accuracy:.2%}\n'
  output += '\nDetailed classification report:\n'
  output += report_text
  output += distribution_report

  return output

def save_model(model, vectorizer, storage):
  model_buffer = io.BytesIO()
  joblib.dump(model, model_buffer)
  model_buffer.seek(0)

  vectorizer_buffer = io.BytesIO()
  joblib.dump(vectorizer, vectorizer_buffer)
  vectorizer_buffer.seek(0)

  model_path = storage.save('model.joblib', ContentFile(model_buffer.read()))
  vectorizer_path = storage.save('vector.joblib', ContentFile(vectorizer_buffer.read()))

  temp_ouput = f"\n\nModel saved in {model_path}"
  temp_ouput = temp_ouput + f"\nVectorizer saved in {vectorizer_path}"
  return  temp_ouput


def load_model(model_path='model.joblib', vectorizer_path='vectorizer.joblib'):
  model = joblib.load(model_path)
  vectorizer = joblib.load(vectorizer_path)
  return model, vectorizer

def predict_category(model, vectorizer, new_texts):
  texts_vectorized = vectorizer.transform(new_texts)
  predictions = model.predict(texts_vectorized)
  probabilities = model.predict_proba(texts_vectorized)

  return predictions, probabilities

def test_model(user_work, need_return=False):
  printLabel("TESTING...")
  new_examples = user_work

  loaded_model, loaded_vectorizer = load_model(project_path / 'data' / 'models' / 'model.joblib', project_path / 'data' / 'vectors' / 'vectorizer.joblib')

  predictions, probabilities = predict_category(loaded_model, loaded_vectorizer, new_examples)

  pending_path = project_path / 'data' / 'pending.json'

  for i, (text, pred, probs) in enumerate(zip(new_examples, predictions, probabilities)):
    # print(f"Example {i+1}:")
    print(f"Text: {long_text(text, 100)}")
    print(f"Predicted category: {pred}")

    print(f"Probability: {max(probs):.2%}")

    # classes = loaded_model.classes_
    # top_3_idx = np.argsort(probs)[-3:][::-1]
    # print("Top-3:")
    # for idx in top_3_idx:
    #   print(f"  - {classes[idx]}: {probs[idx]:.2%}")
    
    if max(probs) < 0.5:
      pending_works = get_values_from_json(pending_path, 'name')

      if text in pending_works:
        print("⚠️ Already pending")
      else:
        pending_data = {
          'id': 0,
          'name': text,
          'predicted category': pred,
          'probability': f"{max(probs):.2%}",
          'status': 'need labeling'
        }
        append_json(pending_data, pending_path, True)
    if need_return:
      return pred


def save_results_in_json():

  json_path = project_path / 'data' / 'pending.json'
  append_json({"name": "test"}, json_path, True)

