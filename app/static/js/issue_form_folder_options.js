// Transmit data between our backend and frontend when the 
// repo option changes on our issue form
$("#id_repository").change(function () {
    var url = $("#issueForm").attr("data-options-url");
    var repoId = $(this).val();

    // Make an AJAX call to the backend, giving it our repo id
    // and returning a related queryset of folders
    $.ajax({
        url: url,
        data: {
            'repo': repoId
      },
      success: function (data) {
        // Return our options
        $("#id_associated_folder").html(data);
      }
    });

  });