function setupEpisodeClicks() {
  const episodeList = document.getElementById("episodeList")
  if (!episodeList) return

  const showId = episodeList.dataset.showId
  const maxWatched = parseInt(episodeList.dataset.maxWatched)
  const episodes = episodeList.querySelectorAll(".episode-item")

  episodes.forEach(ep => {
    const num = parseInt(ep.dataset.episodeNumber)
    if (num <= maxWatched) {
      ep.classList.add("watched")
    }
  })

  episodes.forEach(ep => {
    ep.addEventListener("click", () => {
      const episodeId = ep.dataset.episodeId
      const episodeNumber = parseInt(ep.dataset.episodeNumber)

      fetch("/watch", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          episode_id: episodeId,
          show_id: showId
        })
      })

      episodes.forEach(e => {
        const num = parseInt(e.dataset.episodeNumber)
        if (num <= episodeNumber) {
          e.classList.add("watched")
        } else {
          e.classList.remove("watched")
        }
      })

      episodeList.dataset.maxWatched = episodeNumber
    })
  })
}

function setupReviewForm() {
  const toggleBtn = document.getElementById("toggleReviewForm")
  const form = document.getElementById("reviewForm")
  const submitBtn = document.getElementById("submitReview")
  const ratingInput = document.getElementById("reviewRating")
  const textInput = document.getElementById("reviewText")
  const episodeList = document.getElementById("episodeList")

  if (!toggleBtn || !submitBtn || !episodeList) return

  const showId = episodeList.dataset.showId
  const hasReview = form.dataset.hasReview === "true"
  const reviewId = form.dataset.reviewId

  toggleBtn.addEventListener("click", () => {
    form.style.display = form.style.display === "none" ? "block" : "none"
  })

  submitBtn.addEventListener("click", () => {
    fetch("/save-review", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        show_id: showId,
        review_id: reviewId,
        rating: ratingInput.value,
        text: textInput.value,
        has_review: hasReview
      })
    }).then(() => {
      location.reload()
    })
  })
}

setupEpisodeClicks()
setupReviewForm()