$(document).ready(function () {
  const magicButton = document.getElementById('prediction_button');
  const csrfToken = document.cookie.match(/csrftoken=([^;]+)/)[1];
  const result = document.getElementById('prediction_output')


  magicButton.addEventListener('click', function () {
    const text_value = document.querySelector('textarea[name="models"]').value;
    
    $.ajax({
      url: '/ajax_magic/',
      method: 'POST',
      headers: { 'X-CSRFToken': csrfToken },
      data: { models : text_value },
      success: function (response) {
        if (response.prediction && Array.isArray(response.prediction)) {
          // Обработка успешного ответа от сервера
          result.innerHTML = response.prediction.join('<br>'); // Используем <br> для переноса строк
        } else {
          console.error('Ошибка: отсутствует свойство prediction или оно не является массивом');
        }
      },
      error: function (xhr, status, error) {
        // Обработка ошибки запроса
        console.error('Ошибка AJAX-запроса:', error);
      }
    })

  })


});