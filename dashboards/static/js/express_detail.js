$(document).ready(function () {
  const plNum = $('#pl_select_id').attr('cur-pl')
  console.log(plNum)
  // Select2: Выбора модели и фильтрация цвета
  var modelField = $("#select2insidemodal");
  var optionsSpan = $('#color_select')
  var colorDiv = $('#color_select_div')

  modelField.on('select2:select', function (e) {
    var selectedModel = $(this).find(':selected').text();
    $.ajax({
      url: '/get_colors/',
      type: 'GET',
      data: {
        'model': selectedModel
      },
      success: function (response) {
        // Очищаем текущие опции в поле выбора цвета
        optionsSpan.empty();
        colorDiv.show();
        // Добавляем новые опции, полученные с сервера
        $.each(response.colors, function (key, value) {
          optionsSpan.append($('<option>', {
            value: value,
            text: value
          }));
        });

      },
      error: function (xhr, status, error) {
        console.error(xhr.responseText);
      }
    });
  });
  // Отображение нулей, реакция на чек бокс
  var showNullsButton = $("#filterCheckbox");
  if (showNullsButton.is(":checked")) {
    var flag=0
  } else{
    var flag=1
  }
  var invoiceNumber = showNullsButton.attr('invoice-num')
  showNullsButton.on('change', function () {
    url = '/tools/express_refresh_detail/' + invoiceNumber + '/' + flag + '/' + plNum
    window.location.href = url;


  });
  // Переключение вкладок
  var nav_buttons = document.querySelectorAll("#plnavibar .nav-link");
  var pl_tab = document.getElementById('pl_table')
  var bought_tab = document.getElementById('tab_bought')
  nav_buttons.forEach(function (button) {
    button.addEventListener('click', (el) => {
      buttonText = button.textContent;
      if (buttonText === "PL") {
        bought_tab.style.display = "none";
        pl_tab.style.display = "block";
      }
      else if (buttonText === "Куплено") {
        pl_tab.style.display = "none";
        bought_tab.style.display = "block";
      };

    });
  });
  // Передача артикула в модальное окно
  const editModelIDinput = document.querySelector('#edit_model_id')
  const editModelIDButtons = document.querySelectorAll('.edit_modal_button')

  editModelIDButtons.forEach(function (button) {
    button.addEventListener('click', function () {
      editModelIDinput.value = button.getAttribute('model-id')
    });
  });

  // Переключение инвойсов
  $("#ivoice_selector").change(function () {
    let invNumber = $(this).val();
    let hideNulls = $(this).attr('hide-nulls')
    let urlLink ='/tools/express_refresh_detail/' + invNumber + '/' + hideNulls + '/' + plNum
    window.location.href = urlLink;
  });

  // Переключение PL
  $("#pl_select_id").change(function () {
    invoiceSelector = $('#ivoice_selector')
    let invNumber = $(invoiceSelector).val();
    let hideNulls = $(invoiceSelector).attr('hide-nulls')
    let plNewVal = $(this).val()
    let urlLink ='/tools/express_refresh_detail/' + invNumber + '/' + hideNulls + '/' + plNewVal
    window.location.href = urlLink;
  });


});
