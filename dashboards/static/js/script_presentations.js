$(document).ready(function () {
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  agGrid.LicenseManager.setLicenseKey("DownloadDevTools_COM_NDEwMjM1ODQwMDAwMA==9ad48a3770fd3752296c91fd87af461e");

  const tableFilterData = $('#json_models').val();
  const rowData = JSON.parse(tableFilterData);
  let gridApi;

  // Настройка 
  const gridOptions = {
    rowData: rowData,
    columnDefs: [
      {
        field: "model", checkboxSelection: true,
        showDisabledCheckboxes: true
      },
      { field: "color" },
      { field: "model_type_id", filter: "agSetColumnFilter" },
      {
        field: "first_model_id_ns"
      }
    ],
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
    }
  };

  const Grid = new GridManager(gridOptions, rowData, csrfToken);

  // Сброс фильтров
  $('#resetFilter').click(function () {
    gridApi.setFilterModel(null); 
    gridApi.onFilterChanged();
  });

  // Ajax для создания тендера
  $('#submit_button').click(function () {
    const selectedRows = gridApi.getSelectedRows();
    const selectedValues = selectedRows.map(row => row.first_model_id_ns);
    const tenderName = $('#tender_name').val()
    const customerName = $('#customer_select_id').val()
    const participants = $('#participants').val()
    console.log(selectedValues)
    if (!tenderName) {
      alert('Имя тендера не может быть пустым.');
      return;
    } else if (selectedValues.length == 0) {
      alert('Выберите хотя бы одну модель');
      return;
    }
    
    $.ajax({
      url: '/tenders/create/',
      method: 'POST',
      headers: { 'X-CSRFToken': csrfToken },

      data: JSON.stringify({ models: selectedValues, tenderName: tenderName, customer: customerName, participants: participants }),
      success: function (response) {
        console.log('Success');
        window.location.href = '/tenders/?success=true'
      },
      error: function (xhr, status, error) {
        console.error('Ошибка AJAX-запроса:', error);
      }
    });

  });


  // Ajax для удаления тендера
  const delSpan = $('#del_span')
  delSpan.click(function() {
    const tenderDelNum = $(this).attr('tender-num')
    console.log(tenderDelNum)
  });
  

});
