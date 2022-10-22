
function validate_datetime() {
    let deadline_date_raw = $("#deadline-datetime").val()
    let deadline = new Date(deadline_date_raw).getTime()
    let timenow = new Date().getTime()
    if (deadline < timenow) {
        $("#error-msg").show(100)
        return false
    } else {
        $("#error-msg").hide(100)
        $("#deadline-datetime").removeClass("error")
        return true
    }
}

$("#deadline-datetime").on('change', validate_datetime)


function check_fields() {
    let title = $("#title").val()
    let datetime = $("#deadline-datetime").val()
    if (title.length == 0) {
        $("#title").focus()
        return false
    }
    if (datetime.length == 0) {
        $(".form-control").focus()
        return false
    }
    let date_valid = validate_datetime()
    if (date_valid) {
        return true
    } else {
        $(".form-control").focus()
        return false
    } 
}

$(document).ready(function(){
    $("#title").focus()
    $("#calendar-icon").on('click', function(){
        $(".form-control").focus()
    })
    $("#create_btn").click(function(event){ 
        event.preventDefault()
        let check_val = check_fields()
        if (check_val) {
            $("#create-assignment-form").submit()
        }
    })
})

