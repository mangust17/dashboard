function showLoader() {
  document.getElementById("loader").style.display = "true";
}

function hideLoader() {
  document.getElementById("loader").style.display = "none";
}

//Покраска маленьких цен
document.addEventListener('DOMContentLoaded', function () {
  // Получаем все элементы с классом "little-price" и "prices"
  var elementsWithClass = document.querySelectorAll('.little-price, .prices');

  // Применяем стиль только для всех ячеек
  elementsWithClass.forEach(function (element) {
    // Получаем текст из ячейки
    var text = element.innerText.trim();

    // Пытаемся преобразовать текст в число
    var value = parseFloat(text.replace(',', '.')); // заменяем запятые на точки

    // Проверяем, является ли значение числовым и отрицательным
    if (!isNaN(value) && value < 0) {
      // Устанавливаем красный цвет
      element.style.color = 'red';

      // Добавляем символ со стрелкой вниз
      element.innerHTML = text + ' &#9660;';
    }
  });
});


// Форматирование таблицы
document.addEventListener('DOMContentLoaded', function () {
  var table = document.querySelector('.cur-table'); // Замените 'your-table-id' на ID вашей таблицы
  var rows = table.querySelectorAll('.cur-table tr');
  console.log(rows)
  for (var i = 1; i < rows.length; i++) { // Начинаем с 1, чтобы пропустить заголовок
    var cellDiff = rows[i].getElementsByTagName('td')[3]; // Замените 2 на индекс столбца 'diff'

    var diffValue = parseFloat(cellDiff.innerText);
    if (diffValue > 0) {
      cellDiff.style.color = 'green';
      cellDiff.innerHTML += ' &#9650;';
    } else if (diffValue < 0) {
      cellDiff.style.color = 'red';
      cellDiff.innerHTML += ' &#9660;';
    }
  }
});






document.addEventListener('DOMContentLoaded', function () {
  var myDivs = document.getElementsByClassName('result_calc');

  for (var i = 0; i < myDivs.length; i++) {
    var currentDiv = myDivs[i];
    var checkmark;  // Переменная checkmark должна быть объявлена здесь

    if (currentDiv.textContent.includes('только')) {
      currentDiv.style.backgroundColor = 'darkred';
      currentDiv.style.color = 'white';
      currentDiv.classList.add('alert');
      checkmark = document.createElement('span');
      checkmark.textContent = ' ✗ ';
      checkmark.style.color = 'red';

      currentDiv.insertBefore(checkmark, currentDiv.firstChild);
    } else if (currentDiv.textContent.includes('Успех')) {
      currentDiv.classList.add('alert');
      currentDiv.style.color = 'white';
      currentDiv.style.backgroundColor = 'darkgreen';
      checkmark = document.createElement('span');
      checkmark.textContent = ' ✔ ';
      checkmark.style.color = 'white';
      currentDiv.insertBefore(checkmark, currentDiv.firstChild);
    }
  }
});

document.addEventListener('DOMContentLoaded', function () {
  var glowingDiv = document.getElementById('glowingDiv');
  var myForm = document.getElementById('myForm');
  var isBright = true;
  var subBut = document.querySelector('.subBut');
  if (subBut) {
    subBut.addEventListener('mouseover', function () {
      subBut.classList.add('glowing');
    });

    subBut.addEventListener('mouseout', function () {
      subBut.classList.remove('glowing');
    });
    myForm.addEventListener('submit', function (event) {
      event.preventDefault(); // Отмена отправки формы, чтобы предотвратить перезагрузку страницы

      // Добавляем плавный переход к яркости
      glowingDiv.style.transition = 'filter 0.5s ease-in-out';

      // Запускаем анимацию изменения яркости
      var interval = setInterval(function () {
        // Переключаемся между ярким и темным состоянием
        if (isBright) {
          glowingDiv.style.filter = 'brightness(5)';
        }
        isBright = !isBright;
      }, 500); // Интервал в 500 миллисекунд (0.5 секунды)

      // Добавляем задержку в 5 секунд перед отправкой формы
      setTimeout(function () {
        // Здесь вы можете добавить код для входа пользователя или других действий
        console.log("Выполняем вход пользователя");

        // Здесь вызываем метод submit для отправки формы
        myForm.submit();

        // Очищаем интервал после отправки формы
        clearInterval(interval);

        // Сбрасываем плавный переход после отправки формы
        glowingDiv.style.transition = 'none';
      }, 1000);
    });
  }
});

