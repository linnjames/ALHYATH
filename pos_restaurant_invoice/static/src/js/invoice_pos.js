odoo.define('pos_restaurant_invoice.invoice_pos', function (require) {
    'use strict';

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');

    const PosInvoiceAutomatePaymentScreen = (PaymentScreen) =>
          class extends PaymentScreen {
              constructor() {
                 super(...arguments);
                 // Ensure that config is loaded
                 if (this.env.pos.config.enable_auto_invoice) {
                    this.currentOrder.set_to_invoice(true);
                 }
              }

              // Alternatively, use an appropriate lifecycle method
              async willStart() {
                  await super.willStart();
                  if (this.env.pos.config.enable_auto_invoice) {
                      this.currentOrder.set_to_invoice(true);
                  }
              }
          };

    Registries.Component.extend(PaymentScreen, PosInvoiceAutomatePaymentScreen);
    console.log("Invoice POS module loaded successfully.");

    return PaymentScreen;
});
