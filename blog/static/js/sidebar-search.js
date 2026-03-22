// Simple sidebar search using index.json
(function () {
  const input = document.getElementById("sidebar-search-input");
  const results = document.getElementById("sidebar-search-results");
  const articles = document.querySelectorAll(".post-list article");
  if (!input) return;

  input.addEventListener("input", function () {
    const query = this.value.toLowerCase().trim();
    if (!query) {
      articles.forEach((a) => (a.style.display = ""));
      results.innerHTML = "";
      return;
    }
    let count = 0;
    articles.forEach((a) => {
      const title = a.querySelector("h2")?.textContent?.toLowerCase() || "";
      const tags = a.querySelector(".entry-tags")?.textContent?.toLowerCase() || "";
      if (title.includes(query) || tags.includes(query)) {
        a.style.display = "";
        count++;
      } else {
        a.style.display = "none";
      }
    });
    results.innerHTML = `<span style="color:var(--secondary)">${count} results</span>`;
  });
})();
