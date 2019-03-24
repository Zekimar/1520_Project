var slideIndex = 0;
var wait_gate = true;
var stuff = [];
get_stuff();

function write_stuff()
{
    console.log("write_stuff!");
    console.log(stuff[0][0]);
    build_slides(stuff); 
}

function get_stuff_helper(response)
{
    console.log("call_back!")
    stuff = response.dump;
    write_stuff();
}

function get_stuff()
{
    post_retrieve('/post_retrieve',get_stuff_helper);
}



function build_slides(stuff)
{
  var slide_area = document.getElementById("slide_area");
  var dot_area = document.getElementById("dot_area");
  var new_slide;
  var new_dot;
  for(let i = 0; i < stuff.length; i++)
  {
    new_slide = build_slide(stuff[i], i+1);
    slide_area.appendChild(new_slide);

    new_dot = build_dot(i+1);
    dot_area.appendChild(new_dot);
  }

  showSlides();
}

function build_slide(attributes, num)
{
   var new_slide = document.createElement("div");
   new_slide.classList.add("mySlides");
   new_slide.classList.add("fade");

   var count_display = document.createElement("div");
   count_display.classList.add("numbertext");
   count_display.innerHTML = num.toString() + " / " + stuff.length.toString();

   var title = document.createElement("div");
   title.classList.add("title_text");
   title.innerHTML = attributes[0];

   var new_img = document.createElement("img");
   new_img.src = attributes[2];
   new_img.style = "width:100%";
   new_img.onclick = function() {load_page(attributes[0],attributes[1]);};


   new_slide.appendChild(count_display);
   new_slide.appendChild(title);
   new_slide.appendChild(new_img);
   return new_slide;
}

function build_dot(num)
{
  var new_dot = document.createElement("span");
  new_dot.classList.add("dot");
  new_dot.onclick = function() {currentSlide(num); };
  return new_dot;
}

function currentSlide(n)
{
  slideIndex = n-1;
  wait_gate = false;
  arr = ["movie 1", "movie 2", "movie 3"];

  var i;
  var slides = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("dot");
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";  
  }
  slideIndex++;
  if (slideIndex > slides.length) {slideIndex = 1}    
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";  
  dots[slideIndex-1].className += " active";
  wait_gate = false;

}

function showSlides() {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("dot");
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";  
  }
  slideIndex++;
  if (slideIndex > slides.length) {slideIndex = 1}    
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";  
  dots[slideIndex-1].className += " active";
  wait_gate = true;
  setTimeout(repeat, 3000); // Change image every 2 seconds
}


function repeat()
{
  if(wait_gate)
  {
    showSlides();
  }
  else
  {
    wait_gate = true;
    setTimeout(repeat,3000);
  }
}