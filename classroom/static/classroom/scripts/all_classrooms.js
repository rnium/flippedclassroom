function send_mail() {
    $.ajax({
        url: send_mail_api_url,
        type: "GET",
        beforeSend: function(xhr){
            $(`#send-verification-btn`).text("Sending");
            $(`#send-verification-btn`).attr("disabled", true);
        },
        cache: false,
        success: function(response){
            $("#verification-btn-con").hide(200, ()=>{
                $("#verification-info-con").hide(200, ()=>{
                    $("#verification-info-con").empty();
                    $("#verification-info-con").html(
                        `<i class='bx bx-mail-send'></i>
                        <div class="info">Verification link sent to your email. Please check your inbox/spam folder</div>`
                    );
                    $("#verification-info-con").show(200, ()=>{
                        setTimeout(()=>{
                            $("#email-unv-con").hide(200)
                        },3000)
                    });
                })
            })
        },
        error: function() {
            alert("Something went wrong!");
            $(`#send-verification-btn`).text("Send verification");
            $(`#send-verification-btn`).attr("disabled", false);
        }
    })
}



function activate_btns() {
    $("#close-verification-con-btn").on('click', ()=>{
        $("#email-unv-con").hide(200)
    })
    $("#send-verification-btn").on('click', ()=>{
        send_mail()
    })
}

let email_unv_containers = $(".email-unverified")
if (email_unv_containers.length > 0) {
    activate_btns()
    setTimeout(()=>{
        $("#email-unv-con").show(200)
    },1000)
}