/**
 * Intelligent Movie Search & Recommendation System
 * Client-Side Interactions & UI Handlers
 */

document.addEventListener('DOMContentLoaded', () => {
  initMobileNav();
  initLiveSearch();
  initImageFallbacks();
  initFilterAutoSubmit();
  initKeyboardShortcuts();
});

/* Mobile Navigation Drawer */
function initMobileNav() {
  const toggleBtn = document.getElementById('menuToggle');
  const mobileNav = document.getElementById('mobileNav');

  if (toggleBtn && mobileNav) {
    toggleBtn.addEventListener('click', () => {
      mobileNav.classList.toggle('open');
      const isOpen = mobileNav.classList.contains('open');
      toggleBtn.innerHTML = isOpen ? '&times;' : '&#9776;';
    });
  }
}

/* Debounced Live Search Autocomplete */
function initLiveSearch() {
  const searchInput = document.getElementById('searchInput');
  const dropdown = document.getElementById('autocompleteDropdown');
  if (!searchInput || !dropdown) return;

  let debounceTimer = null;

  searchInput.addEventListener('input', (e) => {
    const query = e.target.value.trim();
    clearTimeout(debounceTimer);

    if (query.length < 2) {
      dropdown.style.display = 'none';
      dropdown.innerHTML = '';
      return;
    }

    debounceTimer = setTimeout(() => {
      fetch(`/api/suggest?q=${encodeURIComponent(query)}`)
        .then(res => res.json())
        .then(data => {
          if (!data || data.length === 0) {
            dropdown.style.display = 'none';
            dropdown.innerHTML = '';
            return;
          }

          dropdown.innerHTML = data.map(item => `
            <a href="/movie/${item.id}" class="autocomplete-item">
              <img src="${item.poster_url}" alt="${item.title}" onerror="this.onerror=null; this.src='/static/images/fallback.svg';">
              <div class="autocomplete-info">
                <h4>${item.title} (${item.year})</h4>
                <p>${item.genre} &bull; <span style="color:#00e676">${item.category}</span></p>
              </div>
            </a>
          `).join('');

          dropdown.style.display = 'block';
        })
        .catch(err => {
          console.error("Autocomplete error:", err);
          dropdown.style.display = 'none';
        });
    }, 250);
  });

  // Close dropdown on outside click
  document.addEventListener('click', (e) => {
    if (!searchInput.contains(e.target) && !dropdown.contains(e.target)) {
      dropdown.style.display = 'none';
    }
  });
}

/* Robust Dual-Stage Image Fallbacks */
function initImageFallbacks() {
  const genericFallbackUrl = '/static/images/fallback.svg';
  const images = document.querySelectorAll('img.poster-img, .movie-poster-large img');

  images.forEach(img => {
    img.addEventListener('error', function () {
      const currentSrc = this.src;
      // If a .jpg poster fails to render, try the movie's own customized SVG poster
      if (currentSrc.includes('/static/images/poster_') && currentSrc.endsWith('.jpg')) {
        this.src = currentSrc.replace('.jpg', '.svg');
      } else if (!currentSrc.endsWith(genericFallbackUrl)) {
        this.src = genericFallbackUrl;
      }
    });
  });
}

/* Filter Bar Auto-Submit */
function initFilterAutoSubmit() {
  const filterSelects = document.querySelectorAll('.filter-bar select');
  filterSelects.forEach(select => {
    select.addEventListener('change', function () {
      const form = this.closest('form');
      if (form) {
        form.submit();
      }
    });
  });
}

/* Keyboard Shortcut: Press '/' to focus search */
function initKeyboardShortcuts() {
  window.addEventListener('keydown', (e) => {
    if (e.key === '/' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
      const searchInput = document.getElementById('searchInput');
      if (searchInput) {
        e.preventDefault();
        searchInput.focus();
        searchInput.select();
      }
    }
  });
}
