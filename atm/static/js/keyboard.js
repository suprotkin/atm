/**
 * Created by roman on 04.07.15.
 */
$(document).ready(function() {
    $('#btn-clear').on('click', function(evt){
        $('.btn-number').removeAttr('disabled');
    })
    $('#btn-enter').on('click', function(evt){
        $('form#keyboard_form').submit()
    })
});