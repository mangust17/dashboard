$(document).ready(function () {
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  // Ajax для удаления тендера
  const delSpans = $('.del_span')
  delSpans.click(function () {
    const tenderDelNum = $(this).attr('tender-num');
    console.log(tenderDelNum);
    $.ajax({
      url: '/tenders/',
      method: 'POST',
      headers: { 'X-CSRFToken': csrfToken },
      data: { tender_del: tenderDelNum },
      success: function (response) {
        console.log('Success')
        window.location.reload();
      },
      error: function (xhr, status, error) {
        console.error('Ошибка AJAX-запроса:', error);
      }
    });
  });

});
