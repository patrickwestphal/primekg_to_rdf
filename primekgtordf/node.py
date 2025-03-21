import csv
import dataclasses
import logging
from enum import Enum

from rdflib import URIRef, Literal, XSD, Graph, RDF, OWL

from primekgtordf import PRIMEKG_URI_PREFIX, NCBI_PREFIX, DRUGBANK_PREFIX, HPO_PREFIX, MONDO_PREFIX, GO_PREFIX, \
    CTD_PREFIX, REACTOME_PREFIX, UBERON_PREFIX
from primekgtordf.vocab import has_source, has_node_id, node_cls, source_cls

logger = logging.getLogger(__name__)


class UnknownNodeTypeStrException(Exception):
    pass


class UnknownNodeSourceStrException(Exception):
    pass


class NodeType(Enum):
    Gene_Protein = PRIMEKG_URI_PREFIX + 'Gene_Protein'
    Drug = PRIMEKG_URI_PREFIX + 'Drug'
    Effect_Phenotype = PRIMEKG_URI_PREFIX + 'Effect_Phenotype'
    Disease = PRIMEKG_URI_PREFIX + 'Disease'
    BiologicalProcess = PRIMEKG_URI_PREFIX + 'BiologicalProcess'
    MolecularFunction = PRIMEKG_URI_PREFIX + 'MolecularFunction'
    CellularComponent = PRIMEKG_URI_PREFIX + 'CellularComponent'
    Exposure = PRIMEKG_URI_PREFIX + 'Exposure'
    Pathway = PRIMEKG_URI_PREFIX + 'Pathway'
    Anatomy = PRIMEKG_URI_PREFIX + 'Anatomy'

    @classmethod
    def get_type_by_id(cls, type_str: str):
        if type_str == 'gene/protein':
            return cls.Gene_Protein
        elif type_str == 'drug':
            return cls.Drug
        elif type_str == 'effect/phenotype':
            return cls.Effect_Phenotype
        elif type_str == 'disease':
            return cls.Disease
        elif type_str == 'biological_process':
            return cls.BiologicalProcess
        elif type_str == 'molecular_function':
            return cls.MolecularFunction
        elif type_str == 'cellular_component':
            return cls.CellularComponent
        elif type_str == 'exposure':
            return cls.Exposure
        elif type_str == 'pathway':
            return cls.Pathway
        elif type_str == 'anatomy':
            return cls.Anatomy
        else:
            raise UnknownNodeTypeStrException()


class NodeSource(Enum):
    NCBI = NCBI_PREFIX
    DrugBank = DRUGBANK_PREFIX
    HPO = HPO_PREFIX
    MONDO_grouped = MONDO_PREFIX + 'grouped'
    MONDO = MONDO_PREFIX
    GO = GO_PREFIX
    CTD = CTD_PREFIX
    REACTOME = REACTOME_PREFIX
    UBERON = UBERON_PREFIX

    @classmethod
    def get_source_by_str(cls, node_src_str: str):
        if node_src_str == 'NCBI':
            return cls.NCBI
        elif node_src_str == 'DrugBank':
            return cls.DrugBank
        elif node_src_str == 'HPO':
            return cls.HPO
        elif node_src_str == 'MONDO_grouped':
            return cls.MONDO_grouped
        elif node_src_str == 'MONDO':
            return cls.MONDO
        elif node_src_str == 'GO':
            return cls.GO
        elif node_src_str == 'CTD':
            return cls.CTD
        elif node_src_str == 'REACTOME':
            return cls.REACTOME
        elif node_src_str == 'UBERON':
            return cls.UBERON
        else:
            raise UnknownNodeSourceStrException()


@dataclasses.dataclass
class Node:
    """
    Holds a node representation from the PrimeKG nodes CSV file wit the
    following structure:

    node_index,node_id,node_type,node_name,node_source
    0,9796,gene/protein,PHYHIP,NCBI
    1,7918,gene/protein,GPANK1,NCBI
    2,8233,gene/protein,ZRSR2,NCBI
    3,4899,gene/protein,NRF1,NCBI
    4,5297,gene/protein,PI4KA,NCBI
    5,6564,gene/protein,SLC15A1,NCBI
    6,8668,gene/protein,EIF3I,NCBI
    7,10826,gene/protein,FAXDC2,NCBI
    """
    node_index: int
    node_id: str
    node_type: NodeType
    node_name: str
    node_source: NodeSource

    def get_uri(self):
        return URIRef(PRIMEKG_URI_PREFIX + 'node/' + self.node_id)

    def to_rdf(self) -> Graph:
        # TODO: generic URIs or URIs based on source namespace???
        node_uri = self.get_uri()
        source_uri = URIRef(self.node_source.value)
        class_uri = URIRef(self.node_type.value)
        node_id = Literal(self.node_name, None, XSD.string)

        g = Graph()
        g.add((node_uri, has_source, source_uri))
        g.add((source_uri, RDF.type, source_cls))
        g.add((node_uri, RDF.type, class_uri))
        g.add((node_uri, RDF.type, node_cls))
        g.add((class_uri, RDF.type, OWL.Class))
        g.add((node_uri, has_node_id, node_id))

        return g


class NodesReader:
    def __init__(self, nodes_file_path: str):
        self._nodes_by_index = {}

        with open(nodes_file_path) as nodes_file:
            csv_reader = csv.reader(nodes_file, delimiter=',', quotechar='"')
            for node_index, node_id, node_type_str, node_name, node_src_str in csv_reader:
                if node_index == 'node_index':
                    # then line is the header line
                    continue

                if csv_reader.line_num % 1000 == 0:
                    logger.info(f'read {csv_reader.line_num} lines')
                node_type = NodeType.get_type_by_id(node_type_str.strip())
                node_source = NodeSource.get_source_by_str(node_src_str.strip())
                node_index = int(node_index)
                node = Node(
                    node_index=node_index,
                    node_id=node_id,
                    node_type=node_type,
                    node_name=node_name,
                    node_source=node_source
                )
                assert self._nodes_by_index.get(node_index) is None

                self._nodes_by_index[node_index] = node

    def get_node_by_index(self, node_index: int) -> Node:
        return self._nodes_by_index[node_index]
