(function () {
  if (!window.bookmarklet) {
    window.bookmarkletSiteUrl = '//{{ host }}/';

    const bookmarkletScript = document.createElement('script');
    bookmarkletScript.src =
      window.bookmarkletSiteUrl + 'static/js/bookmarklet.js?r=' +
      Math.floor(Math.random() * 999999999999999); /* Prevents loading `bookmarklet.js` from browser cache. */
    document.body.appendChild(bookmarkletScript);
    
    window.bookmarklet = true;
  } else {
    bookmarkletLaunch();
  }
})();
