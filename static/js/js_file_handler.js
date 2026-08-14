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

async function checkFileLoaded() {
  const fileInput = document.getElementById('excel-file-input')
  const files = fileInput.files
  const formData = new FormData()
  formData.append('csrfmiddlewaretoken', AppState.csrfToken)
  for (const file of files) {
    formData.append('files', file)
  }
  postFormData('/sender/send_file/', formData)
}

async function loadFile(inputId=null) {
  const fileInput = document.getElementById(inputId)
  
  if (!AppState.csrfToken) {
    throw new Error('CSRF token not initialized')
  }
  formData.append('csrfmiddlewaretoken', AppState.csrfToken)

  const files = fileInput.files
  const formData = new FormData()
  
  for (const file of files) {
    formData.append('files', file)
  }

  postFormData('/sender/send_file/', formData)
}