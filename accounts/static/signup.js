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

function performSignup() {
    console.log('proceeding')
}

$("#submit").on('click', performSignup)
