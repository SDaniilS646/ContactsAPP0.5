let selectedMaterials = []
let selectedContacts = []
let selectedEmployees = []
let selectedCompanies = []

let currentZIndex = 1000;

function lockMenu() {
  const menuContainer = document.getElementById('menu-btns')
  const menuBtns = menuContainer.querySelectorAll('button')
  menuBtns.forEach(btn => console.log(btn))

  lockButtons(menuBtns)
}

function unlockMenu() {
  const menuContainer = document.getElementById('menu-btns')
  const menuBtns = menuContainer.querySelectorAll('button')
  menuBtns.forEach(btn => console.log(btn))

  unlockButtons(menuBtns)
}

function lockButtons(btns) {
  for (const button of btns) {
    button.disabled = true
  }
}

function unlockButtons(btns) {
  for (const button of btns) {
    button.disabled = false
  }
}

function removeAllModals() {
  const modal_cont = document.getElementById('modals-content')
  if (modal_cont) {
    modal_cont.innerHTML = '';
    AppState.activeModal = []
  }
}

function showModalFrame(modalFrame) {
  modalFrame.style.zIndex = ++currentZIndex
  modalFrame.style.display = 'flex'
}

function trackActiveModal(modalFrameId, modalName, id) {
  AppState.activeModal.push({
      modal_frame_id: modalFrameId,
      modal_name: modalName,
      id: id
    })
}

const pendingModals = new Set()

async function fetchModalHtml(modalName, id) {
  const csrftoken = getCsrfToken()

  const response = await fetch('/modal/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      modal_name:modalName, id
    })
  })
  
  if (!response.ok) {
    throw new Error(`Server responsed with ${response.status}`)
  }
  const data = await response.json()
  return data.html
}

function getCsrfToken() {
  const tokenInput = document.querySelector('[name=csrfmiddlewaretoken]')
  if (!tokenInput) {
    throw new Error('CSRF token not found on page')
  }
  return tokenInput.value
}

async function openModal(modal_frame_id, modal_name=null, id=null) {

  const modal_cont = document.getElementById('modals-content')
  const existingFrame = document.getElementById(modal_frame_id)

  if (existingFrame) {
    showModalFrame(existingFrame)
    trackActiveModal(modal_frame_id, modal_name, id)
    return
  }

  if (pendingModals.has(modal_frame_id)) {
    return
  }
  pendingModals.add(modal_frame_id)

  try {
    const html = await fetchModalHtml(modal_name, id)
    const modalContainer = document.getElementById('modals-content')

    if (!modalContainer) {
      console.error('Modal container not found')
      return
    }

    modalContainer.insertAdjacentHTML('beforeend', html)

    const modalFrame = document.getElementById(modal_frame_id)

    if (modalFrame) {
      showModalFrame(modalFrame)
      trackActiveModal(modal_frame_id, modal_name, id)
    }
  } catch(error) {
    console.error(`Failed to open modal "${modal_name}":`, error)
  } finally {
    pendingModals.delete(modal_frame_id)
  }
}

function clearActiveModal(modalFrameId) {
  AppState.activeModal = AppState.activeModal.filter(
    (modal) => modal.modal_frame_id !== modalFrameId
  )
}

function closeModal(modal_frame_id) {
  const modal_frame = document.getElementById(modal_frame_id)
  if (modal_frame) {
    modal_frame.style.display = 'none';
    clearActiveModal(modal_frame_id)
  }
}

function removeModal(modal_frame_id) {
  const modal_frame = document.getElementById(modal_frame_id)
  if (modal_frame) {
    modal_frame.remove();
    clearActiveModal(modal_frame_id)
  }
}

function reloadModal(modal_frame_id, modal_name, id=null) {
  
  const modal_frame = document.getElementById(modal_frame_id)
  if(modal_frame == null) {return}
  removeModal(modal_frame_id)
  openModal(modal_frame_id, modal_name, id)
}


function selectMaterials(event, element, container_id=null, input_box_id=null) {

  const container = document.getElementById(container_id)

  if (element.classList.contains('selected')) {
    element.classList.remove('selected')
  } else {
    element.classList.add('selected')
  }
}

function saveMaterialsList() {

  const container = document.getElementById('list_material_tree')

  let elements = container.querySelectorAll('span')
  selectedMaterials = []

  elements.forEach(val => {
    if (val.classList.contains('selected')) {
      console.log(val)
      let mat_id = val.getAttribute('id')
      selectedMaterials.push(mat_id)
    }
  })

  closeModal('choose_material_modal_frame')
}

