let fileinputs = document.getElementsByClassName("input-img")
for (let i=0;i<fileinputs.length;i++){
    let inputfield = fileinputs[i]
    inputfield.addEventListener("change", function(){
        let filename = inputfield.files.item(0).name
        let filename_container = document.getElementById(`file-of-${inputfield.id}`)
        filename_container.innerText = filename
    })
}

function intialize_stopwatch(endtime) {
    setInterval(function(){
        starttime = new Date().getTime()
        endtime = new Date(endtime).getTime()
        let duration = endtime - starttime
        let hour = Math.floor((duration / (3600*1000)))
        let minute = Math.floor((duration % (3600*1000))/ (60*1000))
        let second = Math.floor((duration % (60*1000)) / 1000)
        if (duration <= 0) {
            $("#time_hr").text('00')
            $("#time_min").text('00')
            $("#time_sec").text('00')
            $('#id_ans-sheet-form').submit()
        } else {
            if (hour<10) {
                hour = `0${hour}`
            }
            if (minute<10) {
                minute = `0${minute}`
            }
            if (second<10) {
                second = `0${second}`
            }
            $("#time_hr").text(hour)
            $("#time_min").text(minute)
            $("#time_sec").text(second)
            if (duration <= 30000) {
                $('#countdown-toggler').addClass('toggler-warning')
            }
        }
    }, 1000)
}

$("#countdown-toggler").on('click', function(){
    $("#id_countdown-container").toggle(10)
    $(this).toggleClass('toggler-minimised')
})

function refresh_q_numbers(){
    q_no_containers = $('.qno-count')
    for(let i=0;i<q_no_containers.length;i++){
        elem_id = q_no_containers[i].id
        $(`#${elem_id}`).text(i+1)
    }
}


function activate_options() {
    mcq_q = $('.qtype-mcq')
    $.each(mcq_q, function (indexInArray, valueOfElement) { 
         q_id = valueOfElement.id
         radio_inputs = $(`#${q_id} input[type="radio"]`)
         $.each(radio_inputs, function (indexInArray, valueOfElement) { 
              input_id = valueOfElement.id
              $(`#${input_id}`).on('click', function(event){
                  q_id_inner = $(this).parent().parent().parent().attr('id')
                  radio_inputs_inner = $(`#${q_id_inner} input[type="radio"]`)
                  $.each(radio_inputs_inner, function (indexInArray, valueOfElement) { 
                       radio_id = valueOfElement.id
                       if (! $(`#${radio_id}`).is(':checked')) {
                           $(`#${radio_id}`).attr('disabled', true)
                       }
                  });
              })
         });
    });

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

refresh_q_numbers()
refresh_label_leters()
activate_options()

$(document).ready(function() {
    const csrftoken = getCookie('csrftoken'); 
    data = {
        'answer_sheet_pk': $('#id_ans_sheet').val()
    }
    $.ajax({
        type: "POST",
        url: "/test/api/issue/",
        data: JSON.stringify(data),
        cache: false,
        dataType: "json",
        contentType: "application/json",
        beforeSend: function(xhr){
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        },
        success: function (response) {
            intialize_stopwatch(response['endtime'])
            $('#id_countdown-container').show(10)
            $('#id_ans-sheet-form').show('normal')
            let duration_second = response['duration']
            let hours = Math.floor(duration_second / 3600)
            let minutes = Math.floor((duration_second % 3600)/60)
            if (hours==0) {
                $("#duration-hr-container").remove()
            } else {
                $("#duration-hr").text(hours)
            }
            $("#duration-min").text(minutes)
        }
    });
 })
