import { GraphRenderer } from "@web/views/graph/graph_renderer";
import { user } from "@web/core/user";
import { patch } from "@web/core/utils/patch";

import { onWillStart } from "@odoo/owl";
patch(GraphRenderer.prototype, {
  setup() {
    super.setup();
    onWillStart(async () => {
      if (
        !(await user.hasGroup("group_spreadsheet.allow_export_spreadsheet"))
      ) {
        this.canInsertChart = false;
      }
    });
  },
});
