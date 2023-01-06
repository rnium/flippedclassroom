function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


// ---- DESCRIPTION EDIT/ADD -----------------
function updateWeekly(data, callback) {
    payload = JSON.stringify(data)
    $.ajax({
        url: weekly_update_url,
        contentType: "application/json",
        type: "PATCH",
        beforeSend: function(xhr){
            $("#id_create_q_button").attr("disabled", "")
            // $("#id_create_q_button").addClass("disabled-btn")
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        },
        data: payload,
        cache: false,
        dataType: "json",
        success: function(response){
            callback()
        },
        error: function(xhr,status,error){
            console.log(error);
        }
    })
}

function update_infotext_and_hide_editor(editorId, infoTextContainerId, infotextRawId, newText, adder_con_id) {
    $(`#${infotextRawId}`).text(newText)
    if (newText.length > 0) {
        $(`#${editorId}`).hide(0, function(){
            $(`#${infoTextContainerId}`).show()
        })
     } else {
         $(`#${editorId}`).hide(0, function(){
             $(`#${adder_con_id}`).show()
         })
     }
}

// edit description button
let des_edit_btns = $(".des-edit")
$.each(des_edit_btns, function (indexInArray, valueOfElement) { 
     $(`#${valueOfElement.id}`).on('click', ()=>{
         let infoTextID = $(this).parent().attr('id')
         let infoTextContainerId = $(`#${infoTextID}`).parent().attr('id')
         let editor_id = $(`#${infoTextContainerId}`).attr('data-descr-editor')
         let prev_info = $(`#${infoTextID}`).text()
         $(`#${infoTextContainerId}`).hide(0, function(){
            $(`#${editor_id}`).show()
            $(`#${editor_id} .editor-textarea`).text(prev_info)
            $(`#${editor_id} .editor-textarea`).focus()
         })
         
     })
});

// add description button
let adder_btns = $(".des-adder")
$.each(adder_btns, function (indexInArray, valueOfElement) { 
     $(`#${valueOfElement.id}`).on('click', ()=>{
         let editorId = $(this).attr('data-editorId');
         let self_container_id = $(this).parent().attr('id')
         $(`#${self_container_id}`).hide()
         $(`#${editorId}`).show()
         $(`#${editorId} .editor-textarea`).focus()
     })
});

// text editor close button
let des_editor_close_btns = $(".editor-close-btn")
$.each(des_editor_close_btns, function (indexInArray, valueOfElement) { 
     $(`#${valueOfElement.id}`).on('click', ()=>{
        let infoTextId = $(this).attr('data-infoTextId')
        let adderId = $(this).attr('data-adderId')
        let rawTextId = $(this).attr('data-rawText')
        let self_container_id = $(this).parent().parent().parent().attr('id')
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
});

// pre class instruction save
$("#pre-class-info-save-btn").on('click', ()=>{
    let pre_class_instruction = $("#pre-descr").val()
    updateWeekly(data={"pre_class_instruction":pre_class_instruction}, callback=()=>{
        update_infotext_and_hide_editor("pre_cls-description-editor", "pre-class-info-text", "pre-cls-info-text-raw", pre_class_instruction, 'pre_cls_descr_adder_btn_con')
    })
})


// ---- FILE ADD -------------------

// file uploads
let uploadFileBtns = $(".files-add-btn")
$.each(uploadFileBtns, function (indexInArray, valueOfElement) { 
    $(`#${valueOfElement.id}`).on('click', ()=>{
        let containerId = $(this).parent().attr('id')
        let uploaderId = $(this).attr('data-uploaderId')
        $(`#${containerId}`).hide(0, function(){
            $(`#${uploaderId}`).show()
        })
    })
});

// ----- VIDEO ADD -------------------

// video adder
let addVidsBtns = $(".addVideosTogglerBtn")
$.each(addVidsBtns, function (indexInArray, valueOfElement) {
    $(`#${valueOfElement.id}`).on('click', ()=>{
        let containerId = $(this).parent().attr('id')
        let adderId = $(this).attr('data-videoAdderId')
        $(`#${containerId}`).hide(0, function(){
            $(`#${adderId}`).show()
        })
    })
});

// video adder close
let vid_adder_close_btns = $(".vidAdderCloseBtn")
$.each(vid_adder_close_btns, function (indexInArray, valueOfElement) { 
    $(`#${valueOfElement.id}`).on('click', ()=>{
        let vidAdderConId = $(this).parent().parent().attr('id')
        let addVideosTogglerBtnConId = $(this).attr('data-addVideosTogglerBtnCon-Id')
        $(`#${vidAdderConId}`).hide(0, ()=>{
            $(`#${addVideosTogglerBtnConId}`).show()
        })
    })
});