$(document).ready(function () {
  // --------------------------------------------------

  $('.delete-button').on('click', function () {
    var deleteButton = $(this); // Сохраняем ссылку на кнопку
    var csrfToken = $('[name=csrfmiddlewaretoken]').val();
    var taskNumber = deleteButton.data('task-number');
    console.log(1);
    $.ajax({
      url: '/delete_task/',
      method: 'POST',
      headers: { 'X-CSRFToken': csrfToken },
      data: { task_number: taskNumber },
      success: function (response) {
        if (response.success) {
          // Успешное удаление
          deleteButton.closest('.jq-task-row').remove(); // Используем сохраненную ссылку
        }
      },
      error: function (error) {
        console.error('Ошибка при удалении задачи:', error);
      }
    });
  });

    // ----------------------------------------------------
  });