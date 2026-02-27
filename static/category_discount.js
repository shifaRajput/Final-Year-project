// Filter Toggle
    /*const filterBtn = document.getElementById('filterBtn');
    const filterDropdown = document.getElementById('filterDropdown');

    filterBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        filterDropdown.classList.toggle('active');
    });

    window.onclick = (event) => {
        if (filterBtn && !filterBtn.contains(event.target) && !filterDropdown.contains(event.target)) {
            filterDropdown.classList.remove('active');
        }
    };*/
    const filterBtn = document.getElementById('filterBtn');
const filterDropdown = document.getElementById('filterDropdown');

if (filterBtn && filterDropdown) {
    filterBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        filterDropdown.classList.toggle('active');
    });

    window.onclick = (event) => {
        if (!filterBtn.contains(event.target) && !filterDropdown.contains(event.target)) {
            filterDropdown.classList.remove('active');
        }
    };
}

    // Back link
    document.querySelector(".back-btn").addEventListener("click", () => {
      window.history.back();
    });

    // Heart Icon
    document.addEventListener('click', (e) => {
        if(e.target.classList.contains('heart-icon')) {
            e.target.classList.toggle('fas');
            e.target.classList.toggle('far');
            e.target.classList.toggle('active');
        }
    });

    // Filters
    const applyBtn = document.getElementById('applyFilters');
    const searchInput = document.getElementById('searchInput');

    function runFilters() {
        const query = searchInput.value.toLowerCase();
        const minP = parseFloat(document.getElementById('minPrice').value) || 0;
        const maxP = parseFloat(document.getElementById('maxPrice').value) || Infinity;
        const selectedBrands = Array.from(document.querySelectorAll('.brand-filter:checked')).map(cb => cb.value.toLowerCase());

        document.querySelectorAll('.product-card').forEach(card => {
            const title = card.querySelector('h3').innerText.toLowerCase();
            const price = parseFloat(card.dataset.price);
            const brand = card.dataset.brand.toLowerCase();

            const matches = title.includes(query) && 
                            price >= minP && price <= maxP && 
                            (selectedBrands.length === 0 || selectedBrands.includes(brand));
            
            card.style.display = matches ? "block" : "none";
        });
    }

    searchInput.addEventListener('input', runFilters);
    applyBtn.onclick = () => {
        runFilters();
        filterDropdown.classList.remove('active');
    };

    // Slider
    const sliders = document.querySelectorAll('.slider-container');
    sliders.forEach(slider => {
        let isDown = false;
        let startX;
        let scrollLeft;
        slider.addEventListener('mousedown', (e) => {
            isDown = true;
            startX = e.pageX - slider.offsetLeft;
            scrollLeft = slider.scrollLeft;
        });
        slider.addEventListener('mouseleave', () => isDown = false);
        slider.addEventListener('mouseup', () => isDown = false);
        slider.addEventListener('mousemove', (e) => {
            if(!isDown) return;
            e.preventDefault();
            const x = e.pageX - slider.offsetLeft;
            const walk = (x - startX) * 2;
            slider.scrollLeft = scrollLeft - walk;
        });
    });

   // Add to Cart Animation
    document.querySelectorAll('.button').forEach(button => {
      button.addEventListener('click', e => {
          if (!button.classList.contains('loading')) {
             button.classList.add('loading');
             setTimeout(() => button.classList.remove('loading'), 3700);
           }
           e.preventDefault();
        });
    });
