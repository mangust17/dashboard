document.addEventListener("DOMContentLoaded", function () {
// Скрипт на обработку вводимого Quantity 
// Проверка ввода

  const inputs = document.querySelectorAll('#refresh_table input[type="number"]');
  
  inputs.forEach(function(input) {
    var maxQuantity = parseInt(input.getAttribute('data_max'));
    
    input.addEventListener('blur', function(event) {
      var enteredQuantity = parseInt(input.value);
      if (enteredQuantity > maxQuantity || enteredQuantity < 0) {
        alert('Введенное число больше количества или отрицательно');
        input.value = 0; // Очищаем значение поля
      }
    });
  });

// ------------------------------------------------
});

