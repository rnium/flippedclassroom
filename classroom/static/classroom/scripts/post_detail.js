function activate_show_reply(comment_id=null) {
    let reply_btns
    if (comment_id == null) {
        reply_btns = $(".show-reply-box")
    } else {
        reply_btns = $(`#${comment_id} .show-reply-box`)
    }
    for (let btn of reply_btns) {
        $(`#${btn.id}`).on('click', function(){
            let box_con_id = $(this).data('box_con_id')
            let css_display = $(`#${box_con_id}`).css('display')
            let input_id = input = $(`#${box_con_id} input`)[0].id
            if (css_display == 'none') {
                $(`#${box_con_id}`).show(300, function(){
                    $(`#${input_id}`).focus()
                })
            } else {
                let input = $(`#${box_con_id} input`)[0].id
                $(`#${input_id}`).focus()
            }
        })
    }
}

function adjust_times() {
    let times = $(".time")
    for (let time of times) {
        let time_raw = $(`#${time.id}`).text()
        let date_obj = new Date(time_raw)
        $(`#${time.id}`).text(date_obj.toLocaleString())
    }
}

function appendComment(response) {
    let parent_id = response['parent_id']
    let comment_time = new Date(response['comment_time'])
    let locale_time = comment_time.toLocaleString()
    if (parent_id == null) {
        comment = `<li>
                    <div class="comment" id="comment-${response['id']}" style="display:none;">
                    <div class="comment-inner">
                        <div class="avatar"><img src="${response['avatar_url']}" alt="avatar"></div>
                        <div class="comment-body">
                        <div class="${response['cssClass']}">${response['author_name']}</div>
                        <div class="time" id="${response['id']}_time">${locale_time}</div>
                        <div class="comment-text">${response['comment_text']}</div>
                        <div class="reply-btn">
                            <button class="show-reply-box" id="${response['id']}_reply-shower" data-box_con_id="${response['id']}_reply-con"><i class='bx bx-reply' ></i><span>Reply</span></button>
                        </div>
                        </div>
                    </div>
                    <div class="replies">
                        <ul class="reply-list" id="${response['id']}-replyList">
                        </ul>
                    </div>
                    <div class="reply-input" style="display: none;" id="${response['id']}_reply-con">
                        <input type="text" name="" id="${response['id']}_reply" placeholder="Reply to this comment" data-comment_id="${response['id']}">
                        <button class="post-comment-btn" id="${response['id']}_reply-btn" data-input_id="${response['id']}_reply" title="post reply"><i class='bx bx-send'></i></button>
                    </div>
                    </div>
                </li>`
        $(`#id_comments-list`).append(comment)
        $(`#comment-${response['id']}`).show(200);
        activate_show_reply(`comment-${response['id']}`)
        activate_post_reply(`comment-${response['id']}`)
        $("#no-comments").hide(50)
    
    } else {
        let comment = `<li>
                        <div class="reply" id="comment-${response['id']}" style="display:none;">
                        <div class="avatar"><img src="${response['avatar_url']}" alt="avatar"></div>
                        <div class="comment-body">
                            <div class="${response['cssClass']}">${response['author_name']}</div>
                            <div class="time" id="${response['id']}_time">${locale_time}</div>
                            <div class="comment-text">${response['comment_text']}</div>
                        </div>
                        </div>
                    </li>`
        $(`#${response['parent_id']}-replyList`).append(comment)
        $(`#comment-${response['id']}`).show(200);
    }
    let num_comments_str
    let num_comments = response['num_comments']
    if (num_comments < 2) {
        num_comments_str = `${num_comments} Comment`
    } else {
        num_comments_str = `${num_comments} Comments`
    }
    $('#id_num-comments').text(num_comments_str)

    
}

function postcomment(payload, send_btn_id, input_id) {
    $.ajax({
        type: "post",
        url: comment_post_url,
        dataType: "json",
        contentType: "application/json",
        beforeSend: function(xhr){
            $(`#${send_btn_id}`).attr("disabled", true)
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        },
        data: JSON.stringify(payload),
        cache: false,
        success: function(response) {
            appendComment(response)
            $(`#${input_id}`).val("")
        },
        error: function() {
            console.log('error fired')
        },
        complete: function() {
            $(`#${send_btn_id}`).removeAttr("disabled");
        }
    });
}

function activate_post_reply(comment_id=null) {
    let post_btns
    if (comment_id == null) {
        post_btns = $(".post-comment-btn")
    } else {
        post_btns = $(`#${comment_id} .post-comment-btn`)
    }
    for (let btn of post_btns) {
        $(`#${btn.id}`).on('click', function(){
            let inp_id = $(this).data('input_id')
            let parent_id = $(`#${inp_id}`).data('comment_id')
            let inp_data = $(`#${inp_id}`).val()
            if (inp_data.length == 0) {
                $(`#${inp_id}`).focus()
            } else {
                let payload = {'comment_text':inp_data}
                if (parent_id !== undefined) {
                    payload['parent_comment_id'] = parent_id
                } else {
                    payload['parent_comment_id'] = null
                }
                postcomment(payload, this.id, inp_id)
            }
        })
    }
}


$(document).ready(function() {
    adjust_times()
    activate_show_reply()
    activate_post_reply()
})