$(document).ready(function() {
    $(function(){
        $('.menu .item')
            .tab();
    });
    $(function(){
        $('.ui.checkbox')
            .checkbox()
    });

    $('.viewbook.button').click(function() {
        document.location = $(this).attr('goto');
    });

});
