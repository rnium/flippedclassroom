function update_test_score() {
    let value = parseInt($("#work_score_inp").val());
    let score = Number(value);
    if (Number.isInteger(score) && score>0) {
        if (score > marks) {
            $("#work_score_inp").focus()
            return false
        }
    } else {
        $("#work_score_inp").focus()
            return false
    }
    
    let data = {
        score: score,
    }
    
    $.ajax({
        url: update_work_score_api,
        contentType: "application/json",
        type: "POST",
        beforeSend: function(xhr){
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
            $("#update_score_btn").attr('disabled', true)
        },
        data: JSON.stringify(data),
        cache: false,
        dataType: "json",
        success: function(response){
            let elem = `<div class="score-con">
                            <i class='bx bx-trophy'></i>
                            <div class="points"><span class="point">${response['score']}</span>Points</div>
                        </div>`
            $("#id-work-score-con").hide(0, ()=>{
                $("#id-work-score-con").empty()
                $("#id-work-score-con").html(elem)
                $("#id-work-score-con").show(0)
            })
        },
        complete: function(){
            $("#update_score_btn").attr('disabled', false)
        }
    })
}

$(document).ready(function () {
    $("#update_score_btn").on('click', update_test_score)
});