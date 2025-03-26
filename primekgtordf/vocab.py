from urllib.parse import urlencode, quote

from rdflib import URIRef, Graph, RDF, OWL, RDFS, XSD

from primekgtordf import PRIMEKG_URI_PREFIX

node_cls = URIRef(PRIMEKG_URI_PREFIX + 'vocab/Node')
source_cls = URIRef(PRIMEKG_URI_PREFIX + 'vocab/Source')
ppi_cls = URIRef(PRIMEKG_URI_PREFIX + 'vocab/ProteinProteinInteraction')

drug_protein_interaction_cls = \
    URIRef(PRIMEKG_URI_PREFIX + 'vocab/DrugProteinInteraction')

contraindication_cls = URIRef(PRIMEKG_URI_PREFIX + 'vocab/Contraindication')
indication_cls = URIRef(PRIMEKG_URI_PREFIX + 'vocab/Indication')
off_label_use_cls = URIRef(PRIMEKG_URI_PREFIX + 'vocab/OffLabelUse')

phenotype_protein_interaction_cls = \
    URIRef(PRIMEKG_URI_PREFIX + 'vocab/PhenotypeProteinInteraction')

drug_drug_interaction_cls = \
    URIRef(PRIMEKG_URI_PREFIX + 'vocab/DrugDrugInteraction')

phenotype_phenotype_interaction_cls = \
    URIRef(PRIMEKG_URI_PREFIX + 'vocab/PhenotypePhenotypeInteraction')

negative_disease_phenotype_interaction_cls = \
    URIRef(PRIMEKG_URI_PREFIX + 'vocab/NegativeDiseasePhenotypeInteraction')

positive_disease_phenotype_interaction_cls = \
    URIRef(PRIMEKG_URI_PREFIX + 'vocab/PositiveDiseasePhenotypeInteraction')

disease_protein_interaction_cls = \
    URIRef(PRIMEKG_URI_PREFIX + 'vocab/DiseaseProteinInteraction')

disease_disease_interaction_cls = \
    URIRef(PRIMEKG_URI_PREFIX + 'vocab/DiseaseDiseaseInteraction')

drug_effect_cls = URIRef(PRIMEKG_URI_PREFIX + 'vocab/DrugEffect')

bioprocess_bioprocess_interaction_cls = \
    URIRef(PRIMEKG_URI_PREFIX + 'vocab/BioProcessBioProcessInteraction')

molecular_function_molecular_function_interaction_cls = \
    URIRef(
        PRIMEKG_URI_PREFIX +
        'vocab/MolecularFunctionMolecularFunctionInteraction'
    )

cellular_component_cellular_component_interaction_cls = \
    URIRef(
        PRIMEKG_URI_PREFIX +
        'vocab/CellularComponentCellularComponentInteraction'
    )

molecular_function_protein_interaction_cls = \
    URIRef(PRIMEKG_URI_PREFIX, 'vocab/MolecularFunctionProteinInteraction')

cellular_component_protein_interaction_cls = \
    URIRef(PRIMEKG_URI_PREFIX + 'vocab/CellularComponentProteinInteraction')

bioprocess_protein_interaction_cls = \
    URIRef(PRIMEKG_URI_PREFIX + 'vocab/BioProcessProteinInteraction')

exposure_protein_interaction_cls = \
    URIRef(PRIMEKG_URI_PREFIX + 'vocab/ExposureProteinInteraction')

exposure_disease_interaction_cls = \
    URIRef(PRIMEKG_URI_PREFIX + 'vocab/ExposureDiseaseInteraction')

exposure_exposure_interaction_cls = \
    URIRef(PRIMEKG_URI_PREFIX + 'vocab/ExposureExposureInteraction')

exposure_bio_process_interaction_cls = \
    URIRef(PRIMEKG_URI_PREFIX + 'vocab/ExposureBioProcessInteraction')

exposure_molecular_function_interaction_cls = \
    URIRef(PRIMEKG_URI_PREFIX + 'vocab/ExposureMolecularFunctionInteraction')

