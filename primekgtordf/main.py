"""
Script to explore and try out things. To be converted to actual modules.
"""
from argparse import ArgumentParser
import logging

from rdflib import Graph

from primekgtordf import vocab
from primekgtordf.disesefeatures import DiseaseFeaturesReader
from primekgtordf.drugfeatures import DrugFeaturesReader
from primekgtordf.node import NodesReader
from primekgtordf.relation import RelationsReader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main(
        nodes_file_path: str,
        edges_file_path: str,
        output_file_path: str,
        disease_features_file_path: str = None,
        drug_features_file_path: str = None
):
    nodes_reader = NodesReader(nodes_file_path=nodes_file_path)

    relations = RelationsReader(
        relations_file_path=edges_file_path,
        nodes_reader=nodes_reader
    )

    g = Graph()

    g += vocab.get_vocab_triples()
    g += relations.to_rdf()

    if disease_features_file_path is not None:
        g += DiseaseFeaturesReader(disease_features_file_path, nodes_reader).to_rdf()

    if drug_features_file_path is not None:
        g += DrugFeaturesReader(drug_features_file_path, nodes_reader).to_rdf()

    g.serialize(destination=output_file_path, format='turtle')


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('nodes_file')
    arg_parser.add_argument('edges_file')
    arg_parser.add_argument('output_rdf_file')
    arg_parser.add_argument('--diseasefeatures')
    arg_parser.add_argument('--drugfeatures')
    # TODO: Make output format configurable

    args = arg_parser.parse_args()

    main(
        args.nodes_file,
        args.edges_file,
        args.output_rdf_file,
        args.diseasefeatures,
        args.drugfeatures
    )
