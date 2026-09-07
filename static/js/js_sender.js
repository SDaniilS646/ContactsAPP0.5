async function getCategory() {
  const container = document.getElementById("excel-upload-block")
  const input = document.getElementById("work-name-input")

  const label = document.getElementById("category")


  const data = await postJson('/sender/categorize/', {input: input.value})

  if (data.success) {
    label.textContent = data.output
  }
} 

function deleteLabeledData(id) {
  const container = document.getElementById("pending-list")
  const items = container.querySelectorAll('div')
}

async function labelData() {
  const container = document.getElementById("pending-list")

  const items = container.querySelectorAll('div')
  let labeledData = []

  items.forEach(element => {
    let input = element.querySelector('input')
    if (input.value.trim() !== '') {
      console.log(`id: ${element.id} - ${input.value}`)
      labeledData.push({
        id: element.id,
        label: input.value
      })
    }
  })
  if (labeledData.length == 0) {
    return
  }

  const data = await postJson('/sender/label/', {labeledData: labeledData})
  if (data.success) {
    reloadModal('categories_active_learning_modal_frame', 'activeLearningCaterories')
  }
}