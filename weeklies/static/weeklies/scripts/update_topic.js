function updateWeekly(btn_id, data, callback) {
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

$("#update_weekly_btn").on('click',()=>{
    let new_topic = $("#weekly_topic_inp").val()
    if (new_topic.length == 0 || new_topic==pre_topic) {
        $("#weekly_topic_inp").focus()
        return;
    }
    data = {'topic':new_topic}
    updateWeekly('update_weekly_btn', data)
})