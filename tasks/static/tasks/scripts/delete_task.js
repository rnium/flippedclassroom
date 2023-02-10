function deleteTask(btn_id) {
    $.ajax({
        url: task_delete_url,
        type: "DELETE",
        beforeSend: function(xhr){
            $(`#${btn_id}`).attr("disabled", true)
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        },
        cache: false,
        success: function(){
            window.location.href = weekly_url
        },
        error: function(xhr,status,error){
            alert(`An Error Occured`);
            $(`#${btn_id}`).attr("disabled", false)
        }
    })
}

$("#delete-btn").on("click", ()=>{
    let confirmation = confirm("Confirm action?")
    if (confirmation) {
        deleteTask("delete-btn")
    }
})