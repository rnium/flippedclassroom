

function activate_btns() {
    $("#close-verification-con-btn").on('click', ()=>{
        $("#email-unv-con").hide(200)
    })
}

let email_unv_containers = $(".email-unverified")
if (email_unv_containers.length > 0) {
    activate_btns()
    setTimeout(()=>{
        $("#email-unv-con").show(200)
    },1500)
}