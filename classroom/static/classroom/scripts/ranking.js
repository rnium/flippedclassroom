// global variables
var first_rank_jwt
var second_rank_jwt
var third_rank_jwt

function convertFloat(number) {
    if (number === null || isNaN(number)) {
        return 0;
    }
    if (Number.isInteger(number)) { // Check if the number is already an integer
      return number;
    } else {
      const decimal = number.toFixed(1); // Get the number rounded to one decimal place
      const lastDigit = decimal.charAt(decimal.length - 1); // Get the last character of the decimal
      if (lastDigit === "0") {
        return parseInt(decimal); // If the last digit is 0, return the integer value
      } else {
        return number.toFixed(2); // Otherwise, return the original floating point number
      }
    }
  }
let notification_count = 1
function notifyUser(text, alert_class='info', timeout=5000, img_url=null) {
    let img = ""
    if (img_url) {
        img = `<img src="${img_url}">`
    }
    let alertid = `notif-${notification_count}`
    notification_count += 1
    let component = `<li id="${alertid}" style="display: none;">
                        <div class="alert-con ${alert_class} shadow">
                            ${img}
                            <div class="alert-info ms-2">${text}</div>
                        </div>
                    </li>`
    $("#notification-alert-list").append(component)
    if ($("#alert-component-con").css("display") == 'none') {
        $("#alert-component-con").show()
    }
    $(`#${alertid}`).show(200, ()=>{
        setTimeout(()=>{
            $(`#${alertid}`).hide(200, ()=>{
                $(`#${alertid}`).remove()
                let count = $("#notification-alert-list li").length;
                console.log(count);
                if (count == 0) {
                    $("#alert-component-con").hide()
                }
            })
        }, timeout)
    })
}

function show_card_confetti(wrapperid) {
    let canvas = document.createElement("canvas");
    let container = document.getElementById(wrapperid);
    canvas.width = 400;
    canvas.height = 700;
    container.appendChild(canvas);
    let confetti_button = confetti.create(canvas);
    confetti_button().then(() => container.removeChild(canvas));
}


function congratulate_user(user_jwt, btn){
    let payload = {'jwt':user_jwt}
    $.ajax({
        type: "post",
        url: congratulate_user_api_url,
        dataType: "json",
        contentType: "application/json",
        beforeSend: function(xhr){
            $(btn).attr("disabled", true)
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        },
        data: JSON.stringify(payload),
        cache: false,
        success: function(response) {
            let notification_text = `Your applause has been sent to ${response['user_fullname']}`
            notifyUser(notification_text, 'info', 5000, alert_icon_confetti)
        },
        error: function(xhr, error, status) {
            let date_obj = new Date(xhr['responseJSON']['next_time'])
            let next_time = date_obj.toLocaleString()
            let notification_text = `${xhr['responseJSON']['info']}. Please try again after ${next_time}`
            notifyUser(notification_text, 'dark', 5000, alert_icon_alert)
        },
        complete: function() {
            $(btn).attr("disabled", false)
        }
    });

}


function activate_congrats_btn() {
    let btns = $(".congrats-btn")
    $.each(btns, function (indexInArray, valueOfElement) { 
        $(valueOfElement).on('click', ()=>{
            let wrapperId = $(this).data('wrapper')
            let rank = $(this).data('rank')
            let user_jwt
            if (rank==1) {
                user_jwt = first_rank_jwt
            } else if (rank==2) {
                user_jwt = second_rank_jwt
            } else if (rank==3) {
                user_jwt = third_rank_jwt
            } else {
                let notification_text = "User rank must be between 1 to 3 to be congratulated"
                notifyUser(notification_text, 'dark', 5000, alert_icon_alert)
                return null
            }
            show_card_confetti(wrapperId)
            congratulate_user(user_jwt, this)
        })
    });
}

const empty_second_topper_card = `<div class="col-sm-4 second empty">
                                    <div class="leaderboard-card">
                                        <div class="leaderboard-card__top pt-5 pb-3">
                                            
                                        </div>
                                        <div class="leaderboard-card__body">
                                            <div class="text-center">
                                                <div class="dp shadow" style="background-image: url('${blank_dp}');"></div>
                                                <h5 class="mb-0"></h5>
                                                <p class="text-muted mb-0"></p>
                                                <img src="${blank_medal}" alt="" class="rank-icon my-3">
                                                <hr>
                                                <div class="info text-muted my-2">Excellence to be achieved</div>
                                                <hr>
                                                <div class="lb-action d-flex justify-content-center align-items-center mt-2">
                                                    <span class="leaderboard-info"><img class="lb-icon" src="${leaderboard}" alt=""><span class="txt">Reserved Second Place</span></span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>`

