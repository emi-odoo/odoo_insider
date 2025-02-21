from odoo_csv_tools.lib import mapper
from odoo_csv_tools.lib.transform import Processor

import pathlib

config_file = "config.conf"
common_vals_processor = {"delimiter": ";", "encoding": "utf-8", "conf_file": config_file}
NULL_VALUES = ["NULL", False, ".", ""]

input_file = str(pathlib.Path(__file__).parent / "starting_data_olympics.csv")
out_file = str(pathlib.Path(__file__).parent / "output_olympics.csv")
target_script_file = str(pathlib.Path(__file__).parent / "import_olympics.sh")


def prepare_olympics():
    olympics_mapping = {
        "id": mapper.m2o("__import__olympics__", "year"),
        "name": mapper.val("olympic"),
        "date_start": mapper.val("start_date"),
        "date_end": mapper.val("end_date"),
        "olympics_type": mapper.map_val("summer_edition", {"true": "summer", "false": "winter"}, default="winter"),
    }

    processor = Processor(input_file, **common_vals_processor)
    processor.process(
        olympics_mapping,
        out_file,
        {
            **{"worker": 2, "batch_size": 10, "model": "olympics.olympics"},
        },
        "set",
        null_values=NULL_VALUES,
        verbose=False,
    )
    processor.write_to_file(target_script_file, python_exe="", path="", fail=True, append=False)


if __name__ == "__main__":
    prepare_olympics()
