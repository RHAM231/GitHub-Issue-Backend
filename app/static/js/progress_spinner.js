// Let's define a script to hide or show our progress spinner on
// the confirm sync page

// Get the html elements we need
const spinnerBox = document.getElementById('spinner-box')
const loadMsg = document.getElementById('load-msg')
const submitBtn = document.getElementById('sync-btn')

// Define a function to add and remove classes to the elements
// on form submit
$("#github-import-form").submit(function(e) {
    // Change visibility
    e.preventDefault();
    spinnerBox.classList.remove('not-visible');
    loadMsg.classList.remove('not-visible');
    submitBtn.classList.add('not-visible');

    // Read our form submit
    var form = $(this);
    var url = form.attr('action');

    // Use AJAX to process the submission
    $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(),
        // Define success action
        success: function()
        {
            // Redirect to the success page
            window.location = "Success/"
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            // Redirect to the failure page
            window.location = "Failure/"
        }
    })
});