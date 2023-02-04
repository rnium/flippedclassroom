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

let activate_score_box = function(){
    let inp_fields = $(".score-inp");
    $.each(inp_fields, function (indexInArray, valueOfElement) { 
        $(`#${valueOfElement.id}`).keyup(function(){
            check_input(this.id)
        })
    });
    
}


$(document).ready(function () {
    activate_score_box()
});