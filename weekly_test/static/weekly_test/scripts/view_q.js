function refresh_q_numbers(){
    q_no_containers = $('.qno-count')
    for(let i=0;i<q_no_containers.length;i++){
        elem_id = q_no_containers[i].id
        $(`#${elem_id}`).text(i+1)
    }
}

function refresh_label_leters() {
    mcq_q = $('.qtype-mcq')
    $.each(mcq_q, function (indexInArray1, valueOfElement) {
        q_id = valueOfElement.id
        input_labels = $(`#${q_id} .op-label`)
        $.each(input_labels, function (indexInArray2, valueOfElement) {
            radio_label_id = valueOfElement.id
            label_letter = String.fromCharCode(65+indexInArray2)
            $(`#${radio_label_id}`).text(label_letter)
        })
    })
}


function setup_test_time() {
    let duration_second = duration
    let hours = Math.floor(duration_second / 3600)
    let minutes = Math.floor((duration_second % 3600)/60)
    if (hours==0) {
        $("#duration-hr-container").remove()
    } else {
        $("#duration-hr").text(hours)
    }
    $("#duration-min").text(minutes)
}

$(document).ready(function () {
    refresh_q_numbers()
    refresh_label_leters()
    setup_test_time()
});