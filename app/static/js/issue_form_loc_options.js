$("#id_associated_file").change(function () {
    var url = $("#issueForm").attr("data-options-url");
    var fileId = $(this).val();

    $.ajax({
        url: url,
        data: {
            'file': fileId
      },
      success: function (data) {
        $("#id_associated_loc").html(data);
      }
    });
  });