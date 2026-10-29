// const { createElement } = require("react")

async function getCategory() {
  const container = document.getElementById("excel-upload-block")
  const input = document.getElementById("work-name-input")

  const label = document.getElementById("category")


  const data = await postJson('/sender/categorize/', {input: input.value})

  if (data.success) {
    label.textContent = data.output
  }
} 

// async function testInnerHtml(event, element) {
//   const cont = document.getElementById('sender-main-frame')
//   let inpValue
  
//   element.parentElement.querySelectorAll('input').forEach(inp => inpValue =inp.value)
//   const button = createElement('button')
//   button.textContent = inpValue
//   cont.appendChild(button)
// }

// ШАГ 1. ЗАГРЗУКА ФАЙЛА ВОР
async function uploadVor() {
  const fileInput = document.getElementById('vor-file-input')
  if (!AppState.csrfToken) {
    throw new Error('CSRF token not initialized')
  }
  formData.append('csrfmiddlewaretoken', AppState.csrfToken)

  const files = fileInput.files
  const formData = new FormData()
  
  for (const file of files) {
    formData.append('files', file)
  }

  postFormData('/sender/load_vor/', formData)
}

async function postFormData(url, formData) {
  if (!AppState.csrfToken) {
    throw new Error('CSRF token not initialized')
  }

  if (!url) {
    throw new Error('postJson: url required')
  }

  let response 
  try {
    response = await fetch(url, {
      method: 'POST',
      headers: {
        'X-CSRFToken': AppState.csrfToken,
        // 'Content-Type': 'application/json'
      },
      body: formData,
    })
  } catch (networkError) {
    throw new Error(`Network error while requesting ${url}: ${networkError.message}`)
  }

  if (!response.ok) {
    const errorBody = await response.json().catch(() => null)
    const message = errorBody?.error || errorBody?.message || `HTTP ${response.status}: ${response.statusText}`
    throw new Error(message)
  }

  return response
}

// ШАГ 2. ПОИСК РАЗЗДЕЛОВ, ПРОВЕРКА  ФАЙЛА, ПОДБОР ФОРМАТА, ВЫВОД ИНФОРМАЦИИ

// ШАГ 3. ВЫБОР РАЗДЕЛОВ ДЛЯ ОБРАБОТКИ

// ШАГ 4. ПРЕДПРОСМОТР

// ШАГ 5. КОНТАКТЫ

// ШАГ 6. РАССЫЛКА

function deleteLabeledData(id) {
  const container = document.getElementById("pending-list")
  const items = container.querySelectorAll('div')
}

