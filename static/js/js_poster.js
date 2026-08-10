async function postJson(url, payload=null) {
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
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload),
    })
  } catch (networkError) {
    throw new Error(`Network error while requesting ${url}: ${networkError.message}`)
  }

  if (!response.ok) {
    const errorBody = await response.json().catch(() => null)
    const message = errorBody?.error || errorBody?.message || `HTTP ${response.status}: ${response.statusText}`
    throw new Error(message)
  }

  return response.json()
}

async function post_create_meeting() {
  const container = document.getElementById('company-creation')
  const subject = container.querySelector('[name="subject"]')
  if (subject.value.trim() === '') {
    const subjectLabel = container.querySelector('[name="subject-label"]')
    subjectLabel.textContent = "УКАЖИТЕ ТЕМУ ВСТРЕЧИ"
    subjectLabel.style.color = 'red'
    return
  }

  const meetingDateInput = container.querySelector('[name="meeting-date"]')

  try {
    const data = await postJson('/meetings/add_meet/', {
      subject: subject.value,
      comment: container.querySelector('[name="comment"]').value,
      record_link: container.querySelector('[name="record-link"]').value,
      meeting_date: meetingDateInput.value.trim() === '' ? null : meetingDateInput.value,
      meeting_contacts: selectedContacts,
      meeting_employees: selectedEmployees,
      meeting_companies: selectedCompanies
    })
    if (data.success) {
      setPage('page', 'meetings')
    } else {
      console.log(data.error || 'meeting create error')
    }
  } catch {
    console.error('Failed to create meeting:', error)
  }
}

