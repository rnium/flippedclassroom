const empty_second_topper_card = `<div class="col-sm-4 second empty">
                                    <div class="leaderboard-card">
                                        <div class="leaderboard-card__top pt-5 pb-3">
                                            
                                        </div>
                                        <div class="leaderboard-card__body">
                                            <div class="text-center">
                                                <img src="${blank_dp}" class="circle-img mb-2" alt="User Img">
                                                <h5 class="mb-0"></h5>
                                                <p class="text-muted mb-0"></p>
                                                <img src="${blank_medal}" alt="" class="rank-icon my-3">
                                                <hr>
                                                <div class="info text-muted my-2">Excellence to be achieved</div>
                                                <hr>
                                                <div class="lb-action d-flex justify-content-center align-items-center mt-2">
                                                    <span class="leaderboard-info"><img class="lb-icon" src="${leaderboard}" alt=""><span class="txt">Reserved Second Rank</span></span>
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
                                                <img src="${blank_dp}" class="circle-img mb-2" alt="User Img">
                                                <h5 class="mb-0"></h5>
                                                <p class="text-muted mb-0"></p>
                                                <img src="${blank_champion}" alt="" class="rank-icon my-3">
                                                <hr>
                                                <div class="info text-muted my-2">Excellence to be achieved</div>
                                                <hr>
                                                <div class="lb-action d-flex justify-content-center align-items-center mt-2">
                                                    <span class="leaderboard-info"><img class="lb-icon" src="${leaderboard}" alt=""><span class="txt">Reserved First Rank</span></span>
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
                                            <img src="${blank_dp}" class="circle-img mb-2" alt="User Img">
                                            <h5 class="mb-0"></h5>
                                            <p class="text-muted mb-0"></p>
                                            <img src="${blank_medal}" alt="" class="rank-icon my-3">  
                                            <hr>
                                            <div class="info text-muted my-2">Excellence to be achieved</div>
                                            <hr>
                                            <div class="lb-action d-flex justify-content-center align-items-center mt-2">
                                                <span class="leaderboard-info"><img class="lb-icon" src="${leaderboard}" alt=""><span class="txt">Reserved Third Rank</span></span>
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
    let roundedPoints = points.toFixed(2);
    let participation = topper_data['participation'];
    let roundedParticipation = participation.toFixed(2);
    let regularity = topper_data['regularity'];
    let roundedRegularity = regularity.toFixed(2);
    
    let lb_action_elem
    if (topper_data['current_user']) {
        lb_action_elem = `<div class="lb-action d-flex justify-content-center align-items-center mt-2">
                                <span class="leaderboard-info"><img class="lb-icon" src="${leaderboard}" alt=""><span class="txt">First Rank</span></span>
                            </div>`
    } else {
        lb_action_elem = `<div class="lb-action d-flex justify-content-between align-items-center mt-2">
                            <span class="leaderboard-info"><img class="lb-icon" src="${leaderboard}" alt=""><span class="txt">First Rank</span></span>
                            <button class="btn btn-outline-success btn-sm">Congratulate</button>
                        </div>`
    }
    let card = `<div class="col-sm-4 first">
                    <div class="leaderboard-card leaderboard-card--first">
                        <div class="leaderboard-card__top">
                            <h3 class="text-center">${roundedPoints}</h3>
                        </div>
                        <div class="leaderboard-card__body">
                            <div class="text-center">
                                <img src="${topper_data['avatar_url']}" class="circle-img mb-2" alt="User Img">
                                <h5 class="mb-0">${topper_data['full_name']}</h5>
                                <p class="text-muted mb-0">${topper_data['registration']}</p>
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
    let roundedPoints = points.toFixed(2);
    let participation = topper_data['participation'];
    let roundedParticipation = participation.toFixed(2);
    let regularity = topper_data['regularity'];
    let roundedRegularity = regularity.toFixed(2);
    
    let lb_action_elem
    if (topper_data['current_user']) {
        lb_action_elem = `<div class="lb-action d-flex justify-content-center align-items-center mt-2">
                                <span class="leaderboard-info"><img class="lb-icon" src="${leaderboard}" alt=""><span class="txt">Second Rank</span></span>
                            </div>`
    } else {
        lb_action_elem = `<div class="lb-action d-flex justify-content-between align-items-center">
                            <span class="leaderboard-info"><img class="lb-icon" src="${leaderboard}" alt=""><span class="txt">Second Rank</span></span>
                            <button class="btn btn-outline-success btn-sm">Congratulate</button>
                        </div>`
    }
    let card = `<div class="col-sm-4 second" style="display: none;">
                <div class="leaderboard-card">
                    <div class="leaderboard-card__top">
                        <h3 class="text-center">${roundedPoints}</h3>
                    </div>
                    <div class="leaderboard-card__body">
                        <div class="text-center">
                            <img src="${topper_data['avatar_url']}" class="circle-img mb-2" alt="User Img">
                            <h5 class="mb-0">${topper_data['full_name']}</h5>
                            <p class="text-muted mb-0">${topper_data['registration']}</p>
                            <img src="${second_rank}" alt="" class="rank-icon my-3">
                            
                            <hr>
                            <div class="stats d-flex justify-content-around align-items-center my-2">
                                <div class="s-item">
                                    <span class="label">Participation:</span>
                                    <span class="value">${roundedParticipation}%%</span>
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
    let roundedPoints = points.toFixed(2);
    let participation = topper_data['participation'];
    let roundedParticipation = participation.toFixed(2);
    let regularity = topper_data['regularity'];
    let roundedRegularity = regularity.toFixed(2);
    
    let lb_action_elem
    if (topper_data['current_user']) {
        lb_action_elem = `<div class="lb-action d-flex justify-content-center align-items-center mt-2">
                                <span class="leaderboard-info"><img class="lb-icon" src="${leaderboard}" alt=""><span class="txt">Third Rank</span></span>
                            </div>`
    } else {
        lb_action_elem = `<div class="lb-action d-flex justify-content-between align-items-center">
                            <span class="leaderboard-info"><img class="lb-icon" src="${leaderboard}" alt=""><span class="txt">Third Rank</span></span>
                            <button class="btn btn-outline-success btn-sm">Congratulate</button>
                        </div>`
    }
    let card = `<div class="col-sm-4 third" style="display: none;">
                <div class="leaderboard-card">
                    <div class="leaderboard-card__top">
                        <h3 class="text-center">${roundedPoints}</h3>
                    </div>
                    <div class="leaderboard-card__body">
                        <div class="text-center">
                            <img src="${topper_data['avatar_url']}" class="circle-img mb-2" alt="User Img">
                            <h5 class="mb-0">${topper_data['full_name']}</h5>
                            <p class="text-muted mb-0">${topper_data['registration']}</p>
                            <img src="${third_rank}" alt="" class="rank-icon my-3">
                            
                            <hr>
                            <div class="stats d-flex justify-content-around align-items-center my-2">
                                <div class="s-item">
                                    <span class="label">Participation:</span>
                                    <span class="value">${roundedParticipation}%%</span>
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

    if (toppers_data.length == 1) {
        first_rank_card = render_first_rank_card(toppers_data['first'])
        second_rank_card = empty_second_topper_card
        third_rank_card = empty_third_topper_card
    } else if (toppers_data.length == 2) {
        first_rank_card = render_first_rank_card(toppers_data['first'])
        second_rank_card = render_second_rank_card(toppers_data['second'])
        third_rank_card = empty_third_topper_card
    } else if (toppers_data.length == 3) {
        first_rank_card = render_first_rank_card(toppers_data['first'])
        second_rank_card = render_second_rank_card(toppers_data['second'])
        third_rank_card = render_third_rank_card(toppers_data['third'])
    } else {
        first_rank_card = empty_first_topper_card
        second_rank_card = empty_second_topper_card
        third_rank_card = empty_third_topper_card
    }
    let topper_section = `<div class="row">
                                ${first_rank_card}
                                ${second_rank_card}
                                ${third_rank_card}
                          </div>`
    return topper_section
}

