(function () {
  if (!window.bookmarklet) {
    window.bookmarklet = {};
    window.bookmarklet.siteUrl = "//{{ host }}/";

    const bookmarkletScript = document.createElement("script");
    bookmarkletScript.src =
      window.bookmarklet.siteUrl +
      "static/js/bookmarklet.js?r=" +
      Math.floor(
        Math.random() * 999999999999999
      ); /* Prevents loading `bookmarklet.js` from browser cache. */
    document.body.appendChild(bookmarkletScript);
  } else {
    window.bookmarklet.launch();
  }
})();
