// assets/js/main.js  (fixed, robust version)
(function () {
  /* ========= Preloader ======== */
  const preloaders = document.querySelectorAll('#preloader');

  window.addEventListener('load', function () {
    if (preloaders && preloaders.length) {
      const el = document.getElementById('preloader');
      if (el) el.style.display = 'none';
    }
  });

  /* ========= Add Box Shadow in Header on Scroll ======== */
  window.addEventListener('scroll', function () {
    const header = document.querySelector('.header');
    if (!header) return; // guard
    if (window.scrollY > 0) {
      header.style.boxShadow = '0px 0px 30px 0px rgba(200, 208, 216, 0.30)';
    } else {
      header.style.boxShadow = 'none';
    }
  });

  /* ========= sidebar toggle ======== */
  const sidebarNavWrapper = document.querySelector(".sidebar-nav-wrapper");
  const mainWrapper = document.querySelector(".main-wrapper");
  const menuToggleButton = document.querySelector("#menu-toggle");
  const menuToggleButtonIcon = document.querySelector("#menu-toggle i");
  const overlay = document.querySelector(".overlay");

  // Only attach menu toggle if the button and sidebar exist
  if (menuToggleButton && sidebarNavWrapper && mainWrapper && overlay) {
    menuToggleButton.addEventListener("click", () => {
      sidebarNavWrapper.classList.toggle("active");
      overlay.classList.add("active");
      mainWrapper.classList.toggle("active");

      // safely check icon exists before toggling classes
      if (menuToggleButtonIcon) {
        if (document.body.clientWidth > 1200) {
          if (menuToggleButtonIcon.classList.contains("lni-chevron-left")) {
            menuToggleButtonIcon.classList.remove("lni-chevron-left");
            menuToggleButtonIcon.classList.add("lni-menu");
          } else {
            menuToggleButtonIcon.classList.remove("lni-menu");
            menuToggleButtonIcon.classList.add("lni-chevron-left");
          }
        } else {
          if (menuToggleButtonIcon.classList.contains("lni-chevron-left")) {
            menuToggleButtonIcon.classList.remove("lni-chevron-left");
            menuToggleButtonIcon.classList.add("lni-menu");
          }
        }
      }
    });

    overlay.addEventListener("click", () => {
      sidebarNavWrapper.classList.remove("active");
      overlay.classList.remove("active");
      mainWrapper.classList.remove("active");
    });
  } else {
    // If some elements missing — quietly skip (prevents runtime errors)
    // console.debug('menuToggle or sidebar elements not found; skipping sidebar handlers.');
  }

})();
