$(document).ready(function () {
    // Ваш JavaScript код для выполнения на определенном URL-адресе
    const insertButtons = document.querySelectorAll('.check_list_insert')
    const csrfToken = document.cookie.match(/csrftoken=([^;]+)/)[1];

    insertButtons.forEach(button => {
      button.addEventListener('click', (event) => {
        event.preventDefault();
        const invoiceNumber = button.getAttribute('invoice_number');
        var taskType = button.getAttribute('check_task');;

        if (taskType == "multi_check") {
          var taskType1 = button.getAttribute('check_task_1');
          var taskType2 = button.getAttribute('check_task_2');
          var fieldValue1 = document.getElementById(taskType1).checked;
          var fieldValue2 = document.getElementById(taskType2).checked;
          console.log(fieldValue1, fieldValue2);
          var fieldInsert = document.getElementById(taskType1 + "_cur_state")
        }
        else {
          var fieldValue = document.getElementById(taskType).value;
          var fieldInsert = document.getElementById(taskType + "_cur_state");

          if ((document.getElementById(taskType).checked)) {
            fieldValue = document.getElementById(taskType).checked
          };

        };



        $.ajax({
          url: '/tools/checklist/invoices/1/',
          method: 'POST',
          headers: { 'X-CSRFToken': csrfToken },
          data: {
            invoice: invoiceNumber,
            field: taskType,
            field_value: fieldValue,
            field1: taskType1,
            field1_value: fieldValue1,
            field2: taskType2,
            field2_value: fieldValue2
          },
          success: function (response) {
            console.log('Успешный AJAX-запрос:', response.message);
            if (response.field_value) {
              fieldInsert.textContent = response.field_value
            }
            else {
              fieldInsert.innerHTML = response.field_value1 + "<br>" + response.field_value2
            }
          },
          error: function (xhr, status, error) {
            console.error('Ошибка AJAX-запроса:', error);
          }
        })
      })
    })

    // Скрипт для обработки загрузки файла
    document.getElementById("uploadLink").addEventListener("click", function () {
      document.getElementById("fileInput").click();
    });


    document.getElementById("fileInput").addEventListener("change", function () {
      var fileInput = document.getElementById("fileInput");
      var fileName = document.getElementById("fileName");
      var uploadLink = document.getElementById("uploadLink");

      if (fileInput.files.length > 0) {
        var file = fileInput.files[0];
        fileName.innerText = "Выбранный файл: " + file.name;
        fileName.style.display = "block";
        uploadLink.innerText = "Изменить файл";
      } else {
        fileName.innerText = "";
        fileName.style.display = "none";
        uploadLink.innerText = "Выбрать файл";
      }
    });



    const uploadLinks = document.querySelectorAll(".file_change_button");
    uploadLinks.forEach((button) => {
      button.addEventListener("click", (event) => {
        event.preventDefault();
        const invoiceNumber = button.getAttribute('invoice_number');
        const taskType = button.getAttribute('check_task');
        const fileInput = document.querySelector("#fileInput").files[0];
        var fileName = fileInput.name;
        var fieldInsert = document.getElementById(taskType + "_cur_state")
        console.log(fieldInsert)
        var formData = new FormData();
        formData.append('file', fileInput);
        formData.append('invoice', invoiceNumber);
        formData.append('field', taskType);
        formData.append('field_value', fileName);

        $.ajax({
          url: '/tools/checklist/invoices/1',
          method: 'POST',
          headers: { 'X-CSRFToken': csrfToken },
          data: formData,
          processData: false, // Не обрабатываем данные
          contentType: false, // Не устанавливаем тип контента

          success: function (response) {
            console.log('Успешный AJAX-запрос:', response.message);
            fieldInsert.textContent = response.field_value;

          },
          error: function (xhr, status, error) {
            console.error('Ошибка AJAX-запроса:', error);
          }
        })
      });

    })
});