# -*- coding: utf-8 -*

import sys
from pathlib import Path

this_file_path = Path(__file__).parent
project_path = this_file_path.parent
sys.path.append(str(this_file_path.parent))

from work_classifier import full_model_update

from ....apps.sender.helpers import printLabel, read_json, long_text, update_json, append_json, delete_from_json, get_values_from_json

from collections import Counter
from datetime import datetime



def start_pending():
  pending_path = project_path / 'data' / 'pending.json'
  labeled_path = project_path / 'data' / 'labeled_data' / 'labeled_works.json'

  printLabel("✅ FILES FOUND. DATA ANALYSIS")

  labeled_categories = get_values_from_json(labeled_path, 'category')
  print(f"Examples for each category count:\n")
  for val in Counter(labeled_categories).items():
    print(f"{val[0]} - {val[1]}")

  labeled_categories = list(set(labeled_categories))
  print(f"\nCategories count: {len(labeled_categories)}")

  labeled_works = get_values_from_json(labeled_path, 'name')
  print(f"\nLabeled works count: {len(labeled_works)}")

  pending_works = get_values_from_json(pending_path, 'name')
  if len(pending_works) <= 0:
    print("\n⚠️ No works in need of labeling")
    return
  
  print(f"\nWorks in need of labeling count: {len(pending_works)}")

  start_choice = input(f"\nWanna start labeleing? y/n\n")
  if start_choice == 'y':
    pending_data = read_json(pending_path)
    for i, item in enumerate(pending_data):
      labeled_works = get_values_from_json(labeled_path, 'name')
      print("=" * 60)
      print(f"{i + 1}. Work name: {item['name']}")
      print(f"Predicted category: {item['predicted category']}")
      print(f"Probability: {item['probability']}")
      print()

      if item['name'] in labeled_works:
        print("\n⚠️ Work already labeled\n")
        print("[code stub] Добавить вывод категории и возможность редактирования❗❗❗")
        
        delete_from_json('id', item['id'], pending_path)
        continue

      print(f"❗ Choose category. Enter number from list or new text value if there is no category needed.")
      for i, cat in enumerate(labeled_categories):
        print(f"{i + 1} - {cat}")
      print(f"{len(labeled_categories) + 1} - Predicted category")
      print(f"{len(labeled_categories) + 2} - pass")
      print(f"0 - to stop labeling")
      label_choice = input()

      try:
        label_choice = int(label_choice)
        if label_choice == 0:
          printLabel("Finished")
          break
          
        elif label_choice == len(labeled_categories) + 1:
          print(f"\n{item['predicted category']}\n")
          labeled_work = {
            'name': item['name'],
            'category': item['predicted category'],
            'keywords': [],
            'added_by': 'active_learning',
            'added_at': str(datetime.now())
          }
          append_json(labeled_work, labeled_path)
          delete_from_json('id', item['id'], pending_path)
          print(f"\n✅ WORK LABELED\n")
        
        elif label_choice == len(labeled_categories) + 2:
          print("Left this work unlabeled")
          continue

        elif label_choice > len(labeled_categories) + 2:
          printLabel("❌ Error")
          return
          
        else:
          print(f"\n{labeled_categories[label_choice - 1]}\n")
          labeled_work = {
            'name': item['name'],
            'category': labeled_categories[label_choice - 1],
            'keywords': [],
            'added_by': 'active_learning',
            'added_at': str(datetime.now())
          }
          append_json(labeled_work, labeled_path)
          delete_from_json('id', item['id'], pending_path)
          print(f"\n✅ WORK LABELED\n")
          
      except:
        print(f"\nNew category: {label_choice}\n")
        labeled_work = {
            'name': item['name'],
            'category': label_choice,
            'keywords': [],
            'added_by': 'active_learning',
            'added_at': str(datetime.now())
          }
        append_json(labeled_work, labeled_path)
        delete_from_json('id', item['id'], pending_path)
        print(f"\n✅ WORK LABELED\n")

    printLabel("✅ Labeling finished")

    update_model = input("Wanna updatee (retrain) model? y/n\n")
    if update_model == 'y':
      full_model_update()
      printLabel("✅ Model Retrained")
    else:
      printLabel("Finished")
  else:
    printLabel("Finished")

  

if __name__ == "__main__":
  start_pending()