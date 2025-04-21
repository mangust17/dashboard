$(document).ready(function () {
  var cropperImage;
  var cropper;
  const csrfToken = $('[name=csrfmiddlewaretoken]').val();

  $("#load-file-field").change(function() {
    var fileInput = $(this).get(0).files[0];

    // Проверяем, что выбран файл
    if (fileInput) {
      var reader = new FileReader();
      
      // Событие, которое срабатывает при загрузке файла
      reader.onload = function(e) {
        // Получаем обычный DOM элемент из jQuery объекта
        var imgElement = $("#image-to-crop").get(0);
        
        // Устанавливаем источник изображения для элемента <img>
        imgElement.src = e.target.result;
        
        // Инициализируем Cropper после добавления изображения в DOM
        cropper = new Cropper(imgElement, {
          aspectRatio: 14 / 16, // Соотношение сторон выбранной области
          crop: function(event) {
              console.log(event.detail.x);
              console.log(event.detail.y);
              console.log(event.detail.width);
              console.log(event.detail.height);
              console.log(event.detail.rotate);
              console.log(event.detail.scaleX);
              console.log(event.detail.scaleY);
          }
        });
      };
      
      // Читаем файл как данные URL (Data URL)
      reader.readAsDataURL(fileInput);
    }
  });
  
  // Обработка нажатия кнопки для сохранения обрезанного изображения
  $("#save-cropped-image-button").click(function() {
    var user_img_name = $(this).attr("img-name")
    // Проверяем, что Cropper был инициализирован и изображение было обрезано
    if (cropper) {
      // Получаем обрезанное изображение в формате Blob
      cropper.getCroppedCanvas({type: 'png'}).toBlob(function(blob) {
        // Сохраняем обрезанное изображение в переменную cropperImage
        cropperImage = blob;
        
        var formData = new FormData();
        formData.append('croppedImage', blob, user_img_name);     
        $.ajax({
          url: '/profile/change_photo',
          method: 'POST',
          headers: { 'X-CSRFToken': csrfToken },
          data: formData,
          processData: false, // Не обрабатывать данные
          contentType: false, // Не устанавливать Content-Type
          success: function (response) {
            console.log('Success')
            window.location.reload();
          },
          error: function (xhr, status, error) {
            console.error('Ошибка AJAX-запроса:', error);
          }});  
      });
    } else {
      console.log("Cropper не был инициализирован или изображение не было обрезано.");
    }
  });
});
