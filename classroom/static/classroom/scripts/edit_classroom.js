function validate_fields(){
    let fields = $(".inp_required")
    for (let field of fields) {
        let field_id = field.id
        let inp_value = $(`#${field_id}`).val()
        if (inp_value.length === 0) {
            $(`#${field_id}`).focus()
            return false
        }
    }
    return true
}


function get_payload() {
    let raw_data = {
        name: $("#classname").val(),
        course: $("#course").val(),
        quote: $("#quote").val()
    }
    console.log(raw_data['quote'].length);
    payload = JSON.stringify(raw_data)
    return payload
}


$("#update-btn").on("click", function(){
    let field_is_valid = validate_fields()
    if (field_is_valid === false) {
        return null
    }
    let payload = get_payload()
    $.ajax({
        type: "patch",
        url: update_clssroom_api,
        dataType: "json",
        contentType: "application/json",
        beforeSend: function(xhr){
            $(`#update-btn`).attr("disabled", true)
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        },
        data: payload,
        cache: false,
        success: function(response) {
            $("#new-classroom-name").text(response['name'])
            $("#form-container").hide(100, ()=>{
                $("#success-container").show(100)
            })
        },
        error: function() {
            alert("Something went wrong")
            $(`#update-btn`).removeAttr("disabled");
        },
    });
})