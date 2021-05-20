$("#id_repository").change(function () {
    var url = $("#issueForm").attr("data-options-url");
    var repoId = $(this).val();

    $.ajax({
        url: url,
        data: {
            'repo': repoId
      },
      success: function (data) {
        $("#id_associated_folder").html(data);
      }
    });
  });