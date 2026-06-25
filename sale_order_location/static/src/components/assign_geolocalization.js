import { session } from "@web/session";
import { standardWidgetProps } from "@web/views/widgets/standard_widget_props";
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class AssignGeolocalization extends Component {
  static template = "sale_order_location.AssignGeolocalization";
  static props = {
    ...standardWidgetProps,
  };
  setup() {
    this.orm = useService("orm");
    this.action = useService("action");
  }

  async _setCoordinates(coordinates) {
    const { latitude, longitude } = coordinates.coords;
    await this.orm.call("sale.order.line", "write", [
      [this.props.record.resId],
      { latitude, longitude },
    ]);
    await this.props.record.load();
  }

  async onAssignGeolocationClicked() {
    const options = {
      enableHighAccuracy: true,
      timeout: 5000,
      maximumAge: 0,
    };
    function error(err) {
      console.warn(`ERROR(${err.code}): ${err.message}`);
    }
    navigator.geolocation.getCurrentPosition((coordinates) =>
      this._setCoordinates(coordinates),
      error,
      options
    
    );
  }
}

export const assignGeolocalization = {
  component: AssignGeolocalization,
};

registry
  .category("view_widgets")
  .add("assign_geolocation", assignGeolocalization);
