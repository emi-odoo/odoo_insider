from odoo_csv_tools.lib import mapper
from odoo_csv_tools.lib.transform import Processor
from odoo_csv_tools.lib.internal.tools import to_xmlid

import pathlib

config_file = "config.conf"
common_vals_processor = {"delimiter": ";", "encoding": "utf-8", "conf_file": config_file}
NULL_VALUES = ["NULL", False, ".", ""]

input_file = str(pathlib.Path(__file__).parent / "starting_data_results.csv")
out_file = str(pathlib.Path(__file__).parent / "output_olympics.csv")
target_script_file = str(pathlib.Path(__file__).parent / "import_results.sh")


def to_m2o_with_model(PREFIX, model, value, default=""):
    if not value:
        return default
    ext_id = to_xmlid(value).replace("@", "_").replace(" ", "_")
    return f"{PREFIX}.{to_xmlid(model)}_{ext_id}"


def custom_map_event(prefix):

    def map_event(line):
        return to_m2o_with_model(prefix, "olympics.event", line.get("olympics") + line.get("event"), default="")

    return map_event


def custom_map_athlete(prefix):

    def map_athlete(line):
        return to_m2o_with_model(prefix, "res.partner", line.get("athlete") + line.get("country"), default="")

    return map_athlete


def custom_map_result(prefix):

    def map_result(line):
        return to_m2o_with_model(
            prefix,
            "olympics.result",
            line.get("olympics") + line.get("event") + line.get("athlete") + line.get("country"),
            default="",
        )

    return map_result


def prepare_olympics():
    event_mapping = {
        "id": custom_map_event("__import__olympics__"),
        "olympics_id/id": mapper.m2o("__import__olympics__", "olympics"),
        "name": mapper.val("event"),
        "state": mapper.const("done"),
    }
    athlete_mapping = {
        "id": custom_map_athlete("__import__olympics__"),
        "name": mapper.val("athlete"),
        "country_id": mapper.val("country"),
    }
    result_mapping = {
        "id": custom_map_result("__import__olympics__"),
        "event_id/id": custom_map_event("__import__olympics__"),
        "athlete_id/id": custom_map_athlete("__import__olympics__"),
        "position": mapper.val("position"),
    }
    processor = Processor(input_file, **common_vals_processor)
    processor.process(
        event_mapping,
        str(pathlib.Path(__file__).parent / "output_olympics_events.csv"),
        {
            **{"worker": 2, "batch_size": 10, "model": "olympics.event"},
        },
        "set",
        null_values=NULL_VALUES,
        verbose=False,
    )
    processor.process(
        athlete_mapping,
        str(pathlib.Path(__file__).parent / "output_olympics_athletes.csv"),
        {
            **{"worker": 2, "batch_size": 10, "model": "res.partner"},
        },
        "set",
        null_values=NULL_VALUES,
        verbose=False,
    )
    processor.process(
        result_mapping,
        str(pathlib.Path(__file__).parent / "output_olympics_results.csv"),
        {
            **{"worker": 2, "batch_size": 10, "model": "olympics.result"},
        },
        "set",
        null_values=NULL_VALUES,
        verbose=False,
    )
    processor.write_to_file(target_script_file, python_exe="", path="", fail=True, append=False)


if __name__ == "__main__":
    prepare_olympics()
