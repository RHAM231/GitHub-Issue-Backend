// Transmit data between our backend and frontend when the 
// associated folder option changes on our issue form
$("#id_associated_folder").change(function () {
    var url = $("#issueForm").attr("data-options-url");
    var folderId = $(this).val();

    // Make an AJAX call to the backend, giving it our folder id
    // and returning a related queryset of files
    $.ajax({
        url: url,
        data: {
            'folder': folderId
      },
      success: function (data) {
        // Return our options
        $("#id_associated_file").html(data);
      }
    });

  });