function upload_work() {
    let inputfield = document.getElementById('post-files')
    let file_nums = inputfield.files.length

    let files = $("#post-files")[0].files
    let post_form = new FormData
    if (files.length > 0) {
        for (let file of files) {
            post_form.append("files", file)
        }
    } 
    $.ajax({
        type: "post",
        url: upload_work_url,
        data: post_form,
        contentType: false,
        processData: false,
        beforeSend: function(){
            $("#post-files").attr('disabled', true)
            $("#postfiles-file-status").text(`${file_nums} files uploading`);
            $("#postfiles-file-status").show();
        },
        success: function(){
            location.reload()
        },
        error: function(){
            $("#postfiles-file-status").hide(100)
            $("#post-files").removeAttr('disabled');
        }
    });
}

function change_work_status() {
    $.ajax({
        url: change_work_submission_status_api,
        contentType: "application/json",
        type: "POST",
        beforeSend: function(xhr){
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            $("#alt_sub_status_btn").attr('disabled', true);
        },
        cache: false,
        dataType: "json",
        success: function(response){
            if (response['is_submitted']) {
                $("#alt_sub_status_btn").text("Unsubmit")
                $("#alt_sub_status_btn").removeClass("submit")
                $("#alt_sub_status_btn").addClass("unsubmit")
            } else {
                $("#alt_sub_status_btn").text("Submit")
                $("#alt_sub_status_btn").removeClass("unsubmit")
                $("#alt_sub_status_btn").addClass("submit")
            }
        },
        complete: function(){
            $("#alt_sub_status_btn").attr('disabled', false);
        }
    })
}



$(document).ready(function () {
    $("#post-files").on('change', ()=>{
        upload_work()
    })
    $("#alt_sub_status_btn").on('click', change_work_status)    
});

