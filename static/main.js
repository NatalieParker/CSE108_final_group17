const titleInput = document.getElementById("titleSearch")
const genreDropdown = document.getElementById("genreDropdown")
const ratingDropdown = document.getElementById("ratingDropdown")
const rows = document.querySelectorAll(".show-table tbody tr")

function filterShows() {
  const titleValue = titleInput.value.toLowerCase()
  const genreValue = genreDropdown.value.toLowerCase()
  const ratingValue = ratingDropdown.value

  rows.forEach(row => {
    const title = row.dataset.title || ""
    const genre = row.dataset.genre || ""
    const rating = row.dataset.rating || ""

    const matchesTitle = title.includes(titleValue)
    const matchesGenre = !genreValue || genre.includes(genreValue)
    const matchesRating = !ratingValue || rating === ratingValue

    row.style.display =
      matchesTitle && matchesGenre && matchesRating
        ? ""
        : "none"
  })
}

titleInput.addEventListener("input", filterShows)
genreDropdown.addEventListener("change", filterShows)
ratingDropdown.addEventListener("change", filterShows)