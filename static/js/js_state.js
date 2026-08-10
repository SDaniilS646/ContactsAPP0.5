const AppState = {
  currentPage: null,
  activeModal: [],
  csrfToken: null
}

function initAppState() {
  const tokenInput = document.querySelector('[name=csrfmiddlewaretoken]')

  if (!tokenInput) {
    console.log('CSRF element not found')
    return
  }
  AppState.csrfToken = tokenInput.value
}

document.addEventListener('DOMContentLoaded', initAppState)