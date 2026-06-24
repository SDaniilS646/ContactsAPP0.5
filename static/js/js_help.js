function openModal(modal_name) {
  document
  .getElementById(modal_name)
  .style.display = 'flex'

}

function closeModal(modal_name, is_inputs=false) {
  if (is_inputs == true) {
    document
    .querySelectorAll('#'+modal_name+' input').forEach(input => {
    input.value = '';
    });
  }
  

  document
  .getElementById(modal_name)
  .style.display = 'none'
}


let contacts = []
let materials = []
let selected_contacts = []
// let selected_materials = []
let selectedItem_on_create_mat = null

function saveContact_fromEdit(modal_name) {
  if (document.getElementById('contact_first_name').value == '') {
    document.getElementById('name-sign').textContent += ' • УКАЖИТЕ ИМЯ!!!'
    return
  }

  csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  fetch('/companies/add_cont/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      first_name: document.getElementById('contact_first_name').value,

      last_name: document.getElementById('contact_last_name').value == '' ? null : document.getElementById('contact_last_name').value,

      middle_name: document.getElementById('contact_middle_name').value == '' ? null : document.getElementById('contact_middle_name').value,
      
      position: document.getElementById('contact_position').value == '' ? null : document.getElementById('contact_position').value,

      phone: document.getElementById('contact_phone').value == '' ? null : document.getElementById('contact_phone').value,

      mail: document.getElementById('contact_mail').value == '' ? null : document.getElementById('contact_mail').value,

      comp_id: document.getElementById('comp_id').value
    })
  })
  .then(response => response.json())
  .then(data => {
      if (data.success) {
        window.location.reload()

        // closeModal('contact-modal')
      }
    });

}

function editMaterialList() {
  csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  fetch('/companies/add_mat_comp_connection/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      materials: materials,
      comp_id: document.getElementById('comp_id').value
    })
  })
  .then(response => response.json())
  .then(data => {
      if (data.success) {
        window.location.reload()
      }
    });

  closeModal('material-modal')
  return
}

function saveContact(modal_name) {

  if (document.getElementById('contact_first_name').value == '') {
    document.getElementById('name-sign').textContent += ' • УКАЖИТЕ ИМЯ!!!'
    return
  }

  contacts.push(
    {
      first_name: document.getElementById('contact_first_name').value,

      last_name: document.getElementById('contact_last_name').value == '' ? null : document.getElementById('contact_last_name').value,

      middle_name: document.getElementById('contact_middle_name').value == '' ? null : document.getElementById('contact_middle_name').value,
      
      position: document.getElementById('contact_position').value == '' ? null : document.getElementById('contact_position').value,

      phone: document.getElementById('contact_phone').value == '' ? null : document.getElementById('contact_phone').value,

      mail: document.getElementById('contact_mail').value == '' ? null : document.getElementById('contact_mail').value
    }
  )
  closeModal(modal_name, true)
}

function prepareSave() {
  document.getElementById('contacts_json').value = JSON.stringify(contacts)
}

function saveMaterial(type, source=null, id=null, children=null, prev_id=null) {
  console.log('------------------SAVING-------------------------')
  
  if (type == 'add_comp') {
    document.getElementById('materials_json').value = materials
    closeModal('material-modal')
    return
  }

  if (check_new_material() == false) {
    return
  }

  csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  parent_id = document.getElementById('parent_id').value
  
  if (type == 'edit_mat') {
    children_list = []
    if (children != '') {
      children.forEach(val => children_list.push(String(val['id'])))
    }
    

    if (id == parent_id || children_list.includes(parent_id)) {
      parent_id = prev_id
    } 
    
    if (!selectedItem_on_create_mat && parent_id == '') {
      parent_id = prev_id
    }
  } else {
    
  }

  fetch('/materials/add_mat/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      name: document.getElementById('material_name').value,
      parent_id: parent_id,
      keywords: document.getElementById('keywords').value,
      is_edit: type == 'edit_mat' ? true : false,
      id: id
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.is_edit) {
      window.location.reload()
    } else {
      refreshAllTrees()
      if (type == 'new_mat' && source=='from_list') {
        window.location.reload()
      }
    }
    
    closeModal('add-material-modal')
  });

}

