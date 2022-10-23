let refresh_option_labels = function(q_id){
    classname = `${q_id}-op-label`
    let op_labels = document.getElementsByClassName(classname)
    let char_id = 65
    for(let i=0;i<op_labels.length;i++){
        elem = op_labels[i]
        $(`#${elem.id}`).text(String.fromCharCode(char_id+i));
    }
};

let refresh_q_numbers = function(){
    q_no_containers = $('.qno-count')
    for(let i=0;i<q_no_containers.length;i++){
        elem_id = q_no_containers[i].id
        $(`#${elem_id}`).text(i+1)
    }
}

let refresh_total_marks = function(){
    qs = $(".q-marks-input")
    let marks = 0;
    for(let i=0;i<qs.length;i++){
        let elem_id = qs[i].id
        let mark_str = $(`#${elem_id}`).val()
        let mark = Number(mark_str)
        if(isNaN(mark) || mark_str.length < 1){
            marks = "--"
            break
        } else {
            marks += mark
        }
    }
    $("#id_marks-count").text(marks)
}


let clear_iscorrect = function(q_id){
    options = $(`#${q_id} .option-text`)
    for(let i=0;i<options.length;i++){
        option_input_id = options[i].id
        $(`#${option_input_id}`).attr("data-iscorrect", "0")
    }
};

let activate_marks_box = function(qid_str){
    $(`#${qid_str} .q-marks-input`).keyup(function(){
        let value = $(this).val();
        if (value.length > 0) {
            let n = Number(value);
            if (isNaN(n)) {
                $(this).addClass("error")
                refresh_total_marks()
            } else {
                $(this).removeClass("error")
                refresh_total_marks()
            }
        } else {
            $(this).removeClass("error")
        }
    })
}

let activate_del_q_btn = function(q_id){
    btn_id = `#q${q_id}-del-option`
    $(btn_id).on("click", function(){
        elem = $(this).parent().parent()
        elem.hide('fast', function(){
            elem.remove()
            refresh_q_numbers()
            refresh_total_marks()
        })
    })
};

let activate_radio = function(qid_str){
    $(`#${qid_str} input[type="radio"]`).unbind().on("change", function(){
        radio_id = $(this).attr("id")
        qid = $(this).parent().parent().parent()[0].id
        if($(`#${radio_id}`).is(":checked")){
            clear_iscorrect(qid)
            op_id = $(`input#${radio_id} ~ input.option-text`)[0].id
            $(`#${op_id}`).attr("data-iscorrect", "1")
        }
    })
};



let activate_option_del_btn = function(qid_str){
    $(`#${qid_str} button.op-del`).click(function(event){
        event.preventDefault()
    });
    $(`#${qid_str} button.op-del`).on("click", function(){
        elem = $(this).parent()
        let q_id_str = $(this).parent().parent().parent().attr('id')
        elem.hide('normal', function(){
            elem.remove()
            refresh_option_labels(q_id_str)
        })
    })
};

let activate_option_adder_btn = function(qid){
    btn_id = `#mcq${qid}-add-option`
    $(btn_id).on("click", function(){
        let q_id_str = $(this).parent().parent().attr('id')
        let options_container = `#${q_id_str}-options-container`
        let classname = `${q_id_str}-op-label`
        let op_labels = document.getElementsByClassName(classname)
        let last_op_id = op_labels[op_labels.length - 1].id
        let q_opid = Number($(`#${last_op_id}`).attr("data-q_opid"))
        let new_op_id = q_opid + 1
        let new_op_letter = String.fromCharCode(65 + op_labels.length)
        option_elem = `<div class="option" id="${q_id_str}-op${new_op_id}-con" style="display: none;">
                            <input type="radio" id="${q_id_str}-op${new_op_id}-radio" name="${q_id_str}-op">
                            <label class="${q_id_str}-op-label" id="${q_id_str}-op${new_op_id}-radio-label" for="${q_id_str}-op${new_op_id}-radio" data-q_opid="${new_op_id}">${new_op_letter}</label>
                            <input type="text" class="option-text" id="${q_id_str}-op${new_op_id}" data-iscorrect="0">
                            <button class="op-del" id="${q_id_str}-op${new_op_id}-del"><i class='bx bx-trash-alt' title="delete option"></i></button>
                        </div>`
        $(options_container).append(option_elem)
        $(`#${q_id_str}-op${new_op_id}-con`).show('fast', function(){
            activate_option_del_btn(q_id_str)
            activate_radio(q_id_str)
            refresh_option_labels(q_id_str)
        })
    })

};


