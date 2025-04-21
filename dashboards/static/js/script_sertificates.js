$(document).ready(function () {
  $('.upload-button').each(function() {
    $(this).click(function(){
      let genId = $(this).attr('gen-id');
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

      // Создание скрытой формы для отправки запроса
      let form = $('<form>', {
        method: 'POST',
        action: "/certificate-generator/",
        target: '_blank' // открываем в новой вкладке
      });
      
      // Добавление CSRF-токена
      form.append($('<input>', {
        type: 'hidden',
        name: 'csrfmiddlewaretoken',
        value: csrfToken
      }));
      
      // Добавление генерируемого ID
      form.append($('<input>', {
        type: 'hidden',
        name: 'genId_upload',
        value: genId
      }));

      // Добавление формы в body и отправка
      $('body').append(form);
      form.submit(); // Отправляем форму
      form.remove(); // Удаляем форму после отправки
    });
  });
});