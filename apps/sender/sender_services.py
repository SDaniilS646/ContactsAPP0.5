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


def work_classifier():
  printLabel("Step 1: Loading labeled data")
  x, y = load_labeled_data(project_path / 'data' / 'labeled_data' / 'labeled_works.json')

  printLabel("Step 2: Splitting Data")
  x_train, x_test, y_train, y_test = split_dataset(x, y)

  return

def load_labeled_data(label_data_path):
    
  data = TrainingExample.objects.all()
  works = []

  for work in data:
    if work.status == 'labeled':
      works.append({
        'name': work.text,
        'category': work.label
      })

  x = [item['name'] for item in works]
  y = [item['category'] for item in works]

  return x, y

def create_vectorizer(x_train, x_test):
  vectorizer = TfidfVectorizer(max_features=1000, lowercase=True, token_pattern=r'(?u)\b\w+\b')

  x_train_vectorized = vectorizer.fit_transform(x_train)
  x_test_vectorized = vectorizer.transform(x_test)
  
  print(f"Size: {x_train_vectorized.shape[1]}")

  return x_train_vectorized, x_test_vectorized, vectorizer

def split_dataset(x, y, test_size=0.2, random_state=42):
  
  try:
    x_train, x_test, y_train, y_test = train_test_split(
      x, y,
      test_size=test_size,
      random_state=random_state,
      stratify=y
    )
    print("\n✅ Finished with stratification\n")
  except ValueError as e:
    print(f"⚠️ Stratification ERROR: {e}")
    x_train, x_test, y_train, y_test = train_test_split(
      x, y,
      test_size=test_size,
      random_state=random_state
    )
    print("\nFinished with no stratification\n")

  print(f"Train list: {len(x_train)} examples")
  print(f"Test list: {len(x_test)} examples")

  return x_train, x_test, y_train, y_test

def train_model(x_train_vectorized, y_train):
  model = LogisticRegression(
    max_iter=1000,
    random_state=42,
    C=1.0
  )

  print("Starting training...")
  model.fit(x_train_vectorized, y_train)
  print("✅ Training finished")

  return model

def evaluate_model(model, x_test_vectorized, y_test):
  y_pred = model.predict(x_test_vectorized)

  accuracy = accuracy_score(y_test, y_pred)
  print(f"\nModel Accuracy: {accuracy:.2%}")

  printLabel("Detailed classification report:")
  print(classification_report(y_test, y_pred))

  return y_pred

def save_model(model, vectorizer, model_path='model.joblib', vectorizer_path='vectorizer.joblib'):
  joblib.dump(model, model_path)
  joblib.dump(vectorizer, vectorizer_path)
  print(f"Model saved in {model_path}")
  print(f"Vectorizer saved in {vectorizer_path}")
  return

def load_model(model_path='model.joblib', vectorizer_path='vectorizer.joblib'):
  model = joblib.load(model_path)
  vectorizer = joblib.load(vectorizer_path)
  return model, vectorizer

def predict_category(model, vectorizer, new_texts):
  texts_vectorized = vectorizer.transform(new_texts)
  predictions = model.predict(texts_vectorized)
  probabilities = model.predict_proba(texts_vectorized)

  return predictions, probabilities

def full_model_update():
  printLabel("Step 1: Loading labeled data")
  x, y = load_labeled_data(project_path / 'data' / 'labeled_data' / 'labeled_works.json')

  printLabel("Step 2: Splitting Data")
  x_train, x_test, y_train, y_test = split_dataset(x, y)

  printLabel("Step 3: Vectorizing Texts")
  x_train_vec, x_test_vec, vectorizer = create_vectorizer(x_train, x_test)

  printLabel("Step 4: Training Model")
  model = train_model(x_train_vec, y_train)

  printLabel("Step 5: Model quality analysis")
  evaluate_model(model, x_test_vec, y_test)

  printLabel("Step 6: Saving")
  save_model(model, vectorizer, project_path / 'data' / 'models' / 'model.joblib', project_path / 'data' / 'vectors' / 'vectorizer.joblib')

  printLabel("MODEL UPDATED")  


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



if __name__ == '__main__':
  run_model_update = input("Wanna update model? y/n\n")
  if run_model_update == 'y':
    full_model_update()

  run_test = input("Wanna test model? y/n\n")
  while run_test == 'y':
    
    request = input("Enter work name:\n")
    test_model([request])

    run_test = input("Run new test? y/n\n")
  
  print('finished')

  # save_results_in_json()