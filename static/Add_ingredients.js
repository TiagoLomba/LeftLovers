let addButton = document.querySelector('.add-ingredients-btn');
let ingredientsContainer = document.querySelector('.ingredients-inputs');
let ingredientsInput = document.querySelectorAll(".ingredients");
let errorMessage = document.querySelector('.error-message');
let dietTypeContainer = document.querySelector('.hl-container');
let addDTButton = document.querySelector('.add-dl-btn');

// let availableHealth = JSON.parse(document.querySelector('#health_labels').dataset.availableHealth);

let createInputContainer = () => {
  let inputContainer = document.createElement('div');
  inputContainer.classList.add('mb-3', 'd-flex', 'justify-content-center', 'align-items-center');

  let newInput = document.createElement('input');
  newInput.classList.add('form-control', 'ingr-inp-size');
  newInput.type = 'text';
  newInput.autocomplete = 'off';
  newInput.name = 'ingredients';
  newInput.placeholder = 'Write an ingredient';

  let newButton = document.createElement('button');
  newButton.classList.add('btn', 'btn-secondary', 'add-ingredients-btn');
  newButton.type = 'button';
  let newIcon = document.createElement('i');
  newIcon.classList.add('bi', 'bi-plus');
  newButton.appendChild(newIcon);

  inputContainer.appendChild(newInput);
  inputContainer.appendChild(newButton);
  ingredientsContainer.appendChild(inputContainer);

  return newButton;
};


let createSelectField = (options) => {
  let selectContainer = document.createElement('div');
  selectContainer.classList.add('my-2', 'd-flex', 'justify-content-center', 'align-items-center', 'ms-3');

  let newSelect = document.createElement('select');
  newSelect.name = 'health_labels';
  newSelect.id = 'health_labels';
  newSelect.classList.add('form-select', 'restrictions-inp-size');

  let emptyOption = document.createElement('option');
  emptyOption.value = '';
  emptyOption.textContent = 'Add more health labels';
  newSelect.appendChild(emptyOption);

  options.forEach((option) => {
    let newOption = document.createElement('option');
    newOption.value = option;
    newOption.textContent = option;
    newSelect.appendChild(newOption);
  });

  let newDietButton = document.createElement('button');
  newDietButton.classList.add('btn', 'btn-secondary', 'add-dl-btn');
  newDietButton.type = 'button';
  let newDietIcon = document.createElement('i');
  newDietIcon.classList.add('bi', 'bi-plus');
  newDietButton.appendChild(newDietIcon);

  selectContainer.appendChild(newSelect);
  selectContainer.appendChild(newDietButton);
  dietTypeContainer.appendChild(selectContainer);

  // Attach event listener to the newDietButton
  newDietButton.addEventListener('click', handleSelectChange);

  return selectContainer;
};

let fetchAvailableHealth = () => {
  return fetch('/get_available_health')
    .then(response => response.json())
    .then(data => data.available_health)
    .catch(error => {
      console.error('Error fetching available_health:', error);
    });
};

// Button Click
let handleClick = () => {
  let input = document.querySelector('.ingr-inp-size');
  // remove white spaces
  let inputValue = input.value.trim();
  //If the user did not type anything, show error message
  if (inputValue === '') {
    errorMessage.textContent = 'Please enter an ingredient.';
    errorMessage.style.display = 'block';
  } else {
    errorMessage.textContent = '';

    let newButton = createInputContainer();
    newButton.addEventListener('click', handleClick);
  }
};

let handleSelectChange = (event) => {
  let target = event.target;

  // Check if the event target is the newDietButton
  if (!target.classList.contains('add-dl-btn')) {
    return;
  }

  let selectElements = document.querySelectorAll('select[name="health_labels"]');
  let selectedOptions = Array.from(selectElements).map((select) => select.value);

  fetchAvailableHealth()
    .then((available_health) => {
      let newSelect = createSelectField(available_health.filter((option) => !selectedOptions.includes(option)));
      newSelect.addEventListener('change', handleSelectChange);
    });
};

addButton.addEventListener('click', handleClick);
addDTButton.addEventListener('click', handleSelectChange); // Attach handleSelectChange directly

// Add event listener for the initial select tag
document.addEventListener('DOMContentLoaded', () => {
  let selectElement = document.querySelector('select[name="health_labels"]');
  selectElement.addEventListener('change', handleSelectChange);
});