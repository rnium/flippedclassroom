const no_content = `<div class="no-content" id="id-no-content" style="display: none;">
                        <i class='bx bx-file-blank'></i>
                        <span>No Answersheet has been submitted yet</span>
                    </div>`
let prev_page_url
let next_page_url

function renderTable(row_data, hidden=false) {
    let inline_style
    if (hidden) {
        inline_style =  `style="display:none;"`
    } else {
        inline_style =  ''
    }

    let row_components = ""
    for (let row of row_data) {
        let user_score
        let issue_time = new Date(row['issue_time']).toLocaleString()
        if (row['score'] == null) {
            user_score = `<td class="score-pending"><span>Pending</span></td>`
        } else {
            user_score = `<td class="score">${row['score']}</td>`
        }
        row_components += `<tr>
                            <td class="user">
                                <div class="dp" style="background-image: url('${row['avatar_url']}');"></div>
                                <span>${row['student_name']}</span>
                            </td>
                            <td class="sheet-id"><a href="${row['view_url']}">${row['id']}</a></td>
                            <td>${issue_time}</td>
                            <td>${row['answers_submitted']}</td>
                            <td>${row['answers_correct']}</td>
                            ${user_score}
                        </tr>`
        
    }
    let table = `<table id="id-table" ${inline_style}>
                    <tr>
                        <th>Student</th>
                        <th>Sheet ID</th>
                        <th>Issue Time</th>
                        <th>Submitted Answers</th>
                        <th>Correct Answers</th>
                        <th>Score</th>
                    </tr>
                    ${row_components}
                </table>`
    return table
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

function fetch_new_page(url) {
    $.ajax({
        type: "get",
        url: url,
        dataType: "json",
        success: function (response) {
            let container = renderTable(response['results'])
            let paginator = render_paginator(response)
            let content = container + paginator
            $("#table-content").html(content)
            setTimeout(function(){ 
                activate_paginator_btns()
             }, 50)
            prev_page_url = response['prev']
            next_page_url = response['next']
        }
    });
}

function activate_paginator_btns() {
    $('#first_page').on('click', function(){
        let url = `/test/api/${test_id}/answersheets`
        fetch_new_page(url)
    })
    $('#last_page').on('click', function(){
        let url = `/test/api/${test_id}/answersheets?p=last`
        fetch_new_page(url)
    })
    $('#prev_page').on('click', function(){
        fetch_new_page(prev_page_url)
    })
    $('#next_page').on('click', function(){
        fetch_new_page(next_page_url)
    })
}


function fetchTableData() {
    $.ajax({
        type: "get",
        url: api_url,
        dataType: "json",
        success: function (response) {
            if (response['count'] == 0) {
                $("#table-content").html(no_content)
                $("#id-no-content").show(300)
                $("#loader").hide()
            } else {
                let table_elem = renderTable(response['results'], true)
                let paginator = render_paginator(response, true)
                let content = table_elem + paginator
                $("#loader").hide()
                $("#table-content").html(content)
                $("#id-table").show(200, function(){
                    $("#id_paginator").css('opacity', 1)
                })
                prev_page_url = response['prev']
                next_page_url = response['next']
                activate_paginator_btns()
            }
            
        }
    });
}

function update_test_expiration(is_expired) {
    let data = {
        test_id: test_id,
        is_expired: is_expired
    }
    
    $.ajax({
        url: api_expiration_update_url,
        contentType: "application/json",
        type: "POST",
        beforeSend: function(xhr){
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        },
        data: JSON.stringify(data),
        cache: false,
        dataType: "json",
        success: function(response){
            if (response['expired']) {
                $("#switch-info").text("Test is Inactive")
            } else {
                $("#switch-info").text("Test is Active")
            }
        },
    })
}

$(document).ready(function(){
    fetchTableData()
    $("#test-exp-switch").on("change", function(){
        let checked_status = $("#test-exp-switch").is(":checked")
        if (checked_status === true) {
            update_test_expiration(false)
        } else {
            update_test_expiration(true)
        } 
    })
})