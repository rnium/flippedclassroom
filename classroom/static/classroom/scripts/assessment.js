function check_input(inp_id) {
    inp_selector = `#${inp_id}`
    let score_raw = $(inp_selector).val();
    let marks = $(inp_selector).data('marks');
    if (score_raw.length > 0) {
        let score = Number(score_raw);
        if (isNaN(score)) {
            $(inp_selector).removeClass("empty")
            $(inp_selector).addClass("error")
        } else {
            if (score > marks) {
                $(inp_selector).removeClass("empty")
                $(inp_selector).addClass("error")
            } else {
                $(inp_selector).removeClass("error")
                $(inp_selector).removeClass("empty")
            }
        }
    } else {
        $(inp_selector).removeClass("error")
        $(inp_selector).addClass("empty")
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


$(document).ready(function () {
    activate_score_box()
    $("#a-save-btn").on('click', function(){
        console.log(processData());
    })
});