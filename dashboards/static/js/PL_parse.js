$(document).ready(function () {
  // Парсинг файла
  const ParseButtons = document.querySelectorAll('.PL-parse-button')
  const SaveButtons = document.querySelectorAll('.PL-save-button')
  const summaryTextBlock = document.querySelector('#summary_p')
  ParseButtons.forEach(button => {
    button.addEventListener('click', () => {
      var fileName = button.getAttribute('file-name');
      var csrfToken = document.cookie.match(/csrftoken=([^;]+)/)[1];
      var divToEnter = document.querySelector('#pl_parsed_col')
      $.ajax({
        url: '/parse_PL/',
        method: 'POST',
        headers: { 'X-CSRFToken': csrfToken },
        data: { fileName: fileName },
        success: function (response) {
          // Обработка успешного ответа от сервера
          divToEnter.innerHTML = response.df
          console.log('Успешный AJAX-запрос:', response);
          divToEnter.style.display = "block";
          summaryTextBlock.style.display = "block";
          console.log(summaryTextBlock)
          summaryTextBlock.textContent = 'Общее количество товара: '+response.sum_of_pl

        },
        error: function (xhr, status, error) {
          // Обработка ошибки запроса
          console.error('Ошибка AJAX-запроса:', error);
        }
      })
    });
  });
  // Сохранение PL
  SaveButtons.forEach(button => {
    if (button.textContent.trim() == 'Сохранено') {
      button.style.color = 'green';
      button.style.cursor = 'auto';

    }

    if (button.textContent.trim() != 'Сохранено') {
      button.addEventListener('click', () => {
        var fileName = button.getAttribute('file-name')
        var csrfToken = document.cookie.match(/csrftoken=([^;]+)/)[1];
        var buttonValue = button.textContent.trim();
        console.log('clicked_save')
        $.ajax({
          url: '/save_PL/',
          method: 'POST',
          headers: { 'X-CSRFToken': csrfToken },
          data: { fileName: fileName, fileStatus: buttonValue },
          success: function (response) {
            // Обработка успешного ответа от сервера
            button.textContent = 'Сохранено';
            button.style.color = 'green';
            button.style.cursor = 'auto';
            console.log('Успешный AJAX-запрос:', response);
          },
          error: function (xhr, status, error) {
            // Обработка ошибки запроса
            console.error('Ошибка AJAX-запроса:', error);
          }
        });
      });
    };
  });

  // Загрузка файла
  const AddButton = document.querySelector('add_button')
  document.getElementById("uploadLink").addEventListener("click", function () {
    document.getElementById("fileInput").click();
  });
  const csrfToken = document.cookie.match(/csrftoken=([^;]+)/)[1];

  document.getElementById("fileInput").addEventListener("change", function () {
    var fileInput = document.getElementById("fileInput").files[0];
    var insertRow = document.getElementById("tr_for_insert")
    var formData = new FormData();
    formData.append('file', fileInput);

    console.log(fileInput);
    $.ajax({
      url: '/tools/load_pl/',
      method: 'POST',
      headers: { 'X-CSRFToken': csrfToken },
      data: formData,
      processData: false, // Не обрабатываем данные
      contentType: false, // Не устанавливаем тип контента

      success: function (response) {
        console.log('Успешный AJAX-запрос:', response.data);
        window.location.reload();
      },
      error: function (xhr, status, error) {
        console.error('Ошибка AJAX-запроса:', error);
      }
    })
  });
// Окрашивание и скрытие action buttons при закрытии
  const statusTD = document.querySelectorAll('.status_td');
  statusTD.forEach((elem) => {
    if (elem.textContent.trim() == 'Закрыт') {
      elem.style.color = 'green';
      const row = elem.closest('tr')
      if (row) {
        const actionTDs = row.querySelectorAll('.action_tds');
        actionTDs.forEach((e) => {
          // e.innerHTML = "";
        });
      };
      
    };

    
  });


});