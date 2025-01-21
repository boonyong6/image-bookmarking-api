import { onDomReady } from "./base";

onDomReady(() => {
  const templateData =
    document.querySelector<HTMLDivElement>(".template-data")!.dataset;

  const imageInputElts = Array.from(
    document.querySelectorAll<HTMLInputElement>(
      'input[type="file"].image-field'
    )
  );

  for (const imageInputElt of imageInputElts) {
    imageInputElt.insertAdjacentHTML(
      "beforebegin",
      `
      <div class="${imageInputElt.id} image-preview avatar mb-3">
        <div class="w-24 rounded-full">
          <img src="${imageInputElt.dataset.fileUrl}" />
        </div>
      </div>
      `
    );

    const imageErrorListElt = document.querySelector(
      `.${imageInputElt.id}.errorlist`
    ) as HTMLUListElement;

    const imagePreviewElt = document.querySelector(
      `.${imageInputElt.id}.image-preview img`
    ) as HTMLImageElement;

    imageInputElt.addEventListener("change", () => {
      if (imageInputElt.files == null) {
        return;
      }

      const file = imageInputElt.files[0];
      if (!file.type.startsWith("image/")) {
        const errorListItemElt = document.createElement("li");
        errorListItemElt.textContent = `${imageInputElt.name} must be an image.`;
        imageErrorListElt.replaceChildren(errorListItemElt);

        imagePreviewElt.src = templateData.notAnImage ?? "";
        return;
      }

      imageErrorListElt.textContent = "";

      const reader = new FileReader();
      reader.onload = () => {
        imagePreviewElt.src = reader.result as string;
      };
      reader.readAsDataURL(file);
    });
  }
});
