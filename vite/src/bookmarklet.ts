const siteUrl = window.bookmarklet.siteUrl;
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
  <a id="close">&times;</a>
  <h1>Select an image to bookmark:</h1>
  <div class="images"></div>
`;
const container = document.createElement("div");
container.id = "bookmarklet";
container.innerHTML = containerHtml.trim();
document.body.appendChild(container);

window.bookmarklet.launch = () => {
  const bookmarklet = document.getElementById("bookmarklet") as HTMLDivElement;
  const imagesFound = bookmarklet.querySelector<HTMLDivElement>(".images")!;

  // Clear images found.
  imagesFound.innerHTML = "";
  // Display bookmarklet.
  bookmarklet.style.display = "block";

  // Close event.
  const closeLink = bookmarklet.querySelector<HTMLAnchorElement>("#close")!;
  closeLink.addEventListener("click", function () {
    bookmarklet.style.display = "none";
  });

  // Find images in the DOM with the minimum dimensions.
  const images: NodeListOf<HTMLImageElement> = document.querySelectorAll(
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
      const imageSelected = event.target as HTMLImageElement;
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
};

window.bookmarklet.launch();
