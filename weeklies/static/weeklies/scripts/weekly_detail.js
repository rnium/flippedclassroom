let tabBtns = $(".tab-buttons button")

function clearActives() {
    let btns = $(".tab-buttons button")
    let tabs = $(".tab-body")
    $.each(btns, function (indexInArray, valueOfElement) { 
        $(`#${valueOfElement.id}`).removeClass('active')
    });
    $.each(tabs, function (indexInArray, valueOfElement) { 
        $(`#${valueOfElement.id}`).removeClass('active')
    });
}


$.each(tabBtns, function (indexInArray, valueOfElement) { 
    $(`#${valueOfElement.id}`).on('click', function(){
        clearActives()
        $(this).addClass('active');
        let tab_id = $(this).data('tab_id')
        $(`#${tab_id}`).addClass('active');
    })
});