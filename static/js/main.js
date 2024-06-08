$(function () {

    'use strict';

    $('.js-menu-toggle').click(function (e) {

        var $this = $(this);



        if ($('body').hasClass('show-sidebar')) {
            $('body').removeClass('show-sidebar');
            $this.removeClass('active');
        } else {
            $('body').addClass('show-sidebar');
            $this.addClass('active');
        }

        e.preventDefault();

    });

    // click outisde offcanvas
    $(document).mouseup(function (e) {
        var container = $(".sidebar");
        if (!container.is(e.target) && container.has(e.target).length === 0) {
            if ($('body').hasClass('show-sidebar')) {
                $('body').removeClass('show-sidebar');
                $('body').find('.js-menu-toggle').removeClass('active');
            }
        }
    });



});

$(document).ready(function () {
    $(".toggle-sidebar-btn").click(function () {
        $("#sidebar").toggleClass("collapsed");
        $("#content").toggleClass("col-md-12 col-md-9");
        $(".toggle-sidebar-btn i").toggleClass("fa-arrow-right fa-arrow-left");
    });
});