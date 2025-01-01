import { onDomReady } from "./base";
import { SimpleResponse } from "./types";

onDomReady(({ csrfToken }) => {
  const templateData =
    document.querySelector<HTMLDivElement>(".template-data")!.dataset;
  const url = templateData.url!;
  const options: RequestInit = {
    method: "POST",
    headers: { "X-CSRFToken": csrfToken },
    mode: "same-origin",
  };

  const followButton = document.querySelector("a.follow") as HTMLAnchorElement;
  followButton.addEventListener("click", async (e) => {
    e.preventDefault();

    // Add request body.
    const formData = new FormData();
    formData.append("id", followButton.dataset.id ?? "");
    formData.append("action", followButton.dataset.action ?? "");
    options.body = formData;

    // Send HTTP request.
    const response = await fetch(url, options);
    const data: SimpleResponse = await response.json();
    if (data.status === "ok") {
      const previousAction = followButton.dataset.action;

      // Toggle button text and data-action.
      const action = previousAction === "follow" ? "unfollow" : "follow";
      followButton.dataset.action = action;
      followButton.textContent = action;

      // Update follower count.
      const followerCount = document.querySelector(
        "span.count .total"
      ) as HTMLSpanElement;
      const totalFollowers = parseInt(followerCount.innerText);
      followerCount.textContent = (
        previousAction === "follow" ? totalFollowers + 1 : totalFollowers - 1
      ).toString();
    }
  });
});
