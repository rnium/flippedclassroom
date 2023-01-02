let prev_page_url
let next_page_url

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

let inputfield = document.getElementById('post-files')
if (inputfield !== null) {
    inputfield.addEventListener("change", function(){
        let file_nums = inputfield.files.length
        let filename_container = document.getElementById(`postfiles-file`)
        let num_str
        if (file_nums > 1) {
            num_str = 'files'
        } else {
            num_str = 'file'
        }
        filename_container.innerText = `${file_nums} ${num_str} selected`
    })
}


// create weekly
$("#create-weekly-btn").on('click', ()=>{
    // $(this).text("Create");
    let is_double = $("#create-weekly-btns-con").hasClass("double");
    if (!is_double) {
        $("#weekly-topic-inp-con").show(100)
        $("#create-weekly-btns-con").addClass("double");
        $("#create-weekly-cancel-btn").show(100)
        $("#create-weekly-btn").text("Create");
    } else {
        console.log('proceed to request');
    }
})

$("#create-weekly-cancel-btn").on('click', ()=>{
    let is_double = $("#create-weekly-btns-con").hasClass("double");
    if (is_double) {
        $("#weekly-topic-inp-con").hide(100)
        $("#create-weekly-btns-con").removeClass("double");
        $("#create-weekly-cancel-btn").hide(100)
        $("#create-weekly-btn").text("Create Weekly");
    }
})

function check_existing_input_files(){
    let inputfield = document.getElementById('post-files')
    if (inputfield !== null) {
        let file_nums = inputfield.files.length
        if (file_nums > 0) {
            let filename_container = document.getElementById(`postfiles-file`)
            let num_str
            if (file_nums > 1) {
                num_str = 'files'
            } else {
                num_str = 'file'
            }
            filename_container.innerText = `${file_nums} ${num_str} selected`
        } else {
            $("#postfiles-file").text('No files selected')
        }
    }
}


function render_post_component(post_data, hidden=false) {
    let inline_style
    let topic_container
    if (hidden) {
        inline_style =  `style="display:none;"`
    } else {
        inline_style =  ''
    }
    let description = post_data['description'].split(' ').slice(0, 7).join(' ')
    let date_raw = new Date(post_data['posted'])
    let topics_data = post_data['topics']
    if (topics_data.length > 0) {
        let topic_elements = ''
        topics_data.forEach(element => {
            topic_elements += `<a href="${element['topic_url']}" class="topic"><span class="content"><i class='bx bx-tag-alt'></i><span>${element['name']}</span></span></a> `
        })
        topic_container = `<div class="topics">
                                    ${topic_elements}
                                </div>`


    } else {
        topic_container = ''
    }

    let date = date_raw.toLocaleString("en-US")
    let options = ""
    if (post_data['action_permitted']) {
        options = `<div class="options">
                        <div class="options-container" id="${post_data['id']}-op-con" style="display: none;">
                            <a href="${post_data['edit_url']}">Edit</a>
                            <a href="${post_data['delete_url']}">Delete</a>
                        </div>
                        <button class="option-toggle" id="${post_data['id']}-option-toggle" data-op_con="${post_data['id']}-op-con"><i class='bx bx-dots-horizontal-rounded'></i></button>
                    </div>`
    }
    post_comp = `<div class="post-item" ${inline_style}>
                    <div class="icon"><i class='bx bx-file'></i></div>
                    <div class="contents">
                    <a href="${post_data['view_url']}" class="title">${description}</a>
                    <div class="post-time" id="${post_data['id']}-time">${date}</div>
                    ${topic_container}
                    <div class="info">
                        <div class="info-item"><i class='bx bx-paperclip'></i><span>${post_data['num_attachments']} attachments</span></div>
                        <div class="info-item"><i class='bx bx-comment'></i><span>${post_data['num_comments']} comments</span></div>
                    </div>
                    </div>
                    ${options}
                </div>`
    return post_comp
}