const empty_first_topper_card = `<div class="col-sm-4 first empty">
                                    <div class="leaderboard-card leaderboard-card--first">
                                        <div class="leaderboard-card__top pt-5">
                                            
                                        </div>
                                        <div class="leaderboard-card__body">
                                            <div class="text-center">
                                                <div class="dp shadow" style="background-image: url('${blank_dp}');"></div>
                                                <h5 class="mb-0"></h5>
                                                <p class="text-muted mb-0"></p>
                                                <img src="${blank_champion}" alt="" class="rank-icon my-3">
                                                <hr>
                                                <div class="info text-muted my-2">Excellence to be achieved</div>
                                                <hr>
                                                <div class="lb-action d-flex justify-content-center align-items-center mt-2">
                                                    <span class="leaderboard-info"><img class="lb-icon" src="${leaderboard}" alt=""><span class="txt">Reserved First Place</span></span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>`

const empty_third_topper_card = `<div class="col-sm-4 third empty">
                                <div class="leaderboard-card">
                                    <div class="leaderboard-card__top pt-5 pb-3">
                                    </div>
                                    <div class="leaderboard-card__body">
                                        <div class="text-center">
                                            <div class="dp shadow" style="background-image: url('${blank_dp}');"></div>
                                            <h5 class="mb-0"></h5>
                                            <p class="text-muted mb-0"></p>
                                            <img src="${blank_medal}" alt="" class="rank-icon my-3">  
                                            <hr>
                                            <div class="info text-muted my-2">Excellence to be achieved</div>
                                            <hr>
                                            <div class="lb-action d-flex justify-content-center align-items-center mt-2">
                                                <span class="leaderboard-info"><img class="lb-icon" src="${leaderboard}" alt=""><span class="txt">Reserved Third Place</span></span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                </div>`

const empty_topper_row = `<div class="row">
                            ${empty_second_topper_card}
                            ${empty_first_topper_card}
                            ${empty_third_topper_card}
                          </div>`


function render_first_rank_card(topper_data) {
    let points = topper_data['classroom_points'];
    let roundedPoints = convertFloat(points);
    let participation = topper_data['participation'];
    let roundedParticipation = convertFloat(participation);
    let regularity = topper_data['regularity'];
    let roundedRegularity = convertFloat(regularity);
    first_rank_jwt = topper_data['jwt']
    let lb_action_elem
    if (topper_data['current_user']) {
        lb_action_elem = `<div class="lb-action d-flex justify-content-center align-items-center mt-2">
                                <span class="leaderboard-info"><img class="lb-icon" src="${leaderboard}" alt=""><span class="txt">Primus</span></span>
                            </div>`
    } else {
        lb_action_elem = `<div class="lb-action d-flex justify-content-between align-items-center mt-2">
                            <span class="leaderboard-info"><img class="lb-icon" src="${leaderboard}" alt=""><span class="txt">Primus</span></span>
                            <button class="congrats-btn congr-btn-first" data-wrapper="first-place-wrapper" data-rank="${topper_data['rank']}">Congratulate</button>
                        </div>`
    }
    let card = `<div class="col-sm-4 first">
                    <div class="leaderboard-card leaderboard-card--first shadow" id="first-place-wrapper">
                        <div class="leaderboard-card__top">
                            <h3 class="text-center points">${roundedPoints}</h3>
                        </div>
                        <div class="leaderboard-card__body">
                            <div class="text-center content">
                            <div class="dp shadow" style="background-image: url('${topper_data['avatar_url']}');"></div>
                                <h5 class="mb-0 name">${topper_data['full_name']}</h5>
                                <p class="text-muted mb-0 reg-no">${topper_data['registration']}</p>
                                <img src="${first_rank}" alt="" class="rank-icon my-3">
                                <hr>
                                <div class="stats d-flex justify-content-around align-items-center my-2">
                                    <div class="s-item">
                                        <span class="label">Participation:</span>
                                        <span class="value">${roundedParticipation}%</span>
                                    </div>
                                    <div class="s-item">
                                        <span class="label">Regularity:</span>
                                        <span class="value">${roundedRegularity}</span>
                                    </div>
                                </div>
                                <hr>
                                ${lb_action_elem}
                            </div>
                        </div>
                    </div>
                </div>`
    return card
}

