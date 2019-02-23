$(function() {
    $('#reading-modal')
        .modal('attach events', '.reading-link', 'show')
        .modal('attach events', '#reading-cancel', 'cancel')
    ;
});