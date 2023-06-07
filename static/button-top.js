let showOnPx = 100;
let backToTopButton = document.querySelector(".back-to-top");

let scrollContainer = () => {
    return document.documentElement || document.body;
  };

let goToTop= () => {
    document.body.scrollIntoView();
}


document.addEventListener("scroll", () => {
    if (scrollContainer().scrollTop > showOnPx) {
        backToTopButton.classList.remove("hidden")
      } else {
        backToTopButton.classList.add("hidden")
      }
});

backToTopButton.addEventListener("click", goToTop);