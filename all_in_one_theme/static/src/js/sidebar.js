/** @odoo-module */

import { NavBar } from "@web/webclient/navbar/navbar";
import { patch } from "@web/core/utils/patch";

patch(NavBar.prototype, {
    
    setup() {
        super.setup(...arguments);
        this.menuService.getMenuAsTree = (menuID) => {
            const menu = this.menuService.getMenu(menuID);
            return menu;
        }
    },

    onToggleMenu(ev) {
        $('.o_main_navbar').toggleClass('o_main_navbar_shown');
    },

    onNavBarMenuSelection(ev) {
        var $target = $(ev.currentTarget);
        if($target.hasClass('has-no-child')) {
            $('ul.o_menu_apps li.dropdown .dropdown-menu .active').removeClass('active');
            $('a.o_menu_brand').empty();
            if($target.hasClass('first_level')) {
                $target.addClass('active');
                // update brand navbar
                $('a.o_menu_brand').append($('<div>'+$target.find('span').text()+'</div>'));
            }
            else if($target.hasClass('second_level')) {
                $target.addClass('active');
                $target.parent().addClass('active');
                $target.parent().parent().prev().addClass('active');
                // update brand navbar
                $('a.o_menu_brand').append($('<div>'+$target.parent().parent().prev().find('span').text()+'</div>'));
                $('a.o_menu_brand').append($('<i class="fa fa-chevron-right"/>'));
                $('a.o_menu_brand').append($('<div>'+$target.find('span').text()+'</div>'));
            }
            else if($target.hasClass('third_level')) {
                $target.addClass('active');
                $target.parent().addClass('active');
                $target.parent().parent().parent().parent().prev().addClass('active');
                // update brand navbar
                $('a.o_menu_brand').append($('<div>'+$target.parent().parent().parent().parent().prev().find('span').text()+'</div>'));
                $('a.o_menu_brand').append($('<i class="fa fa-chevron-right"/>'));
                $('a.o_menu_brand').append($('<div>'+$target.find('span').text()+'</div>'));
            }
            else {
                $target.addClass('active');
                $target.parent().addClass('active');
                $target.parent().parent().parent().parent().parent().parent().prev().addClass('active');
                // update brand navbar
                $('a.o_menu_brand').append($('<div>'+$target.parent().parent().parent().parent().parent().parent().prev().find('span').text()+'</div>'));
                $('a.o_menu_brand').append($('<i class="fa fa-chevron-right"/>'));
                $('a.o_menu_brand').append($('<div>'+$target.find('span').text()+'</div>'));
            }
        }
    }

});