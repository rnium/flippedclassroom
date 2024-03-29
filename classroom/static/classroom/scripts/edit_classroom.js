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

function regenerate_join_code() {
    $.ajax({
        url: change_join_code_url,
        type: "GET",
        dataType: "json",
        beforeSend: function(xhr){
            $(`#code-regen-btn`).attr("disabled", true);
        },
        cache: false,
        success: function(response){
            $("#cls-code-txt").text(response['newcode'])
            $(`#code-regen-btn`).attr("disabled", false);
        },
        error: function(xhr, error, status) {
            alert('something went wrong')
            $(`#code-regen-btn`).attr("disabled", false);
        }
    })
}


function delete_classroom() {
    $.ajax({
        url: delete_classroom_api_url,
        type: "DELETE",
        dataType: "json",
        beforeSend: function(xhr){
            $(`#dlt-classroom-btn`).attr("disabled", true);
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        },
        cache: false,
        success: function(response){
            window.location.href = response['homepage']
            $(`#dlt-classroom-btn`).attr("disabled", false);
        },
        error: function(xhr, error, status) {
            alert('something went wrong')
            $(`#dlt-classroom-btn`).attr("disabled", false);
        }
    })
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
            $("#btn-con").hide()
            $("#form-container").hide(200, ()=>{
                $("#success-container").show(200)
            })
        },
        error: function() {
            $("#posting-loader").hide()
            $(`#update-btn`).removeAttr("disabled");
            alert("Cannot upload banner!")
        }
    });

}


function set_banner_to_default(btn_id) {
    $.ajax({
        type: "POST",
        url: set_banner_to_default_api,
        beforeSend: function(xhr){
            $(`#${btn_id}`).attr("disabled", true)
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        },
        cache: false,
        success: function(response) {
            $(`#${btn_id}`).hide()
            alert("Classroom banner set to default")
        },
        statusCode: {
            400: function() {
              alert( "Bad request" );
            },
            401: function() {
              alert( "You're not authorized to perform this action" );
            },
            404: function() {
              alert( "classroom not found" );
            },
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

let char_inputs = $(".inp_input")
$.each(char_inputs, function (indexInArray, valueOfElement) { 
    $(valueOfElement).on('keyup', ()=>{
        let newval = $(this).val()
        let charcounter_id = $(this).data('charcounter')
        let maxlength = $(`#${charcounter_id}`).data('maxlength')
        $(`#${charcounter_id}`).text(newval.length)
        let counter_container = $(`#${charcounter_id}`).parent()
        if (newval.length > maxlength) {
            $(counter_container).addClass('error');
        } else {
            $(counter_container).removeClass('error');
        }
    })
});

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
                $("#btn-con").hide()
                $("#form-container").hide(200, ()=>{
                    $("#success-container").show(200)
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

$("#code-regen-btn").on('click', regenerate_join_code)


$("#dlt-classroom-btn").on('click', ()=>{
    let confirmation = confirm("Are you sure to delete this classroom and all the data associated with it?")
    if (confirmation) {
        delete_classroom()
    }
})

$("#change_active_btn").on('click', ()=>{
    let current_status = $("#change_active_btn").data('active');
    let data = {"active":!current_status};
    let confirmation = confirm("Confirm action?");
    if (confirmation) {
        updateClassroom("change_active_btn", data);
    }
})

let restore_banner_btns = $(".restore-btn")
if (restore_banner_btns.length > 0) {
    $("#restore_to_default_btn").on('click', ()=>{
        set_banner_to_default("restore_to_default_btn")
    })
}