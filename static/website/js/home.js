(function () {
    const portraits = Array.from(document.querySelectorAll("[data-portrait]"));
    if (portraits.length < 2) return;

    const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
    if (mediaQuery.matches) return;

    let current = 0;
    let intervalId = null;
    const interval = 3200;

    function stopRotation() {
        if (intervalId !== null) {
            window.clearInterval(intervalId);
            intervalId = null;
        }
    }

    function startRotation() {
        if (intervalId !== null || document.hidden || mediaQuery.matches) return;
        intervalId = window.setInterval(() => {
            portraits[current].classList.remove("is-active");
            current = (current + 1) % portraits.length;
            portraits[current].classList.add("is-active");
        }, interval);
    }

    document.addEventListener("visibilitychange", () => {
        if (document.hidden) {
            stopRotation();
        } else {
            startRotation();
        }
    });

    mediaQuery.addEventListener?.("change", () => {
        if (mediaQuery.matches) {
            stopRotation();
            portraits.forEach((portrait, index) => {
                portrait.classList.toggle("is-active", index === current);
            });
        } else {
            startRotation();
        }
    });

    startRotation();
})();
