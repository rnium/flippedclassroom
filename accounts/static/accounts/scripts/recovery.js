function showError(msg) {
    $("#email-inp-con").hide(50, ()=>{
        $("#error-info-raw").text(msg)
        $("#error-info-con").show(50, ()=>{
            setTimeout(()=>{
                $("#error-info-con").hide(50, ()=>{
                    $("#email-inp-con").show(50)
                })
            }, 3000)
        })
    })
}

function send_mail(btn_id, data) {
    let payload = JSON.stringify(data)
    $.ajax({
        url: send_mail_url,
        contentType: "application/json",
        type: "POST",
        beforeSend: function(xhr){
            $(`#${btn_id}`).attr("disabled", true)
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        },
        data: payload,
        dataType: "json",
        cache: false,
        success: function(response){
            $("#content-con").hide(50, ()=>{
                $("#success-info-con").show(50)
            })
        },
        statusCode: {
            400: function() {
                showError("Email not  sent")
                $(`#${btn_id}`).attr("disabled", false)
            },
            404: function() {
                showError("No user found with this email")
                $(`#${btn_id}`).attr("disabled", false)
            },
            503: function() {
                showError("Cannot send email")
                $(`#${btn_id}`).attr("disabled", false)
            }
        }
    })
}

$("#submit_email_btn").on('click', ()=>{
    let email = $("#email").val()
    if (email.length == 0) {
        $("#email").focus()
    } else {
        data = {"email":email}
        send_mail("submit_email_btn", data)
    }
})