window.onload = function () { 
    $('div.hovcontent').hide();
    $('div.hov').bind('mouseover', function() {
        $('#'+$(this).attr('id')+'rev').fadeIn();
    });
}
