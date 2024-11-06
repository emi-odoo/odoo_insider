import { patch } from "@web/core/utils/patch";
import { ListController } from "@web/views/list/list_controller";
import { _t } from "@web/core/l10n/translation";
import { user } from "@web/core/user";
import { onWillStart } from "@odoo/owl";

const newPatchListControllerExportSelection = {
  setup() {
    super.setup();
    this.hasGroupExportSpreadsheet = false;
    onWillStart(async () => {
      this.hasGroupExportSpreadsheet = await user.hasGroup(
        "group_spreadsheet.allow_export_spreadsheet"
      );
    });
  },
  getStaticActionMenuItems() {
    const list = this.model.root;
    const isM2MGrouped = list.groupBy.some((groupBy) => {
      const fieldName = groupBy.split(":")[0];
      return list.fields[fieldName].type === "many2many";
    });
    const menuitems = super.getStaticActionMenuItems(...arguments);
    const canExportSpreadsheet =
      this.hasGroupExportSpreadsheet && !isM2MGrouped;
    menuitems.insert.isAvailable = () => canExportSpreadsheet;
    return menuitems;
  },
};
export const unpatchListControllerExportSelection = patch(
  ListController.prototype,
  newPatchListControllerExportSelection
);
