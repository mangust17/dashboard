
class GridManager {
  
  constructor(gridOptions, rowData ,csrfToken) {
    this.gridOptions = gridOptions;
    this.rowData = rowData;
    this.gridApi = null;
    this.initGrid();
    this.csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    this.changedRows = [];
  }

  initGrid() {
    const gridDiv = document.querySelector("#myGrid");

    // Создаем сетку и сохраняем ссылку на API
    this.gridApi = agGrid.createGrid(gridDiv, this.gridOptions);

    // Можно установить данные, если они есть
    if (this.rowData) {
      this.gridApi.setGridOption('rowData', this.rowData);
    }
  }

  getSelectedRowsFromGrid(field) {
    const selectedRows = this.gridApi.getSelectedRows();
    const selectedValues = selectedRows.map(row => row[field]);
    const filterModel = {
      first_model_id_ns: {
        filterType: 'set',
        values: selectedValues
      } 
    };
    this.gridApi.setFilterModel(filterModel);
    this.gridApi.onFilterChanged();

  }

  handleCellValueChanged(event) {
    const rowIndex = event.rowIndex;
    const changedData = event.data;

    const existingIndex = this.changedRows.findIndex(row => row.rowIndex === rowIndex);
    if (existingIndex !== -1) {
      this.changedRows[existingIndex].data = changedData;
    } else {
      this.changedRows.push({ rowIndex, data: changedData });
    }
  }

  getAllRows() {
    const allRows = [];
    this.gridApi.forEachNode(node => allRows.push(node.data));
    return allRows;
  }

  getChangedRows() {
    return this.changedRows.map(row => row.data);
  }

  getAllRowsAsHtml() {
    const gridDiv = document.querySelector("#myGrid");
    const tableHtml = gridDiv.querySelector('.ag-root').outerHTML;
    return tableHtml;
  }

  sendGridToAjax(url, successFunc) {
    const allRows = this.getAllRows()
    $.ajax({
      url: url,
      method: 'POST',
      headers: { 'X-CSRFToken': this.csrfToken },
      data: JSON.stringify({ grid: allRows }),
      contentType: 'application/json',
      
      success: function (response) {
        if (response.success == true) {
          successFunc()
        }
        
      },
      error: function (xhr, status, error) {
        console.error('Ошибка AJAX-запроса:', error);
      }
    });
  }
  
  exportGridAsXlsx() {
    this.gridApi.exportDataAsExcel({ fileName: 'Таблица для тендара.xlsx' })
  }

  exportGridAsImage(url, successFunc) {
    
    const gridDiv = document.querySelector("#myGrid");

    html2canvas(gridDiv, { scale: 2 }) // Установка масштаба
        .then(canvas => {
            const imageData = canvas.toDataURL('image/png');
            
            $.ajax({
                url: url, // Замените на ваш URL
                method: 'POST',
                headers: { 'X-CSRFToken': this.csrfToken },
                data: JSON.stringify({ png_image: imageData }),
                contentType: 'application/json',
                success: function (response) {
                    if (response.success === true) {
                      successFunc()
                    }
                },
                error: function (xhr, status, error) {
                    console.error('Ошибка AJAX-запроса:', error);
                }
            });
        });
}
}