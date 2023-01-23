$("#tasktype-group").on("click", ()=>{
    if ($("#tasktype-group").is(':checked')) {
      $("#num-group-member-con").show(100, ()=>{
        $("#num-group-member").focus()
      })
    }
  })

$("#tasktype-indiv").on("click", ()=>{
if ($("#tasktype-indiv").is(':checked')) {
    $("#num-group-member-con").hide(100)
}
})

$("#num-group-member").on('keyup', ()=>{
    let value = $("#num-group-member").val();
    if (value.length > 0) {
        let n = Number(value);
        if (Number.isInteger(n) && n>0) {
            if (value > num_students) {
                $("#num-group-member-error").text('*Not enough students')
                if ($("#num-group-member-error").css('display') == "none") {
                    $("#num-group-member-error").show(100)
                }
            } else {
                if ($("#num-group-member-error").css('display') == "block") {
                    $("#num-group-member-error").hide(100)
                }
            }
            
        } else {
            $("#num-group-member-error").text('*Invalid value')
            if ($("#num-group-member-error").css('display') == "none") {
                $("#num-group-member-error").show(100)
            }
        }
    } else {
        if ($("#num-group-member-error").css('display') == "block") {
            $("#num-group-member-error").hide(100)
        }
    }
})

$(document).ready(function () {
    if ($("#tasktype-group").is(':checked')) {
        $("#num-group-member-con").show(100)
      }
});


function validate_datetime() {
    let deadline_date_raw = $("#deadline-datetime").val()
    let deadline = new Date(deadline_date_raw).getTime()
    let timenow = new Date().getTime()
    if (deadline < timenow) {
        $("#deadline-datetime-error-msg").show(100)
        return false
    } else {
        $("#deadline-datetime-error-msg").hide(100)
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
        } else {
            console.log('improper form');
        }
    })
})

