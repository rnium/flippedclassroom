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

// weekly viewfile modal
let file_a_tags = $(".week-content-file")
$.each(file_a_tags, function (indexInArray, valueOfElement) { 
     $(valueOfElement).on('click', (event)=>{
        event.preventDefault()
        let fileurl = $(this).attr("href")
        $("#filemodal-href").attr('href', fileurl);
        $("#filemodal-embed").attr('src', fileurl);
        $("#modal").show();
     })
});

$("#closemodal").on('click', ()=>{
    $("#modal").hide();
})

function append_post(response) {
    let post_time = new Date(response['post_time'])
    let locale_time = post_time.toLocaleString()
    let post_elem_id = `post-${response['id']}`
    let user_designation_div
    if (response['is_teacher']) {
        user_designation_div = `<div class="teacher-badge"></div>`
    } else {
        user_designation_div = `<div class="registration">${response['inst_id']}</div>`
    }
    let post_elem = `<div class="post" id="${post_elem_id}" style="display:none;">
                        <div class="post-inner">
                        <div class="top-panel">
                            <div class="post-time"><span class="sub-title">Posted</span><span class="time">${locale_time}</span></div>
                        </div>
                        <div class="bottom-panel">
                            <div class="user">
                            <div class="username">${response['author_name']}</div>
                            ${user_designation_div}
                            <div class="avatar"><img src="${response['avatar_url']}" alt=""></div>
                            </div>
                            <div class="post-body">${response['postcontent']}</div>
                        </div>
                        <a class="edit" href="${response['edit_url']}"><i class='bx bx-pencil'></i></a>
                        </div>
                    </div>`
    $("#forum_post_container").append(post_elem)
    $(`#${post_elem_id}`).show(200)
    $("#no-forum-posts").hide(100)
}


function create_post() {
    console.log('hi');
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
            append_post(response)
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

