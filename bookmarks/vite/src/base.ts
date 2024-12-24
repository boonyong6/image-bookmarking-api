import Cookies from "js-cookie";

export const onDomReady = (
  callback: (params: { event: Event; csrfToken: string }) => void
) => {
  const csrfToken = Cookies.get("csrftoken") ?? "";
  document.addEventListener("DOMContentLoaded", (event) => {
    callback({ event, csrfToken });
  });
};
