/**
 * Created by roman on 07.07.15.
 */
$(document).ready(function(){
    var input = $('#id_amount');

    $('#btn-clear').on('click', function(){
        input.val('');
    });

    $('.btn-number').bind('click', function(event){
        event.preventDefault();
        var digit = $(this).data('value'),
            value = input.val();

        input.val(value + digit);
    })
});