function post_create_meeting() {
  const container = document.getElementById('company-creation')
  subject = container.querySelector('[name="subject"]')
  if (subject.value == '') {
    container.querySelector('[name="subject-label"]').textContent = "УКАЖИТЕ ТЕМУ ВСТРЕЧИ"
    container.querySelector('[name="subject-label"]').style.color = 'red'
    return
  }

  csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

  fetch('/meetings/add_meet/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        subject: subject.value,
        comment: container.querySelector('[name="comment"]').value,
        record_link: container.querySelector('[name="record-link"]').value,
        meeting_date: container.querySelector('[name="meeting-date"]').value == '' ? null : container.querySelector('[name="meeting-date"]').value,
        meeting_contacts: selectedContacts,
        meeting_employees: selectedEmployees
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      alert('✅ Встреча добавлена!')
      pgReload()
    }
  })
}

function start_parsing() {
  const container = document.getElementById('company-parsing')

  const parse_btn = container.querySelector('[name="start-parsing-btn"]')
  parse_btn.inert = true;
  parse_btn.style.backgroundColor = "grey"
  div = document.querySelector('[name=companies]')
  div.innerHTML = ''

  csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

  fetch('/companies/parse_company/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        request_txt: container.querySelector('[name="request_txt"]').value
    })
  })
  .then(response => response.json())
  .then(data => {
    parse_btn.inert = false;
    parse_btn.style.backgroundColor = "white"
    if (data.success) {
      
      data.results.forEach((url_val, url_idx) => {
        url_container = document.createElement('div')


        span = document.createElement('span');
        span.textContent = url_val['url'];
        div.appendChild(span);
        
        url_val['mail'].forEach((val, idx) => {

          span = document.createElement('span')
          span.setAttribute('hidden', '')
          span.textContent = url_val['url']
          
          form_container = document.createElement('div')
          form_container.setAttribute('class', 'form_container')
          checkbox = document.createElement('input');
          checkbox.type = 'checkbox';
          checkbox.value = val; 
          checkbox.name = `${url_idx} - ${idx}`;

          label = document.createElement('label');
          
          label.textContent = val;
          label.setAttribute('for', `${url_idx} - ${idx}`)
          

          label.appendChild(checkbox)

          form_container.appendChild(label)
          form_container.appendChild(span);
          url_container.appendChild(form_container);
          
          // div.appendChild(checkbox);
        })
        div.appendChild(url_container)
      })
    }
    else {
      div = document.querySelector('[name=companies]')

      span = document.createElement('span');
      span.textContent = 'Ничего не найдено (возможно лимит)';
      div.appendChild(span);

      div.appendChild(document.createElement('hr'))

      if (data.err_txt) {
        span = document.createElement('span');
        span.textContent = data.err_txt;
        div.appendChild(span);
      }
    }
  })
}

async function post_create_parse_company() {

  const container = document.getElementById('company-parsing')
  added_comps = 0
  new_comps = []

  csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
  checkboxes = null
  checkboxes = container.querySelectorAll('input[type="checkbox"]:checked');

  if (checkboxes.length == 0) {
    return
  }
  for (const checkbox of checkboxes) {
    console.log(checkbox.parentElement.parentElement.querySelector('span').textContent)
    const response = await fetch('/companies/add_comp/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
          company_name: checkbox.parentElement.parentElement.querySelector('span').textContent,
          inn: '',
          site: checkbox.parentElement.parentElement.querySelector('span').textContent,
          rating: 0,
          mail: checkbox.value,
          phone: '',
          comment: '',
          company_contacts: [],
          company_materials: []
      })
    })

    const data = await response.json()

    if (data.success) {
      added_comps++
      new_comps.push({
        'comp_name':data.comp_name,
        'comp_id':data.comp_id
      })
    }
  }
  
  div = container.querySelector('[name=companies]')
  div.innerHTML = ''
  span = document.createElement('span');
  if (added_comps > 0) {
    span.textContent = `Добавлено ${added_comps} компаний`;
    div.appendChild(span);
    for (const new_comp of new_comps) {
      a = document.createElement('a');
      a.textContent = new_comp['comp_name'];
      a.setAttribute('href', `/companies/${new_comp['comp_id']}/`);
      div.appendChild(a);
    }
  } else {
    span.textContent = 'Компании не добавлены, скорее всего они уже есть в базе';
    div.appendChild(span);
  }
  cachePage('parse_page', div.innerHTML)
}

