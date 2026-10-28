(function () {
    const track = document.getElementById("carouselTrack");
    const items = Array.from(document.querySelectorAll("[data-carousel-item]"));
    const galleryItems = Array.from(document.querySelectorAll("[data-gallery-item]"));
    const viewer = document.getElementById("imageViewer");
    const viewerImage = document.getElementById("viewerImage");
    const viewerCategory = document.getElementById("viewerCategory");
    const viewerTitle = document.getElementById("viewerTitle");
    const viewerCounter = document.getElementById("viewerCounter");
    const viewerClose = document.getElementById("viewerClose");
    const viewerPrev = document.getElementById("viewerPrev");
    const viewerNext = document.getElementById("viewerNext");
    const carouselCategory = document.getElementById("carouselCategory");
    const carouselTitle = document.getElementById("carouselTitle");

    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
    function positionCarousel() {
        if (!track || !items.length) return;
        const radius = window.innerWidth < 640 ? Math.min(128, window.innerWidth * 0.28) : window.innerWidth < 900 ? 150 : 190;
        items.forEach((item, index) => {
            const ratio = items.length === 1 ? 0.5 : index / (items.length - 1);
            const angle = -90 + ratio * 180;
            item.style.setProperty("--angle", angle + "deg");
            item.style.setProperty("--radius", radius + "px");
        });
    }
    positionCarousel();
    window.addEventListener("resize", positionCarousel, { passive: true });
    if (reduceMotion.matches && track) track.style.animation = "none";

    if (items.length && carouselCategory && carouselTitle) {
        carouselCategory.textContent = items[0].dataset.category || "";
        carouselTitle.textContent = items[0].dataset.title || "";
    }

    let currentList = [];
    let currentIndex = 0;
    let lastTrigger = null;
    let scrollY = 0;
    let previousBodyStyles = {};

    function buildCategoryList(selectedCategory, selectedId) {
        const seen = new Set();
        currentList = [...galleryItems, ...items]
            .filter((element) => element.dataset.category === selectedCategory)
            .map((element) => ({
                src: element.dataset.src,
                category: element.dataset.category,
                title: element.dataset.title,
                id: element.dataset.id,
            }))
            .filter((entry) => {
                const key = entry.id + "|" + entry.src;
                if (!entry.src || seen.has(key)) return false;
                seen.add(key);
                return true;
            });
        currentIndex = currentList.findIndex((entry) => entry.id === selectedId);
        if (currentIndex < 0) currentIndex = 0;
    }

    function renderViewer() {
        if (!currentList.length) return;
        const entry = currentList[currentIndex];
        viewerImage.src = entry.src;
        viewerImage.alt = entry.title || "Hairstyle";
        viewerCategory.textContent = entry.category || "";
        viewerTitle.textContent = entry.title || "";
        viewerCounter.textContent = `${currentIndex + 1} of ${currentList.length}`;
        const singleImage = currentList.length < 2;
        viewerPrev.disabled = singleImage;
        viewerNext.disabled = singleImage;
    }

    function openViewer(trigger) {
        if (!viewer || !trigger.dataset.src) return;
        lastTrigger = trigger;
        buildCategoryList(trigger.dataset.category, trigger.dataset.id);
        if (!currentList.length) return;

        scrollY = window.scrollY;
        previousBodyStyles = {
            position: document.body.style.position,
            top: document.body.style.top,
            width: document.body.style.width,
            overflow: document.body.style.overflow,
        };
        document.body.style.position = "fixed";
        document.body.style.top = `-${scrollY}px`;
        document.body.style.width = "100%";
        document.body.style.overflow = "hidden";
        viewer.classList.add("is-open");
        viewer.setAttribute("aria-hidden", "false");
        document.body.classList.add("viewer-open");
        renderViewer();
        viewerClose.focus();
    }

    function closeViewer() {
        if (!viewer || !viewer.classList.contains("is-open")) return;
        viewer.classList.remove("is-open");
        viewer.setAttribute("aria-hidden", "true");
        document.body.classList.remove("viewer-open");
        Object.entries(previousBodyStyles).forEach(([property, value]) => {
            document.body.style[property] = value;
        });
        window.scrollTo(0, scrollY);
        if (lastTrigger && typeof lastTrigger.focus === "function") lastTrigger.focus();
    }

    items.forEach((item) => {
        item.addEventListener("click", () => {
            if (carouselCategory && carouselTitle) {
                carouselCategory.textContent = item.dataset.category || "";
                carouselTitle.textContent = item.dataset.title || "";
            }
            openViewer(item);
        });
    });
    galleryItems.forEach((item) => item.addEventListener("click", () => openViewer(item)));

    if (!viewer || !viewerClose || !viewerPrev || !viewerNext || !viewerImage) return;

    viewerClose.addEventListener("click", closeViewer);
    viewerPrev.addEventListener("click", () => {
        if (!currentList.length) return;
        currentIndex = (currentIndex - 1 + currentList.length) % currentList.length;
        renderViewer();
    });
    viewerNext.addEventListener("click", () => {
        if (!currentList.length) return;
        currentIndex = (currentIndex + 1) % currentList.length;
        renderViewer();
    });

    document.addEventListener("keydown", (event) => {
        if (!viewer.classList.contains("is-open")) return;
        if (event.key === "Escape") {
            event.preventDefault();
            closeViewer();
            return;
        }
        if (event.key === "ArrowLeft" && currentList.length > 1) {
            event.preventDefault();
            currentIndex = (currentIndex - 1 + currentList.length) % currentList.length;
            renderViewer();
            return;
        }
        if (event.key === "ArrowRight" && currentList.length > 1) {
            event.preventDefault();
            currentIndex = (currentIndex + 1) % currentList.length;
            renderViewer();
            return;
        }
        if (event.key === "Tab") {
            const controls = [viewerClose, viewerPrev, viewerNext].filter((control) => !control.disabled);
            const first = controls[0];
            const last = controls[controls.length - 1];
            if (event.shiftKey && document.activeElement === first) {
                event.preventDefault();
                last.focus();
            } else if (!event.shiftKey && document.activeElement === last) {
                event.preventDefault();
                first.focus();
            }
        }
    });

    let touchStartX = 0;
    let touchStartY = 0;
    viewerImage.addEventListener("touchstart", (event) => {
        const touch = event.changedTouches[0];
        touchStartX = touch.screenX;
        touchStartY = touch.screenY;
    }, { passive: true });
    viewerImage.addEventListener("touchend", (event) => {
        const touch = event.changedTouches[0];
        const deltaX = touch.screenX - touchStartX;
        const deltaY = touch.screenY - touchStartY;
        if (Math.abs(deltaX) < 60 || Math.abs(deltaX) <= Math.abs(deltaY) || currentList.length < 2) return;
        currentIndex = deltaX < 0
            ? (currentIndex + 1) % currentList.length
            : (currentIndex - 1 + currentList.length) % currentList.length;
        renderViewer();
    }, { passive: true });

})();
