function adjust_answercounts() {
    let counter_divs = $(".qno-count");
    let count = 1;
    for (let cd of counter_divs) {
        $(`#${cd.id}`).text(count)
        count += 1
    }
}

function activate_score_box(){
    let score_divs = $(".q-marks-input");
    for (let sd of score_divs) {
        $(`#${sd.id}`).keyup(function(){
            let value = $(this).val();
            let marks_raw = $(this).attr("data-q-marks");
            if (value.length > 0) {
                let score = Number(value);
                let marks = Number(marks_raw);
                if (isNaN(score) || score>marks || score<0) {
                    $(this).addClass("error")
                } else {
                    $(this).removeClass("error")
                }
            } else {
                $(this).removeClass("error")
            }
        })
    }
}

function checkErrorFields() {
    let fields = $("input.error")
    if(fields.length>0){
        for(let i=0;i<fields.length;i++){
            let field_id = fields[i].id
            $(`#${field_id}`).focus()
            return false
        }
    } else {
        return true
    }
}


function processData(){
    let score_divs = $(".q-marks-input");
    let data_list = []
    $.each(score_divs, function (indexInArray, valueOfElement) { 
         unit_data = {}
         let pk_raw = $(`#${valueOfElement.id}`).attr("data-ans-id")
         let pk = Number(pk_raw)
         let score_raw = $(`#${valueOfElement.id}`).val()
         let score = Number(score_raw)
         unit_data['pk'] = pk
         unit_data['score'] = score
         data_list.push(unit_data)
    });
    return data_list
}





$(document).ready(function () {
    adjust_answercounts()
    activate_score_box()
});