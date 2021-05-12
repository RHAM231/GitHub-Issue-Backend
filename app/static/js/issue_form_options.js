console.log("hello world from options.js");


$("#id_associated_folder").change(function () {
    var url = $("#issueForm").attr("data-files-url");
    console.log(url);
    var folderId = $(this).val();
    console.log(folderId);

    $.ajax({
        url: url,
        data: {
            'folder': folderId
      },
      success: function (data) {
          console.log("log from within success")
        $("#id_associated_file").html(data);
      }
    });

  });