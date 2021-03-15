const menuBtn = document.querySelector('.navbar-toggler');
var navLinks = document.querySelectorAll('.nav-link');
let menuOpen = false;
menuBtn.addEventListener('click', () => {
  if(!menuOpen) {
    menuBtn.classList.add('open');
    for (var i = 0; i < navLinks.length; ++i) {
      navLinks[i].classList.add('squash');
    };
    menuOpen = true;
  } else {
    menuBtn.classList.remove('open');
    for (var i = 0; i < navLinks.length; ++i) {
      navLinks[i].classList.remove('squash');
    };
    menuOpen = false;
  }
});