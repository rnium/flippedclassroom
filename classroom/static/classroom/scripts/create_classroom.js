function validate_fields(){
    let fields = $(".inp_input")
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
        course: $("#course").val()
    }
    payload = JSON.stringify(raw_data)
    return payload
}

function processSuccess(response) {
    let success_container = `<div class="success">
                                <i class='bx bx-message-square-check icon'></i>
                                <div class="classroom-name"><a href="">${response['name']}</a></div>
                                <div class="share-link">
                                <button id="share-link">copy join link <i class='bx bx-copy'></i><div id="copy-info" class="copy-info" style="display: none;">copied</div></button>
                                </div>
                            </div>`
    $("#id-create-classroom").hide(300, function(){
        $("#id-create-classroom").html(success_container);
        $("#id-create-classroom").show(300, function(){
            $('#share-link').on('click', function(){
                navigator.clipboard.writeText(response['join_link'])
                $('#copy-info').show(200, function(){
                    setTimeout(function(){
                        $('#copy-info').hide(200)
                    }, 1200)
                })
                
            })
        })
    })
}

$("#id-create_btn").on("click", function(){
    let field_is_valid = validate_fields()
    if (field_is_valid === false) {
        return null
    }
    let payload = get_payload()
    $.ajax({
        type: "post",
        url: create_classroom_url,
        dataType: "json",
        contentType: "application/json",
        beforeSend: function(xhr){
            $(`#id-create_btn`).attr("disabled", true)
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        },
        data: payload,
        cache: false,
        success: function(response) {
            console.log(response);
            processSuccess(response)
        },
        error: function() {
            console.log('error fired')
            $(`#id-create_btn`).removeAttr("disabled");
        },
    });
})