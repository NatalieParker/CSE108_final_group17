const searchInput = document.getElementById("watchedSearch")
const rows = document.querySelectorAll(".show-table tbody tr")

function filterWatchLog() {
  const value = searchInput.value.toLowerCase()

  rows.forEach(row => {
    const title = row.dataset.title || ""
    row.style.display = title.includes(value) ? "" : "none"
  })
}

  searchInput.addEventListener("input", filterWatchLog)