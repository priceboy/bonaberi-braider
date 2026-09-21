(function () {
  "use strict";

  var carousel = document.querySelector("[data-carousel]");
  if (carousel) {
    var cards = Array.prototype.slice.call(carousel.querySelectorAll("[data-slide]"));
    var caption = document.querySelector("[data-carousel-caption]");
    var dots = Array.prototype.slice.call(document.querySelectorAll("[data-dot]"));
    var n = cards.length;
    var active = 0;

    var captionCategory = caption.querySelector("[data-caption-category]");
    var captionTitle = caption.querySelector("[data-caption-title]");
    var captionLink = caption.querySelector("[data-caption-link]");

    function layout() {
      cards.forEach(function (card, index) {
        var offset = index - active;
        var pos = ((offset % n) + n) % n;
        var displayOffset = pos > Math.floor(n / 2) ? pos - n : pos;
        card.style.setProperty("--x", displayOffset);
        card.style.setProperty("--abs", Math.abs(displayOffset));
        card.setAttribute("aria-current", index === active ? "true" : "false");
      });
      var slide = cards[active];
      captionCategory.textContent = slide.getAttribute("data-category");
      captionTitle.textContent = slide.getAttribute("data-title");
      captionLink.setAttribute("href", slide.getAttribute("data-href"));
      dots.forEach(function (dot, index) {
        dot.classList.toggle("active", index === active);
      });
    }

    var AUTOPLAY_MS = 4500;
    var interval = null;

    function play() {
      stop();
      interval = setInterval(function () {
        active = (active + 1) % n;
        layout();
      }, AUTOPLAY_MS);
    }

    function stop() {
      if (interval) {
        clearInterval(interval);
        interval = null;
      }
    }

    function restart() {
      if (interval) {
        play();
      }
    }

    cards.forEach(function (card, index) {
      card.addEventListener("click", function () {
        active = index;
        layout();
        restart();
      });
    });
    dots.forEach(function (dot, index) {
      dot.addEventListener("click", function () {
        active = index;
        layout();
        restart();
      });
    });

    carousel.addEventListener("mouseenter", stop);
    carousel.addEventListener("mouseleave", play);
    carousel.addEventListener("touchstart", stop, { passive: true });
    carousel.addEventListener("touchend", play);

    layout();
    if (!window.matchMedia || !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      play();
    }
  }

  var filters = Array.prototype.slice.call(document.querySelectorAll("[data-filter]"));
  var galleryItems = Array.prototype.slice.call(document.querySelectorAll("[data-category]"));
  if (filters.length && galleryItems.length) {
    filters.forEach(function (button) {
      button.addEventListener("click", function () {
        filters.forEach(function (b) {
          b.classList.remove("selected");
        });
        button.classList.add("selected");
        var selected = button.getAttribute("data-filter");
        galleryItems.forEach(function (item) {
          item.style.display =
            selected === "All" || item.getAttribute("data-category") === selected ? "" : "none";
        });
      });
    });
  }
})();