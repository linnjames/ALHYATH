odoo.define('pos_restaurant_invoice.PaymentScreenOverride', function (require) {
    'use strict';

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');

    const PaymentScreenOverride = (PaymentScreen) =>
        class extends PaymentScreen {
            shouldDownloadInvoice() {
                // Only download if the custom boolean is enabled
                return this.env.pos.config.automatic_invoice_printing && super.shouldDownloadInvoice();
            }
        };

    Registries.Component.extend(PaymentScreen, PaymentScreenOverride);

    return PaymentScreen;
});
