let passtogglers = $(".password-toggle")
for (let toggler of passtogglers) {
    $(`#${toggler.id}`).on('click', function(){
        let inp_id = $(this).data('inp')
        if ($(`#${inp_id}`).attr('type') == "password") {
            $(`#${inp_id}`).attr('type', 'text')
            $(this).removeClass('bx-hide')
            $(this).addClass('bx-show')
            $(`#${inp_id}`).focus()
        } else {
            $(`#${inp_id}`).attr('type', 'password')
            $(this).removeClass('bx-show')
            $(this).addClass('bx-hide')
            $(`#${inp_id}`).focus()
        }
    })
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

$("#submit").on('click', function(){
    let data = {
        "email": $("#email").val(),
        "password": $("#password").val()
    }
    let payload = JSON.stringify(data)
    $.ajax({
        type: "post",
        url: "/account/api/login",
        data: "data",
        dataType: "json",
        contentType: "application/json",
        beforeSend: function(xhr){
            // $("#id_create_q_button").attr("disabled", true)
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        },
        data: payload,
        cache: false,
        success: function (response) {
            console.log('success fired')
        },
        error: function(xhr, status, error) {
            console.log('error fired')
        },
        statusCode: {
            302: function() {
                console.log('st 302 returned')
            },
            400: function() {
                console.log('st 400 returned')
            }
        }
    });

})

