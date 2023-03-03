const empty_second_topper_card = `<div class="col-sm-4 second empty">
                                    <div class="leaderboard-card">
                                        <div class="leaderboard-card__top pt-5 pb-3">
                                            
                                        </div>
                                        <div class="leaderboard-card__body">
                                            <div class="text-center">
                                                <img src="../images/blank-dp.svg" class="circle-img mb-2" alt="User Img">
                                                <h5 class="mb-0"></h5>
                                                <p class="text-muted mb-0"></p>
                                                <img src="./img/medals.png" alt="" class="rank-icon my-3">
                                                
                                                <hr>
                                                <!-- <div class="lb-action d-flex justify-content-between align-items-center">
                                                    <span class="leaderboard-info"><img class="lb-icon" src="./img/leaderboard.svg" alt=""><span class="txt">Second Rank</span></span>
                                                    <button class="btn btn-outline-success btn-sm">Congratulate</button>
                                                </div> -->
                                                <div class="info text-muted my-2">Excellence to be achieved</div>
                                                <hr>
                                                <div class="lb-action d-flex justify-content-center align-items-center mt-2">
                                                    <span class="leaderboard-info"><img class="lb-icon" src="./img/leaderboard.svg" alt=""><span class="txt">Reserved Second Rank</span></span>
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
                                                <img src="../images/blank-dp.svg" class="circle-img mb-2" alt="User Img">
                                                <h5 class="mb-0"></h5>
                                                <p class="text-muted mb-0"></p>
                                                <img src="./img/trophy.png" alt="" class="rank-icon my-3">
                                                <hr>
                                                <div class="info text-muted my-2">Excellence to be achieved</div>
                                                <hr>
                                                <div class="lb-action d-flex justify-content-center align-items-center mt-2">
                                                    <span class="leaderboard-info"><img class="lb-icon" src="./img/leaderboard.svg" alt=""><span class="txt">Reserved First Rank</span></span>
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
                                            <img src="../images/blank-dp.svg" class="circle-img mb-2" alt="User Img">
                                            <h5 class="mb-0"></h5>
                                            <p class="text-muted mb-0"></p>
                                            <img src="./img/medals.png" alt="" class="rank-icon my-3">
                                            
                                            <hr>
                                            <!-- <div class="lb-action d-flex justify-content-between align-items-center">
                                                <span class="leaderboard-info"><img class="lb-icon" src="./img/leaderboard.svg" alt=""><span class="txt">Second Rank</span></span>
                                                <button class="btn btn-outline-success btn-sm">Congratulate</button>
                                            </div> -->
                                            <div class="info text-muted my-2">Excellence to be achieved</div>
                                            <hr>
                                            <div class="lb-action d-flex justify-content-center align-items-center mt-2">
                                                <span class="leaderboard-info"><img class="lb-icon" src="./img/leaderboard.svg" alt=""><span class="txt">Reserved Third Rank</span></span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                </div>`

const empty_topper_row = null



function render_toppers_section(toppers_data) {
    if (toppers_data.length == 0) {
        return empty_topper_row
    }
}



function get_ranking_data() {
    $.ajax({
        type: "get",
        url: ranking_api_url,
        dataType: "json",
        cache: false,
        success: function(response) {
            console.log(response);
        },
        error: function(error, xhr, status) {
            console.log(error);
        },
    });
}

get_ranking_data()

