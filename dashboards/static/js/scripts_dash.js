document.addEventListener('DOMContentLoaded', function () {
  // -------------------------------
  // Корректировка значений ячеек в остатка
  const availableCells = document.querySelectorAll('.dash_table input[type="number"]');
  const table = document.querySelector('#dash_table');
  const columnIndexColor = Array.from(table.querySelectorAll('#dash_table th')).findIndex(function (th) {
    return th.textContent.trim().includes('Color');
  });

  const columnIndexAvaible = Array.from(table.querySelectorAll('#dash_table th')).findIndex(function (th) {
    return th.textContent.trim().includes('Avaible');
  });

  const columnIndexModel = Array.from(table.querySelectorAll('#dash_table th')).findIndex(function (th) {
    return th.textContent.trim().includes('Model');
  });

  const columnIndexSet = Array.from(table.querySelectorAll('#dash_table th')).findIndex(function (th) {
    return th.textContent.trim().includes('Распределить');
  });

  table.querySelectorAll('#dash_table tr').forEach(row => {
    let initialAvaibleValue = Number(row.cells[columnIndexAvaible].textContent);
    row.cells[columnIndexAvaible].setAttribute('data-start-avaible', initialAvaibleValue);
  });

  function calculateTotalAvaible(color, model) {
    let totalAvaible = 0;
  
    table.querySelectorAll('#dash_table tr').forEach(row => {
      let currentColorField = row.cells[columnIndexColor].textContent;
      let currentModelField = row.cells[columnIndexModel].textContent;
  
      if (currentColorField === color && currentModelField === model) {
        let inputElement = row.cells[columnIndexSet].querySelector('input[type="number"]');
        if (inputElement) {
          let avaibleValue = Number(inputElement.value);
          totalAvaible += avaibleValue;
        }
      }
    });
  
    return totalAvaible;
  }

  // Сохраняем изначальные значения "Avaible" в атрибуте data-start-avaible
  availableCells.forEach(input => {
    input.addEventListener('change', (event) => {
      let rows = table.querySelectorAll('#dash_table tr');
      let changedRow = event.target.closest('tr');
      let colorField = changedRow.cells[columnIndexColor].textContent;
      let modelField = changedRow.cells[columnIndexModel].textContent;
      rows.forEach(row => {
        // Получаем текстовое содержимое ячейки columnIndexModel и columnIndexColor перед применением includes,

        let currentModelField = row.cells[columnIndexModel].textContent;
        let currentColorField = row.cells[columnIndexColor].textContent;
        let initialAvaibleValue = Number(row.cells[columnIndexAvaible].getAttribute('data-start-avaible'));
        
        if (currentModelField.includes(modelField) && currentColorField.includes(colorField)) {

          let newValue = calculateTotalAvaible(currentColorField,currentModelField);
          console.log(newValue)

          let updatedAvaibleValue = initialAvaibleValue - newValue;

          row.cells[columnIndexAvaible].textContent = updatedAvaibleValue;


        }
      });
    });
  });

  $('#js_correntStocksDiv').hide();
  $('#jq_button_collapse').click(function () {
    $('#js_correntStocksDiv').slideToggle(500, function () {
      // Функция обратного вызова, которая выполнится после завершения анимации
      var buttonText = $('#js_correntStocksDiv').is(':visible') ? 'Скрыть' : 'Показать текущие остатки';
      $('#jq_button_collapse').text(buttonText);
    });
  });

  
  //Шкала прогресса 
  $('.percent-cell').each(function () {
    var percentText = parseInt($(this).text()); // Преобразование в целое число
    var progressBar = $('<div class="progress"><div class="progress-bar" role="progressbar" style="width: ' + percentText + '%;" aria-valuenow="' + percentText + '" aria-valuemin="0" aria-valuemax="100">' + percentText + '%</div></div>');
    $(this).html(progressBar);
});

  // -------------------------------
});

