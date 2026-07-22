let selectedMaterials = []
let selectedContacts = []
let selectedEmployees = []

function openModal(modal_frame_id) {
  document.getElementById(modal_frame_id).style.display = 'flex'
}

function closeModal(modal_frame_id) {
  document.getElementById(modal_frame_id).style.display = 'none'
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
  query_id = `[id="${id}"]`
  prev_parent_id = parent_id_input_element.value == '' ? null : `[id="${parent_id_input_element.value}"]` 

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

function updateList(fetch_link, container, style=null, is_meeting=null) {
  if (style) {
    fetch_link = fetch_link + `/?style=${style}&`+ `is_meeting=${is_meeting}`
  }
  fetch(fetch_link)
  .then(response => response.text())
  .then(html => {
    container.innerHTML = html;
  })
}

function selectContacts(event, element, container_id=null, input_box_id=null) {
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

function pgReload() {
  window.location.reload();
}

function sortList(event, query_el='div.card') {

  new_val = event.target.value

  elems = document.querySelectorAll(query_el)
  console.log(elems)
  ordered_array = []

  switch (new_val) {
    case 'A-z':
      elems.forEach(val => {
        ordered_array.push(val.querySelector('[name="name"]').textContent)
      })
      console.log(ordered_array)
      ordered_array.sort((a, b) => a.toLowerCase().localeCompare(b.toLowerCase()))
      console.log(ordered_array)

      elems.forEach(val => {
        ind = ordered_array.indexOf(val.querySelector('[name="name"]').textContent)
        val.style.setProperty('order', ind.toString())
      })
      break;
    case 'Z-a':
      elems.forEach(val => {
        ordered_array.push(val.querySelector('[name="name"]').textContent)
      })

      ordered_array.sort((a, b) => a.toLowerCase().localeCompare(b.toLowerCase()))
      ordered_array.reverse()

      elems.forEach(val => {
        ind = ordered_array.indexOf(val.querySelector('[name="name"]').textContent)
        val.style.setProperty('order', ind.toString())
      })
      break;
    case 'date':
      elems.forEach(val => {
        ordered_array.push(val.querySelector('[name="date"]').textContent)
      })
      ordered_array.sort((a, b) => new Date(a) - new Date(b))
      ordered_array.reverse()
      elems.forEach(val => {
        ind = ordered_array.indexOf(val.querySelector('[name="date"]').textContent)
        val.style.setProperty('order', ind.toString())
      })
      break;
    case '-date':
      elems.forEach(val => {
        ordered_array.push(val.querySelector('[name="date"]').textContent)
      })
      ordered_array.sort((a, b) => new Date(a) - new Date(b))
      
      elems.forEach(val => {
        ind = ordered_array.indexOf(val.querySelector('[name="date"]').textContent)
        val.style.setProperty('order', ind.toString())
      })
      break;
    case '':
      elems.forEach(val => {
        ordered_array.push(Number(val.querySelector('[name="id"]').textContent))
      })
      ordered_array.sort()
      elems.forEach(val => {
        ind = ordered_array.indexOf(Number(val.querySelector('[name="id"]').textContent))
        val.style.setProperty('order', ind.toString())
      })
      break;
  }
}

function executeCMD() {
  

  main_cont = document.getElementById("commands-block")

  cmd = main_cont.querySelector('input').value
  if (cmd == '') {return}
  if (cmd == 'clear') {main_cont.querySelector('textarea').value = ''; main_cont.querySelector('input').value = ''; return}
  
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

  if (cmd == 'load_csv') {
    const form = document.createElement('form')

    form.method = 'POST'
    form.action = '/commands/executeCMD/'

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

    document.body.removeChild(form)

    result = 'loaded archive'
    output = main_cont.querySelector('textarea')
    output_val = output.value
    output.value = output_val == '' ? result : output_val + '\n\n' + result
    main_cont.querySelector('input').value = ''
    return
  }

  
  
  fetch('/commands/executeCMD/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      command: cmd
    })
  })
  .then(response => response.json())
  .then(data => {
      result = data.res
      output = main_cont.querySelector('textarea')
      output_val = output.value
      output.value = output_val == '' ? result : output_val + '\n\n' + result
      main_cont.querySelector('input').value = ''
  })
}


document.addEventListener(
  'input',

  function(event) {
    let input_box = event.target.id;

    switch (input_box) {
      case 'companies-list':
        filter_pg_list(event, '.card')
        break;
      case 'employees-list-search':
        filter_pg_list(event, '.card')
        break;
      case 'employees-list-on-create':
        console.log('nigga')
        filter_pg_list(event, '.employee-list-item')
        break;
      case 'contacts-list-on-comp-edit':
        filter_pg_list(event, '.contact-list-item')
        break
      case 'contacts-list-search':
        filter_pg_list(event, '.card')
        break;
    }

    function filter_pg_list(event, selector_class) {
      input_text = event.target.value.toLowerCase()
      
      document.querySelectorAll(selector_class)
      .forEach(el => {
        const text = el.textContent.toLowerCase();

        //querySelector('.inn').

        el.style.display = text.includes(input_text) ? '' : 'none';
      })
    }
  }
)

window.onload = function() {
  cur_url_path = new URL(window.location.href).pathname

  menu_cont = document.getElementById('menu-btns')

  menu_cont.querySelectorAll('a').forEach(val => {if (val.getAttribute('href') == cur_url_path) {val.querySelector('button').classList.add('active')}})
}
