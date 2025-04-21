$(document).ready(function () {
  const cells = document.querySelectorAll("#check_status_table td.td_color");

  cells.forEach(cell => {
    // Если содержимое ячейки не равно "0", заменяем его на галочку
    if (Number(cell.textContent.trim()) !== 0) {
        cell.innerHTML = '&#x2713;'; // Unicode символ для галочки
        cell.style.color = 'green'; // Задаем зеленый цвет для галочки
    }
});
});