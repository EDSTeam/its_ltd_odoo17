/** @odoo-module **/

// import publicWidget from "@web/legacy/js/public/public_widget";


import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onMounted } from "@odoo/owl";
import { jsonrpc } from "@web/core/network/rpc_service";
import weUtils from "@web_editor/js/common/utils";


export class DuotoneMenu extends Component {
    setup() {
        this.isUserAdmin = useService("user").isAdmin;
        this.orm = useService("orm");
        this.append_font = false;
        
        onMounted(() => {
            // var self = this;
            this.$el = $('#cog-accordian');
            this.reloadpage = $('.reload-page');
            this.reloadpage.css({'color':'green','cursor':'not-allowed'})
            const style = window.getComputedStyle(document.documentElement);
            let wk_range = this.$el.find('input[type=range]');
            let wk_font = this.$el.find('#wk_fontCollapse a');
            let wk_bg_img = this.$el.find('#wk_BackgroundImageCollapse .wk-cog-img');
            let wk_fore_color = this.$el.find('#wk_foregoundColorCollapse span');
            let wk_back_color = this.$el.find('#wk_backgroundColorCollapse span');
            let wk_input_fore_color = this.$el.find('#wk_foregoundColorCollapse input[type=color]');
            let wk_input_back_color = this.$el.find('#wk_backgroundColorCollapse input[type=color]');
            const googleFontsProperty = weUtils.getCSSVariableValue('google-fonts', style);
            const ActiveFontsProperty = weUtils.getCSSVariableValue('active-font', style);
            this.googleFonts = googleFontsProperty ? googleFontsProperty.split(/\s*,\s*/g) : [];
            this.googleFonts = this.googleFonts.map(font => font.substring(1, font.length - 1));
            this.active_font = ActiveFontsProperty ? ActiveFontsProperty.split(/\s*,\s*/g) : [];
            this.active_font = this.active_font.map(font => font.substring(1, font.length - 1));
            jsonrpc('/theme/data', {
                'url': '/duotone_backend_theme/static/src/scss/customized/dynamic_variables.scss'
            })
                .then(function (result) {
                    // Transparency
                    let opacity = [0, 1, .9, .8, .7, .6, .5, .4, .3, .2, .1];
                    let transparency = opacity.indexOf(parseFloat(result.opacity));
                    wk_range.attr('value', transparency);
                    wk_range.next().text(transparency);

                    // Font
                    let font = result.font.slice(1, -1);
                    wk_font.each(function () {
                        if ($(this).text().split(' ').join('') == font) {
                            $(this).addClass('active');
                        }
                    });

                    // Background Image
                    
                    if (result.bck_img == 'None' || result.bck_img == null) {
                       
                        wk_bg_img.attr('src', `/duotone_backend_theme/static/src/images/default.jpg`);
                    } 
                    else {
                        wk_bg_img.attr('src', `/web/content/${result.bck_img}`);
                    }

                    // Foreground Color
                    wk_fore_color.each(function (i, f_color) {
                        if ($(f_color).data('color') == result.foreground_color) {
                            $(f_color).addClass('active');
                        }
                    });

                    // Background Color
                    wk_back_color.each(function (i, b_color) {
                        if ($(b_color).data('color') == result.background_color) {
                            $(b_color).addClass('active');
                        }
                    });

                    // Input Colors
                    wk_input_fore_color.attr('value', result.foreground_color);
                    wk_input_back_color.attr('value', result.background_color);
                });
        });
        
    }

    _reloadPage(ev){
        var $el = $(ev.currentTarget);
        if($el.hasClass('reloadMe')){
            location.reload(true);
        }
    }
    _get_file (files) {
                    var file = $.find(files, function (file) {
                        var baseURL = '/duotone_backend_theme/static/src/scss/customized';
                        return file.url === $.str.sprintf('%s/dynamic_variables.scss', baseURL);
                    });
                    return file;
                }
    _openConfigPanel(ev){
        $("#wk_cog-dropdown").modal('show').bind('this')
        
    }
    _toggle_active($target){
        $target.closest('.card-body').find('.active').removeClass('active');
        $target.find('span').addClass('active')
    }