exposure_cellular_component_interaction_cls = \
    URIRef(PRIMEKG_URI_PREFIX + 'vocab/ExposureCellularComponentInteraction')

pathway_pathway_interaction_cls = \
    URIRef(PRIMEKG_URI_PREFIX + 'vocab/PathwayPathwayInteraction')

pathway_protein_interaction_cls = \
    URIRef(PRIMEKG_URI_PREFIX + 'vocab/PathwayProteinInteraction')

anatomy_anatomy_interaction_cls = \
    URIRef(PRIMEKG_URI_PREFIX + 'vocab/AnatomyAnatomyInteraction')

anatomy_present_protein_interaction_cls = \
    URIRef(PRIMEKG_URI_PREFIX + 'vocab/AnatomyPresentProteinInteraction')

anatomy_absent_protein_interaction_cls = \
    URIRef(PRIMEKG_URI_PREFIX + 'vocab/AnatomyAbsentProteinInteraction')

has_source = URIRef(PRIMEKG_URI_PREFIX + 'vocab/has_source')
has_node_name = URIRef(PRIMEKG_URI_PREFIX + 'vocab/has_node_name')

has_mondo_id = URIRef(PRIMEKG_URI_PREFIX + 'vocab/has_mondo_id')
has_mondo_name = URIRef(PRIMEKG_URI_PREFIX + 'vocab/has_mondo_name')
has_group_name_bert = URIRef(PRIMEKG_URI_PREFIX + 'vocab/has_group_name_bert')
has_mondo_definition = URIRef(PRIMEKG_URI_PREFIX + 'vocab/has_mondo_definition')
has_umls_description = URIRef(PRIMEKG_URI_PREFIX + 'vocab/has_umls_description')

has_orphanet_definition = URIRef(
    PRIMEKG_URI_PREFIX + 'vocab/has_orphanet_definition'
)

has_orphanet_clinical_description = URIRef(
    PRIMEKG_URI_PREFIX + 'vocab/has_orphanet_clinical_description'
)

has_drug_description = URIRef(PRIMEKG_URI_PREFIX + 'vocab/has_drug_description')


class UnknownVocabularyElementException(Exception):
    pass


_known_property_abbreviations = [
    'ppi',
    'carrier',
    'enzyme',
    'target',
    'transporter',
    'contraindication',
    'indication',
    'off-label use',
    'synergistic interaction',
    'associated with',
    'parent-child',
    'phenotype absent',
    'phenotype present',
    'side effect',
    'interacts with',
    'linked to',
    'expression present',
    'expression absent',
]


def get_property(property_abbrv_str: str):
    if property_abbrv_str not in _known_property_abbreviations:
        raise UnknownVocabularyElementException()
    return URIRef(PRIMEKG_URI_PREFIX + 'vocab/' + quote(property_abbrv_str))


