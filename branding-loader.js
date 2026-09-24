(() => {

  /*
   * JSS BROTHERS — CENTRAL PRODUCT BRANDING
   *
   * Product data continues using:
   * images/products/...
   *
   * The website automatically displays:
   * images/products-branded/...
   *
   * Therefore future catalogue products only need their normal
   * product image path. No individual watermark HTML is required.
   */

  const CONFIG = {
    enabled: true,
    sourcePrefix: "/images/products/",
    brandedPrefix: "/images/products-branded/"
  };

  window.JSS_PRODUCT_BRANDING = CONFIG;

  if (!CONFIG.enabled) return;


  function normalise(url) {
    try {
      return new URL(url, window.location.href);
    } catch {
      return null;
    }
  }


  function brandImage(img) {

    if (!img || img.dataset.jssBrandChecked === "1") {
      return;
    }

    const url = normalise(
      img.getAttribute("src") || ""
    );

    if (!url) return;

    const path = url.pathname;

    if (
      !path.startsWith(CONFIG.sourcePrefix) ||
      path.startsWith(CONFIG.brandedPrefix)
    ) {
      return;
    }

    const original =
      path + url.search;

    const branded =
      CONFIG.brandedPrefix +
      path.slice(CONFIG.sourcePrefix.length) +
      url.search;

    img.dataset.jssBrandChecked = "1";
    img.dataset.jssOriginalSrc = original;

    img.addEventListener(
      "error",
      function fallback() {

        if (
          this.dataset.jssFallbackUsed === "1"
        ) return;

        this.dataset.jssFallbackUsed = "1";
        this.src =
          this.dataset.jssOriginalSrc;

      },
      { once:true }
    );

    img.src = branded;
  }


  function scan(root=document) {

    root
      .querySelectorAll?.('img[src]')
      .forEach(brandImage);

  }


  scan();


  new MutationObserver(mutations => {

    for (const mutation of mutations) {

      for (const node of mutation.addedNodes) {

        if (!(node instanceof Element)) {
          continue;
        }

        if (node.matches?.("img[src]")) {
          brandImage(node);
        }

        scan(node);
      }
    }

  }).observe(
    document.documentElement,
    {
      childList:true,
      subtree:true
    }
  );

})();
