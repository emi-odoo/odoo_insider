import { standardWidgetProps } from "@web/views/widgets/standard_widget_props";
import {
  Component,
  onWillStart,
  onMounted,
  useRef,
  useState,
  onWillUnmount,
  onWillUpdateProps,
} from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { useRecordObserver } from "@web/model/relational_model/utils";
import { loadJS } from "@web/core/assets";
const randomNum = () => Math.floor(Math.random() * (235 - 52 + 1) + 52);

const randomRGB = () => `rgb(${randomNum()}, ${randomNum()}, ${randomNum()})`;

export class GraphOrder extends Component {
  static template = "sale_order_graph.GraphOrder";
  static props = {
    ...standardWidgetProps,
  };
  setup() {
    this.canvasRef = useRef("canvas_graph");
    this.orm = useService("orm");
    this.graphData = useState({ data: [] });
    onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
    onMounted(() => {
      this.renderChart(this.props.record);
    });
    onWillUnmount(() => {
      this?.chart.destroy();
    });
    useRecordObserver(async (record) => {
      console.log("record", record);
      await this.renderChart(record);
    });
  }

  get parola() {
    return "ciao";
  }

  async _loadGraphData(record) {
    const { resId } = record;
    const groups = await this.orm.call("sale.order.line", "read_group", [
      [["order_id", "=", resId]],
      ["product_uom"],
      ["product_uom"],
    ]);
    // resulting object
    /* [
      {
          "product_uom": [
              1,
              "Units"
          ],
          "product_uom_count": 3,
          "__domain": [
              "&",
              [
                  "order_id",
                  "=",
                  6
              ],
              [
                  "product_uom",
                  "=",
                  1
              ]
          ]
      }
    ]*/
    // need to transform it to
    /* {
      Units: 3
    }
    */
    const data = groups.reduce((acc, group) => {
      acc[group.product_uom[1]] = group.product_uom_count;
      return acc;
    }, {});
    const labels = Object.keys(data);
    const dataset = Object.values(data);
    return {
      labels: labels,
      datasets: [
        {
          label: "UoM",
          data: dataset,
          // backgroundColor: labels.map((el) => randomRGB()),
        },
      ],
    };
  }

  async renderChart(record) {
    if (typeof Chart === "undefined") {
      console.error("Chart.js is not loaded");
      return;
    }
    if (this.chart) {
      this.chart.destroy();
    }
    this.chart = new Chart(this.canvasRef.el, {
      type: "pie",
      responsive: true,
      data: await this._loadGraphData(record),
      options: {
        onClick: (event, elements) => {
          console.log("called");
          return;
          const element_indexes = elements.map((el) => el._index);
          const states = Object.keys(this.props.data).filter((el, index) =>
            element_indexes.includes(index)
          );
          return this.action.doAction({
            type: "ir.actions.act_window",
            name: `Missions: ${states.join(",")}`,
            res_model: "spaceship.management.mission",
            domain: [["state", "in", states]],
            views: [
              [false, "list"],
              [false, "form"],
            ],
          });
        },
      },
    });
  }
}

export const graphOrder = {
  component: GraphOrder,
};

registry.category("view_widgets").add("so_graph_order", graphOrder);
