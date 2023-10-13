import csv
import dataclasses
import logging
from enum import Enum

from rdflib import URIRef, Graph

from primekgtordf import vocab
from primekgtordf.node import Node, NodesReader


logger = logging.getLogger(__name__)


class RelationType(Enum):
    ProteinProteinInteraction = vocab.ppi_cls
    DrugProteinInteraction = vocab.drug_protein_interaction_cls
    Contraindication = vocab.contraindication_cls
    Indication = vocab.indication_cls
    OffLabelUse = vocab.off_label_use_cls
    DrugDrugInteraction = vocab.drug_drug_interaction_cls
    PhenotypeProteinInteraction = vocab.phenotype_protein_interaction_cls
    PhenotypePhenotypeInteraction = vocab.phenotype_phenotype_interaction_cls

    NegativeDiseasePhenotypeInteraction = \
        vocab.negative_disease_phenotype_interaction_cls

    PositiveDiseasePhenotypeInteraction = \
        vocab.positive_disease_phenotype_interaction_cls

    DiseaseProteinInteraction = vocab.disease_protein_interaction_cls
    DiseaseDiseaseInteraction = vocab.disease_disease_interaction_cls
    DrugEffect = vocab.drug_effect_cls

    BioProcessBioProcessInteraction = \
        vocab.bioprocess_bioprocess_interaction_cls

    MolecularFunctionMolecularFunctionInteraction = \
        vocab.molecular_function_molecular_function_interaction_cls

    CellularComponentCellularComponentInteraction = \
        vocab.cellular_component_cellular_component_interaction_cls

    MolecularFunctionProteinInteraction = \
        vocab.molecular_function_protein_interaction_cls

    CellularComponentProteinInteraction = \
        vocab.cellular_component_protein_interaction_cls

    BioProcessProteinInteraction = vocab.bioprocess_protein_interaction_cls
    ExposureProteinInteraction = vocab.exposure_protein_interaction_cls
    ExposureDiseaseInteraction = vocab.exposure_disease_interaction_cls
    ExposureExposureInteraction = vocab.exposure_exposure_interaction_cls
    ExposureBioProcessInteraction = vocab.exposure_bio_process_interaction_cls

    ExposureMolecularFunctionInteraction = \
        vocab.exposure_molecular_function_interaction_cls

    ExposureCellularComponentInteraction = \
        vocab.exposure_cellular_component_interaction_cls

    PathwayPathwayInteraction = vocab.pathway_pathway_interaction_cls
    PathwayProteinInteraction = vocab.pathway_protein_interaction_cls
    AnatomyAnatomyInteraction = vocab.anatomy_anatomy_interaction_cls

    AnatomyPresentProteinInteraction = \
        vocab.anatomy_present_protein_interaction_cls

    AnatomyAbsentProteinInteraction = \
        vocab.anatomy_absent_protein_interaction_cls

    @classmethod
    def get_type_by_id(cls, relation_type_id: str):
        if relation_type_id == 'protein_protein':
            return cls.ProteinProteinInteraction
        elif relation_type_id == 'drug_protein':
            return cls.DrugProteinInteraction
        elif relation_type_id == 'contraindication':
            return cls.Contraindication
        elif relation_type_id == 'indication':
            return cls.Indication
        elif relation_type_id == 'off-label use':
            return cls.OffLabelUse
        elif relation_type_id == 'drug_drug':
            return cls.DrugDrugInteraction
        elif relation_type_id == 'phenotype_protein':
            return cls.PhenotypeProteinInteraction
        elif relation_type_id == 'phenotype_phenotype':
            return cls.PhenotypePhenotypeInteraction
        elif relation_type_id == 'disease_phenotype_negative':
            return cls.NegativeDiseasePhenotypeInteraction
        elif relation_type_id == 'disease_phenotype_positive':
            return cls.PositiveDiseasePhenotypeInteraction
        elif relation_type_id == 'disease_protein':
            return cls.DiseaseProteinInteraction
        elif relation_type_id == 'disease_disease':
            return cls.DiseaseDiseaseInteraction
        elif relation_type_id == 'drug_effect':
            return cls.DrugEffect
        elif relation_type_id == 'bioprocess_bioprocess':
            return cls.BioProcessBioProcessInteraction
        elif relation_type_id == 'molfunc_molfunc':
            return cls.MolecularFunctionMolecularFunctionInteraction
        elif relation_type_id == 'cellcomp_cellcomp':
            return cls.CellularComponentCellularComponentInteraction
        elif relation_type_id == 'molfunc_protein':
            return cls.MolecularFunctionProteinInteraction
        elif relation_type_id == 'cellcomp_protein':
            return cls.CellularComponentProteinInteraction
        elif relation_type_id == 'bioprocess_protein':
            return cls.BioProcessProteinInteraction
        elif relation_type_id == 'exposure_protein':
            return cls.ExposureProteinInteraction
        elif relation_type_id == 'exposure_disease':
            return cls.ExposureDiseaseInteraction
        elif relation_type_id == 'exposure_exposure':
            return cls.ExposureExposureInteraction
        elif relation_type_id == 'exposure_bioprocess':
            return cls.ExposureBioProcessInteraction
        elif relation_type_id == 'exposure_molfunc':
            return cls.ExposureMolecularFunctionInteraction
        elif relation_type_id == 'exposure_cellcomp':
            return cls.ExposureCellularComponentInteraction
        elif relation_type_id == 'pathway_pathway':
            return cls.PathwayPathwayInteraction
        elif relation_type_id == 'pathway_protein':
            return cls.PathwayProteinInteraction
        elif relation_type_id == 'anatomy_anatomy':
            return cls.AnatomyAnatomyInteraction
        elif relation_type_id == 'anatomy_protein_present':
            return cls.AnatomyPresentProteinInteraction
        elif relation_type_id == 'anatomy_protein_absent':
            return cls.AnatomyAbsentProteinInteraction
        else:
            raise NotImplementedError()


