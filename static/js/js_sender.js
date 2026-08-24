async function getCategory() {
  const container = document.getElementById("excel-upload-block")
  const input = document.getElementById("work-name-input")

  const label = document.getElementById("category")

  label.textContent = input.value
} 