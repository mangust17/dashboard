$(document).ready(function () {
  // Активация ближайшей формы
  $(".fileform-activator").each(function () {
      $(this).click(function () {
          var fileForm = $(this).parent().parent().find('input[type=file]');
          fileForm.click();
      })
      $(this).parent().parent().find('input[type=file]').change(function(event) {
          var files = event.target.files;
          if (files.length > 0) {
              var fileName = files[0].name;
              $(this).parent().find('input[type=text][disabled]').val(fileName);
              console.log(fileName)

          }
      })
  })

});