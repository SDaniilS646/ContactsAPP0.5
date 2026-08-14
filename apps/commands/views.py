from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBase
from django.contrib.auth.decorators import login_required, user_passes_test
import json
import shlex

from services.commands_service import Commands

COMMANDS = {
  'help': Commands.HelpCommand,
  'all_users': Commands.getUsers,
  'create_user': Commands.createUser,
  'reset_password': Commands.resetPassword,
  'delete_user': Commands.deleteUser,
  'load_csv': Commands.getalldata,
  'check_con': Commands.checkConnections,
  'models': Commands.getModels,
  'sql': Commands.sqlQuery
}


@login_required
def commands_page(request):
  if not request.user.is_superuser:
    return redirect('/companies/')

  return render(
    request,
    'commands/commands_page.html'
  )

def executeCMD(request):
  if not Commands.checkrole(request.user):
    return JsonResponse({
      'success': False,
      'res': 'Нет доступа'
    }, status=403)

  if request.method != 'POST':
    return JsonResponse({
      'success': False,
      'res': 'Метод не поддерживается'
    }, status=405)
  
  if request.content_type == 'application/json':
    full_cmd = json.loads(request.body)['command']
  else:
    full_cmd = request.POST['command']

  try:
    full_cmd = shlex.split(full_cmd)
  except ValueError as e:
    return JsonResponse({
      'success': False,
      'res': f'Ошибка разбора команды: {e}'
    }, status=400)
  
  if not full_cmd:
    return JsonResponse({
      'success': False,
      'res': 'Пустая команда'
    }, status=400)
  
  cmd = full_cmd[0]
  args = full_cmd[1:]

  handler = COMMANDS.get(cmd)
  if not handler:
    return JsonResponse({
      'success': False,
      'res': f'Неизвестная команда: {cmd}'
    }, status=400)

  try:
    res = handler(args)
  except Exception as e:
    return JsonResponse({
      'success': False,
      'res': f'Ошибка выполнения команнды: {e}'
    }, status=500)


  if isinstance(res, HttpResponseBase):
    return res
  
  return JsonResponse({
    'success': True,
    'res': res
  })