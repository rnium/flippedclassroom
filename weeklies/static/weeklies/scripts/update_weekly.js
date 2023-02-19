let rm_pre_cls_files = []
let rm_in_cls_files = []
let rm_post_cls_files = []
let rm_pre_cls_tuto = []
let rm_in_cls_tuto = []
let rm_post_cls_tuto = []


function updateWeekly(btn_id, data) {
    payload = JSON.stringify(data)
    $.ajax({
        url: weekly_update_url,
        contentType: "application/json",
        type: "PATCH",
        beforeSend: function(xhr){
            $(`#${btn_id}`).attr("disabled", true)
            // $("#id_create_q_button").addClass("disabled-btn")
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        },
        data: payload,
        cache: false,
        dataType: "json",
        success: function(response){
            window.location.href = weekly_url
        },
        error: function(xhr,status,error){
            alert(`An Error Occured`);
            $(`#${btn_id}`).attr("disabled", false)
        }
    })
}

function deleteWeekly(btn_id) {
    $.ajax({
        url: weekly_delete_url,
        type: "DELETE",
        beforeSend: function(xhr){
            $(`#${btn_id}`).attr("disabled", true)
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        },
        cache: false,
        dataType: "json",
        success: function(){
            window.location.href = classroom_url
        },
        error: function(xhr,status,error){
            alert(`An Error Occured`);
            $(`#${btn_id}`).attr("disabled", false)
        }
    })
}


let del_btns = $(".del-btn")
$.each(del_btns, function (indexInArray, valueOfElement) {
    if ($(valueOfElement).hasClass('pre-cls-file-btn')) {
        $(valueOfElement).on('click', ()=>{
            rm_pre_cls_files.push($(this).data('obj-id'))
            let container = $(this).data('con-id')
            $(`#${container}`).hide()
        })
    } else if ($(valueOfElement).hasClass('in-cls-file-btn')) {
        $(valueOfElement).on('click', ()=>{
            rm_in_cls_files.push($(this).data('obj-id'))
            let container = $(this).data('con-id')
            $(`#${container}`).hide()
        }) 
    } else if ($(valueOfElement).hasClass('post-cls-file-btn')) {
        $(valueOfElement).on('click', ()=>{
            rm_post_cls_files.push($(this).data('obj-id'))
            let container = $(this).data('con-id')
            $(`#${container}`).hide()
        }) 
    } else if ($(valueOfElement).hasClass('pre-tuto-del-btn')) {
        $(valueOfElement).on('click', ()=>{
            rm_pre_cls_tuto.push($(this).data('obj-id'))
            let container = $(this).data('con-id')
            $(`#${container}`).hide()
        }) 
    } else if ($(valueOfElement).hasClass('in-tuto-del-btn')) {
        $(valueOfElement).on('click', ()=>{
            rm_in_cls_tuto.push($(this).data('obj-id'))
            let container = $(this).data('con-id')
            $(`#${container}`).hide()
        }) 
    } else if ($(valueOfElement).hasClass('post-tuto-del-btn')) {
        $(valueOfElement).on('click', ()=>{
            rm_post_cls_tuto.push($(this).data('obj-id'))
            let container = $(this).data('con-id')
            $(`#${container}`).hide()
        }) 
    }
    
});




$("#update_weekly_btn").on('click',()=>{
    let new_topic = $("#weekly_topic_inp").val()
    if (new_topic.length == 0) {
        $("#weekly_topic_inp").focus()
        return;
    }
    data = {'topic':new_topic}
    if (rm_pre_cls_files.length > 0) {
        data['pre_class_files'] = rm_pre_cls_files
    }
    if (rm_in_cls_files.length > 0) {
        data['in_class_files'] = rm_in_cls_files
    }
    if (rm_post_cls_files.length > 0) {
        data['post_class_files'] = rm_post_cls_files
    }
    if (rm_pre_cls_tuto.length > 0) {
        data['pre_class_tuto'] = rm_pre_cls_tuto
    }
    if (rm_in_cls_tuto.length > 0) {
        data['in_class_tuto'] = rm_in_cls_tuto
    }
    if (rm_post_cls_tuto.length > 0) {
        data['post_class_tuto'] = rm_post_cls_tuto
    }
    updateWeekly('update_weekly_btn', data)
})

$("#delete_weekly_btn").on('click', ()=>{
    confirm_val = confirm("Confirm action?")
    if (confirm_val) {
        deleteWeekly("delete_weekly_btn")
    }
})