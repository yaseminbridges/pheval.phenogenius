"""Post-processing functions."""

from pathlib import Path

from pheval_phenogenius.post_process.post_process_results_format import create_standardised_results


def post_process_results_format(raw_results_dir: Path, output_dir: Path) -> None:
    """
    Post-process PhenoGenius result to PhEval gene results.

    Args:
        raw_results_dir (Path): Path to raw results directory.
        output_dir (Path): Path to output directory.

    """
    print("...creating pheval gene results format...")
    create_standardised_results(results_dir=raw_results_dir, output_dir=output_dir, sort_order="DESCENDING")
    print("done")