function selectParent(event, element, container_id='create_material_modal_frame') {

  const container = document.getElementById(container_id)
  checkOtherSelected(container)

  const parent_id_input_element = container.querySelector('[name="parent_id"]')

  let id = element.getAttribute('id')
  let query_id = `[id="${id}"]`
  let prev_parent_id = parent_id_input_element.value == '' ? null : `[id="${parent_id_input_element.value}"]` 

  if (parent_id_input_element.value == id) {
    container.querySelector(query_id).classList.remove('selected')
    parent_id_input_element.value = ''
  } else {
    if (prev_parent_id) {
      container.querySelector(prev_parent_id).classList.remove('selected')
    }
    
    container.querySelector(query_id).classList.add('selected')
    parent_id_input_element.value = id
  }
}

function checkOtherSelected(container) {
  let elements = container.querySelectorAll('span')
  
  elements.forEach(val => val.classList.remove('selected'))
}

// function updateList(fetch_link, container, style=null, is_meeting=null) {
//   if (style) {
//     fetch_link = fetch_link + `/?style=${style}&`+ `is_meeting=${is_meeting}`
//   }
//   fetch(fetch_link)
//   .then(response => response.text())
//   .then(html => {
//     container.innerHTML = html;
//   })
// }

function selectContacts(event, element, container_id=null, input_box_id=null) {
  const container = document.getElementById(container_id)

  if (element.classList.contains('selected')) {
    element.classList.remove('selected')
  } else {
    element.classList.add('selected')
  }
}

function selectCompanies(event, element, container_id=null) {
  const container = document.getElementById(container_id)

  if (element.classList.contains('selected')) {
    element.classList.remove('selected')
  } else {
    element.classList.add('selected')
  }
}

function selectEmployees(event, element, container_id=null, input_box_id=null) {
  const container = document.getElementById(container_id)

  if (element.classList.contains('selected')) {
    element.classList.remove('selected')
  } else {
    element.classList.add('selected')
  }
}

function saveContactsList() {

  const container = document.getElementById('contacts-list')

  let elements = container.querySelectorAll('div')

  selectedContacts = []

  elements.forEach(val => {
    if (val.classList.contains('selected')) {
      let cont_id = val.getAttribute('id')
      let inp_group = container.querySelector(`[id="${val['id']}"]`)
      let corp_mail = inp_group.querySelector('[name=corp-mail]') ? inp_group.querySelector('[name=corp-mail]').value : null
      let corp_phone = inp_group.querySelector('[name=corp-phone]') ? inp_group.querySelector('[name=corp-phone]').value : null
      let position = inp_group.querySelector('[name=position]') ? inp_group.querySelector('[name=position]').value : null

      selectedContacts.push({
        'id': cont_id,
        'corp-mail':corp_mail == '' ? null : corp_mail,
        'corp-phone':corp_phone == '' ? null : corp_phone,
        'position':position == '' ? null : position
      })
    }
  }) 
  closeModal('choose_contact_modal_frame')
}

function saveCompaniesList() {

  const container = document.getElementById('companies-list')
  let elements = container.querySelectorAll('div')

  selectedCompanies = []

  elements.forEach(val => {
    if (val.classList.contains('selected')) {
      
      let company_id = val.getAttribute('id')
      
      selectedCompanies.push({
        'id': company_id
      })
    }
  })
  closeModal('choose_company_modal_frame')
}

function saveEmployeesList() {

  const container = document.getElementById('employees-list')

  let elements = container.querySelectorAll('div')

  selectedEmployees = []

  elements.forEach(val => {
    if (val.classList.contains('selected')) {
      let emp_id = val.getAttribute('id')
      let inp_group = container.querySelector(`[id="${val['id']}"]`)

      selectedEmployees.push({
        'id': emp_id
      })
    }
  }) 
  closeModal('choose_employee_modal_frame')
}

function applySortOrder(elems, getValue, compareFn) {
  const indexed = Array.from(elems).map((el, i) => ({
    el, 
    value: getValue(el), 
    i
  }))
  indexed.sort((a, b) => compareFn(a.value, b.value))
  indexed.forEach((item, order) => {item.el.style.setProperty('order', order.toString())})
}

function sortList(event, query_el='div.card') {

  const newOrderValue = event.target.value

  const elems = document.querySelectorAll(query_el)
  let ordered_array = []

  const sortConfigs = {
    'A-z': {
      field: 'name',
      compare: (a, b) => a.toLowerCase().localeCompare(b.toLowerCase())
    },
    'Z-a': {
      field: 'name',
      compare: (a, b) => b.toLowerCase().localeCompare(a.toLowerCase())
    },
    'date': {
      field: 'date',
      compare: (a, b) => new Date(b) - new Date(a)
    },
    '-date': {
      field: 'date',
      compare: (a, b) => new Date(a) - new Date(b)
    },
    '':{
      field: 'id',
      compare: (a, b) => Number(a) - Number(b),
      isNumeric: true
    }
  }

  const config = sortConfigs[newOrderValue]
  if (!config) {return}

  applySortOrder(
    elems, 
    (el) => el.querySelector(`[name="${config.field}"]`).textContent, 
    config.compare
  )
}