function render_paginator(response, is_first_load=false) {
    if (response['total_pages'] < 2) {
        return ""
    }
    let inline_css = ""
    if (is_first_load) {
        inline_css = `style="opacity:0;"`
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
    } else {
        list_items += `<li style="display:none;"><button class="paginator-btn" id="first_page"><</button></li>`
        list_items += `<li style="display:none;"><button class="paginator-btn" id="prev_page"></button></li>`
    }
    list_items += `<li><span class="current-page" id="current-page">${current_page_no}</span></li>`
    if (response['next'] !== null) {
        list_items += `<li><button class="paginator-btn" id="next_page">${next_page_no}</button></li>`
        if (next_page_no < response['total_pages']) {
            list_items += `<li><button class="paginator-btn" id="last_page">></button></li>`
        }
    } else {
        list_items += `<li style="display:none;"><button class="paginator-btn" id="next_page"></button></li>`
        list_items += `<li style="display:none;"><button class="paginator-btn" id="last_page">></button></li>`
    }
    let paginator =`<div class="paginator" id="id_paginator" ${inline_css}>
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
    if (posts_arr.length == 0) {
        posts = `<div class="no-posts"><i class='bx bx-folder-open'></i><span>No posts yet</span></div>`
    } else {
        for (let post of posts_arr) {
            posts += render_post_component(post)
        }
    }
    posts_container =`<div class="post-container" id="post-container">
                        ${posts}
                        </div>`
    return posts_container
}

function fetch_new_page(url) {
    $.ajax({
        type: "get",
        url: url,
        dataType: "json",
        success: function (response) {
            let container = render_post_container(response['results'])
            let paginator = render_paginator(response)
            let content = container + paginator
            $("#recent-posts").html(content)
            setTimeout(function(){ 
                activate_option_btns()
                activate_paginator_btns()
             }, 50)
            prev_page_url = response['prev']
            next_page_url = response['next']
        }
    });
}

function activate_paginator_btns() {
    $('#first_page').on('click', function(){
        let url = `/classroom/api/${classroom_id}/posts`
        fetch_new_page(url)
    })
    $('#last_page').on('click', function(){
        let url = `/classroom/api/${classroom_id}/posts?p=last`
        fetch_new_page(url)
    })
    $('#prev_page').on('click', function(){
        fetch_new_page(prev_page_url)
    })
    $('#next_page').on('click', function(){
        fetch_new_page(next_page_url)
    })
}

function load_page_data() { 
    url = `/classroom/api/${classroom_id}/posts`
    $.ajax({
        type: "get",
        url: url,
        dataType: "json",
        success: function (response) {
          let container = render_post_container(response['results'])
          let paginator = render_paginator(response, true)
          let content = container + paginator
          $("#recent-posts").html(content)
          $("#recent-posts").show(200, function(){
            activate_option_btns()
            $("#id_paginator").css('opacity', 1)
          })
          prev_page_url = response['prev']
          next_page_url = response['next']
          activate_paginator_btns()
        }
    });
}


function adjust_times() {
    let times = $(".time")
    for (let time of times) {
        let time_raw = $(`#${time.id}`).text()
        let date_obj = new Date(time_raw)
        $(`#${time.id}`).text(date_obj.toLocaleString())
    }
}


$(document).ready(function(){
    check_existing_input_files()
    adjust_times()
    load_page_data()
    
})

function processTopics() {
    let topics_str = $("#topics").val()
    if (topics_str.length > 0) {
        topics_arr = topics_str.split(',')
        let topics = []
        topics_arr.forEach(element => {
            let trimmed = element.trim()
            let arr = trimmed.split("")
            arr[0] = arr[0].toUpperCase()
            formatted_topic = arr.join("")
            topics.push(formatted_topic)
        });
        return topics.join(',')
    } else {
        return ''
    }
}

function perform_post() {
    files = $("#post-files")[0].files
    let post_form = new FormData

    // fix csrftoken with formdata
    let post_description = $("#post-descr").val()
    let topics = processTopics()
    post_form.append("post_description", post_description)
    post_form.append("topics", topics)
    if (files.length > 0) {
        for (let file of files) {
            post_form.append("files", file)
        }
    } 
    $.ajax({
        type: "post",
        url: post_create_url,
        data: post_form,
        contentType: false,
        processData: false,
        beforeSend: function(){
            $("#loader").show(100)
            $("#create-post").attr('disabled', true)
        },
        success: function(){
            console.log('success fired')
            $("#recent-posts").hide(100)
            load_page_data()
            $("#post-files").val("")
            $("#post-descr").val("")
            $("#topics").val("")
            check_existing_input_files()
        },
        complete: function(){
            console.log('complete');
            $("#loader").hide(100)
            $("#create-post").removeAttr('disabled');
        }
    });
 }

$("#create-post").on('click', function () {
    let post_description = $("#post-descr").val()
    if (post_description.length < 1) {
        $("#post-descr").focus()
        return null
    }
    perform_post()
 })
