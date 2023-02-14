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

function updateClassroom(btn_id, payload){
    $.ajax({
        type: "PATCH",
        url: update_clssroom_api,
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


function setupBanner(image_file) {
    let image_form = new FormData
    image_form.append("dp", image_file)
    $.ajax({
        type: "post",
        url: set_banner_api,
        data: image_form,
        contentType: false,
        processData: false,
        success: function(){
            $("#posting-loader").hide()
            $("#form-container").hide(100, ()=>{
                $("#success-container").show(100)
            })
        },
        error: function() {
            $("#posting-loader").hide()
            $(`#update-btn`).removeAttr("disabled");
            alert("Cannot upload banner!")
        }
    });

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


let inputfield = document.getElementsByClassName("input-img")[0]
inputfield.addEventListener("change", function(){
    let filename = inputfield.files.item(0).name
    if (filename.length > 12) {
        filename = filename.slice(0, 12) + "..."
    }
    let filename_container = document.getElementById(`selected-file`)
    filename_container.innerText = filename
})


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
            $("#posting-loader").show()
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        },
        data: payload,
        cache: false,
        success: function(response) {
            $("#new-classroom-name").text(response['name'])
            avatar_files = $("#dp")[0].files
            if (avatar_files.length > 0) {
                console.log('up avatar');
                setupBanner(avatar_files[0])
            } else {
                $("#posting-loader").hide()
                $("#form-container").hide(100, ()=>{
                    $("#success-container").show(100)
                })
            }
        },
        error: function() {
            $("#posting-loader").hide()
            alert("Something went wrong")
            $(`#update-btn`).removeAttr("disabled");
        },
    });
})


$("#change_active_btn").on('click', ()=>{
    let current_status = $("#change_active_btn").data('active');
    let data = {"active":!current_status};
    let confirmation = confirm("Confirm action?");
    if (confirmation) {
        updateClassroom("change_active_btn", data);
    }
})