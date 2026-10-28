(function () {
    const portraits = Array.from(document.querySelectorAll("[data-portrait]"));
    if (portraits.length < 2) return;

    const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
    let current = Math.max(0, portraits.findIndex((portrait) => portrait.classList.contains("is-active")));
    let intervalId = null;
    const interval = 3200;

    function stopRotation() {
        if (intervalId !== null) {
            window.clearInterval(intervalId);
            intervalId = null;
        }
    }

    function showCurrentPortrait() {
        portraits.forEach((portrait, index) => {
            portrait.classList.toggle("is-active", index === current);
        });
    }

    function startRotation() {
        if (intervalId !== null || document.hidden || mediaQuery.matches) return;
        intervalId = window.setInterval(() => {
            current = (current + 1) % portraits.length;
            showCurrentPortrait();
        }, interval);
    }

    document.addEventListener("visibilitychange", () => {
        if (document.hidden) stopRotation();
        else startRotation();
    });

    mediaQuery.addEventListener?.("change", () => {
        if (mediaQuery.matches) stopRotation();
        else startRotation();
    });

    showCurrentPortrait();
    startRotation();
})();
