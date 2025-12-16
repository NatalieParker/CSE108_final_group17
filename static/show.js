function setupEpisodeClicks() {
  const episodeList = document.getElementById("episodeList")
  if (!episodeList) return

  const showId = Number(episodeList.dataset.showId)
  let maxWatched = parseInt(episodeList.dataset.maxWatched, 10) || 0

  const episodeItems = Array.from(episodeList.querySelectorAll(".episode-item"))

  function applyWatchedUI(newMax) {
    episodeItems.forEach(item => {
      const num = parseInt(item.dataset.episodeNumber, 10)
      const cb = item.querySelector(".episode-checkbox")
      const watched = num <= newMax

      item.classList.toggle("watched", watched)
      if (cb) cb.checked = watched
    })

    episodeList.dataset.maxWatched = String(newMax)
    maxWatched = newMax
  }

  // Initial paint from server value
  applyWatchedUI(maxWatched)

  // Map episode_number -> episode_id (for sending correct id)
  const numToId = new Map()
  episodeItems.forEach(item => {
    numToId.set(parseInt(item.dataset.episodeNumber, 10), Number(item.dataset.episodeId))
  })

  episodeItems.forEach(item => {
    const cb = item.querySelector(".episode-checkbox")
    if (!cb) return

    cb.addEventListener("change", async () => {
      const clickedNum = parseInt(item.dataset.episodeNumber, 10)
      const targetNum = cb.checked ? clickedNum : (clickedNum - 1)
      console.log("clicked episode", item.dataset.episodeId, "num", item.dataset.episodeNumber);

      const newMax = Math.max(0, targetNum)

      // Minimal-change behavior: don’t support clearing to 0 without a backend route
      if (newMax === 0) {
        applyWatchedUI(maxWatched) // revert
        return
      }

      const episodeId = numToId.get(newMax)
      if (!episodeId) {
        applyWatchedUI(maxWatched)
        return
      }

      try {
        const res = await fetch("/watch", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          credentials: "same-origin",
          body: JSON.stringify({ episode_id: episodeId, show_id: showId })
        })

        if (res.redirected || res.url.includes("/auth/login")) {
          window.location.href = res.url
          return
        }

        if (!res.ok) {
          applyWatchedUI(maxWatched)
          alert("Could not update watched progress. Please try again.")
          return
        }

        applyWatchedUI(newMax)

      } catch (err) {
        console.error(err)
        applyWatchedUI(maxWatched)
        alert("Network error. Please try again.")
      }
    })
  })
}

setupEpisodeClicks()

