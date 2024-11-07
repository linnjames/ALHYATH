odoo.define('hotel_room_dashboard_view.dashboard_reload', function (require) {
    "use strict";

    var FormView = require('web.FormView');

    FormView.include({
        on_attach_callback: function() {
            this._super.apply(this, arguments);
            var $button = this.$('.dashboard_reload');
            if ($button.length) {
                $button.click();
            }
        },
    });
});

