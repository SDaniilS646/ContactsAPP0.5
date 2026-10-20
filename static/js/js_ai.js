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

function exampleTumblerToggle(event, element) {
  if (element.value.trim() === '' ) {
    element.value = true
    element.classList.remove('false')
    element.classList.add('true')
  } else if (element.value === 'false') {
    element.removeAttribute('value')
    element.classList.remove('true')
    element.classList.remove('false')
  } else if (element.value === 'true') {
    element.value = false
    element.classList.remove('true')
    element.classList.add('false')
  }
  
}

async function labelData() {
  const container = document.getElementById("pending-list")

  const items = container.querySelectorAll('[name="pending-list-item"]')
  let labeledData = []

  items.forEach(element => {
    const checks = element.querySelectorAll('[name="example-checkboxes"]')
    checks.forEach(checkbox => {
      const value = checkbox.querySelectorAll('button')[0].value
      const isActive = checkbox.querySelectorAll('input')[0].checked
      temp = {
        id:parseInt(element.id.split('_')[1]),
        value:value,
        is_active:isActive
      }
      labeledData.push(temp)
    })
  })
  if (labeledData.length == 0) {
    return
  }

  const data = await postJson('/ai/label_material/', {labeledData: labeledData})
  if (data.success) {
    reloadModal('categories_active_learning_modal_frame', 'activeLearningCaterories')
  }
}

document.addEventListener('change', async function(event) {
  if (event.target.id !== 'al-categories-selection') {
    return
  }
  const value = event.target.value
  const container = document.getElementById('pending-list')
  const divs = container.querySelectorAll('div')
  divs.forEach(div => {
    if (div.hasAttribute('data-category')) {
      if (div.getAttribute('data-category') === value) {div.classList.remove('is-hidden')}
      else {div.classList.add('is-hidden')}
    }
  })
})


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