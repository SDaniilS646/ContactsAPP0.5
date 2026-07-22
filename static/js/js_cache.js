const cache = {
  contacts: null,
  materials: null,
  companies: null
}

async function openContacts() {
  if (cache.contacts) {
    drawContacts(cache.contacts)
    return;
  }
  const response = await fetch()

  const data = await response.json()

  cache.contacts = data;

  drawContacts(data)
}

function cachePage(key, container) {
  sessionStorage.setItem(key, container)
}

window.addEventListener('load', () => {
  if (window.location.pathname.split('/').includes('parse_company_page')) {
    const html = sessionStorage.getItem('parse_page')

    if (html) {
      document.getElementById('company-parsing').querySelector('[name=companies]').innerHTML = html;
    }
  }
})