@dataclasses.dataclass
class Relation:
    subject: Node
    property: URIRef
    object_: Node
    relation_type: RelationType

    def to_rdf(self):
        g = Graph()

        g += self.subject.to_rdf()
        g += self.object_.to_rdf()
        g.add((self.subject.get_uri(), self.property, self.object_.get_uri()))

        # TODO: Add reification with relation type

        return g


class RelationsReader:
    def __init__(self, relations_file_path: str, nodes_reader: NodesReader):
        self._relations = []
        self._nodes_reader = nodes_reader

        with open(relations_file_path) as relations_file:
            csv_reader = csv.reader(relations_file, delimiter=',', quotechar='"')
            # relation,display_relation,x_index,y_index
            # protein_protein,ppi,0,8889
            # protein_protein,ppi,1,2798
            # protein_protein,ppi,2,5646
            # protein_protein,ppi,3,11592
            # protein_protein,ppi,4,2122
            for relation_type_str, relation_type_abbrv, subj_node_idx, obj_node_idx in csv_reader:

                if relation_type_str == 'relation' and \
                        relation_type_abbrv == 'display_relation':
                    # then we just read the header line
                    continue

                if csv_reader.line_num % 1000 == 0:
                    logger.info(f'read {csv_reader.line_num} lines')

                relation_type = RelationType.get_type_by_id(relation_type_str)
                property_uri = vocab.get_property(relation_type_abbrv)

                subj_node = nodes_reader.get_node_by_index(int(subj_node_idx))
                obj_node = nodes_reader.get_node_by_index(int(obj_node_idx))

                relation = Relation(
                    subject=subj_node,
                    property=property_uri,
                    object_=obj_node,
                    relation_type=relation_type
                )

                self._relations.append(relation)

    def get_relations(self):
        return self._relations

    def to_rdf(self):
        g = Graph()

        cntr = 0
        for relation in self._relations:
            cntr += 1
            g += relation.to_rdf()
            if cntr % 1000 == 0:
                logger.info(
                    f'Generated RDF triples for {cntr} relations (and their '
                    f'referenced nodes)')

        return g
