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

setupEpisodeClicks()