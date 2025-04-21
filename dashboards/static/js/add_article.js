$(document).ready(function () {
  const modelForm = document.querySelectorAll('.model_get_color_form')
  const colorForm = document.querySelectorAll('.article_color_form')[0]
  const articleForm = document.querySelectorAll('.article_form_input')[0]
  console.log(modelForm)
  const csrfToken = document.cookie.match(/csrftoken=([^;]+)/)[1];
  modelForm.forEach(elem => {
    elem.addEventListener('change', () => {
      var model_id = elem.value;
      var color = colorForm.value;
      console.log(model_id)
      $.ajax({
        url: '/get_color/',
        method: 'POST',
        headers: { 'X-CSRFToken': csrfToken },
        data: { model: model_id, color: color },
        success: function (response) {
          console.log('Успешный AJAX-запрос:', response.colors);
          const insertDiv = document.getElementById('insert_color_div')
          insertDiv.innerHTML = response.colors.join('<br>');
          articleForm.value = response.article;
        },
        error: function (xhr, status, error) {
          console.error('Ошибка AJAX-запроса:', error);
        }
      });
    });
  });
});