$(document).ready(function () {
  console.log(1)
  agGrid.LicenseManager.setLicenseKey("DownloadDevTools_COM_NDEwMjM1ODQwMDAwMA==9ad48a3770fd3752296c91fd87af461e");

  const tableFilterData = $('#json_content').val();
  const rowData = JSON.parse(tableFilterData).map(item => ({
    ...item.fields,
    pk: item.pk // Убедитесь, что добавляется поле pk
  }));
  var gridApi;

  var columnDefs = [
        { headerName: "Артикул", field: "pk" },
        { headerName: "Модель", field: "model" },
        { headerName: "Цвет", field: "color" },
        { headerName: "Тип", field: "model_type" },
        { headerName: "Бренд", field: "brand" },

      ]
  

  // Настройка 
  const gridOptions = {
    rowData: rowData,
    columnDefs: columnDefs,
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

  const gridDiv = document.querySelector("#myGrid");
  gridApi = agGrid.createGrid(gridDiv, gridOptions);


});