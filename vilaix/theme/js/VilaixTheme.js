// Main custom JS

$(document).ready(function () {

    $('#portal-globalnav ul.nav li.dropdown').hover(function() {
      $(this).find('.dropdown-menu').stop(true, true).delay(0).fadeIn();
    }, function() {
      $(this).find('.dropdown-menu').stop(true, true).delay(200).fadeOut();
    });

});
