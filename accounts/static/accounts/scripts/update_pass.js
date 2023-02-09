function updatePassword(btn_id, data) {
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
            let confirm_val = confirm("Password updated! Please login again.")
            if (confirm_val) {
                window.location.href =  login_url
            }
        },
        complete: function(xhr,status,error){
            $(`#${btn_id}`).attr("disabled", false)
        },
        statusCode: {
            400: function() {
                alert("Something went wrong")
            },
            401: function() {
                alert('Current password does not match')
            }
        }
    })
}


function validate_and_get_data() {
    let inputs = $(".inp_input")
    for (let input of inputs) {
        let parentid = $(`#${input.id}`).data("parentid")
        $(`#${parentid}`).removeClass('error');
    }
    let data = {}
    for (let input of inputs) {
        let val = $(`#${input.id}`).val()
        if (val.length == 0 ) {
            let parentid = $(`#${input.id}`).data("parentid");
            $(`#${parentid}`).addClass('error');
            $(`#${input.id}`).focus();
            return false
        } else {
            data[input.id] = val;
        }
    }
    if (data['new_password'] != data['new_pass_repeat']) {
        $("#new_pass_repeat_con").addClass('error')
        $("#new_pass_repeat").focus()
        alert("Password Mismatch")
        return false;
    } else {
        return data;
    }
}


$("#update-pass-btn").on('click', ()=>{
    let validated_data = validate_and_get_data()
    if (validated_data != false) {
        updatePassword('update-pass-btn', validated_data)
    }
})
