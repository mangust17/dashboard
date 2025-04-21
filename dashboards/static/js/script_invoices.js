$(document).ready(function () {


  // Удаление инвойса
  const delInvButtons = document.querySelectorAll('.ajax_delete_button')
  const csrfToken = $('[name=csrfmiddlewaretoken]').val();

  delInvButtons.forEach(function (button) {
    button.addEventListener('click', () => {
      var invoiceNumber = button.getAttribute('invoice')
      console.log(invoiceNumber)
      $.ajax({
        url: '/ajax_delete_invoice/',
        method: 'POST',
        headers: { 'X-CSRFToken': csrfToken },
        data: { invoice_to_del: invoiceNumber },
        success: function (response) {
          console.log('Success')
          location.reload();
        },
        error: function (xhr, status, error) {
          // Обработка ошибки запроса
          console.error('Ошибка AJAX-запроса:', error);
        }
      });
    });
  });


  // Скрипт на добавление строки в ручной инвойс
  var counter = 1;
  $(document).ready(function () {
    // При нажатии на кнопку "Добавить строку"
    $('#add_invoice_button').on('click', function () {
      // Найти последний ряд таблицы
      var lastRow = $('#last_row_in_invoices').prev();
      // Клонировать последний ряд
      lastRow.find('.single-select2-field').select2('destroy');
      var newRow = lastRow.clone();



      newRow.find('select').val('').trigger('change');
      console.log(lastRow)
      lastRow.after(newRow);
      // Повторно инициализировать Select2 для всех элементов после клонирования
      $('.single-select2-field').select2({
        theme: 'bootstrap-5',
        width: '250px',
        language: 'ru',
      }
      );
    });
  });


  // Удаление по нажатию на Delete
  $(document).on('click', '.delete-row', function () {
    $(this).closest('tr').remove();
  });


  //  Открытие меню для создания инвойса
  $("#show_inv_menu").click(function () {
    if ($(this).html() === "Скрыть меню создания") {
      $(".create_inv_block").slideUp()
      $(this).html('Создать новый инвойс');
    }
    else {
      $(".create_inv_block").slideDown();
      $(this).html('Скрыть меню создания');
    };
  })

  const ParseButtons = document.querySelectorAll('.PL-parse-button')
  const summaryTextBlock = document.querySelector('#summary_p')


  // Парсинг PL
  $("#toggle_div").hide()
  ParseButtons.forEach(button => {
    button.addEventListener('click', () => {
      var fileName = button.getAttribute('file-name');
      var csrfToken = document.cookie.match(/csrftoken=([^;]+)/)[1];
      var divToEnter = document.querySelector('#pl_parsed_col');
      var toggleDiv = document.getElementById("toggle_div")
      $.ajax({
        url: '/parse_PL/',
        method: 'POST',
        headers: { 'X-CSRFToken': csrfToken },
        data: { fileName: fileName },
        success: function (response) {
          // Обработка успешного ответа от сервера
          $("#toggle_div").slideDown()
          closeDiv = `<span id='close_span' style='cursor:pointer;'>Скрыть ; </span>Общая сумма: ${response.sum_of_pl}`
          divToEnter.innerHTML = closeDiv + response.df;
          console.log('Успешный AJAX-запрос:', response);
          divToEnter.style.display = "block";
          $("#close_span").click(function () {
            console.log($(this))
            $("#toggle_div").slideUp()
          });

        },
        error: function (xhr, status, error) {
          // Обработка ошибки запроса
          console.error('Ошибка AJAX-запроса:', error);
        }
      })
    });
  });


  // Загрузка файла
  const AddButton = document.querySelector('add_button')
  document.getElementById("uploadLink").addEventListener("click", function () {
    document.getElementById("fileInput").click();
  });

  document.getElementById("fileInput").addEventListener("change", function () {
    var fileInput = document.getElementById("fileInput").files[0];
    var orderTo = document.getElementById('order_to_select');
    var insertRow = document.getElementById("tr_for_insert");
    var formData = new FormData();
    formData.append('file', fileInput);
    formData.append('order_to', orderTo.value)
    console.log(orderTo.value)

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


  // Сохранение PL
  const SaveButtons = document.querySelectorAll('.PL-save-button')
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
        // Views_ajax/AjaxSavePl
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
            window.location.reload();
          },
          error: function (xhr, status, error) {
            // Обработка ошибки запроса
            console.error('Ошибка AJAX-запроса:', error);
          }
        });
      });
    };
  });



  //Загрузка AWB
  const awbButtons = $(".awbloader")
  awbButtons.each(function () {
    $(this).click(function () {
      var awbInputId = "#awb_input_" + $(this).attr('pl-number');
      $(awbInputId).click();
      console.log(1)
    });
  });
  // Добавляем обработчик события change за пределами итерации по кнопкам
  $(".awb_buttons").change(function () {
    var fileInput = $(this).get(0).files[0]; // Получаем файл, связанный с текущим измененным полем ввода файла
    var formData = new FormData();
    const innerFilename = $(this).attr('innerFilename')
    const plNum = $(this).attr('pl-num');
    formData.append("awb_file", fileInput);
    formData.append("pl_id", plNum);
    formData.append('inner_filename', innerFilename)


    $.ajax({
      url: "/tools/invoices/",
      method: "POST",
      headers: { 'X-CSRFToken': csrfToken },
      data: formData,
      processData: false,
      contentType: false,
      success: function (response) {
        location.reload();
      },
      error: function (xhr, status, error) {
        console.error('Ошибка AJAX-запроса:', error);
      }
    })

  })


  // Удаление AWB
  const awbDelSpans = $(".awb_del").each(function () {
    $(this).click(function () {
      var awbPlNum = $(this).attr('pl-num');
      console.log(awbPlNum);
      $.ajax({
        url: "/tools/invoices/",
        method: "POST",
        headers: { 'X-CSRFToken': csrfToken },
        data: { awb_del_num: awbPlNum },
        success: function (response) {
          location.reload();
        },
        error: function (xhr, status, error) {
          console.error('Ошибка AJAX-запроса:', error)
        }
      });
    });
  });
  $('.opp_modal').each(function () {
    $(this).click(() => {
      $('#myModalCreate').modal('show');

    })
  })
  $('#myModalCreate').on('shown.bs.modal', function () {
    $(this).find('input:first').focus(); // Устанавливаем фокус на первом поле ввода
  });


  // Отмена согласования
  const cancelAcceptSpan = $('.cancel_accept_span').each(function () {
    $(this).click(function () {
      var plNumber = $(this).attr('cancel-accept')
      console.log(plNumber)
      $.ajax({
        url: "/tools/invoices/",
        method: "POST",
        headers: { 'X-CSRFToken': csrfToken },
        data: { cancelAccept: plNumber },
        success: function (response) {
          location.reload();
        },
        error: function (xhr, status, error) {
          console.error('Ошибка AJAX-запроса:', error)
        }
      });

    });
  });


  // Загрузка GTD
  $('.gtd_loader').each(function () {
    $(this).click(function () {
      var gtdInputId = "#gtd_input_" + $(this).attr('pl-num-gtd');
      $(gtdInputId).click();
      console.log(gtdInputId)
    });
  });
  $(".gtd_buttons").change(function () {
    var fileInput = $(this).get(0).files[0]; // Получаем файл, связанный с текущим измененным полем ввода файла
    var formData = new FormData();
    const invNum = $(this).attr('gtd-to-invoice');
    const plNum = $(this).attr('gtd-pl-num');
    formData.append("gtd_file", fileInput);
    formData.append("gtd_toinvoice", invNum);
    formData.append('gtd_pl_num', plNum);

    $.ajax({
      url: "/tools/invoices/",
      method: "POST",
      headers: { 'X-CSRFToken': csrfToken },
      data: formData,
      processData: false,
      contentType: false,
      success: function (response) {
        location.reload();
      },
      error: function (xhr, status, error) {
        console.error('Ошибка AJAX-запроса:', error);
      }
    })

  })


  // Удаление ГТД
  $(".delete_gtd").each(function () {
    $(this).click(function () {
      var gtdDelSpans = $(this).attr('gtd-del-invoice');
      const gtdPlNum = $(this).attr('gtd-pl-num');
      console.log(gtdPlNum)
      $.ajax({
        url: "/tools/invoices/",
        method: "POST",
        headers: { 'X-CSRFToken': csrfToken },
        data: { gtd_del_invoice: gtdDelSpans, gtd_pl_num: gtdPlNum },
        success: function (response) {
          location.reload();
        },
        error: function (xhr, status, error) {
          console.error('Ошибка AJAX-запроса:', error)
        }
      });
    });
  });
  $('.opp_modal').each(function () {
    $(this).click(() => {
      $('#myModalCreate').modal('show');

    })
  })


  // Получение списка цветов
  $(".single-select2-field").each(function () {
    var selectElement = $(this).closest('tr');
    $(this).change(function () {
      colors = $(this).val()
      $.ajax({
        url: "/get_colors/",
        method: "POST",
        headers: { 'X-CSRFToken': csrfToken },
        data: { model: colors },
        success: function (response) {
          console.log(response.colors)
          console.log(selectElement)

        },
        error: function (xhr, status, error) {
          console.error('Ошибка AJAX-запроса:', error)
        }
      });
    });
  });


  // Добавление артикулов
  $(".add-article-b").each(function () {
    $(this).click(function () {
      console.log($(this).attr('color-to-add'))
      $.ajax({
        url: "/get_color/",
        method: "POST",
        headers: { 'X-CSRFToken': csrfToken },
        data: { model: $(this).attr('model-to-add'), color: $(this).attr('color-to-add') },
        success: function (response) {
          $.ajax({
            url: "/create_article_ajax/",
            method: "POST",
            headers: { 'X-CSRFToken': csrfToken },
            data: { model: response.model, color: response.color, article: response.article },
            success: function (response) {
              let insertId = response.model + response.color
              let el = document.getElementById(insertId)
              el.textContent = response.article
              el.style.color = "#959ba1"

            },
            error: function (xhr, status, error) {
              console.error('Ошибка AJAX-запроса:', error)
            }
          });

        },
        error: function (xhr, status, error) {
          console.error('Ошибка AJAX-запроса:', error)
        }
      });
    });
  });

  $('#testsss').click(function () {
    var datalist = $('.corr_df_model_id').map(function () {
      return $(this).text();
    }).get()
    console.log(datalist)
  })

  // Очистка проставленных цен
  $('.cancel_link_span').click(function (event) {
    event.preventDefault();
    let pl_number = $(this).attr('cancel-link')
    console.log(pl_number)
    $.ajax({
      url: "/tools/invoices/",
      method: "POST",
      headers: { 'X-CSRFToken': csrfToken },
      data: { link_del_pl: pl_number },
      success: function (response) {
        location.reload()
      },
      error: function (xhr, status, error) {
        console.error('Ошибка AJAX-запроса:', error)
      }
    });
  });
  // ----------------- Блок ссылка-----------------------------
  // Скрипт проверяет, чтобы не отправляли пустую форму.
  $('#pay_form').on('submit', function (event) {
    var selectedValue = $('#pay_select_id').val();
    console.log(selectedValue)
    if (selectedValue === '' || selectedValue === null) {
      alert('Пожалуйста, выберите платеж.');
      event.preventDefault();
    }
  });

  const modalButtons = $('.opp_modal');
  modalButtons.click(function () {
      let invoice_num = $(this).attr('invoice');
      $('#modal-pl-val').val(invoice_num);
      $('#pay_form').attr('action', `/tools/invoices/pllinks/${invoice_num}`);
  
      // Получение списка распределенных заказов как строки
      let table_pays = $('#distributed-pays').val();
  
      // Преобразование строки JSON в массив (если это JSON)
      try {
          table_pays = JSON.parse(table_pays);
      } catch (error) {
          console.error('Ошибка преобразования данных: ', error);
      }
  
      // Фильтрация данных
      let filteredData = table_pays.filter(item => item.invoice_to === parseInt(invoice_num));
      let paysSpan = $('#pays-span');
      if (filteredData.length > 0) {
          // Очистка перед добавлением новых данных
          paysSpan.empty();
  
          // Форматирование данных для вставки
          let paysText = filteredData.map(pay => pay.pay_id).join(', ');
          
          // Использование text() для установки текста напрямую
          paysSpan.text(paysText);
  
          console.log(filteredData);
      } else {
          paysSpan.html('Нет платежей'); // Сообщение, если данных нет
      }
  });
  

  

  // Скрипт на удаление распределений платежа
  $('.pay_delete_button').each(function() {
    $(this).click(function () {
      let invoice = $(this).attr('invoice');
      $.ajax({
        url: "/tools/invoices/",
        method: "POST",
        headers: { 'X-CSRFToken': csrfToken },
        data: { pay_del_invoice: invoice },
        success: function (response) {
          if (response.success) {
            window.location.reload()
          } else {
            alert('Failed to load invoice data');
          }
        },
        error: function (xhr, status, error) {
          console.error('Ошибка AJAX-запроса:', error);
        }
      });
     
    })
  })

  
});

