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

function removeUser(btn_id, user_id){
    payload = {
        "user_id" :user_id
    }
    $.ajax({
        type: "post",
        url: remove_user_from_classroom_url,
        dataType: "json",
        contentType: "application/json",
        beforeSend: function(xhr){
            $(`#${btn_id}`).attr("disabled", true)
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        },
        data: JSON.stringify(payload),
        cache: false,
        success: function(response) {
            window.location.href = "/"
        },
        statusCode: {
            401: function() {
                $(`#${btn_id}`).attr("disabled", false)
                alert( "Bad request" );
            },
            406: function() {
                $(`#${btn_id}`).attr("disabled", false)
                alert( "As you're the only teacher of this classroom, you cannot leave!" );
            },
        }
    });

}

$("#leave-btn").on('click', ()=>{
    let user_id = $("#leave-btn").data("user-id");
    let confirmation = confirm("Confirm action?");
    if (confirmation) {
        removeUser("leave-btn", user_id)
    } 
})