function render_ranking_table_rows(rows_data, unranked=false) {
    rows = ''
    for (let row of rows_data) {
        let points = row['classroom_points'];
        let roundedPoints = points.toFixed(2);
        let participation = row['participation'];
        let roundedParticipation = participation.toFixed(2);
        let regularity = row['regularity'];
        let roundedRegularity = regularity.toFixed(2);
        let rankNum
        let rankingClass = ''
        if (unranked) {
            rankNum = row['rank']
            rankingClass = 'unranked'
        } else {
            rankNum = "--"
        }
        
        row_elem = `<tr class="${rankingClass}">
                        <td>
                            <div class="d-flex align-items-center">
                                <img src="${row['avatar_url']}" class="circle-img circle-img--small mr-2" alt="User Img">
                                <div class="user-info__basic">
                                    <h5 class="mb-0">${row['full_name']}</h5>
                                    <p class="text-muted mb-0">${row['registration']}</p>
                                </div>
                            </div>
                        </td>
                        <td>
                            <div class="d-flex align-items-baseline">
                                <h4 class="mr-1">${roundedPoints}</h4>
                            </div>
                        </td>
                        <td>${roundedParticipation}%</td>
                        <td>${roundedRegularity}</td>
                        <td>${rankNum}</td>
                    </tr>`
        rows += row_elem
    }
    return rows
}

function render_table(ranked_students, unranked_students) {
    let ranked_rows = render_ranking_table_rows(ranked_students)
    let unranked_rows = render_ranking_table_rows(unranked_students, unranked=true)
    let table_rows = ranked_rows + unranked_rows
    let ranking_table = `<table class="table">
                            <thead>
                                <tr>
                                    <th>Student</th>
                                    <th>Points</th>
                                    <th>Participation</th>
                                    <th>Regularity</th>
                                    <th>Rank</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${table_rows} 
                            </tbody>
                        </table>`
    return ranking_table
}

function process_ranking_data(response) {
    let data = response['data']
    let toppers_section = render_toppers_section(data['toppers'])
    let table = render_table(data['ranked_students'], data['unranked_students'])
    let container = `<div class="container">
                        ${toppers_section}
                        ${table}
                    </div>`
    $("#leaderboard-container").html(container);
    $("#loader-con").hide(0, ()=>{
        $("##leaderboard-container").show()
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

