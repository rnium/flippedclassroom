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
            $(`#${field.id}`).focus()
            showError("Please fill the field")
            return false
        }
    }
    return true
}

function setupAvatar(image_file, btn_id) {
    let image_form = new FormData
    // fix csrftoken with formdata
    image_form.append("dp", image_file)
    $.ajax({
        type: "post",
        url: avatar_set_url,
        data: image_form,
        contentType: false,
        processData: false,
        success: function(){
            location.reload()
        },
        error: function(xhr, error, status) {
            $(`#${btn_id}`).attr("disabled", false)
            $("#loader-con").hide(0 ,()=>{
                showError(xhr['responseJSON']['info'])
            })
        }
    });

}


function updateProfile(btn_id, data) {
    let payload = JSON.stringify(data)
    $.ajax({
        url: update_profile_api,
        contentType: "application/json",
        type: "POST",
        beforeSend: function(xhr){
            $(`#${btn_id}`).attr("disabled", true)
            $("#loader-con").show()
            // $("#id_create_q_button").addClass("disabled-btn")
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        },
        data: payload,
        cache: false,
        success: function(response){
            avatar_files = $("#dp")[0].files
            if (avatar_files.length > 0) {
                setupAvatar(avatar_files[0], btn_id)
            } else {
                $(`#${btn_id}`).attr("disabled", false)
                $("#loader-con").hide()
                location.reload()
            }
        },
        statusCode: {
            400: function() {
              showError("Email Already Used");
              $("#loader-con").hide()
              $(`#${btn_id}`).attr("disabled", false)
            },
            406: function() {
                showError("An Error Occurred");
                $("#loader-con").hide()
                $(`#${btn_id}`).attr("disabled", false)
            }
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

$("#submit-btn").on('click', ()=>{
    let check_res = checkForm()
    if (!check_res) {
        return;
    }
    let first_name = $("#first_name").val();
    let last_name = $("#last_name").val();
    let institution = $("#institution").val();
    let institutional_id = $("#inst-id").val();
    let email = $("#email").val();
    let data = {
        'user_data': {
            'first_name': first_name,
            'last_name': last_name,
            'username': email,
            'email': email,
        },
        'account_data': {
            'institution':institution,
            'institutional_id': institutional_id
        }
    };
    updateProfile('submit-btn', data)
})