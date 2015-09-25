$(function () {
    var shutter = {
        element: $('div.shutter'),
        text: 'Loading...',
        duration: 250,
        defaultContent: '<img src="/images/preloader.gif"><h1>Loading...</h1>',
        reset: function () {
            var that = this;
            this.element.find('td.shutter-content').html(this.defaultContent);
            return this;
        },
        error: function (message) {
            var that = this;
            this.element.find('img').remove();
            this.element.find('h1')
                .addClass('text-error').html(message)
                .after($('<h2/>').html(
                    $('<a/>')
                        .attr('href', document.location.href)
                        .text('Get back')
                        .on('click', function() { that.reset(); })
                ));
            return that;
        },
        show: function () {
            this.element.fadeIn(this.duration);
            return this;
        },
        hide: function () {
            this.element.fadeOut(this.duration);
            return this;
        }
    };

    var pageData = JSON.parse($('script.page-data').remove().html());

    var File = Backbone.Model.extend({
        defaults: {
            id: 0,
            size: '',
            name: '',
            type: ''
        }
    });
    var Files = Backbone.Collection.extend({});
    var files = new Files();

    var FilesView = Backbone.View.extend({
        model: files,
        el: $('div.menu-files'),
        initialize: function () {
            this.template = _.template($('script.template-menu-files').text());
            this.model.on('add', this.render, this);
            this.model.on('change', function () {
                setTimeout(function () {
                    self.render();
                }, 500);
            }, this);
            _.each(pageData['user']['files'], function (element) {
                files.add(new File(element));
            });
        },
        render: function () {
            this.$el.html('');
            _.each(this.model.toArray(), function (current) {
                var file = current.attributes;
                var id = current.id;
                pageData['user']['files'][id] = file;
            });
            this.$el.html('').html($(this.template(pageData)));
            return this;
        }
    });
    var filesView = new FilesView();

    var MenuUploadView = Backbone.View.extend({
        el: $('div.menu-upload'),
        initialize: function () {
            this.template = _.template($('script.template-menu-upload').text());
            this.render();
        },
        render: function () {
            this.$el.html('').html($(this.template(pageData)));
        }
    });
    var menuUploadView = new MenuUploadView();

    var UploadView = Backbone.View.extend({
        el: $('input.file-input'),
        initialize: function () {
            var that = this;
            that.$el.upload();
            _.each(this.events, function (method, event) {
                that.$el.on(event, that[method]);
            });
        },
        events: {
            'start.upload': 'start',
            'progress.upload': 'progress',
            'success.upload': 'success',
            'error.upload': 'error'
        },
        start: function (file, id) {
            $('div.upload-container').attr('disabled', true);
            $('div.upload-container button.file-upload').attr('disabled', true);
            $('div.upload-container input.file-input').attr('disabled', true);
            files.add(new File({
                id: id,
                size: file.size,
                name: file.name,
                type: file.type
            }));
        },
        progress: function (event, id) {
            var percent = Math.floor(event.loaded * 100 / event.total);
            var file = $('div.file[data-id="' + id + '"]');
            file
                .find('div.percentage')
                .removeClass('hide')
                .html(percent + ' %');
            if (!file.hasClass('progress')) {
                file.addClass('progress')
            }
        },
        success: function (data, id) {
            $('div.upload-container').attr('disabled', false);
            $('div.upload-container button.file-upload').attr('disabled', false);
            $('div.upload-container input.file-input').attr('disabled', false);
            var json = JSON.parse(data);
            $('div.file[data-id="' + id + '"]')
                .attr('data-id', json.id)
                .removeClass('progress')
                .addClass('success')
                .closest('a')
                .attr('href', '/file/' + json.id)
                .find('div.percentage')
                .remove();
            console.log(files.models);
            console.log(id);
            var model = _.findWhere(files.models, {id: id});
            model.id = json.id;
            model.attributes.id = model.id;
        },
        error: function (data, id) {
            $('div.file[data-id="' + id + '"]')
                .removeClass('progress')
                .addClass('error');
        }
    });
    var upload = new UploadView();

    var CardSettingsView = Backbone.View.extend({
        el: $('div.card.settings'),
        initialize: function () {
            this.template = _.template($('script.template-card-settings').text());
            this.render();
        },
        render: function () {
            this.$el.html('').html($(this.template(pageData)).html()).foundation();
            return this;
        },
        events: {
            'click a.button-convert': 'convert',
            'click a.button-convert-download': 'convert',
            'click input[type=radio][data-setting-name=extension]': 'tab'
        },
        convert: function (event) {
            event.preventDefault();
            var target = $(event.target);
            var that = this;
            var fmt = $('input[name=format-group]:checked').val();
            var settings = this.extractSettings();
            console.log(settings);
            var url = '/conv/' + pageData.file.id;
            shutter.show();
            $.post(url, settings)
                .fail(function () {
                    shutter.error('Something goes wrong.<br />Please, try again later').show();
                })
                .done(function (data) {
                    if (target.hasClass('button-convert-download')) {
                        that.download(data.url);
                    }
                    shutter.hide();
                    console.log(data);
                });
            return this;
        },
        tab: function (event) {
            event.preventDefault();
            console.log(pageData);
            pageData['selected'] = $(event.target).val();
            return this.render();
        },
        download: function (url) {
            document.location = url;
        },
        extractSettings: function () {
            var settings = {};
            this.$el.find('input.setting-value, select.setting-value').each(function (key, element) {
                var $element = $(element);
                var type = $element.attr('type');
                var name = $element.attr('data-setting-name');
                switch (type) {
                    case 'checkbox':
                        settings[name] = !!$element.prop('checked');
                        break;
                    case 'radio':
                        if ($element.prop('checked') === true) {
                            settings[name] = $element.val();
                        }
                        break;
                    default:
                        if (settings.hasOwnProperty(name)) {
                            settings[name] += '-' + $element.val();
                        } else {
                            settings[name] = $element.val();
                        }
                        break;
                }
            });
            return settings;
        }
    });
    var cardSettingsView = new CardSettingsView();

    var UserView = Backbone.View.extend({
        el: $('.menu-user'),
        initialize: function () {
            this.template = _.template($('script.template-menu-user').text());
            this.render();
        },
        render: function () {
            this.$el.html('').html($(this.template(pageData)));
            return this;
        }
    });
    var userView = new UserView();

    var App = Backbone.View.extend({
        el: $(document),
        initialize: function () {
            this.$el.foundation();
            var toggleSideMenuWidth = 769;
            function sideNav() {
                if ($(window).width() < toggleSideMenuWidth) {
                    $('.off-canvas-wrap').removeClass('move-right');
                    $('.left-off-canvas-toggle').show();
                } else {
                    $('.off-canvas-wrap').addClass('move-right');
                    $('.left-off-canvas-toggle').hide();
                }
            }
            $(window).resize(function () {
                sideNav();
            });
            $(function () {
                var translate = function (source, target, post_class) {
                    $.post('/translate', {
                        text: $(post_class).text(),
                        source: source,
                        target: target
                    }, function (response) {
                        $(post_class).text(response['text']);
                    })
                };
            });
            shutter.hide();
        }
    });
    var app = new App();
});