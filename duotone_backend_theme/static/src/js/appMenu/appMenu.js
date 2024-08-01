/** @odoo-module **/

import { NavBar } from '@web/webclient/navbar/navbar';
import { session } from "@web/session";
import { url } from "@web/core/utils/urls";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { patch } from "@web/core/utils/patch";
import { computeAppsAndMenuItems } from "@web/webclient/menus/menu_helpers";
import weUtils from "@web_editor/js/common/utils";



patch(NavBar.prototype, {
    setup() {
        super.setup();
        let { apps, menuItems } = computeAppsAndMenuItems(this.menuService.getMenuAsTree("root"));
        let combine_menu_items = apps.concat(menuItems)
        session._searchableMenus = combine_menu_items;
    },
});

patch(Dropdown.prototype, {
    setup() {
        super.setup();
        const style = window.getComputedStyle(document.documentElement);
        const bg_img = weUtils.getCSSVariableValue('bck-img', style);
        if (!(bg_img.includes('None')) && bg_img) {
            this.backgroundImageUrl = url('/web/content/' + bg_img);
        } else {
            this.backgroundImageUrl = '/duotone_backend_theme/static/src/images/default.jpg';
        }
        if ($('.wk_search-results-container').length) {
            $('.result-hover-effect').on('click', $('.o_main_navbar').click());
        }
    },

    onClickSearch() {
        let search_val = $('#appmenu-search-input').val();
        if (!search_val.length) {

            $('.o_app').show();
            $('.wk_search-results-container').hide();
            return;
        }
        $('.o_app').hide();
        $('.wk_search-results-container').show();


        var options = {
            shouldSort: true,
            threshold: 0.6,
            location: 0,
            distance: 100,
            findAllMatches: true,
            maxPatternLength: 32,
            minMatchCharLength: 1,
            keys: [
                "label",
                "parents"
            ]
        };

        search_val = search_val.toLowerCase();
        var fuse = new Fuse(session._searchableMenus, options); // "list" is the item array
        var result = fuse.search(search_val);
        $('.wk_search-results-container').children().empty();
        if (!result.length == 0) {
            $(result).each(function () {
                let path = "#action=" + this.actionID;
                if (this.menuID) {
                    path = path + "&menu_id=" + this.menuID;
                }
                else {
                    path = path + "&menu_id=" + this.id;
                }
                let web_icon;
                if (this.webIconData == undefined) {
                    web_icon = [];
                }
                else {
                    web_icon = "true";
                }
                let src;
                let parent_path;
                if (web_icon.length) {
                    src = 'web/content/ir.ui.menu/' + this.appID + '/web_icon_data';
                }

                //GET http://localhost:8070/undefined 404 (NOT FOUND) => solution
                if (src == undefined) {
                    src = '/';
                }

                if (this.parents == "") {
                    parent_path = '';
                }
                else {
                    parent_path = this.parents + ' / ';
                }
                $('.wk_search-results-container').find('.wk_search-results').append('<a href="' + path + '" class="result-hover-effect"><img src=' + src + ' alt=""/><span class="show">' + parent_path + this.label + '</span></a>');
            });
        }
        else {
            $('.wk_search-results-container').find('.wk_search-results').append('<span>No result for "' + $('#appmenu-search-input').val() + '"</span>');
        }
    }
});

