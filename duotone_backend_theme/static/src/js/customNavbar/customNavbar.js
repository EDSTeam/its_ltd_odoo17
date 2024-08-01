/** @odoo-module **/

/* Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */


import { patch } from "@web/core/utils/patch";
// import { registry } from "@web/core/registry";
import { NavBar } from "@web/webclient/navbar/navbar";
// import { AppMenu } from "@duotone_backend_theme/js/appMenu/appMenu";
// import { SwitchCompanyMenu } from "@web/webclient/switch_company_menu/switch_company_menu";
// import { UserMenu } from "@web/webclient/user_menu/user_menu";


patch(NavBar.prototype, {
    setup() {
        super.setup();
    },

    _onSbClick: function (evt) {
        this._toggleSideBar($(evt.currentTarget).closest('.wk_duotone_sidebar_panel'));
    },

    _toggleSideBar: function ($o_action_manager) {
        let state = $o_action_manager.hasClass('sidebar_in') ? 'to_collapse' : 'to_rise';
        if (state == 'to_rise') {
            $o_action_manager.removeClass('sidebar_out').addClass('sidebar_in');
            $('.o_action_manager').removeClass('sidebar_out_panel').addClass('sidebar_in_panel');
            this._toggle_fa($o_action_manager.find('.sb_toggler .fa'));
        } else {
            $o_action_manager.removeClass('sidebar_in').addClass('sidebar_out');
            $('.o_action_manager').removeClass('sidebar_in_panel').addClass('sidebar_out_panel');
            this._toggle_fa($o_action_manager.find('.sb_toggler .fa'));
        }
    },

    _toggle_fa: function ($fa) {
        if ($fa.hasClass('fa-angle-right')) {
            $fa.removeClass('fa-angle-right').addClass('fa-angle-left');
        } else {
            $fa.removeClass('fa-angle-left').addClass('fa-angle-right');
        }
    }
});

