// Autumn color palette for tags — hash-based so same tag always gets same color
(function () {
  var AUTUMN = [
    { bg: "#f0d9b5", fg: "#6b4226" },
    { bg: "#e8c8a0", fg: "#5c3a1e" },
    { bg: "#d4a574", fg: "#4a2e14" },
    { bg: "#c9b896", fg: "#4a3f2a" },
    { bg: "#d6bfa8", fg: "#5a3e28" },
    { bg: "#e0c4a8", fg: "#6a4430" },
    { bg: "#c8a882", fg: "#4e3318" },
    { bg: "#dab88a", fg: "#5e3d1a" },
    { bg: "#c4a67a", fg: "#4a3216" },
    { bg: "#d8c4a0", fg: "#5a4828" },
    { bg: "#ccb090", fg: "#503a20" },
    { bg: "#e4d0a8", fg: "#6a5030" },
    { bg: "#bfa878", fg: "#483212" },
    { bg: "#d0b898", fg: "#544024" },
    { bg: "#c8b48c", fg: "#4c3a1e" },
    { bg: "#dcc098", fg: "#604828" },
  ];

  function hash(str) {
    var h = 0;
    for (var i = 0; i < str.length; i++) {
      h = ((h << 5) - h + str.charCodeAt(i)) | 0;
    }
    return Math.abs(h);
  }

  // Assign unique colors: same tag name → same color everywhere
  var tagColorMap = {};
  var usedIndices = [];
  var badges = document.querySelectorAll(".tag-badge");

  badges.forEach(function (badge) {
    var name = badge.textContent.trim().replace(/\s*\d+$/, "").trim();
    if (!tagColorMap[name]) {
      var idx = hash(name) % AUTUMN.length;
      // Avoid collisions with already-used indices
      var attempts = 0;
      while (usedIndices.indexOf(idx) !== -1 && attempts < AUTUMN.length) {
        idx = (idx + 1) % AUTUMN.length;
        attempts++;
      }
      usedIndices.push(idx);
      tagColorMap[name] = AUTUMN[idx];
    }
    var c = tagColorMap[name];
    badge.style.background = c.bg;
    badge.style.color = c.fg;
  });

  // Sidebar search: filter posts by title/tags
  var input = document.getElementById("sidebar-search-input");
  var results = document.getElementById("sidebar-search-results");
  var articles = document.querySelectorAll(".post-list article");
  if (!input) return;

  input.addEventListener("input", function () {
    var query = this.value.toLowerCase().trim();
    if (!query) {
      articles.forEach(function (a) { a.style.display = ""; });
      results.innerHTML = "";
      return;
    }
    var count = 0;
    articles.forEach(function (a) {
      var title = (a.querySelector("h2") || {}).textContent || "";
      var tags = (a.querySelector(".entry-tags") || {}).textContent || "";
      if (title.toLowerCase().includes(query) || tags.toLowerCase().includes(query)) {
        a.style.display = "";
        count++;
      } else {
        a.style.display = "none";
      }
    });
    results.innerHTML = '<span style="color:var(--secondary)">' + count + " results</span>";
  });
})();
