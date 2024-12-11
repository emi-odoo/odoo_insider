/** @odoo-module **/

import { Dropdown } from "@web/core/dropdown/dropdown";
import { registry } from "@web/core/registry";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";

import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
import { onWillStart } from "@odoo/owl";
const cogMenuRegistry = registry.category("cogMenu");

export class PrintDirectlyCogMenu extends Component {
  setup() {
    super.setup();
    this.orm = useService("orm");
    onWillStart(async () => {});
  }
  static template = "print_directly.PrintDirectlyCogMenu";
  static components = {
    Dropdown,
    DropdownItem,
  };
  static props = {};
  async printImmediately() {
    const examples =
      "http://localhost:8069/report/pdf/sale.report_saleorder_raw/115";
    var frame = document.createElement("iframe");
    // frame.classList.add("d-none");
    frame.onload = function () {
      try {
        this.contentWindow && this.contentWindow.print();
        return;
      } catch (e) {}
      console.error("in a protective iframe?");
    };
    frame.src = examples;
    document.body.appendChild(frame);
  }
}

cogMenuRegistry.add(
  "print-directly-cog-menu",
  {
    Component: PrintDirectlyCogMenu,
    groupNumber: 30,
    isDisplayed: ({ config, isSmall }) =>
      !isSmall &&
      config.actionType === "ir.actions.act_window" &&
      config.viewType === "form",
  },
  { sequence: 2 }
);
