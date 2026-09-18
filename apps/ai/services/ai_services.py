from apps.ai.models import AiTask, AiTaskVersion

class AiService:
  @staticmethod
  def get_ai_models():
    tasks = AiTask.objects.all()
    output_list = [{'tech_name':task.name, 'description':task.description, 'id':task.id} for task in tasks]

    return output_list

  @staticmethod
  def get_ai_model(id):
    task = AiTask.objects.filter(id=id).first()
    return task

  @staticmethod
  def get_ai_versions(task):
    versions = AiTaskVersion.objects.filter(task=task)

    return versions

  @staticmethod
  def activate(version_id):
    version = AiTaskVersion.objects.filter(id=version_id)
    AiTaskVersion.objects.filter(task=version.first().task).update(is_active=False)
    version.update(is_active=True)

    return

  @staticmethod
  def get_version_info(version_id):
    fields = AiTaskVersion._meta.get_fields()
    task_version = AiTaskVersion.objects.filter(id=version_id)
    fields_data = []
    for field in fields:
      if field.name in ['created_at', 'updated_at', 'created_by', 'updated_by', 'task', 'id']:
        continue
      if field.name in ['system_prompt', 'notes']:
        if field.name == 'notes' and task_version.values(field.name)[0][field.name] == '':
          continue
        fields_data.append({
          'field_name': field.name,
          'field_value': task_version.values(field.name)[0][field.name],
          'html_start': '<textarea disabled>',
          'html_end': '</textarea>'
        })
        continue
      fields_data.append({
        'field_name': field.name,
        'field_value': task_version.values(field.name)[0][field.name],
        'html_start': '<span>',
        'html_end': '</span>'
      })

    return fields_data