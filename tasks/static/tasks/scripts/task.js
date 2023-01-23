$("#tasktype-group").on("click", ()=>{
    if ($("#tasktype-group").is(':checked')) {
      $("#num-group-member-con").show(100, ()=>{
        $("#num-group-member").focus()
      })
    }
  })

$("#tasktype-indiv").on("click", ()=>{
if ($("#tasktype-indiv").is(':checked')) {
    $("#num-group-member-con").hide(100)
}
})

$("#num-group-member").on('keyup', ()=>{
    let value = $("#num-group-member").val();
    if (value.length > 0) {
        let n = Number(value);
        if (Number.isInteger(n) && n>0) {
            if (value > num_students) {
                $("#num-group-member-error").text('*Not enough students')
                if ($("#num-group-member-error").css('display') == "none") {
                    $("#num-group-member-error").show(100)
                }
            } else {
                if ($("#num-group-member-error").css('display') == "block") {
                    $("#num-group-member-error").hide(100)
                }
            }
            
        } else {
            $("#num-group-member-error").text('*Invalid value')
            if ($("#num-group-member-error").css('display') == "none") {
                $("#num-group-member-error").show(100)
            }
        }
    } else {
        if ($("#num-group-member-error").css('display') == "block") {
            $("#num-group-member-error").hide(100)
        }
    }
})

$(document).ready(function () {
    if ($("#tasktype-group").is(':checked')) {
        $("#num-group-member-con").show(100)
      }
});