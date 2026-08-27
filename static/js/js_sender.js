async function getCategory() {
  const container = document.getElementById("excel-upload-block")
  const input = document.getElementById("work-name-input")

  const label = document.getElementById("category")


  const data = await postJson('/sender/categorize/', {input: input.value})

  if (data.success) {
    label.textContent = data.output
  }
} 