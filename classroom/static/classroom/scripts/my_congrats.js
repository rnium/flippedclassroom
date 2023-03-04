let notification_count = 1
function congratsNotification(sender_name, dp_url, timeout=10000) {
    let alertid = `notif-${notification_count}`
    notification_count += 1
    let component = `<li id="${alertid}" style="display: none;">
                        <div class="alert-con shadow with-dp">
                        <img src="${dp_url}" class="shadow dp">
                        <div class="alert-info ms-2">${sender_name} has congratulated you on your ranking</div>
                        </div>
                    </li>`
    $("#notification-alert-list").append(component)
    $(`#${alertid}`).show(300, ()=>{
        setTimeout(()=>{
            $(`#${alertid}`).hide(200, ()=>{
                $(`#${alertid}`).remove()
            })
        }, timeout)
    })
}


function showConfetti() {
    var count = 200;
    var defaults = {
    origin: { y: 0.7 }
    };

    function fire(particleRatio, opts) {
    confetti(Object.assign({}, defaults, opts, {
        particleCount: Math.floor(count * particleRatio)
    }));
    }

    fire(0.25, {
    spread: 26,
    startVelocity: 55,
    });
    fire(0.2, {
    spread: 60,
    });
    fire(0.35, {
    spread: 100,
    decay: 0.91,
    scalar: 0.8
    });
    fire(0.1, {
    spread: 120,
    startVelocity: 25,
    decay: 0.92,
    scalar: 1.2
    });
    fire(0.1, {
    spread: 120,
    startVelocity: 45,
    });

}

function showConfetti2(counts=2) {
    var end = Date.now() + (counts * 1000);
    // go Buckeyes!
    var colors = ['#bb0000', '#ffffff'];

    (function frame() {
    confetti({
        particleCount: 2,
        angle: 60,
        spread: 55,
        origin: { x: 0 },
        colors: colors
    });
    confetti({
        particleCount: 2,
        angle: 120,
        spread: 55,
        origin: { x: 1 },
        colors: colors
    });

    if (Date.now() < end) {
        requestAnimationFrame(frame);
    }
    }());
}

function show_full_confetti_sequence(count_congrats) {
    setTimeout(()=>{
        showConfetti()
        setTimeout(()=>{
            showConfetti()
            setTimeout(()=>{
                showConfetti()
                setTimeout(()=>{
                    showConfetti2(count_congrats)
                }, 1200)
            }, 200)
        }, 200)
    }, 300)
}

$("#tst-conf").on('click', ()=>{
    congrats_count = 30
    setTimeout(()=>{
        showConfetti()
        setTimeout(()=>{
            showConfetti()
            setTimeout(()=>{
                showConfetti()
                setTimeout(()=>{
                    showConfetti2(congrats_count)
                }, 1200)
            }, 200)
        }, 200)
    }, 300)
})

function request_and_process_congrats() {
    $.ajax({
        type: "get",
        url: get_congrats_api_url,
        dataType: "json",
        cache: false,
        success: function(response) {
            let congrats = response['congrats']
            if (response['has_congrats']) {
                for (let i = 0; i < response['num_congrats']; i++) {
                    setTimeout(function() {
                        let sender_fullname = congrats[i]['sender_name']
                        let sender_avatar = congrats[i]['sender_avatar']
                        congratsNotification(sender_fullname, sender_avatar)
                    }, i * 200);
                }
                show_full_confetti_sequence()
            }
        },
        error: function(error, xhr, status) {
            console.log(error);
        },
    });
}

request_and_process_congrats()