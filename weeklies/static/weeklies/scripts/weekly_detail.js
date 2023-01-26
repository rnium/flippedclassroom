let tabBtns = $(".tab-buttons button")

function clearActives() {
    let btns = $(".tab-buttons button")
    let tabs = $(".tab-body")
    $.each(btns, function (indexInArray, valueOfElement) { 
        $(`#${valueOfElement.id}`).removeClass('active')
    });
    $.each(tabs, function (indexInArray, valueOfElement) { 
        $(`#${valueOfElement.id}`).removeClass('active')
    });
}


$.each(tabBtns, function (indexInArray, valueOfElement) { 
    $(`#${valueOfElement.id}`).on('click', function(){
        clearActives()
        $(this).addClass('active');
        let tab_id = $(this).data('tab_id')
        $(`#${tab_id}`).addClass('active');
    })
});


function create_post() {
    let postcontent = $("#post_text_inp").val()
    if (postcontent.length < 1) {
        $("#post_text_inp").focus()
        return null
    }
    let payload = {"post_text":postcontent}
    $.ajax({
        type: "post",
        url: weekly_create_post_url,
        dataType: "json",
        contentType: "application/json",
        beforeSend: function(xhr){
            $("#create_post_btn").attr("disabled", true)
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        },
        data: JSON.stringify(payload),
        cache: false,
        success: function(response) {
            // appendComment(response)
            $("#post_text_inp").val("")
        },
        error: function() {
            console.log('error fired')
        },
        complete: function() {
            $("#create_post_btn").removeAttr("disabled");
        }
    });
}

$("#create_post_btn").on('click', create_post)

