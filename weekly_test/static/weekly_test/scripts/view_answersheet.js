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





$(document).ready(function () {
    adjust_answercounts()
    activate_score_box()
});