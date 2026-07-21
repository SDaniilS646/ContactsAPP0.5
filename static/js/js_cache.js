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