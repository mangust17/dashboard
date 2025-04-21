document.addEventListener("DOMContentLoaded", function () {
  const priceInput = document.getElementsByName('price')[0];
  const taxInput = document.getElementsByName('rate')[0];
  const comissionInput = document.getElementById('tax');
  const totalSpan = document.getElementById('total-rub');
  const totalDollar = document.getElementById('total-dollar');
  const comissionRubSpan = document.getElementById('comission_rub');
  const comissionDollarSpan = document.getElementById('comission_dollar');

  function updateTotal() {
    const price = parseFloat(priceInput.value) || 0;
    const tax = parseFloat(taxInput.value) || 1;
    const commisionPercent = parseFloat(comissionInput.value) || 0;

    // Рассчитываем комиссию в рублях
    const comissionRub = price * (commisionPercent / 100);
    const finalPriceRub = price + comissionRub; // Итог с учетом комиссии

    // Рассчитываем комиссию в долларах
    const finalPriceDollar = finalPriceRub / tax;
    const comissionDollar = comissionRub / tax;

    // Обновляем HTML
    totalSpan.innerHTML = finalPriceRub.toFixed(2);
    totalDollar.innerHTML = finalPriceDollar.toFixed(2);
    comissionRubSpan.innerHTML = comissionRub.toFixed(2);
    comissionDollarSpan.innerHTML = comissionDollar.toFixed(2);
  }

  // Добавляем обработчик события на все поля
  priceInput.addEventListener('input', updateTotal);
  taxInput.addEventListener('input', updateTotal);
  comissionInput.addEventListener('input', updateTotal);

  updateTotal(); // Запускаем пересчет при загрузке
});