function post_create_company() {
  const container = document.getElementById('company-creation')
  comp_name = container.querySelector('[name="company_name"]')
  if (comp_name.value == '') {
    //company_name_label
    container.querySelector('[name="company_name_label"]').textContent = "УКАЖИТЕ НАЗВАНИЕ КОМПАНИИ"
    container.querySelector('[name="company_name_label"]').style.color = 'red'
    return
  }

  rating = container.querySelector('[name="rating"]').value
  rating = rating >= 5 ? 5 : rating
  rating = rating < 0 ? 0 : rating

  csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value


  fetch('/companies/add_comp/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        company_name: comp_name.value,
        inn: container.querySelector('[name="inn"]').value,
        site: container.querySelector('[name="site"]').value,
        rating: rating,
        mail: container.querySelector('[name="mail"]').value,
        phone: container.querySelector('[name="phone"]').value,
        comment: container.querySelector('[name="comment"]').value,
        company_contacts: selectedContacts,
        company_materials: selectedMaterials
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      setPage('page', 'companies')
    } else {
      if (data.result == 'Exists') {
        container.querySelector('[name="company_name_label"]').textContent = "Компания с таким названием или почтой уже существует"
      }
    }
  })
}

function post_company_edit() {
  const container = document.getElementById('edit_company_modal_frame') 
  comp_name = container.querySelector('[name="company_name"]')
  if (comp_name.value == '') {
    //company_name_label
    container.querySelector('[name="company_name_label"]').textContent = "УКАЖИТЕ НАЗВАНИЕ КОМПАНИИ"
    container.querySelector('[name="company_name_label"]').style.color = 'red'
    return
  }

  csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

  rating = container.querySelector('[name="rating"]').value
  rating = rating >= 5 ? 5 : rating
  rating = rating < 0 ? 0 : rating

  const comp_id = container.querySelector('[name="id"]').value

  fetch('/companies/edit_cont/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        id: comp_id,
        company_name: comp_name.value,
        inn: container.querySelector('[name="inn"]').value,
        site: container.querySelector('[name="site"]').value,
        rating: rating,
        mail: container.querySelector('[name="mail"]').value,
        phone: container.querySelector('[name="phone"]').value,
        comment: container.querySelector('[name="comment"]').value
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      setPage('details', 'companies', comp_id)
      removeModal('edit_company_modal_frame')
    }
  })
}

async function post_contact_create(comp_id=null) {
  const container = document.getElementById('create_contact_modal_frame') 
  cont_first_name = container.querySelector('[name="first_name"]')
  cont_last_name = container.querySelector('[name="last_name"]')
  if (cont_first_name.value == '' && cont_last_name.value == '') {
    if (cont_first_name.value == '') {
      container.querySelector('[name="first_name_label"]').textContent = "ВВЕДИТЕ ИМЯ"
    }
    if (cont_last_name.value == '') {
      container.querySelector('[name="last_name_label"]').textContent = "ВВЕДИТЕ ФАМИЛИЮ"
    }
    return
  }
  // style = document.getElementById('contacts-list').classList[1]

  csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

  await fetch('/contacts/add_cont/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        first_name: cont_first_name.value,
        last_name: cont_last_name.value,
        patronymic: container.querySelector('[name="patronymic"]').value,
        phone: container.querySelector('[name="phone"]').value,
        mail: container.querySelector('[name="mail"]').value,
        comment: container.querySelector('[name="comment"]').value
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      removeModal('create_contact_modal_frame')
      reloadModal('choose_contact_modal_frame', 'chooseContact', comp_id)
    }
  })
  
}

function post_contact_edit() {
  const container = document.getElementById('edit_contact_modal_frame') 
  cont_first_name = container.querySelector('[name="first_name"]')
  cont_last_name = container.querySelector('[name="last_name"]')
  if (cont_first_name.value == '' && cont_last_name.value == '') {
    if (cont_first_name.value == '') {
      container.querySelector('[name="first_name_label"]').textContent = "ВВЕДИТЕ ИМЯ"
    }
    if (cont_last_name.value == '') {
      container.querySelector('[name="last_name_label"]').textContent = "ВВЕДИТЕ ФАМИЛИЮ"
    }
    return
  }

  csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

  fetch('/contacts/edit_cont/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        id: container.querySelector('[name="id"]').value,
        first_name: cont_first_name.value,
        last_name: cont_last_name.value,
        patronymic: container.querySelector('[name="patronymic"]').value,
        phone: container.querySelector('[name="phone"]').value,
        mail: container.querySelector('[name="mail"]').value,
        comment: container.querySelector('[name="comment"]').value
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      pgReload()
    }
  })
}

