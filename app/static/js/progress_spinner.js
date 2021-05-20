const spinnerBox = document.getElementById('spinner-box')
const loadMsg = document.getElementById('load-msg')
const submitBtn = document.getElementById('sync-btn')

$("#github-import-form").submit(function(e) {
    e.preventDefault();
    spinnerBox.classList.remove('not-visible');
    loadMsg.classList.remove('not-visible');
    submitBtn.classList.add('not-visible');

    var form = $(this);
    var url = form.attr('action');

    $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(),
        success: function()
        {
            window.location = "Success/"
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            window.location = "Failure/"
        }
    })
});