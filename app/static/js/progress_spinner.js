console.log('hello world')

const spinnerBox = document.getElementById('spinner-box')
const loadMsg = document.getElementById('load-msg')
const submitBtn = document.getElementById('sync-btn')

console.log(spinnerBox)
console.log(dataBox)

$("#github-import-form").submit(function() {
    spinnerBox.classList.remove('not-visible');
    loadMsg.classList.remove('not-visible');
    submitBtn.classList.add('not-visible');

    var form = $(this);
    var url = form.attr('action');

    $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(),
        succuss: function(data)
        {
            alert(data)
        }
    })
});