function post_employee_create() {
  const container = document.getElementById('create_employee_modal_frame')
  emp_first_name = container.querySelector('[name="first_name"]')
  emp_last_name = container.querySelector('[name="last_name"]')
  if (emp_first_name.value == '' && emp_last_name.value == '') {
    if (emp_first_name.value == '') {
      container.querySelector('[name="first_name_label"]').textContent = "ВВЕДИТЕ ИМЯ"
    }
    if (emp_last_name.value == '') {
      container.querySelector('[name="last_name_label"]').textContent = "ВВЕДИТЕ ФАМИЛИЮ"
    }
    return
  }

  style = document.getElementById('employees-list').classList[1]

  csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

  fetch('/employees/add_emp/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        first_name: emp_first_name.value,
        last_name: emp_last_name.value,
        patronymic: container.querySelector('[name="patronymic"]').value,
        phone: container.querySelector('[name="phone"]').value,
        mail: container.querySelector('[name="mail"]').value
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      updateList('/employees/employees_list', document.getElementById('employees-list'), style)
      closeModal('create_employee_modal_frame')
    }
  })
}

function post_employee_edit() {
  const container = document.getElementById('edit_employee_modal_frame') 
  emp_first_name = container.querySelector('[name="first_name"]')
  emp_last_name = container.querySelector('[name="last_name"]')
  if (emp_first_name.value == '' && emp_last_name.value == '') {
    if (emp_first_name.value == '') {
      container.querySelector('[name="first_name_label"]').textContent = "ВВЕДИТЕ ИМЯ"
    }
    if (emp_last_name.value == '') {
      container.querySelector('[name="last_name_label"]').textContent = "ВВЕДИТЕ ФАМИЛИЮ"
    }
    return
  }

  csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

  fetch('/employees/edit_emp/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        id: container.querySelector('[name="id"]').value,
        first_name: emp_first_name.value,
        last_name: emp_last_name.value,
        patronymic: container.querySelector('[name="patronymic"]').value,
        phone: container.querySelector('[name="phone"]').value,
        mail: container.querySelector('[name="mail"]').value
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      pgReload()
    }
  })
}

async function post_material_create(comp_id) {
  const container = document.getElementById('create_material_modal_frame')
  mat_name = container.querySelector('[name="material_name"]')
  if (mat_name.value == '') {
    container.querySelector('[name="material_name_label"]').value = "ВВЕДИТЕ НАИМЕНОВАНИЕ"
    container.querySelector('[name="material_name_label"]').style.color = 'red'
    return
  }
  style = document.getElementById('list_material_tree').classList[1]

  csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

  await fetch('/materials/add_mat/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        material_name: mat_name.value,
        keywords: container.querySelector('[name="keywords"]').value,
        parent_id: container.querySelector('[name="parent_id"]').value == '' ? null : container.querySelector('[name="parent_id"]').value
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      removeModal('create_material_modal_frame')
      reloadModal('choose_material_modal_frame', 'chooseMaterial', comp_id)
    }
  })
}

function post_material_edit(all_children) {
  const container = document.getElementById('edit_material_modal_frame')

  mat_name = container.querySelector('[name="material_name"]')
  if (mat_name.value == '') {
    container.querySelector('[name="material_name_label"]').value = "ВВЕДИТЕ НАИМЕНОВАНИЕ"
    container.querySelector('[name="material_name_label"]').style.color = 'red'
    return
  }

  let new_parent_id = container.querySelector('[name="parent_id"]').value

  let this_mat_id = container.querySelector('[name="id"]').value

  if (all_children.includes(Number(new_parent_id))) {
    alert('Родительский элемент не может быть ниже')
    return
  }

  if (this_mat_id == new_parent_id) {
    alert('Родительский элемент не может быть самим собой')
    return
  }

  csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

  fetch('/materials/edit_mat/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        id: this_mat_id,
        material_name: mat_name.value,
        keywords: container.querySelector('[name="keywords"]').value,
        parent_id: new_parent_id == '' ? null : new_parent_id
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      pgReload()
    }
  })
}

function post_delItem(table, id) {

  if (!confirm('Удалить?')) {
    return
  }

  csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

  fetch('/' + table + '/delete/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        id: id
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      window.location.href = '/' + table +'/'
    }
  })
}

function post_delConnection(table, id_1, id_2, page=null) {

  if (!confirm('Удалить?')) {
    return
  }

  csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

  fetch('/companies/delete_connection/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        table: table,
        id_1: id_1,
        id_2: id_2
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      // pgReload()
      if (page) {
        setPage(page['type'], page['table'], page['id'])
      }
    }
  })
}

function post_ContactsList(table, comp_id) {
  csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

  fetch('/companies/edit_contact_list/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      id: comp_id,
      company_contacts: selectedContacts
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      setPage('details', table, comp_id)
      removeAllModals()
    }
  })
}

function post_MaterialsList(comp_id) {
  csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value


  fetch('/companies/edit_material_list/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      id: comp_id,
      company_materials: selectedMaterials
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      setPage('details', 'companies', comp_id)
      removeAllModals()
    }
  })
}