$(document).ready(function () {
    const csrftoken = $('[name=csrfmiddlewaretoken]').val();
    const path = $('#tree_path_id');
    const dir = path.attr('dir');
  
    $.ajaxSetup({
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });
  
    path.fileTree({
        root: dir,
        script: window.location.pathname,
        expandSpeed: 200,
        collapseSpeed: 200,
        multiSelect: true
    }, function (file) {
        window.location.href = "/download_file/?file=" + encodeURIComponent(file);
    });
  });
  