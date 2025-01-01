import { onDomReady } from "./base";
import { SimpleResponse } from "./types";

onDomReady(({ csrfToken }) => {
  const templateData =
    document.querySelector<HTMLDivElement>(".template-data")!.dataset;
  const url = templateData.url!;

  const options: RequestInit = {
    method: "POST",
    headers: { "X-CSRFToken": csrfToken },
    mode: "same-origin", // Indicates the request is made to the same origin.
  };

  const likeButton = document.querySelector("a.like") as HTMLAnchorElement;
  likeButton.addEventListener("click", async (e) => {
    e.preventDefault();

    // Add request body.
    const formData = new FormData();
    formData.append("id", likeButton.dataset.id ?? "");
    formData.append("action", likeButton.dataset.action ?? "");
    options.body = formData;

    // Send HTTP request.
    const response = await fetch(url, options);
    const data: SimpleResponse = await response.json();
    if (data.status === "ok") {
      const previousAction = likeButton.dataset.action;

      // Toggle button text and data-action
      const action = previousAction === "like" ? "unlike" : "like";
      likeButton.dataset.action = action;
      likeButton.textContent = action;

      // Update like count.
      const likeCount = document.querySelector(
        "span.count .total"
      ) as HTMLSpanElement;
      const totalLikes = parseInt(likeCount.innerText);
      likeCount.textContent = (
        previousAction === "like" ? totalLikes + 1 : totalLikes - 1
      ).toString();
    }
  });
});
