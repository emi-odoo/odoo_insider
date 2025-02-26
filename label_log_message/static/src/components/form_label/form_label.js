/** @odoo-module **/

import { FormLabel } from "@web/views/form/form_label";
import { patch } from "@web/core/utils/patch";

patch(FormLabel.prototype, {
  onLabelOver() {
    console.log("onLabelOver");
  },
  onLabelOut() {
    console.log("onLabelOut");
  },
});