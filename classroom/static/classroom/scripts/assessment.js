function check_input(inp_id) {
    inp_selector = `#${inp_id}`
    let score_raw = $(inp_selector).val();
    let marks = $(inp_selector).data('marks');
    if (score_raw.length > 0) {
        let score = Number(score_raw);
        if (isNaN(score)) {
            $(inp_selector).removeClass("empty")
            $(inp_selector).addClass("error")
            return false
        } else {
            if (score > marks) {
                $(inp_selector).removeClass("empty")
                $(inp_selector).addClass("error")
                return false
            } else {
                $(inp_selector).removeClass("error")
                $(inp_selector).removeClass("empty")
                return true
            }
        }
    } else {
        $(inp_selector).removeClass("error")
        $(inp_selector).addClass("empty")
        return null
    }
}

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

function activate_score_box(){
    let inp_fields = $(".score-inp");
    $.each(inp_fields, function (indexInArray, valueOfElement) { 
        $(`#${valueOfElement.id}`).keyup(function(){
            check_input(this.id)
        })
    });
    
}

function validate_inputs() {
    inp_fields = $(".score-inp");
    for (let index = 0; index < inp_fields.length; index++) {
        let element = inp_fields[index].id;
        check_input(element)
    }
    let error_fields = $(".error");
    if (error_fields.length > 0) {
        $(`#${error_fields[0].id}`).focus()
        return false
    } else {
        return true
    }
}


function processData() {
    let inp_fields = $(".score-inp");
    let dataset = {}
    $.each(inp_fields, function (indexInArray, valueOfElement) { 
        let elem_selector = `#${valueOfElement.id}`
        let aid = $(elem_selector).data('aid')
        let value = $(elem_selector).val()
        if (value.length > 0) {
            let score = Number(value);
            if (!isNaN(score)) {
                let is_attendance = $(elem_selector).hasClass('attendance-score');
                let is_classtest = $(elem_selector).hasClass('classtest-score');
                if (!(aid in dataset)) {
                    dataset[aid] = {}
                }
                if (is_attendance) {
                    dataset[aid]['attendance_score'] = score;
                } else if (is_classtest) {
                    dataset[aid]['classtest_score'] = score;
                }
            }
        }
    });
    return dataset
}

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

function processRow(assessment_data, meta) {
    let assessment_id = assessment_data['id'];
    let student_name = assessment_data['student_name'];
    let registration = assessment_data['registration'];
    let assessment_url = assessment_data['assessment_url'];
    let classtest_score = assessment_data['classtest_score'];
    let attendance_score = assessment_data['attendance_score'];
    let pre_cls_points = assessment_data['pre_cls_points'];
    let in_cls_points = assessment_data['in_cls_points'];
    let post_cls_points = assessment_data['post_cls_points'];

    let preclassScoreRaw = (pre_cls_points/meta.pre_class_total_points) * meta.pre_class_marks;
    let inclassScoreRaw = (in_cls_points/meta.in_class_total_points) * meta.in_class_marks;
    let postclassScoreRaw = (post_cls_points/meta.post_class_total_points) * meta.post_class_marks;
    let preClassScore = convertFloat(preclassScoreRaw);
    let inClassScore = convertFloat(inclassScoreRaw);
    let postClassScore = convertFloat(postclassScoreRaw);
    
    // total
    let totalScoreRaw = attendance_score + classtest_score + preclassScoreRaw + inclassScoreRaw + postclassScoreRaw;
    let totalScore = convertFloat(totalScoreRaw)
    
    // todo: render the input fields of attendance and classtest fields
    let atendance_inp = "";
    let total_css_class = "";
    if (!totalScore) {
        total_css_class += "pending"
    }
    if (attendance_score == null) {
        atendance_inp += `<input type="text" id="aid-${assessment_id}-attendance-score" class="score-inp attendance-score empty" data-marks=${meta.attendance_marks} data-aid="${assessment_id}">`
    } else {
        atendance_inp += `<input type="text" id="aid-${assessment_id}-attendance-score" class="score-inp attendance-score" data-marks=${meta.attendance_marks} data-aid="${assessment_id}" value="${attendance_score}">`
    }
    let classtest_inp = "";
    if (classtest_score == null) {
        classtest_inp += `<input type="text" id="aid-${assessment_id}-ct-score" class="score-inp classtest-score empty" data-marks=${meta.classtest_marks} data-aid="${assessment_id}">`
    } else {
        classtest_inp += `<input type="text" id="aid-${assessment_id}-ct-score" class="score-inp classtest-score" data-marks=${meta.classtest_marks} data-aid="${assessment_id}" value="${classtest_score}">`
    }
    let row = `<tr>
                    <td>${student_name}</td>
                    <td><a href="${assessment_url}">${registration}</a></td>
                    <td class="inp-con">
                        ${atendance_inp}
                    </td>
                    <td class="inp-con">
                        ${classtest_inp}
                    </td>
                    <td>${preClassScore}</td>
                    <td>${inClassScore}</td>
                    <td>${postClassScore}</td>
                    <td class="${total_css_class}">${totalScore}</td>
            </tr>`
    $("#assessments-tbody").append(row);
}

