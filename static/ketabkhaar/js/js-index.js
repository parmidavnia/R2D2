$(document).ready(function() {
    $(function() {
        $('.special.cards .image').dimmer({
            on: 'hover'
        });

        $('#reading-progress').progress();

        $('.carousel').flickity({
            // options
            cellAlign: 'left',
            wrapAround : true,
            draggable: false,
            // contain: true,
            autoPlay: 4000,
            // imagesLoaded: true,
            percentPosition: false,
        });

        $('#reading-modal')
            .modal('attach events', '.reading-button', 'show')
            .modal('attach events', '#reading-cancel', 'cancel')
        ;
        $('#reading-progress-update').progress({
            label: 'ratio',
            text: {
                ratio: '{value} از {total}'
            }
        });
        $('#inputPageNo').on('input',function(){

            value = parseInt($('#inputPageNo').val());
            console.log('value: ' + value);
            // $('#reading-progress-update').attr('data-value', value);
            $('#reading-progress-update').progress('update progress', value);
        });

    });
});
