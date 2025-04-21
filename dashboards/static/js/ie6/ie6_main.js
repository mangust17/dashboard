"use strict";

function _typeof(o) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (o) { return typeof o; } : function (o) { return o && "function" == typeof Symbol && o.constructor === Symbol && o !== Symbol.prototype ? "symbol" : typeof o; }, _typeof(o); }
function _classCallCheck(a, n) { if (!(a instanceof n)) throw new TypeError("Cannot call a class as a function"); }
function _defineProperties(e, r) { for (var t = 0; t < r.length; t++) { var o = r[t]; o.enumerable = o.enumerable || !1, o.configurable = !0, "value" in o && (o.writable = !0), Object.defineProperty(e, _toPropertyKey(o.key), o); } }
function _createClass(e, r, t) { return r && _defineProperties(e.prototype, r), t && _defineProperties(e, t), Object.defineProperty(e, "prototype", { writable: !1 }), e; }
function _toPropertyKey(t) { var i = _toPrimitive(t, "string"); return "symbol" == _typeof(i) ? i : i + ""; }
function _toPrimitive(t, r) { if ("object" != _typeof(t) || !t) return t; var e = t[Symbol.toPrimitive]; if (void 0 !== e) { var i = e.call(t, r || "default"); if ("object" != _typeof(i)) return i; throw new TypeError("@@toPrimitive must return a primitive value."); } return ("string" === r ? String : Number)(t); }
var GridManager = /*#__PURE__*/function () {
  function GridManager(gridOptions, rowData, csrfToken) {
    _classCallCheck(this, GridManager);
    this.gridOptions = gridOptions;
    this.rowData = rowData;
    this.csrfToken = csrfToken;
    this.gridApi = null;
    this.initGrid();
  }
  return _createClass(GridManager, [{
    key: "initGrid",
    value: function initGrid() {
      var gridDiv = document.querySelector("#myGrid");

      // Создаем сетку и сохраняем ссылку на API
      new agGrid.Grid(gridDiv, this.gridOptions);
      this.gridApi = this.gridOptions.api;

      // Можно установить данные, если они есть
      if (this.rowData) {
        this.gridApi.setRowData(this.rowData);
      }
    }
  }, {
    key: "getSelectedRowsFromGrid",
    value: function getSelectedRowsFromGrid(field) {
      var selectedRows = this.gridApi.getSelectedRows();
      var selectedValues = selectedRows.map(function (row) {
        return row[field];
      });
      var filterModel = {
        first_model_id_ns: {
          filterType: 'set',
          values: selectedValues
        }
      };
      this.gridApi.setFilterModel(filterModel);
      this.gridApi.onFilterChanged();
    }
  }, {
    key: "getAllRows",
    value: function getAllRows() {
      var allRows = [];
      this.gridApi.forEachNode(function (node) {
        return allRows.push(node.data);
      });
      return allRows;
    }
  }, {
    key: "sendGridToAjax",
    value: function sendGridToAjax(url, successFunc) {
      var allRows = this.getAllRows();
      $.ajax({
        url: url,
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken
        },
        data: {
          grid: allRows
        },
        contentType: 'application/json',
        success: function success(response) {
          successFunc();
        },
        error: function error(xhr, status, _error) {
          console.error('Ошибка AJAX-запроса:', _error);
        }
      });
    }
  }]);
}();