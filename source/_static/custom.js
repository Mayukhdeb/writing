// Change search placeholder text
document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('search-input');
  if (searchInput) {
    searchInput.setAttribute('placeholder', 'Search');
  }
});
