async function activateModel(comboboxId) {
  const combobox = document.getElementById(comboboxId)
  if (!combobox) {return}
  const value = combobox.value
  const data =  await postJson('/ai/activate_version/', {id:value})
}

async function post_create_model_version(task_id) {
  const form = document.getElementById('aiversion-creation')

  const model_name = form.querySelectorAll('[name="model_name"]')[0].value
  const temperature = form.querySelectorAll('[name="temperature"]')[0].value
  const max_tokens = form.querySelectorAll('[name="max_tokens"]')[0].value
  const system_prompt = form.querySelectorAll('[name="system_prompt"]')[0].value
  const notes = form.querySelectorAll('[name="notes"]')[0].value

  if (model_name.trim() === '') {alertFrame('nigga'); return}

  const data = await postJson('/ai/create_version/', {
    task_id:task_id,
    model_name:model_name,
    temperature:temperature,
    max_tokens:max_tokens,
    system_prompt:system_prompt,
    notes:notes
  })

  if (data.success) {removeAllModels(); return}
}


document.addEventListener('change', async function(event) {
  if (event.target.id !== 'model-version-select') {
    return
  }
  const value = event.target.value
  const infoContainer = document.getElementById('model-version-information')
  const data = await postJson('/ai/version_info/', {id:value})
  if (!data.success) {return}
  const output = data.output
  html = ''
  output.forEach(element => {
      html += `<div class="model-version-item"><span>${element['field_name']}:</span>${element['html_start']}${element['field_value']}${element['html_end']}</div>`
  });

  infoContainer.innerHTML = html
})