    _set_foreground_color(ev){
        this._toggle_active($(ev.currentTarget));
        let color = $(ev.target).data('color');
        this.change_theme('foreground_color', color);
    }
    _set_background_color (evt) {
                    this._toggle_active($(evt.currentTarget));
                    let color = $(evt.target).data('color');
                    this.change_theme('background_color', color);
                }

    _set_foreground_input_color (evt) {
                    let color = evt.target.value;
                    this.change_theme('foreground_color', color);
                }

    change_theme(key, value, callback = false, google_fonts = false) {
        var self = this;
        var url = '/duotone_backend_theme/static/src/scss/customized/dynamic_variables.scss';
        jsonrpc('/theme/backend/make_scss_custo', {
            'url': url,
            'key': key,
            'value': value,
            'google_fonts': google_fonts,
        }).then(function () {
            jsonrpc('/backend/theme_customize', {
                'get_bundle': true,
            }).then(function (bundles) {
                var $allLinks = $();
                var defs = $.map(bundles, function (bundleURLs, bundleName) {
                    var $links = $('link[href*="' + bundleName + '"]');
                    $allLinks = $allLinks.add($links);
                    var $newLinks = $();
                    $.each(bundleURLs, function (url) {
                        $newLinks = $newLinks.add($('<link/>', {
                            type: 'text/css',
                            rel: 'stylesheet',
                            href: url,
                        }));
                    });

                    var linksLoaded = new Promise(function (resolve, reject) {
                        var nbLoaded = 0;
                        $newLinks.on('load', function () {
                            if (++nbLoaded >= $newLinks.length) {
                                resolve();
                            }
                        });
                        $newLinks.on('error', function () {
                            reject();
                            window.location.hash = 'theme=true';
                            window.location.reload();
                        });
                    });
                    $links.last().after($newLinks);
                    return linksLoaded;
                });
                return Promise.all(defs).then(function () {
                    if (callback) {
                        callback();
                    }
                    $allLinks.remove();
                }).catch(function () {
                    if (callback) {
                        callback();
                    }
                    $allLinks.remove();
                });
            })
        });
        this.reloadpage.addClass("reloadMe")
    }

    _set_font (evt) {
                    let $target = $(evt.target);
                    $target.closest('.card-body').find('.active').removeClass('active');
                    $target.addClass('active');
                    let font = $(evt.target).attr('data-font');
                    this.change_theme('font', font);
                }
                
                _set_foreground_input_color (evt) {
                    let color = evt.target.value;
                    this.change_theme('foreground_color', color);
                }
                
                _set_background_input_color (evt) {
                    let color = evt.target.value;
                    this.change_theme('background_color', color);
                }
                _set_transparency (evt) {
                    let $target = $(evt.currentTarget);
                    $target.siblings('.wk-range').text(evt.target.value);
                    let transparency = evt.target.value;
                    let opacity = [0, 1, .9, .8, .7, .6, .5, .4, .3, .2, .1];
                    transparency = opacity[transparency];
                    this.change_theme('opacity', transparency);
                }
                _remove_background_image (evt) {
                    var self = this;
                    return jsonrpc('/duotone/remove/image',{}).then(function (result) {
                        self.change_theme('bck_img', null, self._set_default_image($(evt.currentTarget)));
                    });
                }
                _set_browse_background_image (evt) {
                    let $target = $(evt.currentTarget);
                    var self = this;
                    const file = evt.target.files[0];
                    var name = ''
                    if (file){
                        name = evt.target.files[0].name;
                    }
                    var reader = new FileReader();
                    reader.addEventListener("load", function () {
                        var data = reader.result;
                        return jsonrpc('/create/image',{
                                'data': data,
                                'name': name
                            }).then(function (result) {
                            $target.closest('.card-body').find('.wk-cog-img').attr('src', `/web/content/${result.id}`);
                            self.change_theme('bck_img', result.id);
                        });
                    }, false);
                    if (file) {
                        reader.readAsDataURL(file);
                    }
                }
                _set_button (evt) {
                    let $target = $(evt.target);
                    let button_type = $target.data('btn_type');
                    this.change_theme('button_type', button_type);
                }

