function submitClosestForm(element) {
  var form = element.closest('form');
  if (form) {
    form.submit();
  }
}

$(document).ready(function () {
  // Окрашивание статуса
  $('.pay-status').each(function(){
    var statusText = $(this).text().trim(); 
    if (statusText === "Распределен") {
      $(this).css("color", "red"); 
    }
  })


});