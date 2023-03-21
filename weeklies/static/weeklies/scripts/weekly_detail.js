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
        let filename = $(this).text()
        $("#filemodal-href").attr('href', fileurl);
        $("#filemodal-filename").text(filename);
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

function render_performance_chart(data, raw_points, raw_regularity) {
    let studentNames = data['studentNames']
    let scaled_points = data['points']['scaled']
    let participation = data['participation']
    let scaled_regularity = data['regularity']['scaled']
    var ctx = document.getElementById('weekly_stats_chart').getContext('2d');
    let gridlinecolor = "#073b4c";
    let legendcolor = "#a5a58d"
    var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: studentNames,
        datasets: [
        {
            label: 'Points',
            data: scaled_points,
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 2,
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            fill: true
        },
        {
            label: 'Participation',
            data: participation,
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 2,
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            fill: true
        },
        {
            label: 'Regularity',
            data: scaled_regularity,
            borderColor: 'rgb(55, 224, 176)',
            borderWidth: 2,
            backgroundColor: 'rgba(55, 224, 176, 0.2)',
            fill: true
        }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
        x: {
            display: true,
            ticks: {
            display: false
            },
            grid: {
            color: gridlinecolor
            }
        },
        y: {
            display: true,
            ticks: {
            display: false
            },
            grid: {
            color: gridlinecolor
            }
        }
        },
        legend: {
        labels: {
            fontColor: 'white'
        }
        },
        plugins: {
            legend: {
                display: true,
                labels: {
                    color: legendcolor
                }
            },
            tooltip: {
                callbacks: {
                  label: function (context) {
                    let label = context.dataset.label || '';
                     // get the raw value from the corresponding raw_data array
                    if (label === 'Points') {
                        let pointValue = convertFloat(raw_points[context.dataIndex]);
                        return `Points: ${pointValue}`;
                      } else if (label === 'Regularity') {
                        let regularityValue = convertFloat(raw_regularity[context.dataIndex]);
                        return `Regularity: ${regularityValue}`;
                      } else {
                        return label + ': ' + convertFloat(context.raw) + "%";
                      }
                  }
                }
              }
        },
        animations: {
        tension: {
            duration: 2000,
            easing: 'linear',
            from: 1,
            to: 0,
            loop: false
        }
        },
    }
    });
}

function convertFloat(num) {
    if (num === null || isNaN(num)) {
        return '--';
    }
    if (Number.isInteger(num)) { // Check if the number is already an integer
      return num;
    } else {
      const decimal = num.toFixed(1); // Get the number rounded to one decimal place
      const lastDigit = decimal.charAt(decimal.length - 1); // Get the last character of the decimal
      if (lastDigit === "0") {
        return parseInt(decimal); // If the last digit is 0, return the integer value
      } else {
        return num.toFixed(2); // Otherwise, return the original floating point number
      }
    }
  }

function get_performance_chart_data() {
    $.ajax({
        type: "get",
        url: weekly_performance_api,
        dataType: "json",
        cache: false,
        success: function(response) {
            if (response['has_stats']) {
                $("#chart-loader").hide(0, ()=>{
                    $("#weekly_stats_chart").show()
                    let raw_points = response['points']['raw']
                    let raw_regularity = response['regularity']['raw']
                    render_performance_chart(response, raw_points, raw_regularity) 
                })
            } else {
                $("#chart-loader").hide(0, ()=>{
                    $("#stat-info-con .info").text('No Data Available')
                    $("#stat-info-con").show()
                })
            }
        },
        error: function(xhr, error, status) {
            // $("#chart-loader").hide(0, ()=>{
            //     $("#stat-info-con .info").text(xhr['responseJSON']['info'])
            //     $("#stat-info-con").show()
            // })
            console.log(xhr);
        },
    });
}

$(document).ready(function () {
    $("#create_post_btn").on('click', create_post)
    get_performance_chart_data() 
});

