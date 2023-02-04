function check_input(inp_id) {
    inp_selector = `#${inp_id}`
    let score_raw = $(inp_selector).val();
    let marks = $(inp_selector).data('marks');
    if (score_raw.length > 0) {
        let score = Number(score_raw);
        if (isNaN(score)) {
            $(inp_selector).removeClass("empty")
            $(inp_selector).addClass("error")
            return false
        } else {
            if (score > marks) {
                $(inp_selector).removeClass("empty")
                $(inp_selector).addClass("error")
                return false
            } else {
                $(inp_selector).removeClass("error")
                $(inp_selector).removeClass("empty")
                return true
            }
        }
    } else {
        $(inp_selector).removeClass("error")
        $(inp_selector).addClass("empty")
        return null
    }
}

function activate_score_box(){
    let inp_fields = $(".score-inp");
    $.each(inp_fields, function (indexInArray, valueOfElement) { 
        $(`#${valueOfElement.id}`).keyup(function(){
            check_input(this.id)
        })
    });
    
}

function validate_inputs() {
    inp_fields = $(".score-inp");
    for (let index = 0; index < inp_fields.length; index++) {
        let element = inp_fields[index].id;
        check_input(element)
    }
    let error_fields = $(".error");
    if (error_fields.length > 0) {
        $(`#${error_fields[0].id}`).focus()
        return false
    } else {
        return true
    }
}


function processData() {
    let inp_fields = $(".score-inp");
    let dataset = {}
    $.each(inp_fields, function (indexInArray, valueOfElement) { 
        let elem_selector = `#${valueOfElement.id}`
        let aid = $(elem_selector).data('aid')
        let value = $(elem_selector).val()
        if (value.length > 0) {
            let score = Number(value);
            if (!isNaN(score)) {
                let is_attendance = $(elem_selector).hasClass('attendance-score');
                let is_classtest = $(elem_selector).hasClass('classtest-score');
                if (!(aid in dataset)) {
                    dataset[aid] = {}
                }
                if (is_attendance) {
                    dataset[aid]['attendance_score'] = score;
                } else if (is_classtest) {
                    dataset[aid]['classtest_score'] = score;
                }
            }
        }
    });
    return dataset
}

function post_data(data) {
    let payload = JSON.stringify(data)
    $.ajax({
        url: update_assessment_url,
        contentType: "application/json",
        type: "POST",
        beforeSend: function(xhr){
            $("#a-save-btn").attr("disabled", true)
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        },
        data: payload,
        cache: false,
        success: function(response){
            alert('Data saved')
        },
        error: function(xhr,status,error){
            alert('something went wrong')
        },
        complete: function(){
            $("#a-save-btn").attr("disabled", false)
        }
    })
}


$(document).ready(function () {
    activate_score_box()
    $("#a-save-btn").on('click', function(){
        let validated = validate_inputs()
        if (!validated) {
            return;
        } else {
            let data = processData()
            post_data(data)
        }
        
    })
});