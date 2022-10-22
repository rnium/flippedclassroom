
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

let inputfield = document.getElementById('post-files')
if (inputfield !== null) {
    inputfield.addEventListener("change", function(){
        let file_nums = inputfield.files.length
        let filename_container = document.getElementById(`postfiles-file`)
        let num_str
        if (file_nums > 1) {
            num_str = 'files'
        } else {
            num_str = 'file'
        }
        filename_container.innerText = `${file_nums} ${num_str} selected`
    })
}

function check_existing_input_files(){
    let inputfield = document.getElementById('post-files')
    if (inputfield !== null) {
        let file_nums = inputfield.files.length
        if (file_nums > 0) {
            let filename_container = document.getElementById(`postfiles-file`)
            let num_str
            if (file_nums > 1) {
                num_str = 'files'
            } else {
                num_str = 'file'
            }
            filename_container.innerText = `${file_nums} ${num_str} selected`
        } else {
            $("#postfiles-file").text('No files selected')
        }
    }
}

$(document).ready(function(){
    $("#title").focus()
    $("#calendar-icon").on('click', function(){
        $(".form-control").focus()
    })
    check_existing_input_files()
    $("#create_btn").click(function(event){ 
        event.preventDefault()
        let check_val = check_fields()
        if (check_val) {
            $("#create-assignment-form").submit()
        }
    })
})