let q_count = 1;
$("button").click(function(event){
    event.preventDefault()
});

activate_marks_box(`qid_${0}`)
activate_option_del_btn(`qid_${0}`)
activate_del_q_btn(0)
activate_radio(`qid_${0}`)
activate_option_adder_btn(0)

// api error hide btn
$("#api-error-hide").on('click', function(){
    $("#api-error-container").hide('fast')
})

// mcq adder
$("#mcq-question-adder").click(function(){
    let options = "";
    for(let o_count=0;o_count<4;o_count++){
        optionletter = String.fromCharCode(65+o_count)
        if (o_count<2) {
            options += `<div class="option" id="qid_${q_count}-op${o_count}-con">
                            <input type="radio" id="qid_${q_count}-op${o_count}-radio" name="qid_${q_count}-op">
                            <label class="qid_${q_count}-op-label" id="qid_${q_count}-op${o_count}-radio-label" for="qid_${q_count}-op${o_count}-radio"  data-q_opid="${o_count}">${optionletter}</label>
                            <input type="text" class="option-text" id="qid_${q_count}-op${o_count}" data-iscorrect="0">
                        </div>`
        } else {
            options += `<div class="option" id="qid_${q_count}-op${o_count}-con">
                            <input type="radio" id="qid_${q_count}-op${o_count}-radio" name="qid_${q_count}-op">
                            <label class="qid_${q_count}-op-label" id="qid_${q_count}-op${o_count}-radio-label"  for="qid_${q_count}-op${o_count}-radio" data-q_opid="${o_count}">${optionletter}</label>
                            <input type="text" class="option-text" id="qid_${q_count}-op${o_count}" data-iscorrect="0">
                            <button class="op-del" id="qid_${q_count}-op${o_count}-del"><i class='bx bx-trash-alt' title="delete option"></i></button>
                        </div>`
        }
    }
    let mcq_elem = `<div class="q qtype-mcq" id="qid_${q_count}" style="display: none;">
                        <div class="q-anchor" id="qid_${q_count}-anchor"></div>
                        <div class="qno-count-container">
                            <div class="qno-count-inner">
                                <div class="label">Question number:&nbsp;</div>
                                <div class="qno-count" id="qid_${q_count}_count">${q_count + 1}</div>
                            </div>
                            <div class="qtype-info">MCQ</div>
                        </div>
                        <div class="meta">
                            <div class="q-title inset-float-textinput">
                                <input type="text" id="qid_${q_count}-title" name="mcq-${q_count}_title">
                                <label for="id_mcq-${q_count}_title">Question statement</label>
                            </div>
                            <div class="q-marks inset-float-textinput">
                                <input type="text" class="q-marks-input" id="qid_${q_count}-marks" name="mcq_${q_count}_marks">
                                <label for="id_mcq-${q_count}-marks">Marks</label>
                            </div>
                        </div>
                        <div class="options-container" id="qid_${q_count}-options-container">
                            ${options}
                        </div>
                        <div class="actions">
                            <button class="add-option" id="mcq${q_count}-add-option" title="Add more options"><i class='bx bx-list-plus me-1'></i><span>Add Option</span></button>
                            <button class="delete-question" id="q${q_count}-del-option" title="Delete MCQ"><i class='bx bxs-trash-alt'></i><span>Delete MCQ</span></button>
                        </div>
                    </div>`;
    $("#id_questions-container").append(mcq_elem)
    $(`#qid_${q_count}`).show('fast')
    refresh_q_numbers()
    $(`button.op-del, button#mcq${q_count}-add-option, button#q${q_count}-del-option`).click(function(event){
        event.preventDefault()
    });
    activate_marks_box(`qid_${q_count}`)
    activate_option_adder_btn(q_count);
    activate_option_del_btn(`qid_${q_count}`);
    activate_radio(`qid_${q_count}`);
    activate_del_q_btn(q_count);
    if(q_count==1){
        setTimeout(function(){
            $("#id_marks-counter-container").hide()
            $("#id_marks-counter-container").css("visibility", 'visible')
            $("#id_marks-counter-container").show("fast")
        }, 2000)
    }
    refresh_total_marks()
    q_count += 1;
});

