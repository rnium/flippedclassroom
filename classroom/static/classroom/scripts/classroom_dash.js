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
    post_comp = `<div class="post-item">
                    <div class="icon"><i class='bx bx-file'></i></div>
                    <div class="contents">
                    <a href="" class="title">${description}</a>
                    <div class="post-time">${post_data['posted']}</div>
                    <div class="info">
                        <div class="info-item"><i class='bx bx-paperclip'></i><span>${post_data['num_attachments']} attachments</span></div>
                        <div class="info-item"><i class='bx bx-comment'></i><span>7 comments</span></div>
                    </div>
                    </div>
                    <div class="options">
                    <div class="options-container" id="post0-op-con" style="display: none;">
                        <a href="">Edit</a>
                        <a href="">Delete</a>
                    </div>
                    <button class="option-toggle" id="post0-option-toggle" data-op_con="post0-op-con"><i class='bx bx-dots-horizontal-rounded'></i></button>
                    </div>
                </div>`
    return post_comp
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
          $("#recent-posts").html(container)
          $("#recent-posts").show(500, function(){
            activate_option_btns()
          })
        }
    });
}

$(document).ready(function(){
  load_page_data()
})