async function executeCMD() {
  
  const mainContainer = document.getElementById("commands-block")
  const cmdInput = mainContainer.querySelector('input')

  const cmd = cmdInput.value
  if (cmd == '') {return}
  if (cmd == 'clear') {mainContainer.querySelector('textarea').value = ''; cmdInput.value = ''; return}
  
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

  if (cmd == 'load_csv') {

    // const iframe = document.createElement('iframe')
    // iframe.style.display = 'none'
    // document.body.appendChild(iframe)

    const form = document.createElement('form')
    form.method = 'POST'
    form.action = '/commands/executeCMD/'
    // form.target = iframe.name = 'hidden_download_frame_' + Date.now() 

    const csrf = document.createElement('input')
    csrf.type = 'hidden'
    csrf.name = 'csrfmiddlewaretoken'
    csrf.value = csrftoken

    const command = document.createElement('input')
    command.type = 'hidden'
    command.name = 'command'
    command.value = cmd

    form.appendChild(csrf)
    form.appendChild(command)
    document.body.appendChild(form)
    form.submit()

    setTimeout(() => {
      document.body.removeChild(form)
      // document.body.removeChild(iframe)
    }, 5000)

    const result = 'loaded archive'
    const output = mainContainer.querySelector('textarea')
    const outputValue = output.value
    output.value = outputValue == '' ? result : outputValue + '\n\n' + result
    cmdInput.value = ''
    return
  }

  const output = mainContainer.querySelector('textarea')
  try {
    const data = await postJson('/commands/executeCMD/', {command: cmd})
    const result = data.res
    output.value += output.value == '' ? result : '\n\n' + result
    cmdInput.value = ''
  } catch (error) {
    output.value += output.value == '' ? error.message : '\n\n' + error.message
  }
}

function setPage(type, table, id=null) {

  const outer = document.getElementById("outer")
  if (outer) {outer.classList.remove('show')}

  csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

  fetch('/open_page/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      type: type,
      table: table,
      id: id
    })
  })
  .then(response => response.json())
  .then(data => { 
      if (!data.success) {return}
      AppState.currentPage = `${type}-${table}`
      const menu_cont = document.getElementById('menu-btns')
      menu_cont.querySelectorAll('button').forEach(val => {
        if (val.getAttribute('id') == AppState.currentPage) {
          val.classList.add('active')
          val.setAttribute('disabled', '')
        } else {
          val.removeAttribute('disabled')
          val.classList.remove('active')
        }
      })

      

      document.getElementById('content').innerHTML = data.html
      
      const outer = document.getElementById("outer")

      setTimeout(() => {
        if (outer) {outer.classList.add('show')}
      }, 10);

      if (type == 'page') {
        removeAllModals()
        menu_cont.querySelectorAll('.sub-menu-btns').forEach(val => {
          if (val.getAttribute('name') == `${table}-menu-btns`) {
            val.removeAttribute('disabled')
            val.classList.remove('hidden')
          } else {
            if (!val.classList.contains('hidden')) {
              val.setAttribute('disabled', '')
              val.classList.add('hidden')
            }
          }
        })
      } 
    }
  )
}

const FILTER_TARGETS = {
  'companies-list': '.card',
  'companies-list':'.card',
  'contacts-list-search': '.card',
  'employees-list-on-create': '.employee-list-item',
  'contacts-list-on-comp-edit': '.contact-list-item',
  'companies-list-search': '.company-list-item'
}

function filterPageList(event, selector_class) {
  const inputText = event.target.value.toLowerCase()
  
  document.querySelectorAll(selector_class)
  .forEach(el => {
    const text = el.textContent.toLowerCase();
    const isMatch = text.includes(inputText)
    el.classList.toggle('is-hidden', !isMatch)
  })
}

function debounce(fn,  delay) {
  let timeoutId
  return function(...args) {
    clearTimeout(timeoutId)
    timeoutId = setTimeout(() => fn.apply(this, args), delay)
  }
}

const debouncedFilter = debounce((event, selectorClass) => {
  filterPageList(event, selectorClass)
}, 200)

document.addEventListener(
  'input',

  function(event) {
    let input_box = event.target.id;
    const selectorClass = FILTER_TARGETS[event.target.id]
    if (selectorClass) {
      debouncedFilter(event, selectorClass)
    }
  }
)