async function refreshAllTrees() {

  data1 = await refreshMaterialTree('new_mat')

  data2 = await refreshMaterialTree('new_comp')
  console.log({data1, data2})

}

async function refreshMaterialTree(modal_task='') {
  clear_chosen_mats()

  if (modal_task != '') {
    fetch_link = '/materials/modal_frames/'+'?modal_task=' +modal_task

    if (modal_task == 'new_mat') {
      tree_id = 'materials-tree'
    } else if (modal_task == 'new_comp') {
      tree_id = 'tree-head'
    }
    
  } else {
    fetch_link = '/materials/modal_frames/'
    tree_id = 'tree-head'
  }

  const data = await fetch(fetch_link)
  .then(response => response.text())
  .then(html => {
    document.getElementById(
      tree_id
    ).innerHTML = html
  })
  return modal_task+' success'
}

function check_new_material() {
  mat_name = document.getElementById('material_name').value
  if (mat_name == '') {
    document.getElementById('mat-name-error').textContent += ' УКАЖИТЕ НАИМЕНОВАНИЕ'
    return false
  } else {
    document.getElementById('mat-name-error').textContent = 'Наименование'
    return true
  }
}

function select_parent(event, element, name = null, prev_id = null) {
  
  event.stopPropagation();
  const container = document.getElementById(
    'tree2'
  )

  if (prev_id) {
    document.getElementById('_'+prev_id).classList.remove('selected')
    document.getElementById('parent_id').value = prev_id

  }

  if (selectedItem_on_create_mat) {
    selectedItem_on_create_mat.classList.remove('selected');
  }

  element.classList.add('selected')
  selectedItem_on_create_mat = element 

  if (name === null) {
    document.getElementById('parent_id').value = ''
    selectedItem_on_create_mat = document.getElementById('root-category')

    selectedItem_on_create_mat.classList.add('selected')
    return
  }
  else {
    chosen_id = name.id
    document.getElementById('root-category').classList.remove('selected')
    document.getElementById('parent_id').value = chosen_id
    return
  }
}




function select_materials(event, element, name = null) {
  console.log('tapping')
  event.stopPropagation();
  mat_id = name.id
  mat_name = name.name
  
  console.log(mat_id + " - " + mat_name)

  const container = document.getElementById(
    'material-tree-from-company'
  )
  check_parents(container, element)
  clear_children(container, name)
  
  if (materials.includes(mat_id)) {


    materials.splice(materials.indexOf(mat_id), 1)
    
    container.querySelector('#_'+mat_id).classList.remove('selected')
  } else {
    materials.push(mat_id)
    container.querySelector('#_'+mat_id).classList.add('selected')
  }
  console.log(materials)
}


function select_contacts(event, element, id=null) {

  const container = document.getElementById(
    'contact-list'
  )
  
  let cont_classes = Array.from(container.querySelector('#_'+id).classList)
  

  if (cont_classes.includes('selected')) {
    container.querySelector('#_'+id).classList.remove('selected')
    if (selected_contacts.indexOf(id) >= 0) {

      selected_contacts.splice(selected_contacts.indexOf(id), 1)
    }
    
  } else {
    container.querySelector('#_'+id).classList.add('selected')
    selected_contacts.push(id)
  }
}

function save_selected_contacts(comp_id) {
  console.log('saving')
  const contact_container = document.getElementById(
        'contact-list'
      )
  contacts_poses = []
  selected_contacts.forEach(val => {

    let item = contact_container.querySelector('#_'+val)
    contacts_poses.push(
      {
        'id': val,
        'pos': item.querySelector('input').value
      }
    )
  })
  
  // СОЗДАТЬ НОВУЮ СВЯЗЬ И ЗАКРЫТЬ МОДАЛКУ
  csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  fetch('/companies/upd_company_contacts/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        company_id: comp_id,
        contacts: contacts_poses
      })
    }
  )
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      window.location.reload()
    }
  })

}

