// ---- DESCRIPTION EDIT/ADD -----------------

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
        let self_container_id = $(this).parent().parent().parent().attr('id')
        let infoText = $(`#${infoTextId}`)
        
        if (infoText.length == 1) {
           if (infoText.css('display') == 'none') {
               $(`#${self_container_id}`).hide(0, function(){
                   $(`#${infoTextId}`).show()
               })
           }
        } else {
            $(`#${self_container_id}`).hide(0, function(){
                $(`#${adderId}`).show()
            })
        }
     })
});


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