"""Run functions."""

import os
import subprocess
from pathlib import Path

from pheval_phenogenius.run.prepare_commands import write_commands


def run(testdata_dir: Path, input_dir: Path, raw_results_dir: Path, tool_input_commands_dir: Path) -> None:
    """
    Run the commands on the phenopackets corpus.

    Args:
        testdata_dir (Path): Path to the test data directory.
        input_dir (Path): Path to the input directory.
        raw_results_dir (Path): Path to the raw results directory.
        tool_input_commands_dir (Path): Path to the tool input commands directory.

    """
    os.chdir(input_dir.joinpath("PhenoGeniusCLI"))
    write_commands(testdata_dir.joinpath("phenopackets"), input_dir, raw_results_dir, tool_input_commands_dir)
    print("Running commands...")
    subprocess.run(
        ["bash", str(tool_input_commands_dir.joinpath(testdata_dir.name + "_commands.tsv"))], shell=False
    )  # noqa
