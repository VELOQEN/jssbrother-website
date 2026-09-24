(() => {

  const routes = {
    "colored": "/products/colored/",
    "crystal": "/products/crystal/",
    "stylo": "/products/stylo/",
    "shamuk": "/products/shamuk/",
    "markfil": "/products/markfil/",

    "bobin": "/products/bobbin/",
    "bobbin": "/products/bobbin/",

    "solving": "/products/solving/",
    "dissolving": "/products/dissolving/",

    "sequence": "/products/sequence/",
    "sequence / cd": "/products/sequence/",
    "cd": "/products/sequence/",

    "needles": "/products/needles/",
    "polyester": "/products/polyester/",
    "fusing": "/products/fusing/",
    "nylon": "/products/nylon/",
    "panni": "/products/panni/",

    "spare parts": "/products/spare-parts/"
  };

  function clean(value){
    return String(value || "")
      .replace(/\s+/g," ")
      .trim()
      .toLowerCase();
  }

  document.addEventListener("click", event => {

    const grid = document.getElementById("productGrid");

    if(!grid || !grid.contains(event.target)){
      return;
    }

    const candidate = event.target.closest(
      "a,button,.product-card,.catalogue-card,.crystal-card,.product-item,.catalog-item"
    );

    if(!candidate){
      return;
    }

    const text = clean(candidate.textContent);

    let destination = null;

    for(const [label,url] of Object.entries(routes)){
      if(
        text === label ||
        text.startsWith(label + " ") ||
        text.includes("\n" + label)
      ){
        destination = url;
        break;
      }
    }

    if(!destination){
      return;
    }

    event.preventDefault();
    event.stopImmediatePropagation();

    window.location.href = destination;

  }, true);

})();
