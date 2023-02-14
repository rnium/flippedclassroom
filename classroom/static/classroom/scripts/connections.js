let btns = $(".remove-btn")

function removeUser(btn_id, user_id, container_id){
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
            $(`#${container_id}`).hide(100, ()=>{
                $(`#${container_id}`).remove();
                let prev_count = $("#student-count").text();
                let new_count = Number(prev_count) - 1;
                $("#student-count").text(new_count)
            })
        },
        error: function() {
            alert("Something went wrong")
            $(`#${btn_id}`).removeAttr("disabled");
        },
    });

}

function addTeacher() {
    let new_email = $("#add-t-email").val()
    if (new_email.length > 0) {
        let payload = {
            "email" :new_email
        }
        $.ajax({
            type: "post",
            url: add_teacher_url,
            contentType: "application/json",
            beforeSend: function(xhr){
                $("#add-teacher-btn").attr("disabled", true)
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            },
            data: JSON.stringify(payload),
            cache: false,
            complete: function() {
                $("#add-teacher-btn").removeAttr("disabled");
            },
            statusCode: {
                404: function() {
                  alert( "User not found" );
                },
                208: function() {
                    alert("User already a teacher of this classroom")
                },
                403: function() {
                    alert("You have no permission to perform this action")
                },
                406: function() {
                    alert("Cannot add student as teacher")
                },
                200: function() {
                    let confirmation = confirm("Teacher added. Reload page?")
                    if (confirmation) {
                        location.reload()
                    }
                },
              }
        });
    } else {
        $("#add-t-email").focus()
    }
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

$("#add-teacher-btn").on('click', function(){
    addTeacher()
})