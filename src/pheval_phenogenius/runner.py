"""Runner."""

from dataclasses import dataclass
from pathlib import Path

from pheval.runners.runner import PhEvalRunner

from pheval_phenogenius.post_process.post_process import post_process_results_format
from pheval_phenogenius.run.run import run


@dataclass
class PhEvalPhenoGeniusRunner(PhEvalRunner):
    """Runner class implementation."""

    input_dir: Path
    testdata_dir: Path
    tmp_dir: Path
    output_dir: Path
    config_file: Path
    version: str

    def prepare(self):
        """Prepare."""
        print("preparing")

    def run(self):
        """Run."""
        print("running")
        run(
            testdata_dir=self.testdata_dir,
            input_dir=self.input_dir,
            raw_results_dir=self.raw_results_dir,
            tool_input_commands_dir=self.tool_input_commands_dir,
        )

    def post_process(self):
        """Post Process."""
        print("post processing")
        post_process_results_format(
            raw_results_dir=self.raw_results_dir,
            output_dir=self.output_dir,
        )
