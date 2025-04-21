
$(document).ready(function () {
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  agGrid.LicenseManager.setLicenseKey("DownloadDevTools_COM_NDEwMjM1ODQwMDAwMA==9ad48a3770fd3752296c91fd87af461e");

  const tableFilterData = $('#json_models').val();
  const rowData = JSON.parse(tableFilterData);
  const marginInput = $("#margin-input")
  const spinner = $('#spinner');
  var gridApi;
  spinner.removeClass('show');
  var columnDefs = [
    {
      headerName: 'Основные параметры',
      children: [
        {
          headerName: "Артикул", field: "model_id_id", checkboxSelection: true,
          showDisabledCheckboxes: true
        },
        { headerName: "Модель", field: "model_id_id__model" },
        { headerName: "Цвет", field: "model_id_id__color" },
        { headerName: "Прошлая цена продажи", field: "last_price" },
        {
          headerName: "Минимальная цена", field: "min_price",
        },
        { headerName: "Цена с закупкой", field: "min_price", valueGetter: params => params.data.min_price * (1 + marginInput.val() / 100), valueFormatter: p => Number(p.value).toFixed(2) },
        {
          headerName: "Отклонение (%)",
          valueGetter: params => {
            var minPrice = params.data.min_price * (1 + marginInput.val() / 100);
            var purchasePrice = params.data.min_price; // предполагаем, что это цена закупки
            if (purchasePrice !== 0) {
              return ((minPrice / purchasePrice) - 1) * 100;
            } else {
              return null; // обработка деления на ноль или другие случаи
            }
          },
          valueFormatter: params => params.value.toFixed(1) + "%"
        },
        {
          headerName: "Группа презентации", field: "group", editable: true,
          valueGetter: params => {
            if (params.data.group === undefined || params.data.group === null) {
              params.data.group = 1; // Установить значение 1, если оно не определено
            }
            return params.data.group;
          },
          valueSetter: params => {
            params.data.group = params.newValue;
            return true; // Указывает, что установка успешна
          }
        },
        { headerName: "Количество", field: "quantity", editable: true },
      ]
    },
    {
      headerName: "Продавец 1", children: [
        { headerName: "Цена", field: "vendor1_price", cellClassRules: { 'ag-highlight-cell': params => params.value === params.data.min_price } },
        { headerName: "Количество", field: "vendor1_qty" },
      ]
    },
    {
      headerName: "Продавец 2", children: [
        { headerName: "Цена", field: "vendor2_price", cellClassRules: { 'ag-highlight-cell': params => params.value === params.data.min_price } },
        { headerName: "Количество", field: "vendor2_qty" },
      ]
    },
    {
      headerName: "Продавец 3", children: [
        { headerName: "Цена", field: "vendor3_price", cellClassRules: { 'ag-highlight-cell': params => params.value === params.data.min_price } },
        { headerName: "Количество", field: "vendor3_qty" },
      ]
    },
    {
      headerName: "Продавец 4", children: [
        { headerName: "Цена", field: "vendor4_price", cellClassRules: { 'ag-highlight-cell': params => params.value === params.data.min_price } },
        { headerName: "Количество", field: "vendor4_qty" },
      ]
    },
    {
      headerName: "Продавец 5", children: [
        { headerName: "Цена", field: "vendor5_price", cellClassRules: { 'ag-highlight-cell': params => params.value === params.data.min_price } },
        { headerName: "Количество", field: "vendor5_qty" },
      ]
    }
  ]

  // Настройка 
  const gridOptions = {
    rowData: rowData,
    columnDefs: columnDefs,
    enableRangeSelection: true,
    clipboardPaste: true,
    defaultColDef: {
      flex: 1,
      filter: true,
      menuTabs: ["filterMenuTab"],
      filterParams: {
        buttons: ['reset', 'apply'], // Используем кнопки "сбросить" и "применить"
        excelMode: 'windows' // Включаем Excel-подобный режим
      }
    },
    rowSelection: "multiple",
    suppressRowClickSelection: true,
    onGridReady: function (params) {
      gridApi = params.api;
    },
    rowClassRules: {
      'ag-highlight-row': function (p) {
        return p.data.quantity > 0;
      }
    }
  };

  const Grid = new GridManager(gridOptions, rowData, csrfToken)

  // Сохранение презентации
  const createButton = $('#create-button')
  createButton.click(function () {
    spinner.addClass('show_transparent');
    url = window.location.href;
    function successFunc() {
      $('#download-pptx-button').show();
      spinner.removeClass('show_transparent');
    }
    Grid.sendGridToAjax(url, successFunc)
  });

  // Добавление колонок
  const addButton = $('#add_column');
  var counter = 6
  function addColumn() {
    columnDefs = [...columnDefs, {
      headerName: "Продавец " + String(counter),
      children: [
        { headerName: "Цена", field: "price" + String(counter), editable: true },
        { headerName: "Количество", field: "qty" + String(counter), editable: true },
      ]
    }];

    counter++;
    gridApi.setGridOption("columnDefs", columnDefs);
  }

  addButton.click(function () {
    addColumn()
  });

  // Редактирование маржи
  marginInput.change(function () {

    columnDefs.forEach(function (columnDef) {
      if (columnDef.headerName === "Минимальная цена") {
        columnDef.valueGetter = function (params) {
          return params.data.min_price * (1 + marginInput.val() / 100);
        };
        // columnDef.valueFormatter = p => Number(p.value).toFixed(2);
      }
    });
    gridApi.setGridOption("columnDefs", columnDefs);

  })

  // Скачивание таблицы
  $('#download-xls-button').click(() => Grid.exportGridAsXlsx());

});
