$(document).ready(function () {
  // Обработчик события click для кнопки "Добавить в корзину"
  $('.add-to-cart-button').on('click', function (event) {
    // Предотвращаем стандартное действие кнопки
    event.preventDefault();

    // Сохраняем ссылку на кнопку
    var addToCartButton = $(this);
    var csrfToken = $('[name=csrfmiddlewaretoken]').val();
    
    // Получаем идентификатор продукта из атрибута data-product-id кнопки
    var productId = addToCartButton.data('product-id');
    console.log('Идентификатор продукта:', productId);
    
    // Получаем количество товара из соответствующего поля ввода
    var quantityInput = addToCartButton.closest('tr').find('.form-control');
    var quantity = quantityInput.val();
    console.log('Количество товара:', quantity);
    



    // Формируем данные для отправки на сервер
    var data = {
      'product_id': productId,
      'quantity': quantity
    };
    console.log('Данные для отправки:', data);
    
    // Отправляем AJAX-запрос на сервер для добавления товара в корзину
    $.ajax({
      url: '/add-to-cart/',
      method: 'POST',
      headers: { 'X-CSRFToken': csrfToken },
      data: data,
      success: function (response) {
        // Проверяем успешность добавления товара в корзину
        if (response.success) {
          const cart_span = document.querySelector('#cart_cnt_span');
          console.log(cart_span.textContent)
          // Выводим сообщение об успешном добавлении товара
          quantityInput.val('');
          cart_span.textContent = response.new_quantity;

        } else {
          // Выводим сообщение об ошибке
          alert('Ошибка при добавлении товара в корзину');
        }
      },
      error: function (error) {
        // Обработка ошибок при выполнении AJAX-запроса
        console.error('Ошибка при выполнении AJAX-запроса:', error);
      }
      
    });
  });


  




  // --------------
});
