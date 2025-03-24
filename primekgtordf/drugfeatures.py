import csv
import logging

from rdflib import Graph, Literal

from primekgtordf.node import NodesReader
from primekgtordf.vocab import has_drug_description

logger = logging.getLogger(__name__)


class DrugFeaturesReader:
    def __init__(self, drug_features_file_path: str, nodes_reader: NodesReader):
        with open(drug_features_file_path) as drug_features_file:
            csv_reader = csv.reader(drug_features_file, delimiter=',', quotechar='"')

            self._g = Graph()

            for node_index, description, half_life, indication, \
                    mechanism_of_action, protein_binding, pharmacodynamics, \
                    state, atc_1, atc_2, atc_3, atc_4, category, group, \
                    pathway, molecular_weight, tpsa, clogp in csv_reader:

                if node_index == 'node_index':
                    continue

                if csv_reader.line_num % 1000 == 0:
                    logger.info(f'read {csv_reader.line_num} lines')

                # e.g. '27165'
                if node_index in [None, '']:
                    # if we don't have a node index we cannot attach the
                    # disease features to any resource
                    continue

                node = nodes_reader.get_node_by_index(int(node_index))

                if node is None:
                    continue

                node_uri = node.get_uri()

                # description (e.g. 'Copper is a transition metal and a trace element in the body. It is important to
                # the function of many enzymes including ...', 'Flunisolide (marketed as AeroBid, Nasalide, Nasarel) is
                # a corticosteroid with anti-inflammatory actions. It is often prescribed as ...')
                if description != '':
                    description_literal = Literal(description, 'en')
                    self._g.add((node_uri, has_drug_description, description_literal))

                # half_life (e.g. 'The half-life is approximately 122.24 seconds', 'The half-life is 1.8 hours')
                #   -> ignored

                # indication (e.g. 'For use in the supplementation of total parenteral nutrition and in contraception
                # with intrauterine devices.', 'Oxygen therapy in clinical settings is used across diverse specialties,
                # including various types of anoxia, hypoxia or dyspnea and ...')
                #   -> ignored

                # mechanism_of_action (e.g. 'Copper is absorbed from the gut via high affinity copper uptake protein
                # and likely through low affinity copper uptake protein and ...', 'Oxygen therapy increases the arterial
                # pressure of oxygen and is effective in improving gas exchange and oxygen delivery to ...')
                #   -> ignored

                # protein_binding ('Copper is nearly entirely bound by ceruloplasmin (65-90%), plasma albumin (18%),
                # and alpha 2-macroglobulin (12%).', 'Oxygen binds to oxygen-carrying protein in red blood cells called
                # hemoglobin with high affinity. The amount of oxygen molecules bound to the fixed amount of ...')
                #   -> ignored

                # pharmacodynamics (e.g. 'Copper is incorporated into many enzymes throughout the body as an essential
                # part of their function. Copper ions are known to reduce fertility when released ...', 'Oxygen therapy
                # improves effective cellular oxygenation, even at a low rate of tissue perfusion. Oxygen molecules
                # adjust hypoxic ventilatory ...')
                #   -> ignored

                # state (e.g. 'Copper is a solid.', 'Oxygen is a gas.')
                #   -> ignored

                # atc_1 (e.g. 'Oxygen is anatomically related to various.', 'Flunisolide is anatomically related to
                # respiratory system and respiratory system.')
                #   -> ignored

                # atc_2 (e.g. 'Oxygen is in the therapeutic group of all other therapeutic products.', 'Flunisolide is
                # in the therapeutic group of nasal preparations and drugs for obstructive airway diseases.')
                #   -> ignored

                # atc_3 (e.g. 'Oxygen is pharmacologically related to all other therapeutic products.', 'Flunisolide is
                # pharmacologically related to decongestants and other nasal preparations for topical use and other
                # drugs for obstructive airway diseases, inhalants.')
                #   -> ignored

                # atc_4 (e.g. 'The chemical and functional group of  is medical gases.', 'The chemical and functional
                # group of  is corticosteroids, moderately potent (group ii) and corticosteroids, plain.')
                #   -> ignored

                # category (e.g. 'Copper is part of Copper-containing Intrauterine Device ; Decreased Embryonic
                # Implantation ; Decreased Sperm Motility ; Diet, Food, and Nutrition ; Elements ; Food ; Food and
                # Beverages ; Growth Substances ; Inhibit Ovum Fertilization ; Metals ; Metals, Heavy ; Micronutrients ;
                # Minerals ; Physiological Phenomena ; Replacement Preparations ; Trace Elements ; Transition
                # Elements.', ''Oxygen is part of Chalcogens ; Elements ; Gases ; Medical Gases ; Miscellaneous
                # Therapeutic Agents ; Other Miscellaneous Therapeutic Agents.')
                #   -> ignored

                # group (e.g. 'Copper is approved and investigational.', 'Oxygen is approved and vet_approved.')
                #   -> ignored

                # pathway (e.g. 'Prednisone uses Prednisone Action Pathway ; Prednisone Metabolism Pathway.',
                # 'Hydrocortisone uses Adrenal Hyperplasia Type 5 or Congenital Adrenal Hyperplasia Due to 17
                # alpha-Hydroxylase Deficiency ; Corticosterone Methyl Oxidase I Deficiency (CMO I) ;
                # 3-beta-Hydroxysteroid Dehydrogenase Deficiency ; Corticotropin Activation of Cortisol Production ;
                # Congenital Lipoid Adrenal Hyperplasia (CLAH) or Lipoid CAH ; 11-beta-Hydroxylase Deficiency
                # (CYP11B1) ; Apparent Mineralocorticoid Excess Syndrome ; Steroidogenesis ; ...')
                #   -> ignored

                # molecular_weight (e.g 'The molecular weight is 32.0.', 'The molecular weight is 434.5.')
                #   -> ignored

                # tpsa (e.g. 'Oxygen has a topological polar surface area of 34.14.', 'Flunisolide has a topological
                # polar surface area of 93.06.')
                #   -> ignored

                # clogp (e.g. 'The log p value of  is 2.41.', 'The log p value of  is 3.36.')
                #   -> ignored

    def to_rdf(self) -> Graph:
        return self._g