function processAssessmentsList(response) {
    const meta = {
        attendance_marks: response['attendance_marks'],
        classtest_marks: response['classtest_marks'],
        pre_class_marks: response['pre_class_marks'],
        in_class_marks: response['in_class_marks'],
        post_class_marks: response['post_class_marks'],
        pre_class_total_points: response['pre_class_total_points'],
        in_class_total_points: response['in_class_total_points'],
        post_class_total_points: response['post_class_total_points'],
    }
    $("#loader-con").hide(0, ()=>{
        $("#assessment-list-con").show(0, ()=>{
            for(assessment_data of response['assessments']) {
                processRow(assessment_data, meta);
            }
            activate_score_box()
            $("#a-save-btn").on('click', function(){
                let validated = validate_inputs()
                if (!validated) {
                    return;
                } else {
                    let data = processData()
                    post_data(data)
                }
            })
            $("#rst-assessment-btn").on('click', function(){
                let confirmation = confirm('Are you sure to perform this action? This will reset the current assessment state and metadata!')
                if (confirmation) {
                    delete_meta()
                }
            })
        })
    })
}

function fetch_assessments_data(data) {
    $.ajax({
        url: assessments_url,
        dataType: "json",
        type: "GET",
        cache: false,
        success: function(response){
            processAssessmentsList(response[0])
        },
        error: function(xhr,status,error){
            alert('something went wrong')
        }
    })
}

function post_data(data) {
    let payload = JSON.stringify(data)
    $.ajax({
        url: update_assessment_url,
        contentType: "application/json",
        type: "POST",
        beforeSend: function(xhr){
            $("#a-save-btn").attr("disabled", true)
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        },
        data: payload,
        cache: false,
        success: function(response){
            let confirmation = confirm("Score saved successfully! reload page?")
            if (confirmation) {
                location.reload()
            }
        },
        error: function(xhr,status,error){
            alert('something went wrong')
        },
        complete: function(){
            $("#a-save-btn").attr("disabled", false)
        }
    })
}


function delete_meta(){
    $.ajax({
        url: delete_assessment_url,
        type: "DELETE",
        beforeSend: function(xhr){
            $("#rst-assessment-btn").attr("disabled", true)
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        },
        cache: false,
        success: function(response){
            location.reload()
        },
        error: function(xhr,status,error){
            alert('something went wrong');
            $("#rst-assessment-btn").attr("disabled", false);
        }
    })
}

$(document).ready(function () {
    let assessment_list = $(".assessment-list");
    if (assessment_list.length > 0) {
        fetch_assessments_data()
    }
});