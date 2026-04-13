const qty = {};

function filterItems() {
  const q = document.getElementById('item-filter').value.trim().toLowerCase();
  const dd = document.getElementById('dropdown');
  if (!q) { dd.style.display = 'none'; return; }

  const matches = allItems.filter(i => i.name.toLowerCase().includes(q));
  if (!matches.length) {
    dd.style.display = 'block';
    dd.innerHTML = '<div class="no-results">No items found</div>';
    return;
  }
  dd.style.display = 'block';
  dd.innerHTML = matches.map(i => `
    <div class="dropdown-item" onclick="addItem(${i.id})">
      <div>
        <div class="di-name">${i.name}</div>
        <div class="di-price">₹${i.price}</div>
      </div>
      <span class="di-plus">+</span>
    </div>
  `).join('');
}

function addItem(id) {
  qty[id] = (qty[id] || 0) + 1;
  syncInputs(id);
  updateCart();
  document.getElementById('item-filter').value = '';
  document.getElementById('dropdown').style.display = 'none';
}

function change(id, delta) {
  qty[id] = Math.max(0, (qty[id] || 0) + delta);
  syncInputs(id);
  updateCart();
}

function syncInputs(id) {
  document.querySelectorAll(`input[data-item="${id}"]`).forEach(e => e.remove());
  if (qty[id] > 0) {
    document.getElementById('cart-section').insertAdjacentHTML('beforeend',
      `<input type="hidden" name="items" value="${id}" data-item="${id}">
       <input type="hidden" name="qty_${id}" value="${qty[id]}" data-item="${id}">`
    );
  }
}

function updateCart() {
  const sel = allItems.filter(i => qty[i.id] > 0);
  const cs = document.getElementById('cart-section');
  if (!sel.length) { cs.style.display = 'none'; return; }
  cs.style.display = 'block';
  let total = 0;
  document.getElementById('cart-rows').innerHTML = sel.map(i => {
    const sub = i.price * qty[i.id]; total += sub;
    return `<div class="cart-item">
      <div>
        <div class="cart-item-name">${i.name}</div>
        <div class="cart-item-price">₹${i.price} each</div>
      </div>
      <div class="qty-row">
        <button type="button" class="qty-btn" onclick="change(${i.id}, -1)">−</button>
        <span class="qty-num">${qty[i.id]}</span>
        <button type="button" class="qty-btn" onclick="change(${i.id}, 1)">+</button>
      </div>
    </div>`;
  }).join('');
  document.getElementById('cart-total').textContent = '₹' + total;
  document.getElementById('items-error').textContent = '';
}

function validateItems() {
  const hasItems = Object.values(qty).some(q => q > 0);
  if (!hasItems) {
    document.getElementById('items-error').textContent = 'Please select at least one item.';
    return false;
  }
  return true;
}

document.addEventListener('click', e => {
  if (!e.target.closest('#item-filter') && !e.target.closest('#dropdown'))
    document.getElementById('dropdown').style.display = 'none';
});

const today = new Date().toISOString().split('T')[0];
const dateInput = document.getElementById('booking_date');
dateInput.value = today; dateInput.min = today; dateInput.max = today;