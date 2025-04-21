document.addEventListener("DOMContentLoaded", function () {
  var btn = document.getElementById("catalog-button");
  var modal = document.getElementById("catalog-modal");
  var close = document.getElementsByClassName("close")[0];
  console.log('asjkdhasd');
  // При клике на кнопку открываем модальное окно
  btn.onclick = function () {
    modal.style.display = "block";
  }

  // При клике на кнопку закрытия закрываем модальное окно
  close.onclick = function () {
    modal.style.display = "none";
  }

  // Закрываем модальное окно при клике за его пределами
  window.onclick = function (event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }

  // Корзина

  console.log('hi');
})