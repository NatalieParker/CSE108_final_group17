const titleInput = document.getElementById("titleSearch");
const genreDropdown = document.getElementById("genreDropdown");
const ratingDropdown = document.getElementById("ratingDropdown");
const cards = document.querySelectorAll(".show-card");

function filterShows() {
  const titleValue = titleInput.value.toLowerCase();
  const genreValue = genreDropdown.value.toLowerCase();
  const ratingValue = ratingDropdown.value;

  cards.forEach(card => {
    const title = card.dataset.title || "";
    const genre = card.dataset.genre || "";
    const rating = card.dataset.rating || "";

    const matchesTitle = title.includes(titleValue);
    const matchesGenre = !genreValue || genre.includes(genreValue);
    const matchesRating = !ratingValue || rating === ratingValue;

    card.style.display =
      matchesTitle && matchesGenre && matchesRating
        ? "block"
        : "none";
  });
}

titleInput.addEventListener("input", filterShows);
genreDropdown.addEventListener("change", filterShows);
ratingDropdown.addEventListener("change", filterShows);

