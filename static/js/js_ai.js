async function activateModel(comboboxId) {
  const combobox = document.getElementById(comboboxId)
  if (!combobox) {return}
  const value = combobox.value
  const data =  await postJson('/ai/activate_version/', {id:value})
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