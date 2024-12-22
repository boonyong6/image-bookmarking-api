const siteUrl = window.bookmarkletSiteUrl;
const styleUrl = siteUrl + "static/css/bookmarklet.css";
// Min width and height of the captured images.
const minWidth = 250;
const minHeight = 250;

// Load CSS.
const link = document.createElement("link");
link.rel = "stylesheet";
link.type = "text/css";
link.href = styleUrl + "?r=" + Math.floor(Math.random() * 999999999999999);
document.head.appendChild(link);

// Load HTML.
const containerHtml = `
  <div id="bookmarklet">
    <a id="close">&times;</a>
    <h1>Select an image to bookmark:</h1>
    <div class="images"></div>
  </div>
`;
const container = document.createElement("div");
container.innerHTML = containerHtml.trim();
document.body.appendChild(container);

function bookmarkletLaunch() {
  const bookmarklet = document.getElementById("bookmarklet");
  const imagesFound = bookmarklet.querySelector(".images");

  // Clear images found.
  imagesFound.innerHTML = "";
  // Display bookmarklet.
  bookmarklet.style.display = "block";

  // Close event.
  bookmarklet.querySelector("#close").addEventListener("click", function () {
    bookmarklet.style.display = "none";
  });

  // Find images in the DOM with the minimum dimensions.
  const images = document.querySelectorAll(
    'img[src*=".jpg"], img[src*=".jpeg"], img[src*=".png"]' // `*=` means contains.
    // 'img[src$=".jpg"], img[src$=".jpeg"], img[src$=".png"]' // `$=` means ends with.
  );

  images.forEach((image) => {
    if (image.naturalWidth >= minWidth && image.naturalHeight >= minHeight) {
      const imageFound = document.createElement("img");
      imageFound.src = image.src;
      imagesFound.appendChild(imageFound);
    }
  });

  // Select image event.
  imagesFound.querySelectorAll("img").forEach((image) => {
    image.addEventListener("click", function (event) {
      const imageSelected = event.target;
      bookmarklet.style.display = "none";
      window.open(
        siteUrl +
          "images/create/?url=" +
          encodeURIComponent(imageSelected.src) +
          "&title=" +
          encodeURIComponent(document.title),
        "_blank"
      );
    });
  });
}

bookmarkletLaunch();
