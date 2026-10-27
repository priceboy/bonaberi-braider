(function () {
    // Position carousel items around a semicircle
    const track = document.getElementById('carouselTrack');
    const items = Array.from(document.querySelectorAll('[data-carousel-item]'));
    if (track && items.length > 0) {
        const radius = window.innerWidth < 640 ? 130 : window.innerWidth < 900 ? 150 : 190;
        items.forEach((item, idx) => {
            const angle = (idx / items.length) * 180; // 180 degree semicircle
            item.style.setProperty('--angle', angle + 'deg');
            item.style.setProperty('--radius', radius + 'px');
            item.style.transform = `translate(-50%, -50%) rotate(${angle}deg) translateY(-${radius}px) rotate(-${angle}deg)`;
        });
    }

    // Carousel caption
    const carouselCategory = document.getElementById('carouselCategory');
    const carouselTitle = document.getElementById('carouselTitle');
    if (items.length > 0 && carouselCategory && carouselTitle) {
        const first = items[0];
        carouselCategory.textContent = first.dataset.category || '';
        carouselTitle.textContent = first.dataset.title || '';
        items.forEach(item => {
            item.addEventListener('click', () => {
                carouselCategory.textContent = item.dataset.category || '';
                carouselTitle.textContent = item.dataset.title || '';
                openViewer({ src: item.dataset.src, category: item.dataset.category, title: item.dataset.title, id: item.dataset.id });
            });
        });
    }

    // Gallery items
    const galleryItems = Array.from(document.querySelectorAll('[data-gallery-item]'));
    galleryItems.forEach(item => {
        item.addEventListener('click', () => {
            openViewer({ src: item.dataset.src, category: item.dataset.category, title: item.dataset.title, id: item.dataset.id });
        });
    });

    // Viewer
    const viewer = document.getElementById('imageViewer');
    const viewerImage = document.getElementById('viewerImage');
    const viewerCategory = document.getElementById('viewerCategory');
    const viewerTitle = document.getElementById('viewerTitle');
    const viewerCounter = document.getElementById('viewerCounter');
    const viewerClose = document.getElementById('viewerClose');
    const viewerPrev = document.getElementById('viewerPrev');
    const viewerNext = document.getElementById('viewerNext');
    const body = document.body;

    let currentList = [];
    let currentIndex = 0;

    function buildCategoryList(selectedCategory, selectedId) {
        const list = [];
        // Include all items (gallery + carousel) that share category
        [...galleryItems, ...items].forEach(el => {
            if (el.dataset.category === selectedCategory) {
                list.push({
                    src: el.dataset.src,
                    category: el.dataset.category,
                    title: el.dataset.title,
                    id: el.dataset.id
                });
            }
        });
        // Remove duplicates by src+id if any
        const unique = [];
        const seen = new Set();
        list.forEach(x => {
            const key = x.id + '|' + x.src;
            if (!seen.has(key)) {
                seen.add(key);
                unique.push(x);
            }
        });
        // Sort by DOM order approximation - keep original order
        currentList = unique;
        currentIndex = unique.findIndex(x => x.id === selectedId && x.src);
        if (currentIndex < 0 && unique.length > 0) currentIndex = 0;
    }

    function renderViewer() {
        if (currentList.length === 0) return;
        const item = currentList[currentIndex];
        viewerImage.src = item.src;
        viewerImage.alt = item.title || '';
        viewerCategory.textContent = item.category || '';
        viewerTitle.textContent = item.title || '';
        viewerCounter.textContent = (currentIndex + 1) + ' of ' + currentList.length;
    }

    function openViewer(data) {
        buildCategoryList(data.category, data.id);
        viewer.classList.add('is-open');
        body.classList.add('viewer-open');
        body.style.overflow = 'hidden';
        renderViewer();
        // Focus management
        viewerClose.focus();
    }

    function closeViewer() {
        viewer.classList.remove('is-open');
        body.classList.remove('viewer-open');
        body.style.overflow = '';
    }

    viewerClose.addEventListener('click', closeViewer);
    document.addEventListener('keydown', (e) => {
        if (!viewer.classList.contains('is-open')) return;
        if (e.key === 'Escape') {
            closeViewer();
        } else if (e.key === 'ArrowLeft') {
            currentIndex = (currentIndex - 1 + currentList.length) % currentList.length;
            renderViewer();
        } else if (e.key === 'ArrowRight') {
            currentIndex = (currentIndex + 1) % currentList.length;
            renderViewer();
        }
    });

    viewerPrev.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + currentList.length) % currentList.length;
        renderViewer();
    });
    viewerNext.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % currentList.length;
        renderViewer();
    });

    // Touch swipe
    let touchStartX = 0;
    let touchEndX = 0;
    viewerImage.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });
    viewerImage.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        if (Math.abs(touchEndX - touchStartX) > 60) {
            if (touchEndX < touchStartX) {
                currentIndex = (currentIndex + 1) % currentList.length;
            } else {
                currentIndex = (currentIndex - 1 + currentList.length) % currentList.length;
            }
            renderViewer();
        }
    }, { passive: true });
})();
