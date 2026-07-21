from django.shortcuts import render, redirect
from django.http import JsonResponse
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
  'load_csv': Commands.getalldata
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
      'success': True,
      'res': 'Нет доступа'
    })
  full_cmd = json.loads(request.body)['command']
  full_cmd = shlex.split(full_cmd)
  cmd = full_cmd[0]
  args = full_cmd[1:]
  if COMMANDS.get(cmd):
    res = COMMANDS.get(cmd)(args)
  else:
    res = 'unknown'

  return JsonResponse({
    'success': True,
    'res': res
  })