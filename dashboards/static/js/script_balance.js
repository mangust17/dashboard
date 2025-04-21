
agGrid.LicenseManager.setLicenseKey("DownloadDevTools_COM_NDEwMjM1ODQwMDAwMA==9ad48a3770fd3752296c91fd87af461e");


const tableFilterData = $('#json_content').val();
const rowData = JSON.parse(tableFilterData);

function customPercentAggFunc(params) {
  let sumQty = 0;
  let sumPlQty = 0;


  params.rowNode.childrenAfterGroup.forEach(childNode => {
    const data = childNode.data;
    if (data && data.invoicecontents__quantity != null && data.pl_qty != null) {
      sumQty += data.invoicecontents__quantity;
      sumPlQty += data.pl_qty;
    }
  });

  const percentage = sumQty ? (sumPlQty / sumQty) * 100 : 0;
  return Math.round(percentage);  // Округление до целого числа
}

function percentsFormatter(params) {
  return params.value + "%";
}

const columnDefs = [
  { field: "pk", rowGroup: true, hide: true },
  { headerName: "Присвоенный номер", field: "real_number", aggFunc: "first" },
  {
    field: "date_start", aggFunc: "max", valueFormatter: function (params) {
      // Пример форматирования даты
      const date = new Date(params.value);
      const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
      return date.toLocaleDateString('ru-RU', options); // Форматирование для русского языка
    }, filter: 'agDateColumnFilter'
  },
  { headerName: "Покупатель", field: "customer", aggFunc: "first" },
  { headerName: "Модель", field: "invoicecontents__model_id", aggFunc: 'count' },
  { headerName: "Кол-во в заказе", field: "invoicecontents__quantity", aggFunc: "sum" },
  { headerName: "Отгружено", field: "pl_qty", aggFunc: "sum" },
  { headerName: "Осталось", field: "left", aggFunc: "sum" },
  {
    headerName: "Процент выполнения",
    field: "percent",
    valueGetter: function (params) {
      const quantity = params.data.invoicecontents__quantity || 0;
      const pl_qty = params.data.pl_qty || 0;
      const percentage = quantity ? (pl_qty / quantity) * 100 : 0;
      return Math.round(percentage);  // Округление до целого числа
    },
    aggFunc: customPercentAggFunc,
    cellClassRules: {
      "ag-red": "x < 30",
      "ag-yellow": "x >= 30 && x < 90",
      "ag-green": "x >= 90",
    },
    valueFormatter: percentsFormatter

  },
  { field: "select_flag", aggFunc: 'first'}
];


const gridOptions = {
  rowData: rowData,
  columnDefs: columnDefs,
  defaultColDef: {
    flex: 1,
    filter: true,
    menuTabs: ["filterMenuTab"],
    filterParams: {
      buttons: ['reset', 'apply'],
      excelMode: 'windows'
    },
  },
  autoGroupColumnDef: {
    headerName: "Заказ",
    field: "pk",
    headerCheckboxSelection: true,
    cellRenderer: 'agGroupCellRenderer',
    cellRendererParams: {
      checkbox: true,
    },
  },
  groupSelectsChildren: true,
  rowSelection: "multiple",
  suppressRowClickSelection: true,
  suppressAggFuncInHeader: true,
  grandTotalRow: "top",
  onGridReady: function (params) {
    gridApi = params.api;
  },
  onFirstDataRendered: function (params) {
    params.api.forEachNode((node) => {
      // Проверяем, есть ли данные в узле
      if (node.data && node.data.select_flag === 'default') {
        node.setSelected(true);  // Выделяем строки с определенным статусом
      }
    });
  }
};



$(document).ready(function () {
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const gridDiv = document.querySelector("#myGrid");
  new agGrid.Grid(gridDiv, gridOptions); // Инициализация грида
  // Сохранение представления в базу данных
  const saveButton = $('#save-button')
  const spinner = saveButton.find('.spinner-border');
  const buttonTextSpan = saveButton.find('.botton-text-span')
  const resetButton = $('#reset-button')
  function enableSpinner() {
    spinner.show()
    buttonTextSpan.text('Сохранение')
  }

  function disableSpinner() {
    spinner.hide()
    buttonTextSpan.text('Сохранить представление')
  }


  saveButton.click(function () {
    enableSpinner()
    var selectedNodes = gridApi.getSelectedNodes();
    // Создаем массив для хранения данных JSON
    var jsonData = [];

    // Перебираем выбранные строки и собираем данные в JSON
    selectedNodes.forEach(function (node) {
      var data = node.data;
      // Добавляем в массив только необходимые поля
      jsonData.push({
        invoice: data.pk,
        model_id: data.invoicecontents__model_id,
      });
    });
    setTimeout(function () {
      $.ajax({
        url: "/tools/balance/",
        method: "POST",
        headers: { 'X-CSRFToken': csrfToken, 'Content-Type': 'application/json' },
        data: JSON.stringify({ data: jsonData }),
        success: function (response) {
          disableSpinner()
          window.location.href = '/tools/balance/';
        },
        error: function (xhr, status, error) {
          console.error('Ошибка AJAX-запроса:', error);
        }
      });
    }, 1000)

  })

  resetButton.click(function () {
    $.ajax({
      url: "/tools/balance/",
      method: "POST",
      headers: { 'X-CSRFToken': csrfToken },
      data: { reset: true },
      success: function (response) {
        console.log(response.success)
        if (response.success) {
          window.location.href = '/tools/balance/';
        } else {
          alert('Failed to load invoice data');
        }
      },
      error: function (xhr, status, error) {

      }
    });
  })

});

