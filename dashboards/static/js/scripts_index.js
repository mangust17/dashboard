document.addEventListener('DOMContentLoaded', function () {
  // -------------------------------
  // Фильтрация таблицы
  const checkActual = document.querySelector('#js_actual_check');
  const checkClose = document.querySelector('#js_closed_check');
  const selFieldStatus = document.querySelector('#js_Sel_field');
  const table = document.querySelector('.checkFilterTable');

  const filterState = {
    actual: false,
    close: false,
    type: 'All',
  };


  function filtTable(col, value, type) {
    const columnIndex = Array.from(table.querySelectorAll('table th')).findIndex(function (th) {
      return th.textContent.trim().includes(col);
    });
    var rows = table.querySelectorAll('tbody tr')
    rows.forEach((row) => {
      let statusCell = row.cells[columnIndex].textContent;
      if (statusCell.includes(value)) {
        if (type === 'Hide') {
          row.style.display = 'none';
        }
        else {
          row.style.display = '';
        }
      }
    });
  }

  if (checkActual.checked) {
    filtTable('Статус', 'Обработано', 'Hide')
  };
  if (checkClose.checked) {
    filtTable('Статус', 'Закрыто', 'Hide')
  };

  if (checkActual) {
    checkActual.addEventListener('change', () => {
      if (checkActual.checked) {
        filtTable('Статус', 'Обработано', 'Hide')
      }
      else {
        filtTable('Статус', 'Обработано', 'Show')
      }
    })
  }

  if (checkClose) {
    checkClose.addEventListener('change', () => {
      if (checkClose.checked) {
        filtTable('Статус', 'Закрыто', 'Hide');
      }
      else {
        filtTable('Статус', 'Закрыто', 'Show');
      }
    });
  }

  if (selFieldStatus) {
    selFieldStatus.addEventListener('change', () => {
      var jsChoise = selFieldStatus.value;
      console.log(jsChoise);
      if (jsChoise === 'All') {
        filtTable('Тип', 'Заказано', 'Show');
        filtTable('Тип', 'Куплено', 'Show');
      }
      else if (jsChoise === 'Куплено') {
        filtTable('Тип', 'Куплено', 'Show');
        filtTable('Тип', 'Заказано', 'Hide');
      }
      else if (jsChoise === 'Заказано') {
        filtTable('Тип', 'Заказано', 'Show');
        filtTable('Тип', 'Куплено', 'Hide');
      }
    });
  }



  // -------------------------------
});