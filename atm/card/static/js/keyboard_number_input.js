/**
 * Created by roman on 04.07.15.
 */
$(document).ready(function(){
    var input = $('#id_number');

    $('#btn-clear').on('click', function(){
        input.val('');
    });

    $('.btn-number').bind('click', function(event){
        event.preventDefault();
        var digit = $(this).data('value'),
            value = input.val(),
            value_split = value.split('-'),
            last_index = value_split.length - 1;

        if (value_split[last_index].length == 4) {
            value += '-' + digit;
        } else {
            value += digit;
        }
        if (value.length == 19){
            $('.btn-number').attr('disabled', 'disabled')
        }
        input.val(value);
    })
});