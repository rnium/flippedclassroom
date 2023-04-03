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
    let registration = assessment_data['2020338501'];
    let assessment_url = assessment_data['assessment_url'];
    let classtest_score = assessment_data['classtest_score'];
    let attendance_score = assessment_data['attendance_score'];
    let pre_cls_points = assessment_data['pre_cls_points'];
    let in_cls_points = assessment_data['in_cls_points'];
    let post_cls_points = assessment_data['post_cls_points'];

    let preClassScore = convertFloat((pre_cls_points/meta.pre_class_total_points) * meta.pre_class_marks);
    let inClassScore = convertFloat((pre_cls_points/meta.pre_class_total_points) * meta.pre_class_marks);
    let postClassScore = convertFloat((pre_cls_points/meta.pre_class_total_points) * meta.pre_class_marks);
    
    // todo: render the input fields of attendance and classtest fields
    let row = `<tr id="row-aid${assessment_id}">
                    <td>${student_name}</td>
                    <td><a href="${assessment_url}">${registration}</a></td>
                    <td class="inp-con">
                        {% if assessment.attendance_score != None %}
                        <input type="text" id="aid-{{assessment.id}}-attendance-score" class="score-inp attendance-score" data-marks={{assessment.meta.attendance_marks}} data-aid="{{assessment.id}}" value="{{assessment.get_attendance_score}}">
                        {% else %}
                        <input type="text" id="aid-{{assessment.id}}-attendance-score" class="score-inp attendance-score empty" data-marks={{assessment.meta.attendance_marks}} data-aid="{{assessment.id}}">
                        {% endif %}
                    </td>
                    <td class="inp-con">
                    {% if assessment.classtest_score != None %}
                    <input type="text" id="aid-{{assessment.id}}-ct-score" class="score-inp classtest-score" data-marks={{assessment.meta.classtest_marks}} data-aid="{{assessment.id}}" value="{{assessment.get_classtest_score}}">
                    {% else %}
                    <input type="text" id="aid-{{assessment.id}}-ct-score" class="score-inp classtest-score empty" data-marks={{assessment.meta.classtest_marks}} data-aid="{{assessment.id}}">
                    {% endif %}
                    </td>
                    <td>{{assessment.pre_class_score|get_score_or_pending}}</td>
                    <td>{{assessment.in_class_score|get_score_or_pending}}</td>
                    <td>{{assessment.post_class_score|get_score_or_pending}}</td>
                    <td class="{{assessment.total_score|get_total_score_css_class}}">{{assessment.total_score|get_score_or_pending}}</td>
            </tr>`
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
    fetch_assessments_data()
    
    // activate_score_box()
    // $("#a-save-btn").on('click', function(){
    //     let validated = validate_inputs()
    //     if (!validated) {
    //         return;
    //     } else {
    //         let data = processData()
    //         post_data(data)
    //     }
    // })
    // $("#rst-assessment-btn").on('click', function(){
    //     let confirmation = confirm('Are you sure to perform this action? This will reset the current assessment state and metadata!')
    //     if (confirmation) {
    //         delete_meta()
    //     }
    // })

});