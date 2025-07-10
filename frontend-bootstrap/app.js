// Auto-detect API URL based on environment
const API_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:8000/products'
  : 'https://jewelery-wbda.onrender.com/products'; // Backend Render URL'ini buraya ekleyeceksin

document.addEventListener('DOMContentLoaded', () => {
  fetchProducts();
});

function fetchProducts() {
  fetch(API_URL)
    .then(res => {
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}: ${res.statusText}`);
      }
      return res.json();
    })
    .then(data => {
      const products = Array.isArray(data) ? data : (data.products || []);
      if (products.length === 0) {
        document.querySelector('#product-swiper').innerHTML = `<div class='text-warning text-center p-4'>Henüz ürün bulunamadı.</div>`;
        return;
      }
      renderProducts(products);
    })
    .catch(err => {
      console.error('API Error:', err);
      document.querySelector('#product-swiper').innerHTML = `<div class='text-danger text-center p-4'>Ürünler yüklenemedi: ${err.message}</div>`;
    });
}

function renderProducts(products) {
  const colorKeys = ['yellow', 'white', 'rose'];
  const colorNames = {
    yellow: 'Yellow Gold',
    white: 'White Gold',
    rose: 'Rose Gold'
  };
  const colorHex = {
    yellow: '#E6CA97',
    white: '#D9D9D9',
    rose: '#E1A4A9'
  };
  const slides = products.map((product, idx) => {
    const popularity = product.popularityScore !== undefined ? product.popularityScore : (product.popularity !== undefined ? product.popularity/100 : 0);
    return `
      <div class="swiper-slide">
        <div class="card product-card mb-4" data-product-idx="${idx}">
          <div class="product-img-box">
            <img src="${product.images ? product.images.yellow : ''}" class="card-img-top product-img" alt="${product.name}" data-product-idx="${idx}">
          </div>
          <div class="card-body">
            <div class="product-title">${product.name}</div>
            <div class="product-price">$${product.price ? product.price.toFixed(2) : ''} USD</div>
            <div class="color-picker d-flex align-items-center my-2">
              ${colorKeys.map(color => `
                <button class="color-btn${color === 'yellow' ? ' active' : ''}" style="background:${colorHex[color]}" title="${colorNames[color]}" data-color="${color}" data-product-idx="${idx}"></button>
              `).join('')}
            </div>
            <div class="color-label" id="color-label-${idx}" style="color:${colorHex['yellow']}">${colorNames['yellow']}</div>
            <div class="star-rating mt-2">
              <span class="stars">${getStars(popularity)}</span>
              <span class="score ms-2">${(popularity*5).toFixed(1)}/5</span>
            </div>
          </div>
        </div>
      </div>
    `;
  }).join('');
  document.getElementById('product-swiper-wrapper').innerHTML = slides;

  if(window.productSwiper) window.productSwiper.destroy(true, true);
  window.productSwiper = new Swiper('.swiper', {
    slidesPerView: 1,
    spaceBetween: 24,
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
    breakpoints: {
      576: { slidesPerView: 2 },
      992: { slidesPerView: 4 }
    },
    grabCursor: true,
    keyboard: true,
    simulateTouch: true,
    cssMode: true, // Enable native scroll for better touchpad/trackpad support
  });

  setTimeout(() => {
    document.querySelectorAll('.color-btn').forEach(btn => {
      btn.addEventListener('click', function() {
        const color = this.getAttribute('data-color');
        const idx = this.getAttribute('data-product-idx');
        const product = products[idx];
        const img = document.querySelector(`img.product-img[data-product-idx='${idx}']`);
        if(img) img.src = product.images[color];
        const btns = document.querySelectorAll(`.color-btn[data-product-idx='${idx}']`);
        btns.forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        const label = document.getElementById(`color-label-${idx}`);
        if(label) {
          label.textContent = colorNames[color];
          label.style.color = colorHex[color];
        }
      });
    });
  }, 0);
}

function getStars(popularity) {
  const score = Math.round(popularity * 10) / 2; // 0.5'lik adımlar
  let stars = '';
  for(let i=1; i<=5; i++) {
    if(score >= i) stars += '★';
    else if(score >= i-0.5) stars += '☆';
    else stars += '☆';
  }
  return stars;
}
