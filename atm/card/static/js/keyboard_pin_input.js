/**
 * Created by roman on 04.07.15.
 */
$(document).ready(function(){
    var input = $('#id_pin');

    $('#btn-clear').on('click', function(){
        input.val('');
    });

    $('.btn-number').bind('click', function(event){
        event.preventDefault();
        var digit = $(this).data('value'),
            value = input.val();

        value += digit;
        if (value.length == 4){
            $('.btn-number').attr('disabled', 'disabled')
        }
        input.val(value);
    })
});