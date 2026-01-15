// Change search placeholder text
document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('search-input');
  if (searchInput) {
    searchInput.setAttribute('placeholder', 'Search');
  }
  
  // Replace "By" with "~" and add homepage link in footer
  const footer = document.querySelector('.footer p');
  if (footer) {
    footer.innerHTML = footer.innerHTML.replace(/^\s*By\s+/, '~');
    // Add homepage link on a new line after copyright
    footer.innerHTML = footer.innerHTML.replace(
      /(&copy; Copyright \d+\.)/,
      '$1<br/><a href="https://mayukhdeb.github.io/writing/">home</a>'
    );
  }
});
