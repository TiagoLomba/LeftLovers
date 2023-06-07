const imagesc = ["../static/images/food_fruit.png", "../static/images/mealPrep.png", "../static/images/heart_morango.png", "../static/images/foodBowl.png", "../static/images/mealPrep2.png"];

let currentImageCounter = 0;
const nextImageDelay = 3000;

img = document.querySelector(".slideshow-img");
document.slideshow.src = imagesc[currentImageCounter];


setInterval(nextImage, nextImageDelay);

function nextImage(){
    currentImageCounter = (currentImageCounter+1) % imagesc.length;
    document.slideshow.src = imagesc[currentImageCounter];
};