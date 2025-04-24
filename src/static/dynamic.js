document.addEventListener("DOMContentLoaded", () => {
    const starContainer = document.getElementById("star-rating");
    const ratingInput = document.getElementById("rating-value");
  
    let selectedRating = 0;
  
    for (let i = 1; i <= 5; i++) {
      const star = document.createElement("span");
      star.classList.add("fa", "fa-star");
      star.dataset.value = i;
  
      star.addEventListener("mouseover", () => highlightStars(i));
      star.addEventListener("mouseout", () => highlightStars(selectedRating));
      star.addEventListener("click", () => {
        selectedRating = i;
        ratingInput.value = i;
        highlightStars(i);
      });
  
      starContainer.appendChild(star);
    }
  
    function highlightStars(rating) {
      const stars = document.querySelectorAll("#star-rating .fa-star");
      stars.forEach(star => {
        star.classList.remove("hover", "selected");
        if (parseInt(star.dataset.value) <= rating) {
          star.classList.add("selected");
        }
      });
    }
}
);
  



function previewImage(event) {
    const input = event.target;
    const preview = document.getElementById('imagePreview');

    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function (e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
        };
        reader.readAsDataURL(input.files[0]);
    }
}

document.getElementById('fileInput').addEventListener('change', previewImage);


function setValue(value) {
    // Get the input field by its ID
    const inputField = document.getElementById("menu-input");
    // Set the value of the input field to the clicked menu item
    inputField.value = value;
    const dropdownContent = document.querySelector(".dropdown .content");
    dropdownContent.style.display = "none";
}