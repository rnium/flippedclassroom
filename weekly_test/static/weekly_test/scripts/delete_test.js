function deletePost(btn_id, success_callback){
    $.ajax({
        type: "delete",
        url: delete_test_api_url,
        beforeSend: function(xhr){
            $(`#${btn_id}`).attr("disabled", true)
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        },
        cache: false,
        success: function(response) {
            success_callback()
        },
        error: function() {
            alert("Something went wrong")
            $(`#${btn_id}`).removeAttr("disabled");
        },
    });

}

$(document).ready(function () {
    $("#test-del-btn").on('click', ()=>{
        let confirmation = confirm("Confirm action?")
        if (confirmation) {
            deletePost('test-del-btn', ()=>{
                window.location.href = clssroom_url
            })
        }
    })
});