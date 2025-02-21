/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

import { useOlympics } from "../services/olympics_service";

export class OlympicsSystrayItem extends Component {
  setup() {
    this.action = useService("action");
    this.olympics_service = useOlympics();
  }
  openOngoingEvents() {
    this.action.doAction({
      type: "ir.actions.act_window",
      target: "new",
      name: "Ongoing Events",
      res_model: "olympics.event",
      views: [
        [false, "list"],
        [false, "form"],
      ],
      view_mode: "list,form",
      domain: [["state", "=", "in_progress"]],
      context: {
        create: false,
        edit: false,
      },
    });
  }
}
OlympicsSystrayItem.template = "olympics.OlympicsSystrayItem";
OlympicsSystrayItem.components = {};

registry.category("systray").add("olympics.OlympicsSystray", {
  Component: OlympicsSystrayItem,
});