function render_second_rank_card(topper_data) {
    let points = topper_data['classroom_points'];
    let roundedPoints = convertFloat(points);
    let participation = topper_data['participation'];
    let roundedParticipation = convertFloat(participation);
    let regularity = topper_data['regularity'];
    let roundedRegularity = convertFloat(regularity);
    second_rank_jwt = topper_data['jwt']
    
    let lb_action_elem
    if (topper_data['current_user']) {
        lb_action_elem = `<div class="lb-action mt-2 d-flex justify-content-center align-items-center mt-2">
                                <span class="leaderboard-info"><img class="lb-icon" src="${leaderboard}" alt=""><span class="txt">Secundus</span></span>
                            </div>`
    } else {
        lb_action_elem = `<div class="lb-action mt-2 d-flex justify-content-between align-items-center">
                            <span class="leaderboard-info"><img class="lb-icon" src="${leaderboard}" alt=""><span class="txt">Secundus</span></span>
                            <button class="congrats-btn congr-btn-second" data-wrapper="second-place-wrapper" data-rank="${topper_data['rank']}">Congratulate</button>
                        </div>`
    }
    let card = `<div class="col-sm-4 second">
                <div class="leaderboard-card" id="second-place-wrapper">
                    <div class="leaderboard-card__top">
                        <h3 class="text-center points">${roundedPoints}</h3>
                    </div>
                    <div class="leaderboard-card__body">
                        <div class="text-center content">
                            <div class="dp shadow" style="background-image: url('${topper_data['avatar_url']}');"></div>
                            <h5 class="mb-0 name">${topper_data['full_name']}</h5>
                            <p class="text-muted mb-0 reg-no">${topper_data['registration']}</p>
                            <img src="${second_rank}" alt="" class="rank-icon my-3">
                            
                            <hr>
                            <div class="stats d-flex justify-content-around align-items-center my-2">
                                <div class="s-item">
                                    <span class="label">Participation:</span>
                                    <span class="value">${roundedParticipation}%</span>
                                </div>
                                <div class="s-item">
                                    <span class="label">Regularity:</span>
                                    <span class="value">${roundedRegularity}</span>
                                </div>
                            </div>
                            <hr>
                            ${lb_action_elem}
                        </div>
                    </div>
                </div>
            </div>`
    return card
}

function render_third_rank_card(topper_data) {
    let points = topper_data['classroom_points'];
    let roundedPoints = convertFloat(points);
    let participation = topper_data['participation'];
    let roundedParticipation = convertFloat(participation);
    let regularity = topper_data['regularity'];
    let roundedRegularity = convertFloat(regularity);
    third_rank_jwt = topper_data['jwt']
    
    let lb_action_elem
    if (topper_data['current_user']) {
        lb_action_elem = `<div class="lb-action mt-2 d-flex justify-content-center align-items-center mt-2">
                                <span class="leaderboard-info"><img class="lb-icon" src="${leaderboard}" alt=""><span class="txt">Tertius</span></span>
                            </div>`
    } else {
        lb_action_elem = `<div class="lb-action mt-2 d-flex justify-content-between align-items-center">
                            <span class="leaderboard-info"><img class="lb-icon" src="${leaderboard}" alt=""><span class="txt">Tertius</span></span>
                            <button class="congrats-btn congr-btn-third" data-wrapper="third-place-wrapper" data-rank="${topper_data['rank']}">Congratulate</button>
                        </div>`
    }
    let card = `<div class="col-sm-4 third">
                <div class="leaderboard-card" id="third-place-wrapper">
                    <div class="leaderboard-card__top">
                        <h3 class="text-center points">${roundedPoints}</h3>
                    </div>
                    <div class="leaderboard-card__body">
                        <div class="text-center content">
                            <div class="dp shadow" style="background-image: url('${topper_data['avatar_url']}');"></div>
                            <h5 class="mb-0 name">${topper_data['full_name']}</h5>
                            <p class="text-muted mb-0 reg-no">${topper_data['registration']}</p>
                            <img src="${third_rank}" alt="" class="rank-icon my-3">
                            
                            <hr>
                            <div class="stats d-flex justify-content-around align-items-center my-2">
                                <div class="s-item">
                                    <span class="label">Participation:</span>
                                    <span class="value">${roundedParticipation}%</span>
                                </div>
                                <div class="s-item">
                                    <span class="label">Regularity:</span>
                                    <span class="value">${roundedRegularity}</span>
                                </div>
                            </div>
                            <hr>
                            ${lb_action_elem}
                        </div>
                    </div>
                </div>
            </div>`
    return card
}


