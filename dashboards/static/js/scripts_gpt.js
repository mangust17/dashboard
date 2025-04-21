$(document).ready(function () {
  const csrfToken = $('[name=csrfmiddlewaretoken]').val();
  const message = $('#messageWindow');
  const button = $('#sendButton');
  const mainChat = $('#main-chat');

  message.on('keypress', function (event) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      button.click();
    }
  });

  button.click(function () {
    var messageContent = message.val().trim();
    if (messageContent) {
      var messageElement = $('<div class="chat-bubble chat-bubble-left"></div>').text(messageContent);
      messageElement.fadeOut(0);
      mainChat.append(messageElement);
      messageElement.fadeIn(500); // Плавное появление сообщения
      message.val('');
      mainChat.scrollTop(mainChat[0].scrollHeight);

      $.ajax({
        url: "/tools/gpt/",
        method: 'POST',
        headers: { 'X-CSRFToken': csrfToken },
        data: { message: messageContent },
        success: function (response) {
          setTimeout(function () {
            var answerElement = $(`<div class="chat-bubble chat-bubble-right">${response.answer}</div>`);
            answerElement.fadeOut(0);
            mainChat.append(answerElement);
            answerElement.fadeIn(500); // Плавное появление сообщения
            mainChat.scrollTop(mainChat[0].scrollHeight);
          }, 1000); // Задержка 1000 мс (1 секунда)
        }
      });
    }
  });




});