async function post_create_company() {
  const container = document.getElementById('company-creation')
  const comp_name = container.querySelector('[name="company_name"]')
  const companyLabel = container.querySelector('[name="company_name_label"]')
  if (comp_name.value == '') {
    companyLabel.textContent = "УКАЖИТЕ НАЗВАНИЕ КОМПАНИИ"
    companyLabel.style.color = 'red'
    return
  }

  const ratingInput = container.querySelector('[name="rating"]')
  let rating = Number(ratingInput.value)
  if (Number.isNaN(rating)) {
    rating = 0
  }
  rating = Math.min(Math.max(rating, 0), 5)

  try {
    const data = await postJson('/companies/add_comp/', {
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

    if (data.success) {
      setPage('page', 'companies')
    } else {
      if (data.result === 'Exists') {
        companyLabel.textContent = "Компания с таким названием или почтой уже существует"
      } else {
        companyLabel.textContent = 'Не удалось создать компанию'
      }
    }
  } catch (error) {
    console.log('Failed to create company:', error)
  }
  
}

async function post_company_edit() {
  const container = document.getElementById('edit_company_modal_frame') 
  const comp_name = container.querySelector('[name="company_name"]')
  if (comp_name.value == '') {
    const companyLabel = container.querySelector('[name="company_name_label"]')
    companyLabel.textContent = "УКАЖИТЕ НАЗВАНИЕ КОМПАНИИ"
    companyLabel.style.color = 'red'
    return
  }

  const ratingInput = container.querySelector('[name="rating"]')
  let rating = Number(ratingInput.value)
  if (Number.isNaN(rating)) {
    rating = 0
  }
  rating = Math.min(Math.max(rating, 0), 5)

  const comp_id = container.querySelector('[name="id"]').value

  const data = await postJson('/companies/edit_comp/', {
    id: comp_id,
    company_name: comp_name.value,
    inn: container.querySelector('[name="inn"]').value,
    site: container.querySelector('[name="site"]').value,
    rating: rating,
    mail: container.querySelector('[name="mail"]').value,
    phone: container.querySelector('[name="phone"]').value,
    comment: container.querySelector('[name="comment"]').value
  })

  if (data.success) {
    removeModal('edit_company_modal_frame')
    reloadModal('companies-details-modal-frame', 'detailsCompany', comp_id)
  }
}

async function post_contact_create(comp_id=null) {
  const container = document.getElementById('create_contact_modal_frame') 
  const cont_first_name = container.querySelector('[name="first_name"]')
  const cont_last_name = container.querySelector('[name="last_name"]')
  if (cont_first_name.value.trim() == '' && cont_last_name.value.trim() == '') {
    if (cont_first_name.value == '') {
      container.querySelector('[name="first_name_label"]').textContent = "ВВЕДИТЕ ИМЯ"
    }
    if (cont_last_name.value == '') {
      container.querySelector('[name="last_name_label"]').textContent = "ВВЕДИТЕ ФАМИЛИЮ"
    }
    return
  }

  const data = await postJson('/contacts/add_cont/', {
    first_name: cont_first_name.value,
    last_name: cont_last_name.value,
    patronymic: container.querySelector('[name="patronymic"]').value,
    phone: container.querySelector('[name="phone"]').value,
    mail: container.querySelector('[name="mail"]').value,
    comment: container.querySelector('[name="comment"]').value
  })

  if (data.success) {
    if (AppState.currentPage === 'page-contacts') {
      setPage('page', 'contacts')
    }
    removeModal('create_contact_modal_frame')
    reloadModal('choose_contact_modal_frame', 'chooseContact', comp_id)
  }
}

async function post_contact_edit() {
  const container = document.getElementById('edit_contact_modal_frame') 
  const cont_first_name = container.querySelector('[name="first_name"]')
  const cont_last_name = container.querySelector('[name="last_name"]')
  if (cont_first_name.value == '' && cont_last_name.value == '') {
    if (cont_first_name.value == '') {
      container.querySelector('[name="first_name_label"]').textContent = "ВВЕДИТЕ ИМЯ"
    }
    if (cont_last_name.value == '') {
      container.querySelector('[name="last_name_label"]').textContent = "ВВЕДИТЕ ФАМИЛИЮ"
    }
    return
  }

  const contactId = container.querySelector('[name="id"]').value

  const data = await postJson('/contacts/edit_cont/', {
    id: contactId,
    first_name: cont_first_name.value,
    last_name: cont_last_name.value,
    patronymic: container.querySelector('[name="patronymic"]').value,
    phone: container.querySelector('[name="phone"]').value,
    mail: container.querySelector('[name="mail"]').value,
    comment: container.querySelector('[name="comment"]').value
  })

  if (data.success) {   
    removeModal('edit_contact_modal_frame')
    reloadModal('contacts-details-modal-frame', 'detailsContact', contactId)
  }
}

async function post_employee_create() {
  const container = document.getElementById('create_employee_modal_frame')
  const emp_first_name = container.querySelector('[name="first_name"]')
  const emp_last_name = container.querySelector('[name="last_name"]')
  if (emp_first_name.value == '' && emp_last_name.value == '') {
    if (emp_first_name.value == '') {
      container.querySelector('[name="first_name_label"]').textContent = "ВВЕДИТЕ ИМЯ"
    }
    if (emp_last_name.value == '') {
      container.querySelector('[name="last_name_label"]').textContent = "ВВЕДИТЕ ФАМИЛИЮ"
    }
    return
  }

  const data = await postJson('/employees/add_emp/', {
    first_name: emp_first_name.value,
    last_name: emp_last_name.value,
    patronymic: container.querySelector('[name="patronymic"]').value,
    phone: container.querySelector('[name="phone"]').value,
    mail: container.querySelector('[name="mail"]').value
  })

  if (data.success) {
    if (AppState.currentPage === 'page-employees') {
      setPage('page', 'employees')
    }
    
    removeModal('create_employee_modal_frame')
    reloadModal('choose_employee_modal_frame', 'chooseEmployee')
  }
}

async function post_employee_edit() {
  const container = document.getElementById('edit_employee_modal_frame') 
  const emp_first_name = container.querySelector('[name="first_name"]')
  const emp_last_name = container.querySelector('[name="last_name"]')
  if (emp_first_name.value == '' && emp_last_name.value == '') {
    if (emp_first_name.value == '') {
      container.querySelector('[name="first_name_label"]').textContent = "ВВЕДИТЕ ИМЯ"
    }
    if (emp_last_name.value == '') {
      container.querySelector('[name="last_name_label"]').textContent = "ВВЕДИТЕ ФАМИЛИЮ"
    }
    return
  }

  const data = await postJson('/employees/edit_emp/', {
    id: container.querySelector('[name="id"]').value,
    first_name: emp_first_name.value,
    last_name: emp_last_name.value,
    patronymic: container.querySelector('[name="patronymic"]').value,
    phone: container.querySelector('[name="phone"]').value,
    mail: container.querySelector('[name="mail"]').value
  })

  if (data.success) {
    removeModal('edit_employee_modal_frame')
    setPage('page', 'employees')
  }
}

async function post_material_create(comp_id=null) {
  const container = document.getElementById('create_material_modal_frame')
  const mat_name = container.querySelector('[name="material_name"]')
  if (mat_name.value == '') {
    const materialLabel = container.querySelector('[name="material_name_label"]')
    materialLabel.value = "ВВЕДИТЕ НАИМЕНОВАНИЕ"
    materialLabel.style.color = 'red'
    return
  }

  const data = await postJson('/materials/add_mat/', {
    material_name: mat_name.value,
    keywords: container.querySelector('[name="keywords"]').value,
    parent_id: container.querySelector('[name="parent_id"]').value == '' ? null : container.querySelector('[name="parent_id"]').value
  })

  if (data.success) {
    if (AppState.currentPage === 'page-materials') {
      setPage('page', 'materials')
    }
    removeModal('create_material_modal_frame')
    reloadModal('choose_material_modal_frame', 'chooseMaterial', comp_id)
  }
}

async function post_material_edit(all_children) {
  const container = document.getElementById('edit_material_modal_frame')
  const mat_name = container.querySelector('[name="material_name"]')
  if (mat_name.value.trim() === '') {
    const materialLabel = container.querySelector('[name="material_name_label"]')
    materialLabel.value = "ВВЕДИТЕ НАИМЕНОВАНИЕ"
    materialLabel.style.color = 'red'
    return
  }

  const new_parent_id = container.querySelector('[name="parent_id"]').value
  const this_mat_id = container.querySelector('[name="id"]').value

  if (all_children.includes(Number(new_parent_id))) {
    alert('Родительский элемент не может быть ниже')
    return
  }

  if (this_mat_id === new_parent_id) {
    alert('Родительский элемент не может быть самим собой')
    return
  }

  const data = await postJson('/materials/edit_mat/', {
    id: this_mat_id,
    material_name: mat_name.value,
    keywords: container.querySelector('[name="keywords"]').value,
    parent_id: new_parent_id == '' ? null : new_parent_id
  })

  if (data.success) {
    setPage('page', 'materials')
    removeModal('edit_material_modal_frame')
    reloadModal('materials-details-modal-frame', 'detailsMaterial', this_mat_id)
  }
}

async function post_delItem(table, id) {
  if (!confirm('Удалить?')) {
    return
  }

  const data = await postJson('/' + table + '/delete/', {id: id})
  if (data.success) {
    const cur_pg = AppState.currentPage.split('-')
    setPage(cur_pg[0], cur_pg[1])
  }
}

async function post_delConnection(table, id_1, id_2, page=null) {

  if (!confirm('Удалить?')) {
    return
  }
  const data = await postJson('/companies/delete_connection/', {
    table: table,
    id_1: id_1,
    id_2: id_2
  })

  if (data.success) {
    reloadModal(
      AppState.activeModal.at(-1).modal_frame_id,
      AppState.activeModal.at(-1).modal_name,
      AppState.activeModal.at(-1).id,
    )
  }
}

async function post_ContactsList(comp_id) {
  const data = await postJson('/companies/edit_contact_list/', {
      id: comp_id,
      company_contacts: selectedContacts
  })

  if (data.success) {
    removeAllModals()
    openModal('companies-details-modal-frame', 'detailsCompany', comp_id)
  }
}

async function post_MaterialsList(comp_id) {
  const data = await postJson('/companies/edit_material_list/', {
    id: comp_id,
    company_materials: selectedMaterials
  })
  if (data.success) {
    removeAllModals()
    openModal('companies-details-modal-frame', 'detailsCompany', comp_id)
  }
}

function start_parsing() {
  const container = document.getElementById('company-parsing')

  const parse_btn = container.querySelector('[name="start-parsing-btn"]')
  parse_btn.inert = true;
  parse_btn.style.backgroundColor = "grey"
  let div = document.querySelector('[name=companies]')
  div.innerHTML = ''

  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

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
        const url_container = document.createElement('div')


        const span = document.createElement('span');
        span.textContent = url_val['url'];
        div.appendChild(span);
        
        url_val['mail'].forEach((val, idx) => {

          span = document.createElement('span')
          span.setAttribute('hidden', '')
          span.textContent = url_val['url']
          
          const form_container = document.createElement('div')
          form_container.setAttribute('class', 'form_container')
          const checkbox = document.createElement('input');
          checkbox.type = 'checkbox';
          checkbox.value = val; 
          checkbox.name = `${url_idx} - ${idx}`;

          const label = document.createElement('label');
          
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
  let added_comps = 0
  let new_comps = []

  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
  let checkboxes = null
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