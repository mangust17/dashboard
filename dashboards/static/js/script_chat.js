document.addEventListener("DOMContentLoaded", function () {
  // все что связано с поисковой строкой
  const searchInput = $('#search-input');
  initializeSelect2(searchInput);
  styleSelect2();

  searchInput.on('select2:select', function (e) {
      const username = e.params.data.id;
      window.location.href = `/dialog/${username}`;
  });


  function initializeSelect2(searchInput) {
    searchInput.select2({
        placeholder: 'Поиск по пользователям...',
        ajax: {
        url: '/chat/',
        dataType: 'json',
        delay: 250,
        data: function (params) {
            return { search: params.term };
        },
        processResults: function (data) {
            return {
            results: data.users.map(user => ({
                id: user.id,
                text: user.text,
                img_url: user.img_url,
                position: user.position
            }))
            };
        },
        cache: true
        },
        templateResult: formatUser,
        templateSelection: formatUserSelection
    });
  }

  function styleSelect2() {
  $('#search-input').next('.select2-container').find('.select2-selection').css({
      'background-color': '#2dd0ed',
      'color': '#f1f1f1',
      'border-radius': '20px',
      'border': '2px solid var(--primary)',
  });
  }

  function formatUser(user) {
  if (!user.id) return user.text;

  return $(`
      <div class="d-flex align-items-center">
      <img src="${user.img_url}" alt="Avatar" class="rounded-circle me-2" style="width: 30px; height: 30px;">
      <div>
          <div>${user.text}</div>
          <small class="text-muted">${user.position}</small>
      </div>
      </div>
  `);
  }

  function formatUserSelection(user) {
    return user.text || user.id;
  }

  // все что связано с созданием группы
  const chatNameInput = $('#chat-name');
  const saveButton = $('#saveSelection');
  const userCheckboxes = $("input[name='selected_users']"); 
  

  function toggleButtonState() {
    const selectedUsersCount = $("input[name='selected_users']:checked").length;
    saveButton.prop('disabled', chatNameInput.val().trim() === '' || selectedUsersCount < 2);
  }
  
  chatNameInput.on('input', toggleButtonState);
  
  userCheckboxes.on('change', toggleButtonState);
  toggleButtonState();
  
  saveButton.click(function () {
    const selectedUsers = $("input[name='selected_users']:checked")
      .map(function () {
        return $(this).val();
      })
      .get();
  
    const chatName = chatNameInput.val().trim();
    const csrfToken = $('[name=csrfmiddlewaretoken]').val();
    const chatAvatar = $('#chat-avatar')[0].files[0];
     const Avatar = $('#chat-avatar');
  
    if (!chatName) {
      alert("Введите название группы.");
      return;
    }
  
    const formData = new FormData();
    formData.append('selected_users', JSON.stringify(selectedUsers));
    formData.append('chat_name', chatName);
    if (chatAvatar) {
      formData.append('chat_avatar', chatAvatar);
    }
    formData.append('csrfmiddlewaretoken', csrfToken);
  
    $.ajax({
      url: window.location.href,
      type: "POST",
      data: formData,
      processData: false,
      contentType: false, 
      success: function (response) {
        $("#userSelectModal").modal("hide"); 

        const avatarUrl = response.chatAvatarUrl || '/media/default_avatar.png';
        const newChatElement = `
          <li class="list-group-item p-3 d-flex align-items-center chat-item" style="background-color: transparent; border: none; color: var(--table-font); border-bottom: 2px solid var(--primary); transition: transform 0.2s, box-shadow 0.2s;">
            <a href="/dialog/${response.chatId}/" class="d-flex align-items-center text-decoration-none w-100">
              <img 
                  src="${avatarUrl}" 
                  alt="Avatar" 
                  class="rounded-circle me-3" 
                  style="width: 50px; height: 50px; border: 2px solid var(--primary);">
              <div class="flex-grow-1">
                <div class="d-flex justify-content-between">
                  <span class="fw-bold" style="color: var(--light);">
                    ${chatName || 'Без названия'}
                  </span>
                  <small style="color: var(--light);">Последнее сообщение</small>
                </div>
              </div>
            </a>
          </li>`;
  
        $('#chat-list').append(newChatElement);
      },

      error: function (xhr) {
        const response = xhr.responseJSON || {};
        alert(response.error || "Произошла ошибка при создании группы.");
        console.error("Error Response: ", xhr);
      },
    });
  });
  















  // Обработчик для предпросмотра изображения
  document.getElementById('chat-avatar').addEventListener('change', function (event) {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        document.getElementById('avatar-preview').src = e.target.result; 
      };
      reader.readAsDataURL(file);
    }
  });
});

