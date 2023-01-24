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



$("#post-files").on('change', ()=>{
    upload_work()
})