function render_toppers_section(toppers_data) {
    let first_rank_card
    let second_rank_card
    let third_rank_card
    let topper_dataset_length = Object.keys(toppers_data).length;
    if (topper_dataset_length == 1) {
        first_rank_card = render_first_rank_card(toppers_data['first'])
        second_rank_card = empty_second_topper_card
        third_rank_card = empty_third_topper_card
    } else if (topper_dataset_length == 2) {
        first_rank_card = render_first_rank_card(toppers_data['first'])
        second_rank_card = render_second_rank_card(toppers_data['second'])
        third_rank_card = empty_third_topper_card
    } else if (topper_dataset_length == 3) {
        first_rank_card = render_first_rank_card(toppers_data['first'])
        second_rank_card = render_second_rank_card(toppers_data['second'])
        third_rank_card = render_third_rank_card(toppers_data['third'])
    } else {
        first_rank_card = empty_first_topper_card
        second_rank_card = empty_second_topper_card
        third_rank_card = empty_third_topper_card
    }
    let topper_section = `<div class="row">
                                ${second_rank_card}
                                ${first_rank_card}
                                ${third_rank_card}
                          </div>`
    return topper_section
}

function render_ranking_table_rows(rows_data, unranked=false) {
    rows = ''
    for (let row of rows_data) {
        let points = row['classroom_points'];
        let roundedPoints = convertFloat(points);
        let participation = row['participation'];
        let roundedParticipation = convertFloat(participation);
        let regularity = row['regularity'];
        let roundedRegularity = convertFloat(regularity);
        let rankNum
        let rankingClass = ''
        if (unranked) {
            rankNum = "--"
            rankingClass = 'unranked'
        } else {
            rankNum = row['rank']
        }
        
        row_elem = `<tr class="${rankingClass}">
                        <td>
                            <div class="d-flex align-items-center">
                                <div class="dp" style="background-image: url('${row['avatar_url']}');"></div>
                                <div class="user-info__basic">
                                    <h5 class="mb-0">${row['full_name']}</h5>
                                    <p class="text-muted mb-0">${row['registration']}</p>
                                </div>
                            </div>
                        </td>
                        <td>
                            <div class="d-flex align-items-baseline">
                                <h4 class="mr-1">${rankNum}</h4>
                            </div>
                        </td>
                        <td>${roundedPoints}</td>
                        <td>${roundedParticipation}%</td>
                        <td>${roundedRegularity}</td>
                    </tr>`
        rows += row_elem
    }
    return rows
}

function render_table(ranked_students, unranked_students) {
    let ranked_rows = render_ranking_table_rows(ranked_students)
    let unranked_rows = render_ranking_table_rows(unranked_students, unranked=true)
    let table_rows = ranked_rows + unranked_rows
    let ranking_table = `<div class="table-con">
                            <table class="table">
                                <thead>
                                    <tr>
                                        <th>Student</th>
                                        <th>Rank</th>
                                        <th>Points</th>
                                        <th>Participation</th>
                                        <th>Regularity</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${table_rows} 
                                </tbody>
                            </table>
                        </div>`
    return ranking_table
}

function process_ranking_data(response) {
    let data = response['data']
    toppers = data['toppers']
    let toppers_section = render_toppers_section(data['toppers'])
    let table = ""
    if (response['has_ranking']) {
        table = render_table(data['ranked_students'], data['unranked_students'])
    }
    
    let container = `<div class="container">
                        ${toppers_section}
                        ${table}
                    </div>`
    $("#leaderboard-container").html(container);
    $("#loader-con").hide(0, ()=>{
        $("#leaderboard-container").show()
        activate_congrats_btn()
    });
}

function get_ranking_data() {
    $.ajax({
        type: "get",
        url: ranking_api_url,
        dataType: "json",
        cache: false,
        success: function(response) {
            process_ranking_data(response)
        },
        error: function(error, xhr, status) {
            console.log(error);
        },
    });
}


get_ranking_data()

