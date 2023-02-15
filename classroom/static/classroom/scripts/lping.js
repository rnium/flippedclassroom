function update_stat_data(response) {
    for (let test in response['lt_data']) {
        let issued = response['lt_data'][test]['issued'];
        let submitted = response['lt_data'][test]['submitted'];
        $(`#issued-${test}`).text(issued)
        $(`#submitted-${test}`).text(submitted)
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


function pingLiveTest(test_pks, interval_id) {
    data = {'test_pks':test_pks}
    let payload = JSON.stringify(data)
    $.ajax({
        type: "post",
        url: ping_url,
        dataType: "json",
        contentType: "application/json",
        beforeSend: function(xhr){
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        },
        data: payload,
        cache: false,
        success: function(response) {
            update_stat_data(response)
        },
        error: function() {
            console.log('an error occured');
            clearInterval(interval_id)
        },
    });
}

let live_tests = $(".live_test")
if (live_tests.length > 0) {
    let test_pks = [];
    $.each(live_tests, function (indexInArray, valueOfElement) { 
        test_pks.push($(`#${valueOfElement.id}`).data('testid'))
    });
    interval_id = setInterval(()=>{
        pingLiveTest(test_pks, interval_id)
    }, 2000)
}