                _delete_google_font (ev) {
                    var parent_div = $(ev.currentTarget);
                    var remove_font = parent_div.prev().children().attr('data-font');
                    let google_fonts;
                    var google_font_obj = this.googleFonts;
                    const index = google_font_obj.indexOf(remove_font.replace(/['"]+/g, ''));
                    if (index > -1) { // only splice array when item is found
                        google_font_obj.splice(index, 1); // 2nd parameter means remove one item only
                    }
                    if (google_font_obj.length) {
                        google_fonts = "('" + google_font_obj.join("', '") + "')";
                    } else {
                        google_fonts = 'null';
                    }
                    if (parent_div.prev().children().hasClass('active')) {
                        this.change_theme('font', `'Roboto'`, false, google_fonts);
                        $('#wk_fontCollapse > div').find('a:first').children().addClass('active');
                    }
                    else {
                        const temp_style = window.getComputedStyle(document.documentElement);
                        const active_font = weUtils.getCSSVariableValue('active-font', temp_style);
                        this.change_theme('font', active_font, false, google_fonts);
                    }
                    parent_div.parent().remove();
                    ev.stopPropagation();
                }

                _append_google_fonts (ev) {
                    var self = this;
                    $('#google_font_input_field').val('');
                    let available_google_fonts = this.googleFonts;
                    var active_font = this.active_font;
                    if (available_google_fonts && !this.append_font) {
                        $(available_google_fonts).each(function (index, font) {
                            if (font == active_font[0]) {
                                $('#wk_fontCollapse').find('.card-body').append($('<div><a><span class="active" data-font="'+`'${font}'`+'" style="font-family:'+font+'">'+font+'</span></a> <i class="fa fa-trash google_font_trash"></i></div>'))
                            }
                            else {
                                $('#wk_fontCollapse').find('.card-body').append($('<div><a><span data-font="'+`'${font}'`+'" style="font-family:'+font+'">'+font+'</span></a> <i class="fa fa-trash google_font_trash"></i></div>'))
                            }
                            $('.google_font_trash').on('click', self._delete_google_font.bind(self))
                        });
                        this.append_font = true;
                    }
                }
                
                            _onGoogleFontsCustoDuotoneRequest (val) {
                                var self = this;
                                const values = val.values;
                                const googleFonts = val.googleFonts;
                    
                                if (googleFonts.length) {
                                    values['google-fonts'] = "('" + googleFonts.join("', '") + "')";
                                } else {
                                    values['google-fonts'] = 'null';
                                }
                                self.change_theme('font', values.font, false, values['google-fonts']);
                            }
                            async _apply_google_font (ev) {
                                var self = this;
                                const font_url = $(ev.currentTarget).prev().val();
                                if (font_url) {
                                    let m = font_url.match(/\bspecimen\/([\w+]+)/);
                                    if (!m) {
                                        // if embed code (so that it works anyway if the user put the embed code instead of the page link)
                                        m = font_url.match(/\bfamily=([\w+]+)/);
                                        if (!m) {
                                            $(ev.currentTarget).prev().addClass('wrong_font');
                                            return;
                                        }
                                    }
                                    let isValidFamily = false;
                                    try {
                                        const result = await fetch("https://fonts.googleapis.com/css?family=" + m[1] + ':300,300i,400,400i,700,700i', { method: 'HEAD' });
                                        // Google fonts server returns a 400 status code if family is not valid.
                                        if (result.ok) {
                                            isValidFamily = true;
                                        }
                                    } catch (error) {
                                        console.error(error);
                                    }
                    
                                    if (!isValidFamily) {
                                        $('#google_font_input_field').addClass('wrong_font');
                                        return;
                                    }
                                    $('#google_font_input_field').removeClass('wrong_font');
                                    const font = m[1].replace(/\+/g, ' ');
                                    
                                    if (!(self.googleFonts).includes(font)) {
                    
                                        self.googleFonts.push(font)
                                        $('#wk_fontCollapse > div.card-body').find('.active').removeClass('active');
                                        $('#wk_fontCollapse').find('.card-body').append($('<div><a><span class="active" data-font="'+`'${font}'`+'" style="font-family:'+font+'">'+font+'</span></a> <i class="fa fa-trash google_font_trash"></i></div>'))
                                        var font_data = { values: { ["font"]: `'${font}'` }, googleFonts: self.googleFonts, }
                                        $('#google_font_input_field').val('')
                                        self._onGoogleFontsCustoDuotoneRequest(font_data)
                                    }
                                }
                            }
                    
                    
                            _set_default_image ($target) {
                                $target.closest('.card-body').find('.wk-cog-img').attr('src', '/duotone_backend_theme/static/src/images/default.jpg');
                            }
                            _get_content (key, value, updatedFileContent) {
                                var pattern = $.str.sprintf("'%s': %%s,\n", key);
                                var regex = new RegExp($.str.sprintf(pattern, ".+"));
                                var replacement = $.str.sprintf(pattern, value);
                                if (regex.test(updatedFileContent)) {
                                    updatedFileContent = updatedFileContent
                                        .replace(regex, replacement);
                                } else {
                                    updatedFileContent = updatedFileContent
                                        .replace(/( *)(.*hook.*)/, $.str.sprintf('$1%s$1$2', replacement));
                                }
                                return updatedFileContent;
                            }
                            _get_updated_file_content (data, key, value) {
                                var self = this;
                                var file = self._get_file(data.scss[1][1]);
                                var updatedFileContent = file.arch;
                                updatedFileContent = self._get_content(key, value, updatedFileContent);
                                return {
                                    'updatedFileContent': updatedFileContent,
                                    'file': file
                                }
                            }
}

DuotoneMenu.template = "duotone_backend_theme.CogSlider";

export const systrayItem = {
    Component: DuotoneMenu,
};
registry.category("systray").add("duotone_backend_theme.CogSlider", systrayItem, { sequence: 0 });





// odoo.define('duotone_backend_theme.duotone_theme_customize_settings', function (require) {
//     'use strict';

//     var core = require('web.core');
//     var ajax = require('web.ajax');
//     var rpc = require('web.rpc');
//     var SystrayMenu = require('web.SystrayMenu');
//     var Widget = require('web.Widget');
//     var QWeb = core.qweb;
//     var session = require('web.session');
//     const weUtils = require('web_editor.utils');
//     var CogSlider = Widget.extend({
//         template: 'CogSlider',
//         events: {
//             "click #wk_foregoundColorCollapse a": '_set_foreground_color',
//             "change #wk_foregoundColorCollapse input": '_set_foreground_input_color',
//             "click #wk_backgroundColorCollapse a": '_set_background_color',
//             "change #wk_backgroundColorCollapse input": '_set_background_input_color',
//             "click #wk_fontCollapse a": '_set_font',
//             "click #wk_BackgroundImageCollapse .fa-remove": '_remove_background_image',
//             "change #wk_BackgroundImageCollapse input": '_set_browse_background_image',
//             "change #wk_bgtransparency input": '_set_transparency',
//             "click #wk_buttonCollapse .btn": '_set_button',
//             "click #google_font_add_button": '_apply_google_font',
//             "click .google_font_trash": '_delete_google_font',
//             "click #wk_fonts": '_append_google_fonts',
//         },
//         init () {
//             this._is_admin = session.is_system;
//             this.append_font = false;
//         },
//         _get_file (files) {
//             var file = $.find(files, function (file) {
//                 var baseURL = '/duotone_backend_theme/static/src/scss/customized';
//                 return file.url === $.str.sprintf('%s/dynamic_variables.scss', baseURL);
//             });
//             return file;
//         },
//         start () {
//             var self = this;
//             const style = window.getComputedStyle(document.documentElement);
//             let wk_range = this.$el.find('input[type=range]');
//             let wk_font = this.$el.find('#wk_fontCollapse a');
//             let wk_bg_img = this.$el.find('#wk_BackgroundImageCollapse .wk-cog-img');
//             let wk_fore_color = this.$el.find('#wk_foregoundColorCollapse span');
//             let wk_back_color = this.$el.find('#wk_backgroundColorCollapse span');
//             let wk_input_fore_color = this.$el.find('#wk_foregoundColorCollapse input[type=color]');
//             let wk_input_back_color = this.$el.find('#wk_backgroundColorCollapse input[type=color]');
//             const googleFontsProperty = weUtils.getCSSVariableValue('google-fonts', style);
//             const ActiveFontsProperty = weUtils.getCSSVariableValue('active-font', style);
//             this.googleFonts = googleFontsProperty ? googleFontsProperty.split(/\s*,\s*/g) : [];
//             this.googleFonts = this.googleFonts.map(font => font.substring(1, font.length - 1));
//             this.active_font = ActiveFontsProperty ? ActiveFontsProperty.split(/\s*,\s*/g) : [];
//             this.active_font = this.active_font.map(font => font.substring(1, font.length - 1));
//             ajax.jsonrpc('/theme/data', 'call', {
//                 'url': '/duotone_backend_theme/static/src/scss/customized/dynamic_variables.scss'
//             })
//                 .then(function (result) {
//                     // Transparency
//                     let opacity = [0, 1, .9, .8, .7, .6, .5, .4, .3, .2, .1];
//                     let transparency = opacity.indexOf(parseFloat(result.opacity));
//                     wk_range.attr('value', transparency);
//                     wk_range.next().text(transparency);

//                     // Font
//                     let font = result.font.slice(1, -1);
//                     wk_font.each(function () {
//                         if ($(this).text().split(' ').join('') == font) {
//                             $(this).addClass('active');
//                         }
//                     });

//                     // Background Image
                    
//                     if (result.bck_img == 'None' || result.bck_img == null) {
                       
//                         wk_bg_img.attr('src', `/duotone_backend_theme/static/src/images/default.jpg`);
//                     } 
//                     else {
//                         wk_bg_img.attr('src', `/web/content/${result.bck_img}`);
//                     }

//                     // Foreground Color
//                     wk_fore_color.each(function (i, f_color) {
//                         if ($(f_color).data('color') == result.foreground_color) {
//                             $(f_color).addClass('active');
//                         }
//                     });

//                     // Background Color
//                     wk_back_color.each(function (i, b_color) {
//                         if ($(b_color).data('color') == result.background_color) {
//                             $(b_color).addClass('active');
//                         }
//                     });

//                     // Input Colors
//                     wk_input_fore_color.attr('value', result.foreground_color);
//                     wk_input_back_color.attr('value', result.background_color);
//                 });
//         },
         
//         _append_google_fonts (ev) {
//             $('#google_font_input_field').val('');
//             let available_google_fonts = this.googleFonts;
//             var active_font = this.active_font;
//             if (available_google_fonts && !this.append_font) {
//                 $(available_google_fonts).each(function (index, font) {
//                     if (font == active_font[0]) {
//                         $('#wk_fontCollapse').find('.card-body').append($('<div><a><span class="active" data-font="'+`'${font}'`+'" style="font-family:'+font+'">'+font+'</span></a> <i class="fa fa-trash google_font_trash"></i></div>'))
//                     }
//                     else {
//                         $('#wk_fontCollapse').find('.card-body').append($('<div><a><span data-font="'+`'${font}'`+'" style="font-family:'+font+'">'+font+'</span></a> <i class="fa fa-trash google_font_trash"></i></div>'))
//                     }
//                 });
//                 this.append_font = true;
//             }
//         },
//         _delete_google_font (ev) {
//             var parent_div = $(ev.currentTarget);
//             var remove_font = parent_div.prev().children().attr('data-font');
//             let google_fonts;
//             var google_font_obj = this.googleFonts;
//             const index = google_font_obj.indexOf(remove_font.replace(/['"]+/g, ''));
//             if (index > -1) { // only splice array when item is found
//                 google_font_obj.splice(index, 1); // 2nd parameter means remove one item only
//             }
//             if (google_font_obj.length) {
//                 google_fonts = "('" + google_font_obj.join("', '") + "')";
//             } else {
//                 google_fonts = 'null';
//             }
//             if (parent_div.prev().children().hasClass('active')) {
//                 this.change_theme('font', `'Roboto'`, false, google_fonts);
//                 $('#wk_fontCollapse > div').find('a:first').children().addClass('active');
//             }
//             else {
//                 const temp_style = window.getComputedStyle(document.documentElement);
//                 const active_font = weUtils.getCSSVariableValue('active-font', temp_style);
//                 this.change_theme('font', active_font, false, google_fonts);
//             }
//             parent_div.parent().remove();
//             ev.stopPropagation();
//         },
//         _onGoogleFontsCustoDuotoneRequest (val) {
//             var self = this;
//             const values = val.values;
//             const googleFonts = val.googleFonts;

//             if (googleFonts.length) {
//                 values['google-fonts'] = "('" + googleFonts.join("', '") + "')";
//             } else {
//                 values['google-fonts'] = 'null';
//             }
//             self.change_theme('font', values.font, false, values['google-fonts']);
//         },
//         _apply_google_font: async function (ev) {
//             var self = this;
//             const font_url = $('#google_font_input_field').val();
//             if (font_url) {
//                 let m = font_url.match(/\bspecimen\/([\w+]+)/);
//                 if (!m) {
//                     // if embed code (so that it works anyway if the user put the embed code instead of the page link)
//                     m = font_url.match(/\bfamily=([\w+]+)/);
//                     if (!m) {
//                         $('#google_font_input_field').addClass('wrong_font');
//                         return;
//                     }
//                 }
//                 let isValidFamily = false;
//                 try {
//                     const result = await fetch("https://fonts.googleapis.com/css?family=" + m[1] + ':300,300i,400,400i,700,700i', { method: 'HEAD' });
//                     // Google fonts server returns a 400 status code if family is not valid.
//                     if (result.ok) {
//                         isValidFamily = true;
//                     }
//                 } catch (error) {
//                     console.error(error);
//                 }

//                 if (!isValidFamily) {
//                     $('#google_font_input_field').addClass('wrong_font');
//                     return;
//                 }
//                 $('#google_font_input_field').removeClass('wrong_font');
//                 const font = m[1].replace(/\+/g, ' ');
                
//                 if (!(self.googleFonts).includes(font)) {

//                     self.googleFonts.push(font)
//                     $('#wk_fontCollapse > div.card-body').find('.active').removeClass('active');
//                     $('#wk_fontCollapse').find('.card-body').append($('<div><a><span class="active" data-font="'+`'${font}'`+'" style="font-family:'+font+'">'+font+'</span></a> <i class="fa fa-trash google_font_trash"></i></div>'))
//                     var font_data = { values: { ["font"]: `'${font}'` }, googleFonts: self.googleFonts, }
//                     $('#google_font_input_field').val('')
//                     self._onGoogleFontsCustoDuotoneRequest(font_data)
//                 }
//             }
//         },


//         _set_default_image ($target) {
//             $target.closest('.card-body').find('.wk-cog-img').attr('src', '/duotone_backend_theme/static/src/images/default.jpg');
//         },
//         _get_content (key, value, updatedFileContent) {
//             var pattern = $.str.sprintf("'%s': %%s,\n", key);
//             var regex = new RegExp($.str.sprintf(pattern, ".+"));
//             var replacement = $.str.sprintf(pattern, value);
//             if (regex.test(updatedFileContent)) {
//                 updatedFileContent = updatedFileContent
//                     .replace(regex, replacement);
//             } else {
//                 updatedFileContent = updatedFileContent
//                     .replace(/( *)(.*hook.*)/, $.str.sprintf('$1%s$1$2', replacement));
//             }
//             return updatedFileContent;
//         },
//         _get_updated_file_content (data, key, value) {
//             var self = this;
//             var file = self._get_file(data.scss[1][1]);
//             var updatedFileContent = file.arch;
//             updatedFileContent = self._get_content(key, value, updatedFileContent);
//             return {
//                 'updatedFileContent': updatedFileContent,
//                 'file': file
//             }
//         },
//         change_theme (key, value, callback = false, google_fonts = false) {
//             var self = this;
//             var url = '/duotone_backend_theme/static/src/scss/customized/dynamic_variables.scss';
//             ajax.jsonrpc('/theme/backend/make_scss_custo', 'call', {
//                 'url': url,
//                 'key': key,
//                 'value': value,
//                 'google_fonts': google_fonts,
//             }).then(function () {
//                 ajax.jsonrpc('/backend/theme_customize', 'call', {
//                     'get_bundle': true,
//                 }).then(function (bundles) {
//                     var $allLinks = $();
//                     var defs = $.map(bundles, function (bundleURLs, bundleName) {
//                         var $links = $('link[href*="' + bundleName + '"]');
//                         $allLinks = $allLinks.add($links);
//                         var $newLinks = $();
//                         $.each(bundleURLs, function (url) {
//                             $newLinks = $newLinks.add($('<link/>', {
//                                 type: 'text/css',
//                                 rel: 'stylesheet',
//                                 href: url,
//                             }));
//                         });

//                         var linksLoaded = new Promise(function (resolve, reject) {
//                             var nbLoaded = 0;
//                             $newLinks.on('load', function () {
//                                 if (++nbLoaded >= $newLinks.length) {
//                                     resolve();
//                                 }
//                             });
//                             $newLinks.on('error', function () {
//                                 reject();
//                                 window.location.hash = 'theme=true';
//                                 window.location.reload();
//                             });
//                         });
//                         $links.last().after($newLinks);
//                         return linksLoaded;
//                     });
//                     return Promise.all(defs).then(function () {
//                         if (callback) {
//                             callback();
//                         }
//                         $allLinks.remove();
//                     }).guardedCatch(function () {
//                         if (callback) {
//                             callback();
//                         }
//                         $allLinks.remove();
//                     });
//                 })
//             });
//         },
//         _toggle_active ($target) {
//             $target.closest('.card-body').find('.active').removeClass('active');
//             $target.find('span').addClass('active');
//         },
//         _set_font (evt) {
//             let $target = $(evt.target);
//             $target.closest('.card-body').find('.active').removeClass('active');
//             $target.addClass('active');
//             let font = $(evt.target).attr('data-font');
//             this.change_theme('font', font);
//         },
//         _set_foreground_color (evt) {
//             this._toggle_active($(evt.currentTarget));
//             let color = $(evt.target).data('color');
//             this.change_theme('foreground_color', color);
//         },
//         _set_foreground_input_color (evt) {
//             let color = evt.target.value;
//             this.change_theme('foreground_color', color);
//         },
//         _set_background_color (evt) {
//             this._toggle_active($(evt.currentTarget));
//             let color = $(evt.target).data('color');
//             this.change_theme('background_color', color);
//         },
//         _set_background_input_color (evt) {
//             let color = evt.target.value;
//             this.change_theme('background_color', color);
//         },
//         _set_transparency (evt) {
//             let $target = $(evt.currentTarget);
//             $target.siblings('.wk-range').text(evt.target.value);
//             let transparency = evt.target.value;
//             let opacity = [0, 1, .9, .8, .7, .6, .5, .4, .3, .2, .1];
//             transparency = opacity[transparency];
//             this.change_theme('opacity', transparency);
//         },
//         _remove_background_image (evt) {
//             var self = this;
//             return rpc.query({
//                 route: '/duotone/remove/image',
//                 params: {},
//             }).then(function (result) {
//                 self.change_theme('bck_img', null, self._set_default_image($(evt.currentTarget)));
//             });
//         },
//         _set_browse_background_image (evt) {
//             let $target = $(evt.currentTarget);
//             var self = this;
//             const file = evt.target.files[0];
//             const name = evt.target.files[0].name;
//             var reader = new FileReader();
//             reader.addEventListener("load", function () {
//                 var data = reader.result;
//                 return rpc.query({
//                     route: '/create/image',
//                     params: {
//                         'data': data,
//                         'name': name
//                     },
//                 }).then(function (result) {
//                     $target.closest('.card-body').find('.wk-cog-img').attr('src', `/web/content/${result.id}`);
//                     self.change_theme('bck_img', result.id);
//                 });
//             }, false);
//             if (file) {
//                 reader.readAsDataURL(file);
//             }
//         },
//         _set_button (evt) {
//             let $target = $(evt.target);
//             let button_type = $target.data('btn_type');
//             this.change_theme('button_type', button_type);
//         },
//     });
//     SystrayMenu.Items.push(CogSlider);
// });
