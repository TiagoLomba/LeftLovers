// Check if dark mode preference is stored in localStorage
let darkModePreference = localStorage.getItem('darkMode');

function toggleDarkMode() {
  document.body.classList.toggle('dark-mode');
;

  let isDarkMode = document.body.classList.contains('dark-mode');

  // Store dark mode preference in localStorage
  localStorage.setItem('darkMode', isDarkMode);
}


if (darkModePreference === 'true') {
  document.body.classList.add('dark-mode');
}


let darkModeButton = document.querySelector('.dark-mode-btn');
darkModeButton.addEventListener('click', toggleDarkMode);
