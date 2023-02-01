let inputfield = document.getElementById('post-files')
if (inputfield !== null) {
    inputfield.addEventListener("change", function(){
        let file_nums = inputfield.files.length
        let filename_container = document.getElementById(`postfiles-file`)
        let num_str
        if (file_nums > 1) {
            num_str = 'files'
        } else {
            num_str = 'file'
        }
        filename_container.innerText = `${file_nums} ${num_str} selected`
    })
}

function check_existing_input_files(){
    let inputfield = document.getElementById('post-files')
    if (inputfield !== null) {
        let file_nums = inputfield.files.length
        if (file_nums > 0) {
            let filename_container = document.getElementById(`postfiles-file`)
            let num_str
            if (file_nums > 1) {
                num_str = 'files'
            } else {
                num_str = 'file'
            }
            filename_container.innerText = `${file_nums} ${num_str} selected`
        } else {
            $("#postfiles-file").text('No files selected')
        }
    }
}

function updatePost(btn_id, payload){
    $.ajax({
        type: "post",
        url: post_update_url,
        dataType: "json",
        contentType: "application/json",
        beforeSend: function(xhr){
            $(`#${btn_id}`).attr("disabled", true)
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        },
        data: JSON.stringify(payload),
        cache: false,
        success: function(response) {
            alert("updated")
        },
        error: function() {
            alert("Something went wrong")
            $(`#${btn_id}`).removeAttr("disabled");
        },
    });

}

let btns = $(".del-btn")
let removed_files = []
$.each(btns, function (indexInArray, valueOfElement) { 
    $(`#${valueOfElement.id}`).on('click', ()=>{
        let btn_id = $(this).id;
        let file_id = $(this).data('fileid');
        let containerid = $(this).data('container');
        removed_files.push(file_id)
        console.log(removed_files);
        $(`#${containerid}`).hide(300)
    })
});


$(document).ready(function () {
    check_existing_input_files()
    $("#post-save-btn").on('click', ()=>{
        data = {}
        let new_descr = $("#post-descr").val()
        if (new_descr != prev_descr || removed_files.length != 0) {
            if (new_descr != prev_descr) {
                data['description'] = new_descr
            }
            if (removed_files.length != 0) {
                data['removed_files'] = removed_files
            }
            updatePost("post-save-btn", data)
        } else {
            return;
        }
        
    })
});