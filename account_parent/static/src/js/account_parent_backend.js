/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { Component, onWillStart, useState } from "@odoo/owl";
import { download } from "@web/core/network/download";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { useSetupAction } from "@web/webclient/actions/action_hook";

function processLine(line) {
    return { ...line, lines: [], isFolded: true };
}

function extractPrintData(lines) {
    const data = [];
    for (const line of lines) {
        const { id, model_id, model, unfoldable, level } = line;
        data.push({
            id: id,
            model_id: model_id,
            model_name: model,
            unfoldable,
            level: level || 1,
        });
        if (!line.isFolded) {
            data.push(...extractPrintData(line.lines));
        }
    }
    return data;
}

export class CoaReport extends Component {
    static template = "account_parent.CoaReport";
    static components = { Layout };

    setup() {
        this.actionService = useService("action");
        this.orm = useService("orm");
        this.user = useService("user");
        onWillStart(this.onWillStart);
        useSetupAction({
            getLocalState: () => ({
                lines: [...this.state.lines],
                heading: this.state.heading,
                applied_filter: this.state.applied_filter,
            }),
        });

        this.state = useState({
            lines: this.props.state?.lines || [],
            heading: this.props.state?.heading || '',
            applied_filter: this.props.state?.applied_filter || false,
        });

        const { active_id, active_model, auto_unfold, context, url } =
            this.props.action.context;
        this.controllerUrl = url;

        this.context = context || {};
        Object.assign(this.context, {
            active_id: active_id || this.props.action.context.active_id,
            auto_unfold: auto_unfold || false,
            active_model: active_model || false,
//            ttype: ttype || false,
        });
        this.display = {
            controlPanel: {},
            searchPanel: false,
        };
    }

    async onWillStart() {
        if (!this.state.lines.length) {
            const report_data = await this.orm.call("account.open.chart", "get_html", [
                this.context,
            ]);
            const mainLines = report_data.lines;
            const heading = report_data.heading;
            const applied_filter = report_data.applied_filter;
            this.state.lines = mainLines.map(processLine);
            this.state.heading = heading;
            this.state.applied_filter = applied_filter;
        }
    }

    async onClickBoundLink(line) {

        const action = await this.orm.call("account.open.chart", "show_journal_items", [
                line.wiz_id, line.id, line.name
            ]);
        this.actionService.doAction(action);
    }

    onClickPrint() {
//        const data = JSON.stringify(extractPrintData(this.state.lines));
        if (!this.controllerUrl){
            throw new Error('CoA Report not loaded');
        }
        const url = this.controllerUrl
            .replace(":active_id", this.context.active_id)
            .replace(":active_model", this.context.active_model)
            .replace("output_format", "pdf");
        download({
            data: {  },
            url,
        });
    }

    onClickXLSPrint() {
    //        const data = JSON.stringify(extractPrintData(this.state.lines));
        if (!this.controllerUrl){
            throw new Error('CoA Report not loaded')
        }

        const url = this.controllerUrl
            .replace(":active_id", this.context.active_id)
            .replace(":active_model", this.context.active_model)
            .replace("output_format", "xls");
        download({
            data: {  },
            url,
        });
    }


    async toggleLine(line) {
        line.isFolded = !line.isFolded;
        if (!line.lines.length) {
            line.lines = (
                await this.orm.call("account.open.chart", "get_lines", [line.wiz_id, line.id], {
                    model_id: line.model_id,
                    model_name: line.model,
                    level: line.level + 1 || 1,
                })
            ).map(processLine);
        }
    }
}

registry.category("actions").add("coa_hierarchy", CoaReport);


//odoo.define('account_parent.coa_hierarchy', function (require) {
//'use strict';
//
//var AbstractAction = require('web.AbstractAction');
//var core = require('web.core');
//var session = require('web.session');
//var CoAWidget = require('account_parent.CoAWidget');
//var framework = require('web.framework');
//
//var QWeb = core.qweb;
//
//var coa_hierarchy = AbstractAction.extend({
//    hasControlPanel: true,
//    // Stores all the parameters of the action.
//    init: function(parent, action) {
//    	this._super.apply(this, arguments);
//        this.actionManager = parent;
//        this.given_context = action.context;//session.user_context;
//        this.controller_url = action.context.url;
//        if (action.context.context) {
//            this.given_context = action.context.context;
//        }
//        this.given_context.auto_unfold = action.context.auto_unfold || false;
//
//    },
//    willStart: function() {
//    	return Promise.all([this._super.apply(this, arguments), this.get_html()]);
//    },
//    set_html: function() {
//        var self = this;
//        var def = Promise.resolve();
//        if (!this.report_widget) {
//            this.report_widget = new CoAWidget(this, this.given_context);
////            def = this.report_widget.appendTo(this.$el);
//            def = this.report_widget.appendTo(this.$('.o_content'));
//        }
//        return def.then(function () {
//            self.report_widget.$el.html(self.html);
//            if (self.given_context.auto_unfold) {
//                _.each(self.$el.find('.fa-caret-right'), function (line) {
//                    self.report_widget.autounfold(line);
//                });
//            }
//        });
//    },
//    start: async function() {
//        const props = this.getControlPanelProps();
//        this.controlPanelProps.cp_content = props;
//        await this._super(...arguments);
//        this.set_html();
//    },
//    getControlPanelProps: function() {
//        return { $buttons: this.$buttons }
//    },
//    // Fetches the html and is previous report.context if any, else create it
//    get_html: async function() {
//        const { html } = await this._rpc({
//                model: 'account.open.chart',
//                method: 'get_html',
//                args: [this.given_context],
//            });
//        this.html = html;
//        this.renderButtons();
//    },
//
//    // Updates the control panel and render the elements that have yet to be rendered
//    update_cp: function() {
//        if (!this.$buttons) {
//            this.renderButtons();
//        }
//        this.controlPanelProps.cp_content = { $buttons: this.$buttons };
//        return this.updateControlPanel();
//    },
//    renderButtons: function() {
//        var self = this;
//        var parent_self = this;
//        this.$buttons = $(QWeb.render("coaReports.buttons", {}));
//        this.$buttons.bind('click', function () {
//        	if (this.id == "coa_export_xls"){
//        		//xls output
//                var self = parent_self,
//                    view = parent_self.getParent();
////                    children = view.getChildren();
//                framework.blockUI();
//                session.get_file({
//                    url: '/account_parent/export/xls',
//                    data: {data: JSON.stringify({
//                        model: view.modelName,
//                        wiz_id: parent_self.given_context['active_id'],
//                    })},
//                    complete: $.unblockUI,
//                    // error: c.rpc_error.bind(c)
//                    error: (error) => self.call('crash_manager', 'rpc_error', error),
//                });
//        	}
//        	else {
//	    		// pdf output
//                var view = parent_self.getParent()
//	            framework.blockUI();
//	            var url_data = parent_self.controller_url.replace('active_id', parent_self.given_context.active_id);//self.given_context.active_id
//	            session.get_file({
//	                url: url_data.replace('output_format', 'pdf'),
//	                data: {data: JSON.stringify({
//                        model: view.modelName,
//                        wiz_id: parent_self.given_context['active_id'],
//                    })},
//	                complete: framework.unblockUI,
//	                // error: crash_manager.rpc_error.bind(crash_manager),
//	                error: (error) => parent_self.call('crash_manager', 'rpc_error', error),
//	            });
//        	}
//        });
//        return this.$buttons;
//    },
////    do_show: function() {
////        this._super();
////        this.update_cp();
////    },
//});
//
//core.action_registry.add("coa_hierarchy", coa_hierarchy);
//return coa_hierarchy;
//});
