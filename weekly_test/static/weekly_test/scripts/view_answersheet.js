function adjust_answercounts() {
    let counter_divs = $(".qno-count");
    let count = 1;
    for (let cd of counter_divs) {
        $(`#${cd.id}`).text(count)
        count += 1
    }
}

$(document).ready(function () {
    adjust_answercounts()
});