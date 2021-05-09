
// Let's define a simple script to animate the hamburger toggler
// in the navbar when clicked. Also make some adjustments to our
// navbar when expanding and collapsing.

// Grab our toggler
const menuBtn = document.querySelector('.navbar-toggler');
// Grab our links
var navLinks = document.querySelectorAll('.nav-link');
// Start the navbar as being closed
let menuOpen = false;

// Listen for the button click event
menuBtn.addEventListener('click', () => {
  if(!menuOpen) {
    // Add the "open" class to our toggler
    menuBtn.classList.add('open');
    // Add the "squash" class to our navlinks so the link hover bar 
    // is roughly the same length as the link text rather than sig-
    // nificantly longer
    for (var i = 0; i < navLinks.length; ++i) {
      navLinks[i].classList.add('squash');
    };
    // Toggle state to open
    menuOpen = true;
  } else {
    // Remove the "open" and "squash" classes
    menuBtn.classList.remove('open');
    for (var i = 0; i < navLinks.length; ++i) {
      navLinks[i].classList.remove('squash');
    };
    // Toggle state to closed
    menuOpen = false;
  }
});