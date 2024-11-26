"""Post-process results from post-processing pipeline."""

from pathlib import Path
from typing import List

import pandas as pd
from pheval.post_processing.post_processing import PhEvalGeneResult, generate_pheval_result
from pheval.utils.file_utils import all_files
from pheval.utils.phenopacket_utils import GeneIdentifierUpdater, create_hgnc_dict


def read_phenogenius_result(phenogenius_result: Path) -> pd.DataFrame:
    """
    Read PhenoGenius results from a PhenoGenius TSV result file.

    Args:
        phenogenius_result (Path): Path to a PhenoGenius TSV result file.

    Returns:
        pd.DataFrame: PhenoGenius results from a PhenoGenius TSV result file.

    """
    return pd.read_csv(phenogenius_result, delimiter="\t")


class PhEvalGeneResultFromPhenoGeniusCreator:
    """Class for converting PhenoGenius results to PhEvalGeneResults."""

    def __init__(self, phenogenius_result: pd.DataFrame, gene_identifier_updator: GeneIdentifierUpdater):
        """Initialise PhEvalGeneResultFromPhenoGeniusCreator."""
        self.phenogenius_result = phenogenius_result
        self.gene_identifier_updator = gene_identifier_updator

    @staticmethod
    def _find_gene_symbol(result_entry: pd.Series) -> str:
        """
        Find the gene symbol for a result.

        Args:
            result_entry (pd.Series): PhenoGenius TSV result.

        Returns:
            str: Gene symbol.

        """
        return result_entry["gene_symbol"]

    def _find_gene_identifier(self, result_entry: pd.Series) -> str:
        """
        Find the gene identifier for a result.

        Args:
            result_entry (pd.Series): PhenoGenius TSV result.

        Returns:
            str: Gene identifier.

        """
        return self.gene_identifier_updator.find_identifier(result_entry["gene_symbol"])

    @staticmethod
    def _find_score(result_entry: pd.Series) -> float:
        """
        Find the score for a result.

        Args:
            result_entry (pd.Series): PhenoGenius TSV result.

        Returns:
            float: Score.

        """
        return result_entry["score"]

    def extract_pheval_gene_requirements(self) -> List[PhEvalGeneResult]:
        """
        Extract data required to produce PhEval gene output.

        Returns:
            List[PhEvalGeneResult]: List of PhEvalGeneResult objects.

        """
        simplified_phenogenius_result = []
        for _index, row in self.phenogenius_result.iterrows():
            simplified_phenogenius_result.append(
                PhEvalGeneResult(
                    gene_symbol=self._find_gene_symbol(row),
                    gene_identifier=self._find_gene_identifier(row),
                    score=self._find_score(row),
                )
            )
        return simplified_phenogenius_result


def create_standardised_results(results_dir: Path, output_dir: Path, sort_order: str) -> None:
    """
    Write standardised gene results from default PhenoGenius TSV output.

    Args:
        results_dir (Path): Path to the raw results directory.
        output_dir (Path): Path to the output directory.
        sort_order (str): The sort order of the results, either ascending or descending.

    """
    hgnc_data = create_hgnc_dict()
    gene_identifier_updator = GeneIdentifierUpdater(hgnc_data=hgnc_data, gene_identifier="ensembl_id")
    for result in all_files(results_dir):
        phenogenius_tsv = read_phenogenius_result(result)
        pheval_gene_result = PhEvalGeneResultFromPhenoGeniusCreator(
            phenogenius_tsv, gene_identifier_updator
        ).extract_pheval_gene_requirements()
        generate_pheval_result(
            pheval_result=pheval_gene_result,
            sort_order_str=sort_order,
            output_dir=output_dir,
            tool_result_path=result,
        )
