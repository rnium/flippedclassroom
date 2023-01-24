function adjust_times() {
    let times = $(".time")
    for (let time of times) {
        let time_raw = $(`#${time.id}`).text()
        let date_obj = new Date(time_raw)
        $(`#${time.id}`).text(date_obj.toLocaleString())
    }
}

$(document).ready(function () {
    adjust_times()
});