/* Minimal client-side enhancements (no tracking, no external deps) */

(function () {
  function normalize(text) {
    return (text || "")
      .toLowerCase()
      .replace(/\s+/g, " ")
      .trim();
  }

  function setActiveNav() {
    var nav = document.querySelector("[data-site-nav]");
    if (!nav) return;

    var links = nav.querySelectorAll("a[href]");
    var path = window.location.pathname;

    // Support GitHub Pages subpaths: match by ending segment.
    var current = path.split("/").filter(Boolean).pop() || "index.html";

    links.forEach(function (a) {
      a.removeAttribute("aria-current");
      var href = a.getAttribute("href") || "";
      var hrefLast = href.split("/").filter(Boolean).pop();
      if (!hrefLast) return;

      if (hrefLast === current) {
        a.setAttribute("aria-current", "page");
      }

      // Mark Blog as current for /blog/* pages
      if (path.indexOf("/blog/") !== -1 && hrefLast === "index.html" && href.indexOf("blog/") !== -1) {
        a.setAttribute("aria-current", "page");
      }
    });
  }

  function blogSearch() {
    var input = document.querySelector("[data-blog-search]");
    var results = document.querySelectorAll("[data-blog-card]");
    var countEl = document.querySelector("[data-search-count]");

    if (!input || !results.length) return;

    function apply() {
      var q = normalize(input.value);
      var shown = 0;

      results.forEach(function (card) {
        var hay = normalize(card.getAttribute("data-search") || card.textContent);
        var match = !q || hay.indexOf(q) !== -1;
        card.style.display = match ? "" : "none";
        if (match) shown++;
      });

      if (countEl) {
        countEl.textContent = shown + " article" + (shown === 1 ? "" : "s") + " shown";
      }
    }

    input.addEventListener("input", apply);
    apply();
  }

  document.addEventListener("DOMContentLoaded", function () {
    setActiveNav();
    blogSearch();
  });
})();
