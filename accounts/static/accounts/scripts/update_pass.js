function updateProfile(btn_id, data) {
    let payload = JSON.stringify(data)
    $.ajax({
        url: update_password_api,
        contentType: "application/json",
        type: "POST",
        beforeSend: function(xhr){
            $(`#${btn_id}`).attr("disabled", true)
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        },
        data: payload,
        cache: false,
        success: function(response){
            let confirm_val = confirm("Password updated!")
            if (confirm_val) {
                window.location.href =  profile_url
            }
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


$("#update-pass-btn").on('click', ()=>{
    
})
