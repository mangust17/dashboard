agGrid.LicenseManager.setLicenseKey("DownloadDevTools_COM_NDEwMjM1ODQwMDAwMA==9ad48a3770fd3752296c91fd87af461e");
const csrfToken = $('[name=csrfmiddlewaretoken]').val();

// Создание таблицы ag-grid
const tableFilterData = $('#json_content').val();
const rowData = JSON.parse(tableFilterData);
const columnDefs = [
  { field: "id", hide: true},
  { headerName: "Заказ", field: "invoice_id"},
  { headerName: "Модель", field: "model"},
  { headerName: "Артикул", field: "model_id_id"},
  { headerName: "Цвет", field: "color"},
  { headerName: "Количество", field: "quantity", editable: true},
  { headerName: "Цена за шт", field: "price_per_unit", editable: true},
  // Обработка удаления
  {
    headerName: "Действие",
    field: "action",
    cellRenderer: function(params) {
      const divElem = document.createElement('div');
      divElem.innerHTML = 'Удалить';
      divElem.classList.add('cursor-pointer','text-red');
      divElem.addEventListener('click', function() {
        const selectedRow = params.node.data;
        params.api.applyTransaction({ remove: [selectedRow] });
        let invoiceNum = params.data.invoice_id
        let modelId = params.data.model_id_id
        let ajaxUrl = '/tools/invoices/'+String(invoiceNum)
        $.ajax({
          url: ajaxUrl,
          method: "POST",
          headers: { 'X-CSRFToken': csrfToken },
          data: { invoice_id: invoiceNum , modelId: modelId, action: 'delete'},
          success: function (response) {
            if (response.success) {
              console.log(response.success)
            } else {
              alert('Failed to load invoice data');
            }
          },
          error: function (xhr, status, error) {
            console.error('Ошибка AJAX-запроса:', error);
          }
        });
      });
      return divElem;
    },
  }
];

const gridOptions = {
  rowData: rowData,
  columnDefs: columnDefs,
  domLayout: 'autoHeight',
  columnTypes: {
    editableColumn: {
      editable: (params) => isCellEditable(params),
      cellStyle: (params) => {
        if (isCellEditable(params)) {
          return { backgroundColor: "#2244CC44" };
        }
      },
    },
  },
  defaultColDef: {
    flex: 1,
    filter: true,
    menuTabs: ["filterMenuTab"],
    filterParams: {
      buttons: ['reset', 'apply'],
      excelMode: 'windows'
    },
  },
  groupSelectsChildren: true,
  rowSelection: "multiple",
  
  suppressRowClickSelection: true,
  suppressAggFuncInHeader: true,
  onGridReady: function (params) {
    gridApi = params.api;
  }
};



$(document).ready(function () {
  const Grid = new GridManager(gridOptions, rowData, csrfToken);

  // Сохранение изменений
  $('#save-changes-button').click(function() {
    let changes = Grid.getChangedRows();
    const currentUrl = window.location.href;
    $.ajax({
      url: currentUrl,
      method: "POST",
      headers: { 'X-CSRFToken': csrfToken },
      data: JSON.stringify({ changes: changes }),
      contentType: 'application/json',
      success: function (response) {
        if (response.success) {
          alert('Изменения сохранены')
        } else {
          alert('Failed to load invoice data');
        }
      },
      error: function (xhr, status, error) {
        console.error('Ошибка AJAX-запроса:', error);
      }
    });
  });






  // Скрипт для добавления модели
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
  var addButton = $('#add-button')

  addButton.click(function(){
    model = modelField.val();
    color = optionsSpan.val();
    qty = $('#quantity_field').val();
    price = $('#price_field').val();
    let invNumber = $('#invoice-num').val();
    let ajaxUrl = '/tools/invoices/'+String(invNumber)
    console.log(model, color, invNumber)
    $.ajax({
      url: ajaxUrl,
      method: "POST",
      headers: { 'X-CSRFToken': csrfToken },
      data: { invoice_id: invNumber, model: model, color: color, action: 'add', qty: qty, price: price },
      success: function (response) {
        if (response.success) {
          $('#myModal').modal('hide');
          const newRow = {
            invoice_id: response.invoice_id,
            model: response.model,
            model_id_id: response.model_id_id,
            color: response.color,
            quantity: Number(response.quantity),
            price_per_unit: Number(response.price_per_unit),
          };
          gridApi.applyTransaction({ add: [newRow], addIndex: 0 });
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

