from odoo_csv_tools.lib import mapper
from odoo_csv_tools.lib.transform import Processor

import pathlib

config_file = "config.conf"
common_vals_processor = {"delimiter": ",", "encoding": "utf-8", "conf_file": config_file}
NULL_VALUES = ["NULL", False, ".", ""]

input_file = str(pathlib.Path(__file__).parent / "sample_orders.csv")
target_script_file = str(pathlib.Path(__file__).parent / "import_orders.sh")


def map_price(line):
    return float(line["total"]) / float(line["qty"])


def to_xmlid(name):
    return name.replace(".", "_").replace(",", "_").replace("\n", "_").replace(" ", "_").lower().strip()


def to_m2o(PREFIX, value, to_append):

    return PREFIX + "." + to_xmlid(value) + to_append


def custom_m2o(PREFIX, field, to_append=""):
    def m2o_fun(line):
        return to_m2o(PREFIX, line[field], to_append=to_append)

    return m2o_fun


def preprocess(header, data):
    new_header = header + ["index"]
    for index, line in enumerate(data, start=1):
        line += [str(index)]

    return new_header, data


def prepare_sale_orders():
    customer_mapping = {
        "id": mapper.m2o("__import__odoo_insider__", "customer's email"),
        "name": mapper.val("customer"),
        "email": mapper.val("customer's email"),
        "city": mapper.val("city"),
    }

    processor = Processor(input_file, **common_vals_processor, preprocess=preprocess)
    # processor.process(
    #     customer_mapping,
    #     str(pathlib.Path(__file__).parent / "output_partners.csv"),
    #     {
    #         **{"worker": 2, "batch_size": 10, "model": "res.partner"},
    #     },
    #     "set",
    #     null_values=NULL_VALUES,
    #     verbose=False,
    # )
    # product_mapping = {
    #     "id": custom_m2o("__import__odoo_insider__", "item"),
    #     "name": mapper.val("item"),
    #     "type": mapper.const("service"),
    # }
    # processor.process(
    #     product_mapping,
    #     str(pathlib.Path(__file__).parent / "output_products.csv"),
    #     {
    #         **{"worker": 2, "batch_size": 10, "model": "product.template", "context": {"create_product_product": False}},
    #     },
    #     "set",
    #     null_values=NULL_VALUES,
    #     verbose=False,
    # )
    # # add call to `process`
    # order_mapping = {
    #     "id": mapper.m2o("__import__odoo_insider__", "order reference"),
    #     "partner_id/id": mapper.m2o("__import__odoo_insider__", "customer's email"),
    #     "client_order_ref": mapper.val("order reference"),
    # }
    # processor.process(
    #     order_mapping,
    #     str(pathlib.Path(__file__).parent / "output_orders.csv"),
    #     {
    #         **{"worker": 2, "batch_size": 10, "model": "sale.order"},
    #     },
    #     "set",
    #     null_values=NULL_VALUES,
    #     verbose=False,
    # )
    # add call to `process`
    order_line_mapping = {
        "id": mapper.val("index"),
        "order_id/id": mapper.m2o("__import__odoo_insider__", "order reference"),
        "product_id/id": custom_m2o("__import__odoo_insider__", "item", "_variant"),
        "product_uom_qty": mapper.val("qty"),
        "price_unit": map_price,
    }
    processor.process(
        order_line_mapping,
        str(pathlib.Path(__file__).parent / "output_order_lines.csv"),
        {
            **{"worker": 2, "batch_size": 10, "model": "sale.order.line", "groupby": "order_id/id"},
        },
        "set",
        null_values=NULL_VALUES,
        verbose=False,
    )
    processor.write_to_file(target_script_file, python_exe="", path="", fail=True, append=False)


if __name__ == "__main__":
    prepare_sale_orders()
