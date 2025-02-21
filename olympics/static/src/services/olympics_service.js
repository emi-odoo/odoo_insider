/** @odoo-module **/

import { registry } from "@web/core/registry";

import { Reactive } from "@web/core/utils/reactive";

const { EventBus } = owl;

export class OlympicsModel extends Reactive {
  static serviceDependencies = ["orm"];
  constructor() {
    super(...arguments);
    this.ongoingEvents = 0;
    this.ready = this.setup(...arguments).then(() => this);
  }
  async setup(orm, bus_service) {
    this.orm = orm;
    this.updateOngoingEvents();
    this.bus = bus_service;
    this.event_bus = new EventBus();
    this.bus.addChannel("olympic_channel");
    this.bus.subscribe("olympics.event/finished", () =>
      this.updateOngoingEvents()
    );
    this.bus.subscribe("olympics.event/state_changed", () =>
      this.updateOngoingEvents()
    );
  }
  async getOngoingEvents() {
    return this.orm.call("olympics.event", "search_count", [
      [["state", "=", "in_progress"]],
    ]);
  }

  async updateOngoingEvents() {
    this.ongoingEvents = await this.getOngoingEvents();
  }
}

export const olympicsService = {
  dependencies: ["orm", "bus_service", "notification"],
  start(env, { orm, bus_service }) {
    return new OlympicsModel(orm, bus_service);
  },
};

import { useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
export function useOlympics() {
  return useState(useService("olympics_service"));
}

registry.category("services").add("olympics_service", olympicsService);
