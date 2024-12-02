"""Prepare commands functions."""

from dataclasses import dataclass
from pathlib import Path
from typing import List

from pheval.utils.file_utils import all_files
from pheval.utils.phenopacket_utils import PhenopacketUtil, phenopacket_reader


@dataclass
class PhenoGeniusParameters:
    """Class to store PhenoGenius parameters."""

    python_executable: Path
    hpo_list: List[str]
    result_file: Path


def _return_hpo_list(phenopacket_path: Path) -> List[str]:
    """
    Return HPO list from Phenopacket file.

    Args:
        phenopacket_path: Path to Phenopacket file.

    Returns:
        List[str]: HPO list from Phenopacket file.

    """
    phenopacket = phenopacket_reader(phenopacket_path)
    return [hpo.type.id for hpo in PhenopacketUtil(phenopacket).observed_phenotypic_features()]


def _create_parameter_for_sample(
    phenopacket_path: Path, input_dir: Path, raw_results_dir: Path
) -> PhenoGeniusParameters:
    """
    Create PhenoGenius parameters for a sample.

    Args:
        phenopacket_path: Path to Phenopacket file.
        input_dir: Path to input directory.
        raw_results_dir: Path to raw results directory.

    Returns:
        PhenoGeniusParameters: Parameters for a sample.

    """
    return PhenoGeniusParameters(
        python_executable=input_dir.joinpath("PhenoGeniusCli/phenogenius_cli.py"),
        hpo_list=_return_hpo_list(phenopacket_path),
        result_file=raw_results_dir.joinpath(phenopacket_path.stem + ".tsv"),
    )


def get_parameters(phenopacket_dir: Path, input_dir: Path, raw_results_dir: Path) -> List[PhenoGeniusParameters]:
    """
    Create PhenoGenius parameters for a corpus.

    Args:
        phenopacket_dir: Path to Phenopacket directory.
        input_dir: Path to input directory.
        raw_results_dir: Path to raw results directory.

    Returns:
        List[PhenoGeniusParameters]: Parameters for a corpus.

    """
    parameters = []
    for phenopacket_path in all_files(phenopacket_dir):
        parameters.append(_create_parameter_for_sample(phenopacket_path, input_dir, raw_results_dir))
    return parameters


class CommandsWriter:
    """Class to write commands to a file."""

    def __init__(self, output_file: Path):
        """Initialise "CommandsWriter."""
        self.output_file = open(output_file, "w")

    def write_command(self, parameters: PhenoGeniusParameters) -> None:
        """
        Write command to file.

        Args:
            parameters: Parameters for a sample.

        """
        self.output_file.write(
            f"python "
            f"{parameters.python_executable} "
            f"--hpo_list "
            f"{','.join(parameters.hpo_list)} "
            f"--result_file "
            f"{parameters.result_file}\n"
        )

    def close(self):
        """Close output file."""
        self.output_file.close()


def write_commands(
    phenopacket_dir: Path, input_dir: Path, raw_results_dir: Path, tool_input_commands_dir: Path
) -> None:
    """
    Write all commands for a corpus.

    Args:
        phenopacket_dir: Path to Phenopacket directory.
        input_dir: Path to input directory.
        raw_results_dir: Path to raw results directory.
        tool_input_commands_dir: Path to tool input directory.

    """
    parameters = get_parameters(phenopacket_dir, input_dir, raw_results_dir)
    command_writer = CommandsWriter(tool_input_commands_dir.joinpath(phenopacket_dir.parent.name + "_commands.tsv"))
    for parameter in parameters:
        command_writer.write_command(parameter)
    command_writer.close()