// descriptive question adder
$("#des-question-adder").click(function(){
    des_q = `<div class="q qtype-descriptive" id="qid_${q_count}" style="display: none;">
                <div class="q-anchor" id="qid_${q_count}-anchor"></div>
                <div class="qno-count-container">
                    <div class="qno-count-inner">
                        <div class="label">Question number:&nbsp;</div>
                        <div class="qno-count" id="qid_${q_count}_count">${q_count + 1}</div>
                    </div>
                    <div class="qtype-info">DESCRIPTIVE</div>
                </div>
                <div class="meta">
                    <div class="q-title inset-float-textinput">
                        <input type="text" id="qid_${q_count}-title" name="qid_${q_count}_title">
                        <label for="qid_${q_count}-title">Question statement</label>
                    </div>
                    <div class="q-marks inset-float-textinput">
                        <input class="q-marks-input" type="text" id="qid_${q_count}-marks" name="qid_${q_count}_marks">
                        <label for="qid_${q_count}-marks">Marks</label>
                    </div>
                </div>
                <div class="actions">
                    <div class="switch">
                        <input type="checkbox" name="" id="qid_${q_count}-switch">
                        <label for="qid_${q_count}-switch"></label>
                        <span>Enable upload image</span>
                    </div>
                    <button class="delete-question" id="q${q_count}-del-option" title="Delete Question"><i class='bx bxs-trash-alt'></i><span>Delete Question</span></button>
                </div>
            </div>`
    $("#id_questions-container").append(des_q)
    $(`#qid_${q_count}`).show('fast')
    refresh_q_numbers()
    activate_marks_box(`qid_${q_count}`)
    $(`button#q${q_count}-del-option`).click(function(event){
        event.preventDefault()
    });
    activate_del_q_btn(q_count)
    if(q_count==1){
        setTimeout(function(){
            $("#id_marks-counter-container").hide()
            $("#id_marks-counter-container").css("visibility", 'visible')
            $("#id_marks-counter-container").show("fast")
        }, 2000)
    }
    refresh_total_marks()
    q_count += 1;
});


// checking positive integer
$('#id_test-time').keyup(function(){
    let value = $("#id_test-time").val();
    if (value.length > 0) {
        let n = Number(value);
        if (Number.isInteger(n) && n>0) {
            $("#id_time-error_info").css("visibility", "hidden")
            $("#id_test-time").removeClass("error")
        } else {
            $("#id_time-error_info").css("visibility", "visible")
            $("#id_test-time").addClass("error")
        }
    } else {
        $("#id_time-error_info").css("visibility", "hidden")
        $("#id_test-time").removeClass("error")
    }
});

function validate_datetime() {
    let date_raw = $("#test-schedule").val()
    if (date_raw.length == 0) {
        return false
    }
    let deadline = new Date(date_raw).getTime()
    let timenow = new Date().getTime()
    if (deadline < timenow) {
        $("#error-msg").show(100)
        return false
    } else {
        $("#error-msg").hide(100)
        return true
    }
}

$("#test-schedule").on('change', validate_datetime)

// data processing and validation

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


function showError(msg, timeOut=5) {
    $("#api-error-info").text(msg)
    $("#api-error-container").show('fast', function(){
        setTimeout(function(){
            $("#api-error-container").hide('fast')
        }, timeOut*1000)
    })
}

function checkEmptyFields() {
    let textinputs = $(`input[type="text"]`)
    for (let inp_field of textinputs) {
        if (inp_field.classList.contains("form-control")) {
            console.log('date');
            continue
        }
        let textinput_id = inp_field.id
        if($(`#${textinput_id}`).val().length == 0){
            showError("Fill all the fields")
            $(`#${textinput_id}`).focus()
            return false
        }
    }
    return true
}

function checkMcq() {
    mcq_list = $('.qtype-mcq')
    for(let i=0;i<mcq_list.length;i++){
        let q_id = mcq_list[i].id
        q_options = $(`#${q_id} .option-text`)
        is_correct_true_values = []
        for(let j=0;j<q_options.length;j++){
            let opId = q_options[j].id
            let op_isCorrect = $(`#${opId}-radio`).is(':checked')
            if (op_isCorrect) {
                is_correct_true_values.push(op_isCorrect)
            }
        }
        if (is_correct_true_values.length == 0) {
            showError("please select an option of the mcq as the correct answer")
            $(`#${q_id}`).addClass('mcq-error')
            let qid_anchor = document.getElementById(`${q_id}-anchor`);
            qid_anchor.scrollIntoView({behavior: 'smooth'}, true);
            setTimeout(function(){
                $(`#${q_id}`).removeClass('mcq-error')
            }, 10000)
            return false
        } else if (is_correct_true_values.length > 1) {
            showError("Multiple option selected of the mcq as the correct answer")
            $(`#${q_id}`).addClass('mcq-error')
            let qid_anchor = document.getElementById(`${q_id}-anchor`);
            qid_anchor.scrollIntoView({behavior: 'smooth'}, true);
            setTimeout(function(){
                $(`#${q_id}`).removeClass('mcq-error')
            }, 10000)
            return false
        }
    }
    return true
}


