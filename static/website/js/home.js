(function () {
    const portraits = Array.from(document.querySelectorAll('[data-portrait]'));
    if (portraits.length === 0) {
        return;
    }

    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduceMotion) {
        // Keep only the first visible
        portraits.forEach((el, idx) => {
            if (idx !== 0) {
                el.classList.remove('is-active');
            } else {
                el.classList.add('is-active');
            }
        });
        return;
    }

    let current = 0;
    const interval = 3200;

    setInterval(() => {
        portraits[current].classList.remove('is-active');
        current = (current + 1) % portraits.length;
        portraits[current].classList.add('is-active');
    }, interval);
})();
