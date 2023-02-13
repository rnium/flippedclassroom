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


function activate_edit_des_btn() {
    $(`#remarks-info-edit`).on('click', ()=>{
        let infoTextID = "remarks-text-raw"
        let infoTextContainerId = "remarks-text-con"
        let editor_id = "remarks-adder-editor"
        let prev_info = $(`#${infoTextID}`).text()
        $(`#${infoTextContainerId}`).hide(0, function(){
           $(`#${editor_id}`).show()
           $(`#${editor_id} .editor-textarea`).text(prev_info)
           $(`#${editor_id} .editor-textarea`).focus()
        })
    })
}



function activate_remarks_adder() {
    $(`#remarks_adder`).on('click', ()=>{
        let editorId = "remarks-adder-editor";
        let self_container_id = "remarks_adder_btn_con"
        $(`#${self_container_id}`).hide()
        $(`#${editorId}`).show()
        $(`#${editorId} .editor-textarea`).focus()
    })
}

function activate_close_editor() {
    $(`#close-remarks-editor`).on('click', ()=>{
        let infoTextId = "remarks-text-con"
        let adderId = "remarks_adder_btn_con"
        let rawTextId = "remarks-text-raw"
        let self_container_id = "remarks-adder-editor"
        let infoText = $(`#${rawTextId}`).text()
        if (infoText.length > 0) {
            $(`#${self_container_id}`).hide(0, function(){
                $(`#${infoTextId}`).show()
            })
        } else {
            $(`#${self_container_id}`).hide(0, function(){
                $(`#${adderId}`).show()
            })
        }
     })
}

$(document).ready(function () {
    $("#update_score_btn").on('click', update_test_score)
    activate_edit_des_btn()
    activate_remarks_adder()
    activate_close_editor()
});