// Transmit data between our backend and frontend when the 
// associated folder option changes on our issue form
$("#id_associated_file").change(function () {
    var url = $("#issueForm").attr("data-options-url");
    var fileId = $(this).val();

    // Make an AJAX call to the backend, giving it our file id
    // and returning a related queryset of lines of code
    $.ajax({
        url: url,
        data: {
            'file': fileId
      },
      success: function (data) {
        // Return our options
        $("#id_associated_loc").html(data);
      }
    });

  });