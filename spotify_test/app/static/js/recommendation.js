document.addEventListener("DOMContentLoaded", function () {
    const toggleButton = document.getElementById("toggle-genre-btn");
    const moreGenres = document.getElementById("more-genres");

    if (toggleButton && moreGenres) {
        toggleButton.addEventListener("click", function () {
            moreGenres.style.display = "block";
            toggleButton.style.display = "none";
        });
    }
});