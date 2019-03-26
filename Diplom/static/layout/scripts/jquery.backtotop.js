jQuery("#totop").click(function () {
    jQuery("body,html").animate({
        scrollTop: 0
    }, 550);
});
jQuery(window).scroll(function () {
    if (jQuery(window).scrollTop() > 200) {
        jQuery("#totop").addClass("visible");
    } else {
        jQuery("#totop").removeClass("visible");
    }
});