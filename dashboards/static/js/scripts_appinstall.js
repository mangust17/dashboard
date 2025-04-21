$(document).ready(function () { 
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  
  // Инициализация модального окна
  $('.confirm_icon').each(function () {
    $(this).click(function () {
      $('#confirm-button').prop('disabled', true);
      let taskId = $(this).attr('task-id');
      let taskCount = $(this).attr('task-count');
      $('#modal-task-id').val(taskId);
      $('#modal-count').val(taskCount);
      $('#hidden_log_form').val('');
      $('#fake-file-input').val('');
      $('#message-box').empty();
      const modal = new bootstrap.Modal(document.getElementById('exampleModal'));
      $('#count-span').text(`Подтвердите настройку ${taskCount} устройств по задаче № ${taskId}`);
      modal.show();
    })
  });

  // Подтверждение задачи
  $('#confirm-button').click(function () {
    let taskId = $('#modal-task-id').val();
    $.ajax({
      url: "/app_installer/",
      method: "POST",
      headers: { 'X-CSRFToken': csrfToken },
      data: { task_to_accept: taskId },
      success: function (response) {
        if (response.success) {
          window.location.reload();
        } else {
          $('#message-box').html('<p class="text-danger">Ошибка при загрузке данных.</p>');
        }
      },
      error: function (xhr, status, error) {
        console.error('Ошибка AJAX-запроса:', error);
      }
    });
  });

  $('#check-btn').click(function () {
    let count = $('#modal-count').val();
    let formElement = $('#hidden_log_form')[0];
   
    var formData = new FormData();
    if (formElement.files.length > 0) {
      formData.append('log_file', formElement.files[0]);
    } 
    formData.append('count', count);

    $.ajax({
      url: "/app_installer/",
      method: "POST",
      headers: { 'X-CSRFToken': csrfToken },
      data: formData,
      processData: false,  
      contentType: false,  

      success: function (response) {
        let messageBox = $("#message-box");
        if (response.success) {
          $('#confirm-button').prop('disabled', false);
          messageBox.html("<p class='text-green'>" + response.message + "</p>");
        } else {
          messageBox.html("<p class='text-danger'>" + response.message + "</p>");
        }
      },
      error: function (xhr, status, error) {
        console.error('Ошибка AJAX-запроса:', error);
      }
    });
  });
})
