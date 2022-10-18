function activate_post_reply() {
    let post_btns = $('.post-comment-btn')
    for (let btn of post_btns) {
        $(`#${btn.id}`).on('click', function(){
            let inp_id = $(this).data('input_id')
            inp_data = $(`#${inp_id}`).val()
            if (inp_data.length == 0) {
                $(`#${inp_id}`).focus()
            } else {
                console.log('good to post the comment')
                $(`#${inp_id}`).val("")
            }
        })
    }
}

function activate_show_reply() {
    let reply_btns = $(".show-reply-box")
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

activate_show_reply()
activate_post_reply()