def get_vocab_triples():
    g = Graph()

    g.add((node_cls, RDF.type, OWL.Class))
    g.add((source_cls, RDF.type, OWL.Class))
    g.add((ppi_cls, RDF.type, OWL.Class))
    g.add((drug_protein_interaction_cls, RDF.type, OWL.Class))
    g.add((contraindication_cls, RDF.type, OWL.Class))
    g.add((indication_cls, RDF.type, OWL.Class))
    g.add((off_label_use_cls, RDF.type, OWL.Class))
    g.add((drug_drug_interaction_cls, RDF.type, OWL.Class))
    g.add((phenotype_phenotype_interaction_cls, RDF.type, OWL.Class))
    g.add((negative_disease_phenotype_interaction_cls, RDF.type, OWL.Class))
    g.add((positive_disease_phenotype_interaction_cls, RDF.type, OWL.Class))
    g.add((disease_protein_interaction_cls, RDF.type, OWL.Class))
    g.add((disease_disease_interaction_cls, RDF.type, OWL.Class))
    g.add((drug_effect_cls, RDF.type, OWL.Class))
    g.add((bioprocess_bioprocess_interaction_cls, RDF.type, OWL.Class))
    g.add((
        molecular_function_molecular_function_interaction_cls,
        RDF.type,
        OWL.Class
    ))
    g.add((
        cellular_component_cellular_component_interaction_cls,
        RDF.type,
        OWL.Class
    ))
    g.add((molecular_function_protein_interaction_cls, RDF.type, OWL.Class))
    g.add((cellular_component_protein_interaction_cls, RDF.type, OWL.Class))
    g.add((bioprocess_protein_interaction_cls, RDF.type, OWL.Class))
    g.add((exposure_protein_interaction_cls, RDF.type, OWL.Class))
    g.add((exposure_disease_interaction_cls, RDF.type, OWL.Class))
    g.add((exposure_exposure_interaction_cls, RDF.type, OWL.Class))
    g.add((exposure_bio_process_interaction_cls, RDF.type, OWL.Class))
    g.add((exposure_molecular_function_interaction_cls, RDF.type, OWL.Class))
    g.add((exposure_cellular_component_interaction_cls, RDF.type, OWL.Class))
    g.add((pathway_pathway_interaction_cls, RDF.type, OWL.Class))
    g.add((pathway_protein_interaction_cls, RDF.type, OWL.Class))
    g.add((anatomy_anatomy_interaction_cls, RDF.type, OWL.Class))
    g.add((anatomy_present_protein_interaction_cls, RDF.type, OWL.Class))
    g.add((anatomy_absent_protein_interaction_cls, RDF.type, OWL.Class))

    g.add((has_source, RDF.type, OWL.ObjectProperty))
    g.add((has_source, RDFS.domain, OWL.Class))
    g.add((has_source, RDFS.range, source_cls))

    g.add((has_node_id, RDF.type, OWL.DatatypeProperty))
    g.add((has_node_id, RDFS.domain, node_cls))
    g.add((has_node_id, RDFS.range, XSD.string))

    g.add((has_mondo_id, RDF.type, OWL.DatatypeProperty))
    g.add((has_mondo_id, RDFS.domain, node_cls))
    g.add((has_mondo_id, RDFS.range, XSD.string))

    g.add((has_mondo_name, RDF.type, OWL.DatatypeProperty))
    g.add((has_mondo_name, RDFS.domain, node_cls))
    g.add((has_mondo_name, RDFS.range, XSD.string))

    g.add((has_group_name_bert, RDF.type, OWL.DatatypeProperty))
    g.add((has_group_name_bert, RDFS.domain, node_cls))
    g.add((has_group_name_bert, RDFS.range, XSD.string))

    g.add((has_mondo_definition, RDF.type, OWL.DatatypeProperty))
    g.add((has_mondo_definition, RDFS.domain, node_cls))
    g.add((has_mondo_definition, RDFS.range, XSD.string))

    g.add((has_umls_description, RDF.type, OWL.DatatypeProperty))
    g.add((has_umls_description, RDFS.domain, node_cls))
    g.add((has_umls_description, RDFS.range, XSD.string))

    g.add((has_orphanet_definition, RDF.type, OWL.DatatypeProperty))
    g.add((has_orphanet_definition, RDFS.domain, node_cls))
    g.add((has_mondo_definition, RDFS.range, XSD.string))

    g.add((has_orphanet_clinical_description, RDF.type, OWL.DatatypeProperty))
    g.add((has_orphanet_clinical_description, RDFS.domain, node_cls))
    g.add((has_orphanet_clinical_description, RDFS.range, XSD.string))

    g.add((has_drug_description, RDF.type, OWL.DatatypeProperty))
    g.add((has_drug_description, RDFS.domain, node_cls))
    g.add((has_drug_description, RDFS.range, XSD.string))

    for prop_abbrv_str in _known_property_abbreviations:
        prop = get_property(prop_abbrv_str)
        g.add((prop, RDF.type, OWL.ObjectProperty))
        g.add((prop, RDFS.domain, node_cls))
        g.add((prop, RDFS.range, node_cls))

    return g
