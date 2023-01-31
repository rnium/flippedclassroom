function updateClassroom(btn_id, payload){
    $.ajax({
        type: "PATCH",
        url: classroom_update_url,
        dataType: "json",
        contentType: "application/json",
        beforeSend: function(xhr){
            $(`#${btn_id}`).attr("disabled", true)
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        },
        data: JSON.stringify(payload),
        cache: false,
        success: function(response) {
            location.reload()
        },
        error: function() {
            alert("Something went wrong")
            $(`#${btn_id}`).removeAttr("disabled");
        },
    });

}

$("#change_active_btn").on('click', ()=>{
    let current_status = $("#change_active_btn").data('active');
    let data = {"active":!current_status}
    updateClassroom("change_active_btn", data)
    
})