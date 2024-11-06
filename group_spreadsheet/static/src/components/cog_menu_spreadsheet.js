import { registry } from "@web/core/registry";

const cogMenuRegistry = registry.category("cogMenu");
import { user } from "@web/core/user";

import { patch } from "@web/core/utils/patch";

patch(cogMenuRegistry.get("spreadsheet-cog-menu"), {
  isDisplayed: async (env) => {
    if (!(await user.hasGroup("group_spreadsheet.allow_export_spreadsheet"))) {
      return false;
    }
    return (
      !env.isSmall &&
      env.config.actionType === "ir.actions.act_window" &&
      env.config.viewType !== "form"
    );
  },
});
