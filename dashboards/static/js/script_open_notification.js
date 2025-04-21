$(document).ready(function() {
  const urlParams = new URLSearchParams(window.location.search);
  const notificationId = urlParams.get('id');

  if (notificationId) {
      const targetCollapse = $(`#collapse-${notificationId}`);
      const targetButton = $(`button[data-bs-target="#collapse-${notificationId}"]`);
      if (targetCollapse.length && targetButton.length) {
          targetCollapse.collapse('show');
          $('html, body').animate({
              scrollTop: targetCollapse.offset().top
          }, 500);
          targetButton.removeClass('collapsed');
          targetButton.attr('aria-expanded', 'true');
      }
  }
});

