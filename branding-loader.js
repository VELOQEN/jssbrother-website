(() => {

  const WATERMARK_LOGO = "/images/brand/jss-brothers-logo.jpg";

  function productImage(img) {

    if (!img) return false;

    const src =
      (img.getAttribute("src") || "")
      .toLowerCase();

    return (
      src.includes("/images/products/") ||
      src.includes("images/products/")
    );
  }


  function crystalImage(img) {

    const src =
      (img.getAttribute("src") || "")
      .toLowerCase();

    return src.includes(
      "images/products/metallic-yarn/crystal/"
    );
  }


  function addWatermark(img) {

    if (!productImage(img)) return;

    /*
     * Crystal pictures already have the approved
     * watermark baked into the photograph.
     */
    if (crystalImage(img)) return;

    if (
      img.dataset.jssWatermarkApplied === "1"
    ) {
      return;
    }

    const parent = img.parentElement;

    if (!parent) return;

    img.dataset.jssWatermarkApplied = "1";

    if (
      window.getComputedStyle(parent).position
      === "static"
    ) {
      parent.style.position = "relative";
    }

    const mark =
      document.createElement("img");

    mark.src = WATERMARK_LOGO;
    mark.alt = "";
    mark.className =
      "jss-approved-watermark";

    mark.setAttribute(
      "aria-hidden",
      "true"
    );

    mark.style.position = "absolute";
    mark.style.right = "12px";
    mark.style.bottom = "12px";

    mark.style.width = "72px";
    mark.style.height = "auto";
    mark.style.maxWidth = "24%";

    mark.style.opacity = "0.42";

    mark.style.filter = "none";
    mark.style.pointerEvents = "none";

    mark.style.zIndex = "20";

    mark.style.borderRadius = "7px";

    mark.style.objectFit = "contain";

    mark.style.padding = "0";

    parent.appendChild(mark);
  }


  function scan(root = document) {

    if (
      root instanceof HTMLImageElement
    ) {
      addWatermark(root);
    }

    root
      .querySelectorAll?.("img")
      .forEach(addWatermark);
  }


  if (
    document.readyState === "loading"
  ) {

    document.addEventListener(
      "DOMContentLoaded",
      () => scan(document),
      { once: true }
    );

  } else {

    scan(document);

  }


  new MutationObserver(
    mutations => {

      mutations.forEach(
        mutation => {

          mutation.addedNodes.forEach(
            node => {

              if (
                !(node instanceof Element)
              ) {
                return;
              }

              scan(node);

            }
          );

        }
      );

    }
  ).observe(
    document.documentElement,
    {
      childList: true,
      subtree: true
    }
  );

})();
