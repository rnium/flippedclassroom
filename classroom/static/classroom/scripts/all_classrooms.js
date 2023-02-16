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


function join_class(code) {
    let join_api = `${classroom_join_api_url}?code=${code}`
    $.ajax({
        url: join_api,
        type: "GET",
        dataType: "json",
        beforeSend: function(xhr){
            $(`#join_cls_btn`).attr("disabled", true);
        },
        cache: false,
        success: function(response){
            $("#info-error-con").addClass('success');
            $("#info-txt").text("Joined Successfully");
            $("#info-error-con").show(200, ()=>{
                window.location.href = response['dashboard']
            })
        },
        error: function(xhr, error, status) {
            $(`#join_cls_btn`).attr("disabled", false);
            $("#info-error-con").removeClass('success');
            $("#info-txt").text(xhr['responseJSON']['info'])
            $("#info-error-con").show(200, ()=>{
                setTimeout(()=>{
                    $("#info-error-con").hide(200)
                },3000)
            })
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

$("#join_cls_btn").on('click', ()=>{
    let cls_code = $("#cls_code").val()
    join_class(cls_code)
})

$("#plus-i").on('click', ()=>{
    let is_closing = $("#plus-i").hasClass('closing');
    if (is_closing) {
        $("#plus-i").removeClass('closing');
        $("#plus-content").hide(200)
    } else {
        $("#plus-i").addClass('closing');
        $("#plus-content").show(200)
    }
})