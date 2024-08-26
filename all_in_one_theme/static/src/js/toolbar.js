/** @odoo-module */

import { Chatter } from "@mail/core/web/chatter";
import { patch } from "@web/core/utils/patch";
const { onMounted, useRef } = owl;

patch(Chatter.prototype, {
    
    setup() {
        super.setup(...arguments);
        console.log('Get started !!');
        
        onMounted(() => {
            $('.btn_show_toolbar').click(this._onShowToolbar);
            $('.btn_show_notes').click(this._onShowToolbarPanelNotes);
            $('.btn_show_messages').click(this._onShowToolbarPanelMessages);
            $('.btn_show_activities').click(this._onShowToolbarPanelActivities);
            $('.o_toolbar_panel_header_close').click(this._onHideToolbarPanel);
        });
    },

    _onShowToolbar() {
        $('.o_form_view').toggleClass('o_form_view_chatter');
    },

    _onShowToolbarPanel() {
        if ($('.o_Chatter_composer'))
            $('.o_Chatter_composer').remove();
        if ($('.o_topbar_with_toolbar_panel'))
            $('.o_topbar_with_toolbar_panel').remove();
        if ($('.o_container_with_toolbar_panel'))
            $('.o_container_with_toolbar_panel').remove();
        var $topbar_with_toolbar_panel = $('<div class="o_topbar_with_toolbar_panel"/>')
        var $container_with_toolbar_panel = $('<div class="o_container_with_toolbar_panel"/>')
        $topbar_with_toolbar_panel.on('click', () => {
            $('.o_topbar_with_toolbar_panel').remove();
            $('.o_container_with_toolbar_panel').remove();
            $('.o_toolbar').removeClass('invisible');
            $('.o-mail-Chatter').removeClass('show');
            $('.o-mail-Chatter-sidepanel').removeClass('show');
            setTimeout(() => {
                $('.o-mail-Chatter-sidepanel').removeClass('show_notes');
                $('.o-mail-Chatter-sidepanel').removeClass('show_messages');
                $('.o-mail-Chatter-sidepanel').removeClass('show_activities');
            }, 500);
        });
        $container_with_toolbar_panel.on('click', () => {
            $('.o_topbar_with_toolbar_panel').remove();
            $('.o_container_with_toolbar_panel').remove();
            $('.o_toolbar').removeClass('invisible');
            $('.o-mail-Chatter').removeClass('show');
            $('.o-mail-Chatter-sidepanel').removeClass('show');
            setTimeout(() => {
                $('.o-mail-Chatter-sidepanel').removeClass('show_notes');
                $('.o-mail-Chatter-sidepanel').removeClass('show_messages');
                $('.o-mail-Chatter-sidepanel').removeClass('show_activities');
            }, 500);
        });
        $('.o_web_client').prepend($topbar_with_toolbar_panel);
        $('.o_web_client').prepend($container_with_toolbar_panel);
        $('.o_toolbar').addClass('invisible');
        $('.o-mail-Chatter').addClass('show');
        $('.o-mail-Chatter-sidepanel').addClass('show');
    },

    _onShowToolbarPanelNotes() {
        if ($('.o_Chatter_composer'))
            $('.o_Chatter_composer').remove();
        if ($('.o_topbar_with_toolbar_panel'))
            $('.o_topbar_with_toolbar_panel').remove();
        if ($('.o_container_with_toolbar_panel'))
            $('.o_container_with_toolbar_panel').remove();
        var $topbar_with_toolbar_panel = $('<div class="o_topbar_with_toolbar_panel"/>')
        var $container_with_toolbar_panel = $('<div class="o_container_with_toolbar_panel"/>')
        $topbar_with_toolbar_panel.on('click', () => {
            $('.o_topbar_with_toolbar_panel').remove();
            $('.o_container_with_toolbar_panel').remove();
            $('.o_toolbar').removeClass('invisible');
            $('.o-mail-Chatter').removeClass('show');
            $('.o-mail-Chatter-sidepanel').removeClass('show');
            $('.o-mail-Chatter-sidepanel').removeClass('show_notes');
            $('.o-mail-Chatter-sidepanel').removeClass('show_messages');
            $('.o-mail-Chatter-sidepanel').removeClass('show_activities');
        });
        $container_with_toolbar_panel.on('click', () => {
            $('.o_topbar_with_toolbar_panel').remove();
            $('.o_container_with_toolbar_panel').remove();
            $('.o_toolbar').removeClass('invisible');
            $('.o-mail-Chatter').removeClass('show');
            $('.o-mail-Chatter-sidepanel').removeClass('show');
            $('.o-mail-Chatter-sidepanel').removeClass('show_notes');
            $('.o-mail-Chatter-sidepanel').removeClass('show_messages');
            $('.o-mail-Chatter-sidepanel').removeClass('show_activities');
        });
        $('.o_web_client').prepend($topbar_with_toolbar_panel);
        $('.o_web_client').prepend($container_with_toolbar_panel);
        $('.o_toolbar').addClass('invisible');
        $('.o-mail-Chatter').addClass('show');
        $('.o-mail-Chatter-sidepanel').addClass('show show_notes');
    },

    _onShowToolbarPanelMessages() {
        if ($('.o_Chatter_composer'))
            $('.o_Chatter_composer').remove();
        if ($('.o_topbar_with_toolbar_panel'))
            $('.o_topbar_with_toolbar_panel').remove();
        if ($('.o_container_with_toolbar_panel'))
            $('.o_container_with_toolbar_panel').remove();
        var $topbar_with_toolbar_panel = $('<div class="o_topbar_with_toolbar_panel"/>')
        var $container_with_toolbar_panel = $('<div class="o_container_with_toolbar_panel"/>')
        $topbar_with_toolbar_panel.on('click', () => {
            $('.o_topbar_with_toolbar_panel').remove();
            $('.o_container_with_toolbar_panel').remove();
            $('.o_toolbar').removeClass('invisible');
            $('.o-mail-Chatter').removeClass('show');
            $('.o-mail-Chatter-sidepanel').removeClass('show');
            $('.o-mail-Chatter-sidepanel').removeClass('show_notes');
            $('.o-mail-Chatter-sidepanel').removeClass('show_messages');
            $('.o-mail-Chatter-sidepanel').removeClass('show_activities');
        });
        $container_with_toolbar_panel.on('click', () => {
            $('.o_topbar_with_toolbar_panel').remove();
            $('.o_container_with_toolbar_panel').remove();
            $('.o_toolbar').removeClass('invisible');
            $('.o-mail-Chatter').removeClass('show');
            $('.o-mail-Chatter-sidepanel').removeClass('show');
            $('.o-mail-Chatter-sidepanel').removeClass('show_notes');
            $('.o-mail-Chatter-sidepanel').removeClass('show_messages');
            $('.o-mail-Chatter-sidepanel').removeClass('show_activities');
        });
        $('.o_web_client').prepend($topbar_with_toolbar_panel);
        $('.o_web_client').prepend($container_with_toolbar_panel);
        $('.o_toolbar').addClass('invisible');
        $('.o-mail-Chatter').addClass('show');
        $('.o-mail-Chatter-sidepanel').addClass('show');
        $('.o-mail-Chatter-sidepanel').addClass('show show_messages');
    },

    _onShowToolbarPanelActivities() {
        if ($('.o_Chatter_composer'))
            $('.o_Chatter_composer').remove();
        if ($('.o_topbar_with_toolbar_panel'))
            $('.o_topbar_with_toolbar_panel').remove();
        if ($('.o_container_with_toolbar_panel'))
            $('.o_container_with_toolbar_panel').remove();
        var $topbar_with_toolbar_panel = $('<div class="o_topbar_with_toolbar_panel"/>')
        var $container_with_toolbar_panel = $('<div class="o_container_with_toolbar_panel"/>')
        $topbar_with_toolbar_panel.on('click', () => {
            $('.o_topbar_with_toolbar_panel').remove();
            $('.o_container_with_toolbar_panel').remove();
            $('.o_toolbar').removeClass('invisible');
            $('.o-mail-Chatter').removeClass('show');
            $('.o-mail-Chatter-sidepanel').removeClass('show');
            $('.o-mail-Chatter-sidepanel').removeClass('show_notes');
            $('.o-mail-Chatter-sidepanel').removeClass('show_messages');
            $('.o-mail-Chatter-sidepanel').removeClass('show_activities');
        });
        $container_with_toolbar_panel.on('click', () => {
            $('.o_topbar_with_toolbar_panel').remove();
            $('.o_container_with_toolbar_panel').remove();
            $('.o_toolbar').removeClass('invisible');
            $('.o-mail-Chatter').removeClass('show');
            $('.o-mail-Chatter-sidepanel').removeClass('show');
            $('.o-mail-Chatter-sidepanel').removeClass('show_notes');
            $('.o-mail-Chatter-sidepanel').removeClass('show_messages');
            $('.o-mail-Chatter-sidepanel').removeClass('show_activities');
        });
        $('.o_web_client').prepend($topbar_with_toolbar_panel);
        $('.o_web_client').prepend($container_with_toolbar_panel);
        $('.o_toolbar').addClass('invisible');
        $('.o-mail-Chatter').addClass('show');
        $('.o-mail-Chatter-sidepanel').addClass('show show_activities');
    },

    _onHideToolbarPanel() {
        $('.o_topbar_with_toolbar_panel').remove();
        $('.o_container_with_toolbar_panel').remove();
        $('.o_toolbar').removeClass('invisible');
        $('.o-mail-Chatter').removeClass('show');
        $('.o-mail-Chatter-sidepanel').removeClass('show');
        $('.o-mail-Chatter-sidepanel').removeClass('show_notes');
        $('.o-mail-Chatter-sidepanel').removeClass('show_messages');
        $('.o-mail-Chatter-sidepanel').removeClass('show_activities');
    },

});