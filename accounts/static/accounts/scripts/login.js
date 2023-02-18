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

function showError(msg, duration=3000) {
    $("#error-info-text").text(msg)
    $("#error-info-container").show(0, function(){
        setTimeout(function(){
            $("#error-info-text").text(" ")
            $("#error-info-container").hide()
        }, duration)
    })
}

function checkForm() {
    let input_fields = $(".inp_input")
    for (let field of input_fields) {
        field_val = $(`#${field.id}`).val()
        if (field_val.length < 1) {
            showError("Please fill the field")
            $(`#${field.id}`).focus()
            return false
        }
    }
    return true
}

function submitForm() {
    let form_is_valid = checkForm()
    if (!form_is_valid) {
        return false
    }
    let data = {
        "email": $("#email").val(),
        "password": $("#password").val()
    }
    let payload = JSON.stringify(data)
    $.ajax({
        type: "post",
        url: login_url,
        dataType: "json",
        contentType: "application/json",
        beforeSend: function(xhr){
            // $("#id_create_q_button").attr("disabled", true)
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        },
        data: payload,
        cache: false,
        statusCode: {
            200: function() {
                window.location = success_url
            },
            400: function() {
                showError("Something went wrong")
            },
            401: function() {
                showError("Invalid Credentials")
            }
        }
    });

}

$("#password").on('keyup', function (e) { 
    if (e.key == 'Enter' || e.keyCode === 13) {
        submitForm()
    }
 })

$("#submit").on('click', submitForm)