function check_parents(container, element) {
  if (element.dataset.parentId == 'none') {
    return
  }

  let parent_id = element.dataset.parentId;
  let counter =0

  while (parent_id) {
    parent = container.querySelector(
      '[data-id="'+parent_id+'"]'
    )

    if (!parent) {
      break;
    }
    

    parent.classList.remove('selected')
    materials = materials.filter(val => val != parent_id)


    parent_id = parent.dataset.parentId;

    counter += 1
    if (counter >= 1000) {return}
  }
}

function get_all_child(node, result = []) {
  for (const child of node.children) {
    result.push(child.id);

    get_all_child(
      child, 
      result
    )
  }
  return result
}

function clear_children(container, name) {
  child_ids = get_all_child(name)

  child_ids.forEach( val => {

    container.querySelector('#_'+val).classList.remove('selected')

    materials = materials.filter(mat_val => mat_val != val)
    }
  )

}

function clear_chosen_mats() {
  materials = []
  try {
    document.getElementById('materials_json').value = materials
  } catch (error) {
    console.log('no materials_json')
  }
  
}

function delete_card(base, id) {
  if (!confirm('Удалить запись?')) {
    return;
  }

  csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  function fetch_del(table_name) {
    fetch('/'+table_name+'/delete-' + table_name +'/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          table: table_name,
          id: id
        })
      }
    )
    .then(response => response.json())
    .then(data => {window.location.href = data.redirect_url})
  }

  switch (base) {
    case 'comp':
      fetch_del('companies')
    break;
    case 'mat':
      fetch_del('materials')
      break;
    case 'cont':
      fetch_del('contacts')
      break;
  }
}

function delete_connection(table, id_1, id_2) {

  if (!confirm('Удалить запись?')) {
    return;
  }

  csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  function fetch_del(table_name, id_1, id_2) {
    fetch('/connection_delete/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          table: table_name,
          id_1: id_1,
          id_2: id_2
        })
      }
    )
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        window.location.reload()
      }
    })
  }

  switch (table) {
    case 'comp_cont':
    fetch_del('company_contacts', id_1, id_2)
    break;
    case 'comp_mat':
    fetch_del('company_materials', id_1, id_2)
    break;
  }
}

function edit_list(table_name, company_id) {

  switch (table_name) {
    case 'contacts':
      openModal('contact-modal')
      break
    case 'materials':
      openModal('material-modal')
      break
    case 'material':
      openModal('add-material-modal')
      break
    case 'companies':
      openModal('company-info-modal')
      break
  }
}

document.addEventListener(
  'input',

  function(event) {
    let input_box = event.target.id;

    switch (input_box) {
      case 'companies-list':
        filter_pg_list(event, '.card')
        break;
      case 'contacts-list-on-comp-edit':
        filter_pg_list(event, '.contact-pos')
        break
      case 'contacts-list':
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
    path = window.location.pathname
    
    if (path.includes('/add_')) {
      selectedItem_on_create_mat = document.getElementById('root-category')

      selectedItem_on_create_mat.classList.add('selected')
      console.log('adding smthing')
    }
    
    if (/^\/companies\/\d+\/$/.test(path)) {
      const contact_container = document.getElementById(
        'contact-list'
      )
      selected_contacts = Array.from(contact_container.querySelectorAll('.contact-pos.selected')).map(el => Number(el.id.slice(1))
      //   ({
      //   'id': Number(el.id.slice(1)),
      //   'pos': el.querySelector('input').value
      // })
    )


      const material_container = document.getElementById('material-tree-from-company')
      let tree_selected_materials = material_container.querySelectorAll('.tree-item.selected')
      materials = Array.from(tree_selected_materials).map(el => Number(el.id.slice(1)))
      tree_selected_materials.forEach(el =>{
        let parent = el.closest('details');

        while (parent) {
          parent.open = true;

          parent = parent.parentElement?.closest('details');
        }
      })
    }
  
}