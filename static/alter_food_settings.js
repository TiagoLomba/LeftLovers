const cuisineCheckboxes = document.querySelectorAll('.cuisine-chk');
const healthCheckboxes = document.querySelectorAll('.health-chk');
const selectedCuisines = new Set();
const selectedHealth = new Set();

function handleCheckboxChange(event) {
  const { target } = event;
  const checkboxId = target.id;

  if (target.classList.contains('cuisine-chk')) {
    handleCuisineCheckbox(checkboxId, target.checked);
  } else if (target.classList.contains('health-chk')) {
    handleHealthCheckbox(checkboxId, target.checked);
  }

  console.log(selectedCuisines);
  console.log(selectedHealth);
}

function handleCuisineCheckbox(id, checked) {
  if (checked) {
    selectedCuisines.add(id);
  } else {
    selectedCuisines.delete(id);
  }
}

function handleHealthCheckbox(id, checked) {
  if (checked) {
    selectedHealth.add(id);
  } else {
    selectedHealth.delete(id);
  }
}

cuisineCheckboxes.forEach((checkbox) => {
  checkbox.addEventListener('change', handleCheckboxChange);
});

healthCheckboxes.forEach((checkbox) => {
  checkbox.addEventListener('change', handleCheckboxChange);
});

const saveButton = document.querySelector('button[type="submit"]');
saveButton.addEventListener('click', function(event) {
  //Prevent Button from submitting so that I can select data and sent it
  event.preventDefault();


  $.ajax({
    url: '/restrictions',
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify({cuisineType: [...selectedCuisines], health: [...selectedHealth]}),
    success: function(response){
      window.location.replace('/');
    }
  });

});
