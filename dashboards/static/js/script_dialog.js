$(document).ready(function () {
  const form = $("#message-form");
  const input = $("#message-input");
  const messagesContainer = $("#messages-container");
  const chat = $("#chat").val();
  const csrfToken = $('[name=csrfmiddlewaretoken]').val();

  form.on("submit", function (e) {
    e.preventDefault();

    const messageText = input.val().trim();
    if (!messageText) return; 

    $.ajax({
      url: `/dialog/${chat}/`,
      type: "POST",
      headers: { 'X-CSRFToken': csrfToken },
      data: {
        message: messageText,
      },
      success: function (data) {
        if (data.status === "success") {
          const messageDate = new Date(data.message_time);
          messageDate.setHours(messageDate.getHours() + 3);

          const months = ["Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"];
          const formattedDate = `${messageDate.getDate()} ${months[messageDate.getMonth()]} ${messageDate.getFullYear()}, ${messageDate.getHours().toString().padStart(2, "0")}:${messageDate.getMinutes().toString().padStart(2, "0")}`;

          const messageHTML = `
            <div class="d-flex mb-3 justify-content-end">
                <div style="max-width: 70%;">
                    <div class="p-3" style="background-color: #2dd0ed; color: #f1f1f1; border-radius: 10px;">
                        ${data.message}
                    </div>
                    <div class="text-muted text-end" style="font-size: 0.8rem; margin-top: 5px;">
                        ${formattedDate}
                    </div>
                </div>
                <img 
                    src="${data.sender_avatar}" 
                    alt="Avatar" 
                    class="rounded-circle ms-2" 
                    style="width: 40px; height: 40px; border: 2px solid var(--primary);">
            </div>`;

          messagesContainer.append(messageHTML);
          input.val("");
          messagesContainer.scrollTop(messagesContainer[0].scrollHeight);
        }
      },
      error: function (xhr, status, error) {
        console.error("Error:", error);
      }
    });
  });
});