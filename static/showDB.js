document.addEventListener("DOMContentLoaded", () => {
  fetch("/api/debug/db")
    .then(res => res.json())
    .then(data => {
      populateTable("shows-table", data.shows, show => `
        <tr>
          <td>${show.id}</td>
          <td>${show.title}</td>
          <td>${show.release_year ?? ""}</td>
          <td>${show.rating ?? ""}</td>
          <td>${show.seasons ?? ""}</td>
          <td>${show.genres ?? ""}</td>
        </tr>
      `);

      populateTable("episodes-table", data.episodes, ep => `
        <tr>
          <td>${ep.id}</td>
          <td>${ep.show_id}</td>
          <td>${ep.episode_number}</td>
        </tr>
      `);

      populateTable("users-table", data.users, user => `
        <tr>
          <td>${user.id}</td>
          <td>${user.username}</td>
        </tr>
      `);

      populateTable("watched-table", data.watched, w => `
        <tr>
          <td>${w.user_id}</td>
          <td>${w.episode_id}</td>
        </tr>
      `);

      populateTable("reviews-table", data.reviews, r => `
        <tr>
          <td>${r.user_id}</td>
          <td>${r.show_id}</td>
          <td>${r.rating}</td>
          <td>${r.review_text}</td>
        </tr>
      `);
    })
    .catch(err => {
      console.error("Failed to load DB debug data:", err);
    });
});


function populateTable(tableId, rows, rowTemplate) {
  const tableBody = document.querySelector(`#${tableId} tbody`);
  tableBody.innerHTML = "";

  rows.forEach(row => {
    tableBody.insertAdjacentHTML("beforeend", rowTemplate(row));
  });
}