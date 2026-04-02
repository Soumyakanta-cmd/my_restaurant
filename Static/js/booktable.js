
function toggleCard(id, checkbox) {
  document.getElementById('card-' + id).classList.toggle('selected', checkbox.checked);
  updateSummary();
}
const today = new Date().toISOString().split('T')[0];
const dateInput = document.getElementById('booking_date');
dateInput.value = today;
dateInput.min = today;
dateInput.max = today;

function updateSummary() {
  const checked = document.querySelectorAll('#items-grid input:checked');
  const summary = document.getElementById('selected-summary');
  const names   = document.getElementById('selected-names');
  if (checked.length > 0) {
    summary.style.display = 'flex';
    names.textContent = [...checked].map(c =>
      c.closest('.item-card').querySelector('.item-card-name').textContent
    ).join(', ');
  } else {
    summary.style.display = 'none';
  }
  document.getElementById('items-error').textContent = '';
}

function validateItems() {
  const checked = document.querySelectorAll('#items-grid input:checked');
  if (checked.length === 0) {
    document.getElementById('items-error').textContent = 'Please select at least one item.';
    return false;
  }
  return true;
}

