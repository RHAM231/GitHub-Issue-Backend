$("#id_associated_folder").change(function () {
    var url = $("#issueForm").attr("data-options-url");
    var folderId = $(this).val();
    $.ajax({
        url: url,
        data: {
            'folder': folderId
      },
      success: function (data) {
        $("#id_associated_file").html(data);
      }
    });
  });