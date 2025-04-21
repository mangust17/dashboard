$(document).ready(function () {
    // Используем jQuery Lazy для отложенной загрузки содержимого div
    $('#lazy-container.lazy').lazy({
        // После успешной загрузки контента
        afterLoad: function (element) {
            // Очищаем каркас сайта
            $('#skeleton').empty();
        },
        onError: function (element) {
            // В случае ошибки можно отобразить сообщение об ошибке
            $('#skeleton').html('<p>Error loading data</p>');
        }
    });
});