function checkErrorFields() {
    let fields = $("input.error")
    if(fields.length>0){
        for(let i=0;i<fields.length;i++){
            let field_id = fields[i].id
            showError("Please correct errors")
            $(`#${field_id}`).focus()
            return false
        }
    } else {
        return true
    }
}


function processData() {
    let data = {}
    let testinfo = {
        'title':$("#id_test-title").val(),
        'info':$("#id_test-desc").val(),
        'duration_seconds': Number($("#id_test-time").val()) * 60,
        'schedule': $("#test-schedule").val()
    }
    data['test'] = testinfo
    questions = $(".q")
    questions_data = []
    if (questions.length<1) {
        showError("Test must contain a question")
        return false
    }
    for (let i=0;i<questions.length;i++) {
        let q_id = questions[i].id
        q_data_unit = {}
        let q_Metadata = {
            'statement': $(`#${q_id}-title`).val(),
            'marks': Number($(`#${q_id}-marks`).val())
        }
        if ($(`#${q_id}`).hasClass('qtype-mcq')){
            q_Metadata['is_descriptive'] = false
            q_Metadata['ans_as_img'] = false
            q_data_unit['meta'] = q_Metadata
            let q_options = $(`#${q_id} .option-text`)
            let options_data = []
            if (q_options.length<2) {
                showError("MCQ must have two options")
            } else {
                for (let i=0;i<q_options.length;i++) {
                    opId = q_options[i].id
                    op_data = {
                        'id': Number($(`#${opId}-radio-label`).attr('data-q_opid')),
                        'option_text': $(`#${opId}`).val()
                    }
                    op_data["is_correct"] = $(`#${opId}-radio`).is(':checked')
                    options_data.push(op_data)
                }
                q_data_unit['options'] = options_data
            }
        } else {
            q_Metadata['is_descriptive'] = true
            q_Metadata['ans_as_img'] = $(`#${q_id}-switch`).is(':checked')
            q_data_unit['meta'] = q_Metadata
        }
        questions_data.push(q_data_unit)
    }
    data['questions'] = questions_data
    return data
}


$("#id_create_q_button").on('click', function(){
    let isNoError;
    let isAllFilled;
    let is_all_mcq_valid;
    try {
        isNoError = checkErrorFields()
        isAllFilled = checkEmptyFields()
        if (isNoError && isAllFilled) {
            is_all_mcq_valid = checkMcq()
        }
    } catch(err) {
        showError(err.message)
        return null
    }
    let is_valid_date = validate_datetime()
    if (is_valid_date == false) {
        $(".form-control").focus()
        showError("Select valid date and time")
        return null
    }
    if (isNoError && isAllFilled && is_all_mcq_valid) {
        $("#id_create_q_loader").show()
        let data
        try {
            data_obj = processData()
            if (data_obj==false) {
                $("#id_create_q_loader").hide()
                return null
            }
            data = JSON.stringify(data_obj)
        } catch(err) {
            showError(err.message)
            $("#id_create_q_loader").hide()
            return null
        }
        $.ajax({
            url: create_test_url,
            contentType: "application/json",
            type: "POST",
            beforeSend: function(xhr){
                $("#id_create_q_button").attr("disabled", "")
                $("#id_create_q_button").addClass("disabled-btn")
                $("#mcq-question-adder").hide()
                $("#des-question-adder").hide()
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            },
            data: data,
            cache: false,
            dataType: "json",
            success: function(){
                console.log("success")
            },
            error: function(xhr,status,error){
                showError(`error: ${xhr.responseText}`, 60)
                $("#id_create_q_button").removeAttr("disabled")
                $("#id_create_q_button").removeClass("disabled-btn")
                $("#mcq-question-adder").show()
                $("#des-question-adder").show()
            },
            complete: function(){
                $("#id_create_q_loader").hide()
            }
        })
    }
})
