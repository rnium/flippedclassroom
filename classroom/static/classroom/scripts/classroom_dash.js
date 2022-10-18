function activate_option_btns() {
    op_btns = $('.option-toggle')
    $.each(op_btns, function (indexInArray, valueOfElement) { 
        $(`#${valueOfElement.id}`).on('click', function(){
            op_con = $(this).data('op_con')
            $(`#${op_con}`).toggle(100)
            let all_options = $('.options-container')
            for (let opt of all_options) {
                let op_id = opt.id
                if ( op_id != op_con) {
                    if ($(`#${op_id}`).css('display') != 'none') {
                        $(`#${op_id}`).hide(200)
                    }
                }
            }
        })
    });
}

activate_option_btns()

$('#share-link').on('click', function(){
    navigator.clipboard.writeText(join_link)
    $('#copy-info').show(200)
    setTimeout(function(){
        $('#copy-info').hide(200)
    }, 1200)
})
