import { onDomReady } from "./base";

onDomReady(() => {
  let page = 1;
  let emptyPage = false;
  // Prevents sending additional requests while an request is in progress.
  let blockRequest = false;

  window.addEventListener("scroll", async () => {
    // Height of the remaining content.
    const margin = document.body.clientHeight - window.innerHeight - 200;

    if (window.scrollY > margin && !emptyPage && !blockRequest) {
      blockRequest = true;
      page += 1;

      const response = await fetch(`?images_only=1&page=${page}`);
      const htmlText = await response.text();
      if (htmlText === "") {
        emptyPage = true;
      } else {
        const imageList = document.getElementById(
          "image-list"
        ) as HTMLDivElement;
        imageList.insertAdjacentHTML("beforeend", htmlText); // Parses and inserts.
        blockRequest = false;
      }
    }
  });

  // Launch scroll event.
  const scrollEvent = new Event("scroll");
  window.dispatchEvent(scrollEvent);
});