$('#form_task_manager').hide();
$('#jq_button_collapse').click(function () {
  $('#form_task_manager').slideToggle(500, function () {
    // Функция обратного вызова, которая выполнится после завершения анимации
    var buttonText = $('#form_task_manager').is(':visible') ? 'Скрыть' : 'Открыть форму создания заявки';
    $('#jq_button_collapse').text(buttonText);
  });
});

// Подсказка в таск менеджере
var nameCells = document.querySelectorAll('.jq-name');
var popup = document.getElementById('popup');
nameCells.forEach(function (cell) {
  cell.addEventListener('mouseover', function (event) {
    // Получаем данные из скрытого столбца
    var details = cell.parentElement.querySelector('.jq_details').innerText;

    // Позиционируем всплывающее окно над курсором
    var x = event.clientX;
    var y = event.clientY;
    popup.style.left = (x + 10) + 'px';
    popup.style.top = (y + 10) + 'px';

    // Устанавливаем содержимое всплывающего окна
    popup.innerHTML = details;

    // Показываем всплывающее окно
    popup.style.display = 'block';
  });

  cell.addEventListener('mouseout', function () {
    // Скрываем всплывающее окно при уходе курсора
    popup.style.display = 'none';
  });
});

// Добавление строк в форму
document.addEventListener('DOMContentLoaded', function () {
  const jqAddButForm = document.querySelector('#jqAddButForm')
  const jqTable = document.querySelector('.addingTable > tbody')
  let counter = 1; // Инициализация счетчика
  if (jqAddButForm) {
    jqAddButForm.addEventListener('click', (e) => {
      e.preventDefault();
      addFormString();

    })
  };

  function addFormString() {
    const newRow = document.createElement('tr');

    const modelCell = document.createElement('td');
    const colorCell = document.createElement('td');
    const quantityCell = document.createElement('td');

    const modelSelect = document.querySelector('[name="model"]').cloneNode(true);
    const colorSelect = document.querySelector('[name="color"]').cloneNode(true);
    const quantityInput = document.querySelector('[name="quantity"]').cloneNode(true);

    modelSelect.id = `model_${counter}`;
    colorSelect.id = `color_${counter}`;
    quantityInput.id = `quantity_${counter}`;

    modelSelect.name = `model_${counter}`;
    colorSelect.name = `color_${counter}`;
    quantityInput.name = `quantity_${counter}`;

    counter++;

    // Добавляем скопированные поля в ячейки
    modelCell.appendChild(modelSelect);
    colorCell.appendChild(colorSelect);
    quantityCell.appendChild(quantityInput);

    // Добавляем ячейки в строку
    newRow.appendChild(modelCell);
    newRow.appendChild(colorCell);
    newRow.appendChild(quantityCell);

    jqTable.appendChild(newRow);

  };

});

document.addEventListener('DOMContentLoaded', function () {
  const tab = document.querySelector('.table_paint');
  const rows = tab.querySelectorAll('tbody tr');

  for (let i = 0; i < rows.length; i++) {
    const statusCell = rows[i].getElementsByTagName('td')[4]; // Пятая ячейка (индекс 4) в каждой строке

    if (statusCell.textContent.trim() === 'Обработано') {
      statusCell.style.color = '#28a745'; // Зеленый цвет текста, замените на ваш выбор
    }
    if (statusCell.textContent.trim() === 'Закрыто') {
      statusCell.style.color = 'red'; // Зеленый цвет текста, замените на ваш выбор
    }
  }

  // Активация подсказок
});



