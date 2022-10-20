function activate_option_btns() {
    op_btns = $('.option-toggle')
    $.each(op_btns, function (indexInArray, valueOfElement) { 
        $(`#${valueOfElement.id}`).on('click', function(){
            op_con = $(this).data('op_con')
            $(`#${op_con}`).toggle(100)
            let all_options = $('.options-container')
            for (let opt of all_options) {
                let op_id = opt.id
                if ( op_id != op_con) {
                    if ($(`#${op_id}`).css('display') != 'none') {
                        $(`#${op_id}`).hide(200)
                    }
                }
            }
        })
    });
}

$('#share-link').on('click', function(){
    navigator.clipboard.writeText(join_link)
    $('#copy-info').show(200)
    setTimeout(function(){
        $('#copy-info').hide(200)
    }, 1200)
})

// function format_post_dates() { 
//     let times = $('.post-time')
//     for (let time of times) {
//         $(`#${time.id}`).datepicker({
//             altFormat: "yy-mm-dd"
//         });
//     }
//  }

/* <div class="post-container" id="post-container">
      
    </div>
    <div class="paginator">
      <div class="inner">
        <ul>
            <li><button class="paginator-btn" id="first_page"><</button></li>
            <li><button class="paginator-btn" id="prev_page">1</button></li>
            <li><span class="current-page">2</span></li>
            <li><button class="paginator-btn" id="next_page">3</button></li>
            <li><button class="paginator-btn" id="next_page">></button></li>
        </ul>
      </div>
    </div> */


function render_post_component(post_data) {
    let description = post_data['description'].split(' ').slice(0, 7).join(' ')
    let date_raw = new Date(post_data['posted'])
    let date = date_raw.toLocaleString("en-US")
    post_comp = `<div class="post-item">
                    <div class="icon"><i class='bx bx-file'></i></div>
                    <div class="contents">
                    <a href="" class="title">${description}</a>
                    <div class="post-time" id="${post_data['id']}-time">${date}</div>
                    <div class="info">
                        <div class="info-item"><i class='bx bx-paperclip'></i><span>${post_data['num_attachments']} attachments</span></div>
                        <div class="info-item"><i class='bx bx-comment'></i><span>7 comments</span></div>
                    </div>
                    </div>
                    <div class="options">
                    <div class="options-container" id="${post_data['id']}-op-con" style="display: none;">
                        <a href="">Edit</a>
                        <a href="">Delete</a>
                    </div>
                    <button class="option-toggle" id="${post_data['id']}-option-toggle" data-op_con="${post_data['id']}-op-con"><i class='bx bx-dots-horizontal-rounded'></i></button>
                    </div>
                </div>`
    return post_comp
}

function render_paginator(response) {
    if (response['total_pages'] < 2) {
        return ""
    }
    let list_items = ""
    let current_page_no = response['current_page']
    let prev_page_no = current_page_no - 1
    let next_page_no = current_page_no + 1
    if (response['prev'] != null) {
        if (prev_page_no > 1) {
            list_items += `<li><button class="paginator-btn" id="first_page"><</button></li>`
        }
        list_items += `<li><button class="paginator-btn" id="prev_page">${prev_page_no}</button></li>`
    }
    list_items += `<li><span class="current-page">${current_page_no}</span></li>`
    if (response['next'] !== null) {
        list_items += `<li><button class="paginator-btn" id="next_page">${next_page_no}</button></li>`
        if (next_page_no < response['total_pages']) {
            list_items += `<li><button class="paginator-btn" id="next_page">></button></li>`
        }
    }
    let paginator =`<div class="paginator">
                        <div class="inner">
                        <ul>
                            ${list_items}
                        </ul>
                        </div>
                    </div>`
    return paginator
}

function render_post_container(posts_arr) {
  let posts = ""
  for (let post of posts_arr) {
    posts += render_post_component(post)
  }
  posts_container =`<div class="post-container" id="post-container">
                      ${posts}
                    </div>`
  return posts_container
}


function load_page_data() { 
    url = `/classroom/api/${classroom_id}/posts`
    $.ajax({
        type: "get",
        url: url,
        data: "data",
        dataType: "json",
        success: function (response) {
          let container = render_post_container(response['results'])
          let paginator = render_paginator(response)
          let content = container + paginator
          $("#recent-posts").html(content)
          $("#recent-posts").show(500, function(){
            activate_option_btns()
          })
        }
    });
}

$(document).ready(function(){
  load_page_data()
})
