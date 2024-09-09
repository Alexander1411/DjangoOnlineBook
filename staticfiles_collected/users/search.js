const searchInputWrapper = document.querySelector(".search-input-wrapper");
const searchInput = document.querySelector(".search-input input");
const searchIcon = document.querySelector(".search-icon i");
const closeIcon = document.querySelector(".search-input i ");

searchIcon.addEventListener("click", () => {
  searchIcon.parentElement.classList.add("change");
  searchInputWrapper.classList.add("change");

  setTimeout(() => {
    searchInput.focus();
  }, 1000);
});

closeIcon.addEventListener("click", () => {
  searchIcon.parentElement.classList.remove("change");
  searchInputWrapper.classList.remove("change");
});

/* Section Nav */
function navFunction() {
  const containerDefault = document.querySelector(".container-nav");
  document
    .querySelector(".open-navbar-icon-main")
    .addEventListener("click", () => {
      containerDefault.classList.add("change-main");
    });
  document
    .querySelector(".close-navbar-icon-main")
    .addEventListener("click", () => {
      containerDefault.classList.remove("change-main");
    });

  const colors = ["#a4b0be", "#57606f", "#747d8c", "#2f3542", "#ced6e0"];

  let i = 0;

  Array.from(document.querySelectorAll(".nav-link-main")).forEach((item) => {
    item.style.cssText = `background-color: ${colors[i++]}`;
  });
}
navFunction();
