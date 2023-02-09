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

let inputfield = document.getElementsByClassName("input-img")[0]
inputfield.addEventListener("change", function(){
    let filename = inputfield.files.item(0).name
    if (filename.length > 12) {
        filename = filename.slice(0, 12) + "..."
    }
    let filename_container = document.getElementById(`selected-file`)
    filename_container.innerText = filename
})

$("#password2").keyup(function(){
    let p1 = $("#password1").val()
    let p2 = $("#password2").val()
    if (p1 != p2) {
        $("#password2").addClass("inset-error")
    } else {
        $("#password2").removeClass("inset-error")
    }
})


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


function validateEmail(input_text) {
    var validRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
    if (input_text.match(validRegex)) {
      return true;
    } else {
      return false;
    }
}

function checkEmail(){
    let email = $("#email").val()
    let email_validation = validateEmail(email)
    if (!email_validation) {
        $("#email").addClass("inset-error")
        return false;
    } else {
        $("#email").removeClass("inset-error")
        return true;
    }
}

$("#email").keyup(function(){
    checkEmail()
})


function checkForm() {
    let email_validation = checkEmail()
    if (!email_validation) {
        showError("Invalid email")
        return false
    }
    let error_fields = $('.inset-error')
    if (error_fields.length > 0) {
        showError("Please fix the error")
        $(`#${error_fields[0].id}`).focus()
        return false
    }
    let input_fields = $(".inp_input")
    for (let field of input_fields) {
        field_val = $(`#${field.id}`).val()
        if (field_val.length < 1) {
            $(`#${field.id}`).focus()
            showError("Please fill the field")
            return false
        }
    }
    return true
}

function setupAvatar(image_file) {
    let image_form = new FormData
    // fix csrftoken with formdata
    image_form.append("dp", image_file)
    $.ajax({
        type: "post",
        url: avatar_set_url,
        data: image_form,
        contentType: false,
        processData: false,
        complete: function(){
            window.location = success_url
            $("#signup-info").text("Avatar set!")
        },
        error: function() {
            location.reload()
        }
    });

}

function submitForm(){
    let form_is_valid = checkForm()
    if (!form_is_valid) {
        return false
    }
    let data = {
        "first_name":$("#first_name").val(),
        "last_name":$("#last_name").val(),
        "institution":$("#institution").val(),
        "institutional_id":$("#inst-id").val(),
        "email": $("#email").val(),
        "password": $("#password1").val()
    }
    let payload = JSON.stringify(data)
    $.ajax({
        type: "post",
        url: signup_url,
        dataType: "json",
        contentType: "application/json",
        beforeSend: function(xhr){
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            $("#submit").attr('disabled', true);
            $("#signup-info").text("Creating account")
            $("#signup-info").show()
        },
        data: payload,
        cache: false,
        statusCode: {
            201: function() {
                // window.location = success_url
                $("#signup-info").text("Account created")
                avatar_files = $("#dp")[0].files
                if (avatar_files.length > 0) {
                    $("#signup-info").text("Uploading avatar..")
                    setupAvatar(avatar_files[0])
                } else {
                    window.location = success_url
                }
            },
            400: function() {
                $("#signup-info").hide(0, ()=>{
                    $("#submit").attr('disabled', false);
                    showError("Email already used")
                }) 
            },
            406: function() {
                $("#signup-info").hide(0, ()=>{
                    $("#submit").attr('disabled', false);
                    showError("Something went wrong")
                }) 
            }
        }
    });
}


$("#submit").on('click', submitForm)
$("#password2").on('keyup', function (e) { 
    if (e.key == 'Enter' || e.keyCode === 13) {
        submitForm()
    }
 })

$("#footer").html(`Developed by <a href="https://github.com/rnium">MSI Rony</a>`);