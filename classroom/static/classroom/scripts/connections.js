let btns = $(".remove-btn")

function removeUser(btn_id, user_id, container_id){
    payload = {
        "user_id" :user_id
    }
    $.ajax({
        type: "post",
        url: remove_student_url,
        dataType: "json",
        contentType: "application/json",
        beforeSend: function(xhr){
            $(`#${btn_id}`).attr("disabled", true)
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        },
        data: JSON.stringify(payload),
        cache: false,
        success: function(response) {
            $(`#${container_id}`).hide(100, ()=>{
                $(`#${container_id}`).remove()
            })
        },
        error: function() {
            alert("Something went wrong")
            $(`#${btn_id}`).removeAttr("disabled");
        },
    });

}

$.each(btns, function (indexInArray, valueOfElement) { 
    $(`#${valueOfElement.id}`).on('click', ()=>{
        let btn_id = $(this).id
        let user_id = $(this).attr("data-std-id")
        let container = $(this).attr("data-con")

        let confirm_val = confirm("Confirm remove student?")
        if (confirm_val) {
            removeUser(btn_id, user_id, container)
        }
    })
});