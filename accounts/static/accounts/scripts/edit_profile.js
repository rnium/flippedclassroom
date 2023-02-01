function showError(msg, duration=3000) {
    $("#error-info-text").text(msg)
    $("#error-info-container").show(0, function(){
        setTimeout(function(){
            $("#error-info-text").text(" ")
            $("#error-info-container").hide()
        }, duration)
    })
}


function updateProfile(btn_id, data) {
    let payload = JSON.stringify(data)
    $.ajax({
        url: update_profile_api,
        contentType: "application/json",
        type: "POST",
        beforeSend: function(xhr){
            $(`#${btn_id}`).attr("disabled", true)
            // $("#id_create_q_button").addClass("disabled-btn")
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        },
        data: payload,
        cache: false,
        success: function(response){
            alert("Profile Updated")
        },
        complete: function(xhr,status,error){
            $(`#${btn_id}`).attr("disabled", false)
        },
        statusCode: {
            400: function() {
              showError("Email Already Used");
            },
            406: function() {
                showError("An Error Occurred");
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
    let first_name = $("#first_name").val();
    let last_name = $("#last_name").val();
    let institution = $("#institution").val();
    let institutional_id = $("#inst-id").val();
    let email = $("#email").val();
    let data = {
        'user_data': {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
        },
        'account_data': {
            'institution':institution,
            'institutional_id': institutional_id
        }
    };
    updateProfile('submit-btn', data)
})