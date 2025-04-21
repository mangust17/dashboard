/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./assets/scripts/index.js":
/*!*********************************!*\
  !*** ./assets/scripts/index.js ***!
  \*********************************/
/***/ (() => {

eval("\r\nclass GridManager {\r\n\r\n  constructor(gridOptions, rowData, csrfToken) {\r\n    this.gridOptions = gridOptions;\r\n    this.rowData = rowData;\r\n    this.gridApi = null;\r\n    this.csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;\r\n    this.changedRows = [];\r\n    this.initGrid();\r\n  }\r\n\r\n  initGrid() {\r\n    const gridDiv = document.querySelector(\"#myGrid\");\r\n\r\n    // Создаем сетку и сохраняем ссылку на API\r\n    this.gridApi = agGrid.createGrid(gridDiv, this.gridOptions);\r\n    this.gridApi.addEventListener('cellValueChanged', this.handleCellValueChanged.bind(this));\r\n    // Можно установить данные, если они есть\r\n    if (this.rowData) {\r\n      this.gridApi.setGridOption('rowData', this.rowData);\r\n    }\r\n\r\n  }\r\n\r\n  getSelectedRowsFromGrid(field) {\r\n    const selectedRows = this.gridApi.getSelectedRows();\r\n    const selectedValues = selectedRows.map(row => row[field]);\r\n    const filterModel = {\r\n      first_model_id_ns: {\r\n        filterType: 'set',\r\n        values: selectedValues\r\n      }\r\n    };\r\n    this.gridApi.setFilterModel(filterModel);\r\n    this.gridApi.onFilterChanged();\r\n\r\n  }\r\n\r\n  handleCellValueChanged(event) {\r\n    console.log('Cell value changed event:', event);\r\n    const rowIndex = event.rowIndex;\r\n    const changedData = event.data;\r\n    const column = event.column;\r\n    const rowNode = event.node;\r\n\r\n    const existingIndex = this.changedRows.findIndex(row => row.rowIndex === rowIndex);\r\n    if (existingIndex !== -1) {\r\n      this.changedRows[existingIndex].data = changedData;\r\n    } else {\r\n      this.changedRows.push({ rowIndex, data: changedData });\r\n    }\r\n\r\n  }\r\n\r\n  getAllRows() {\r\n    const allRows = [];\r\n    this.gridApi.stopEditing();\r\n    this.gridApi.forEachNode(node => allRows.push(node.data));\r\n    return allRows;\r\n  }\r\n\r\n  getChangedRows() {\r\n    return this.changedRows.map(row => row.data);\r\n  }\r\n\r\n  getAllRowsAsHtml() {\r\n    const gridDiv = document.querySelector(\"#myGrid\");\r\n    const tableHtml = gridDiv.querySelector('.ag-root').outerHTML;\r\n    return tableHtml;\r\n  }\r\n\r\n  sendGridToAjax(url, successFunc) {\r\n    const allRows = this.getAllRows()\r\n    $.ajax({\r\n      url: url,\r\n      method: 'POST',\r\n      headers: { 'X-CSRFToken': this.csrfToken },\r\n      data: JSON.stringify({ grid: allRows }),\r\n      contentType: 'application/json',\r\n\r\n      success: function (response) {\r\n        if (response.success == true) {\r\n          successFunc()\r\n        }\r\n\r\n      },\r\n      error: function (xhr, status, error) {\r\n        console.error('Ошибка AJAX-запроса:', error);\r\n      }\r\n    });\r\n  }\r\n\r\n  exportGridAsXlsx() {\r\n    this.gridApi.exportDataAsExcel({ fileName: 'Таблица для тендара.xlsx' })\r\n  }\r\n\r\n  exportGridAsImage(url, successFunc) {\r\n\r\n    const gridDiv = document.querySelector(\"#myGrid\");\r\n\r\n    html2canvas(gridDiv, { scale: 2 }) // Установка масштаба\r\n      .then(canvas => {\r\n        const imageData = canvas.toDataURL('image/png');\r\n\r\n        $.ajax({\r\n          url: url, // Замените на ваш URL\r\n          method: 'POST',\r\n          headers: { 'X-CSRFToken': this.csrfToken },\r\n          data: JSON.stringify({ png_image: imageData }),\r\n          contentType: 'application/json',\r\n          success: function (response) {\r\n            if (response.success === true) {\r\n              successFunc()\r\n            }\r\n          },\r\n          error: function (xhr, status, error) {\r\n            console.error('Ошибка AJAX-запроса:', error);\r\n          }\r\n        });\r\n      });\r\n  }\r\n}\r\n\r\nwindow.GridManager = GridManager;\n\n//# sourceURL=webpack://opt_one/./assets/scripts/index.js?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = {};
/******/ 	__webpack_modules__["./assets/scripts/index.js"]();
/******/ 	
/******/ })()
;