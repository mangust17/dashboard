$(document).ready(function () {
  $('.sidebar, .content').addClass("disabled");
  $('.sidebar, .content').toggleClass("open");
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  
  // Получение отредактированной таблицы
  var messageTableRows = $('#message-table tbody tr');
  const distributeButton = $('#distribute-button')
  var addArticleButton;


  function getTableData() {
    let data = [];
    messageTableRows = $('#message-table tbody tr');
    messageTableRows.each(function () {
      const row = $(this);
      const rowData = {
        string: row.find('td.text-start').text().trim(),
        model: row.find('td:nth-child(2)').text().trim(),
        color: row.find('td:nth-child(3)').text().trim(),
        qty: row.find('td:nth-child(4)').text().trim(),
        model_id: row.find('td.jq-model-id').text().trim(),
        selected_model_id: row.find('td:nth-child(6) select').val(),
        invoice: row.find('td:nth-child(7) select').val(),
        quantity: row.find('td:nth-child(8) input').val()
      };
      data.push(rowData);
    });

    return data;
  }

  // Функция для окрашивания ячейки
  function colorCard(msgCell, newColor) {
    let borderedElement = msgCell.find('.card')
    borderedElement.attr('class', `card rounded h-100 border-${newColor} p-2 mb-3`);
    let textColor = borderedElement.find('.card-body')
    textColor.attr('class', `card-body p-2 msg-div-text cursor-pointer text-${newColor}`)
  }

  // Действия кнопки распределения
  distributeButton.click(function () {
    if ($('#msg-status').val() === 'saved') {
      $(this).addClass('disabled').prop('disabled', true);
      var tableData = getTableData();
      let msgNum = $('#msg-id').val()
      let dataToSend = {
        distribute_table: tableData,
        msg_num: msgNum
      }
      var tableJson = JSON.stringify(dataToSend);
      console.log(tableJson)
      $.ajax({
        url: "/itask_parse/default/",
        method: "POST",
        headers: { 'X-CSRFToken': csrfToken },
        contentType: "application/json",
        data: tableJson,
        success: function (response) {
          window.location.reload()
        },
        error: function (xhr, status, error) {
          alert('Сначала сохраните сообщение')
          window.location.reload();
        }
      });
    } else {
      alert('Сначала необходимо сохранить сообщение')
    }
  });

  // Добавление артикула в сообщение
  function addArticle(button) {
    $(button).each(function () {
      $(this).click(function () {
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
  }

  // Сохранение контента SMS
  const saveButton = $('#save-button')
  saveButton.click(function () {
    $(this).addClass('disabled').prop('disabled', true);
    data_msg = getTableData()
    let allFieldsFilled = true;

    data_msg.forEach(function (row) {
      if (row.model_id === '+') {
        alert('Заполните все артикулы')
        allFieldsFilled = false;
      }
    });
    if (allFieldsFilled) {
      let msgNum = $('#msg-id').val()
      $.ajax({
        url: "/itask_parse/default/",
        method: "POST",
        contentType: "application/json",
        headers: { 'X-CSRFToken': csrfToken },
        data: JSON.stringify({ msgToSave: data_msg, msgNum: msgNum }),
        success: function (response) {
          if (response.success) {
            colorCard($(`#msg-card-${response.msg_num}`), 'warning');
            $('#msg-status').val('saved')
            $('#save-button').hide()
          } else {
            alert('Failed to load invoice data');
          }
        },
        error: function (xhr, status, error) {
          console.error('Ошибка AJAX-запроса:', error);
        }
      });
    }
  });

  // Отмена сохранения (кнопки U)
  const unselectButtons = $('.msg-unselect-buttons')
  unselectButtons.each(function () {
    $(this).click(function () {
      let msgNum = $(this).attr('msg-id')
      $.ajax({
        url: "/itask_parse/default/",
        method: "POST",
        headers: { 'X-CSRFToken': csrfToken },
        data: { unselect_msg_num: msgNum },
        success: function (response) {
          if (response.success) {
            colorCard($(`#msg-card-${response.msg_id}`), 'primary');
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

  // Удаление хештегов
  const delButtons = $('.msg-del-buttons')
  delButtons.each(function () {
    $(this).click(function () {
      msgId = $(this).attr('msg-id')
      $.ajax({
        url: "/itask_parse/default/",
        method: "POST",
        headers: { 'X-CSRFToken': csrfToken },
        data: { msg_id: msgId },
        success: function (response) {
          if (response.success) {
            msgCard = $('#msg-card-' + String(msgId))
            msgCard.slideUp(500)
          } else {
            console.log('Failed to load invoice data');
          }
        },
        error: function (xhr, status, error) {
          console.error('Ошибка AJAX-запроса:', error);
        }
      });
    })
  })

  // Подгрузка сообщения в поле + парсинг

  messageCardDivs = $('.msg-div-text')
  var modelsString = $('#model_list').val()
  var invoicesString = $('#invoices_list').val()
  var models = JSON.parse(modelsString.replace(/'/g, '"'));
  var invoices = JSON.parse(invoicesString.replace(/'/g, '"'));
  messageCardDivs.click(function () {
    $('.card').each(function () {
      $(this).css('background', 'none')
    })
    $(this).parent().css('background-color', 'rgba(196, 0, 218, 0.173)')

    msgNum = $(this).attr('msg-id');
    $('#msg-id').val(msgNum);
    $.ajax({
      url: "/itask_parse/default/",
      method: "POST",
      headers: { 'X-CSRFToken': csrfToken },
      data: { msgNum: msgNum },
      success: function (response) {
        if (response.success) {
          var tableBody = $('#message-table tbody');
          var parsedData = response.message;
          tableBody.empty();
          console.log(response.message_status)
          if (response.message_status == 'saved') {
            $('#save-button').hide()
            $('#msg-status').val('saved')
          } else {
            $('#save-button').show()
          }

          parsedData.forEach(function (row, index) {
            let hasMatch = models.includes(row.model_id);
            let selectOptions = `<option value="" ${!hasMatch ? 'selected' : ''}></option>`; // Пустая опция

            selectOptions += models.map(model => {
              let isSelected = row.model_id === model ? 'selected' : ''; // Проверяем, совпадает ли model_id с model
              return `<option value="${model}" ${isSelected}>${model}</option>`;
            }).join('');

            let orderOptions = invoices.map(order => {
              return `<option value="${order}">${order}</option>`;
            }).join('');

            let newRow = `
                <tr>
                    <td class="text-start">${row.id}</td>
                    <td>${row.model}</td>
                    <td>${row.color}</td>
                    <td>${row.qty}</td>
                    <td class="jq-model-id" id="${row.model}${row.color}">
                        ${row.model_id ? row.model_id : `<b class="cursor-pointer add-article-b" model-to-add="${row.model}" color-to-add="${row.color}" style="color:green">+</b>`}
                    </td>
                    <td>
                        <select class="form-control form-control-sm distribute_model_id_select">
                            ${selectOptions}
                        </select>
                    </td>
                    <td>
                        <select class="form-control form-control-sm order-select">
                            ${orderOptions}
                        </select>
                    </td>
                    <td>
                        <input type="number" class="form-control form-control-sm" value="${row.qty || 0}">
                    </td>
                </tr>
            `;
            tableBody.append(newRow);
          });
          addArticleButton = $('.add-article-b')
          addArticle(addArticleButton)

        } else {
          alert('Failed to load invoice data');
        }
      },
      error: function (xhr, status, error) {
        console.error('Ошибка AJAX-запроса:', error);
      }
    });
  })

  // Отправка сообщения в группу
  sendMessageButton = $('#send-message-button')
  sendMessageButton.click(function (event) {
    event.preventDefault();
    $.ajax({
      url: "/bot-send-message/",
      method: "POST",
      headers: { 'X-CSRFToken': csrfToken },
      data: { message: 'Тестирование' },
      success: function (response) {
        if (response.success) {
          console.log('123')
        } else {
          alert('Failed to load invoice data');
        }
      },
      error: function (xhr, status, error) {
        console.error('Ошибка AJAX-запроса:', error);
      }
    });
  })
});

