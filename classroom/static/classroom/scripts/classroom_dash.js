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

activate_option_btns()

$('#share-link').on('click', function(){
    navigator.clipboard.writeText(join_link)
    $('#copy-info').show(200)
    setTimeout(function(){
        $('#copy-info').hide(200)
    }, 1200)
})

/* <div class="post-container" id="post-container">
      <div class="post-item">
        <div class="icon"><i class='bx bx-file'></i></div>
        <div class="contents">
          <a href="" class="title">Lorem ipsum dolor sit amet consectetur adipisicing</a>
          <div class="post-time">Oct 7, 2022</div>
          <div class="info">
            <div class="info-item"><i class='bx bx-paperclip'></i><span>2 attachments</span></div>
            <div class="info-item"><i class='bx bx-envelope-open'></i><span>21 student opened</span></div>
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
      </div>
      <div class="post-item">
        <div class="icon"><i class='bx bx-file'></i></div>
        <div class="contents">
          <a href="" class="title">Lorem ipsum dolor sit amet consectetur adipisicing</a>
          <div class="post-time">Oct 7, 2022</div>
          <div class="info">
            <div class="info-item"><i class='bx bx-paperclip'></i><span>2 attachments</span></div>
            <div class="info-item"><i class='bx bx-envelope-open'></i><span>21 student opened</span></div>
            <div class="info-item"><i class='bx bx-comment'></i><span>7 comments</span></div>
          </div>
        </div>
        <div class="options">
          <div class="options-container" id="post1-op-con" style="display: none;">
            <a href="">Edit</a>
            <a href="">Delete</a>
          </div>
          <button class="option-toggle" id="post1-option-toggle" data-op_con="post1-op-con"><i class='bx bx-dots-horizontal-rounded'></i></button>
        </div>
      </div>
      <div class="post-item">
        <div class="icon"><i class='bx bx-file'></i></div>
        <div class="contents">
          <a href="" class="title">Lorem ipsum dolor sit amet consectetur adipisicing</a>
          <div class="post-time">Oct 7, 2022</div>
          <div class="info">
            <div class="info-item"><i class='bx bx-paperclip'></i><span>2 attachments</span></div>
            <div class="info-item"><i class='bx bx-envelope-open'></i><span>21 student opened</span></div>
            <div class="info-item"><i class='bx bx-comment'></i><span>7 comments</span></div>
          </div>
        </div>
        <div class="options">
          <div class="options-container" id="post2-op-con" style="display: none;">
            <a href="">Edit</a>
            <a href="">Delete</a>
          </div>
          <button class="option-toggle" id="post2-option-toggle" data-op_con="post2-op-con"><i class='bx bx-dots-horizontal-rounded'></i></button>
        </div>
      </div>
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

function load_page_data(page_no=null) { 
    if (page_no === null) {
        url = `/classroom/api/${classroom_id}/posts`
    } else {
        url = `/classroom/api/${classroom_id}/posts?p=${page_no}`
    }
    $.ajax({
        type: "get",
        url: url,
        data: "data",
        dataType: "json",
        success: function (response) {
            return response
        }
    });
}

$(document).ready(function(){
    page_data = load_page_data()
    console.log(page_data)
})
