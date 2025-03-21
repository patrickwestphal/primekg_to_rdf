import csv
import logging

from rdflib import Graph, Literal

from primekgtordf import PRIMEKG_URI_PREFIX
from primekgtordf.node import NodesReader
from primekgtordf.vocab import has_mondo_id, has_mondo_name, has_group_name_bert, has_mondo_definition, \
    has_umls_description, has_orphanet_definition, has_orphanet_clinical_description

logger = logging.getLogger(__name__)


class DiseaseFeaturesReader:
    def __init__(self, disease_features_file_path: str, nodes_reader: NodesReader):
        with open(disease_features_file_path) as disease_features_file:
            csv_reader = csv.reader(disease_features_file, delimiter=',', quotechar='"')

            self._g = Graph()

            # node_index,mondo_id,
            #   mondo_name,group_id_bert,group_name_bert,
            #       mondo_definition,
            #       umls_description,
            #       orphanet_definition,
            #           orphanet_prevalence,orphanet_epidemiology,orphanet_clinical_description,orphanet_management_and_treatment,mayo_symptoms,mayo_causes,mayo_risk_factors,mayo_complications,mayo_prevention,mayo_see_doc
            # 27165,8019,
            #   mullerian aplasia and hyperandrogenism,,,
            #       "Deficiency of the glycoprotein WNT4, associated with loss \
            #           of function mutation(s) in the WNT4 gene. The \
            #           condition in 46,XX individuals is characterized by \
            #           mild hyperandrogenism, absence of underdevelopment of \
            #           the uterus, and sometimes absence of underdevelopment \
            #           of the vagina.",
            #       "Deficiency of the glycoprotein wnt4, associated with loss \
            #           of function mutation in the wnt4 gene. The condition \
            #           in 46,xx individuals is characterized by mild \
            #           hyperandrogenism, absence of underdevelopment of the \
            #           uterus, and sometimes absence of underdevelopment of \
            #           the vagina.",
            #       "A rare syndrome with 46,XX disorder of sex development \
            #           characterized by Müllerian duct hypoplasia or agenesis \
            #           associated with clinical and biological evidence of \
            #           hyperandrogenism in 46,XX females. Patients present \
            #           with hypoplastic or absent uterus, variable \
            #           abnormalities of other reproductive organs, primary \
            #           amenorrhea, acne, hirsutism, and sometimes renal \
            #           anomalies. External genitalia and secondary sexual \
            #           characteristics are normal. Hormonal analysis shows \
            #           variably elevated serum levels of androstenedione, \
            #           dehydroepiandrosterone, and/or total and free \
            #           testosterone.",,,,,,,,,,
            # 27166,11043,
            #   "myelodysplasia, immunodeficiency, facial dysmorphism, \
            #       short stature, and psychomotor delay",
            #       ,
            #       ,
            #       ,
            #           ,,,,,,,,,,,
            # 27168,8878,
            #   "bone dysplasia, lethal Holmgren type",
            #       ,
            #       ,
            #       "Bone dysplasia lethal Holmgren type (BDLH) is a lethal \
            #           bone dysplasia characterized at birth by low birth \
            #           weight, a rhizomelic dwarfism, bent femora and short \
            #           chest producing asphyxia. It was described in three \
            #           siblings from healthy, non-consanguineous parents of \
            #           Finnish and in four siblings from non-consanguineous \
            #           parents of French origin with no family history of \
            #           dwarfism. The initial cases could have been diagnosed \
            #           as Desbuquois syndrome, or a recessive Larsen syndrome. \
            #           There has been no further description of BDLH in the \
            #           literature since 1988.",
            #       "A lethal bone dysplasia with characteristics of low birth \
            #           weight, rhizomelic dwarfism, bent femora and short \
            #           chest producing asphyxia. The disease has been \
            #           described in three siblings from healthy, \
            #           non-consanguineous parents of Finnish origin and in \
            #           four siblings from non-consanguineous parents of \
            #           French origin with no family history of dwarfism. \
            #           There has been no further description of this disease \
            #           in the literature since 1988.",
            #       "Bone dysplasia lethal Holmgren type (BDLH) is a lethal \
            #           bone dysplasia characterized at birth by low birth \
            #           weight, a rhizomelic dwarfism, bent femora and short \
            #           chest producing asphyxia. It was described in three \
            #           siblings from healthy, non-consanguineous parents of \
            #           Finnish and in four siblings from non-consanguineous \
            #           parents of French origin with no family history of \
            #           dwarfism. The initial cases could have been diagnosed \
            #           as Desbuquois syndrome, or a recessive Larsen syndrome. \
            #           There has been no further description of BDLH in the \
            #           literature since 1988."
            #           ,<1/1000000,,,,,,,,,
            # 27169,8905,
            #   predisposition to invasive fungal disease due to CARD9 deficiency,
            #       ,
            #       ,
            #       ,
            #         ,"A rare, genetic primary immunodeficiency characterized \
            #           by increased susceptibility to fungal infections, \
            #           typically manifesting as recurrent, chronic \
            #           mucocutaneous candidiasis, systemic candidiasis with \
            #           meningoencephalitis, and deep dermatophystosis with \
            #           dermatophytes invading skin, hair, nails, lymph nodes, \
            #           and brain, resulting in erythematosquamous lesions, \
            #           nodular subcutaneous or ulcerative infiltrations, \
            #           severe onychomycosis, and lymphadenopathy.",,,,,,,,,,
            for node_index, mondo_id, mondo_name, group_id_bert, \
                    group_name_bert, mondo_definition, umls_description, \
                    orphanet_definition, orphanet_prevalence, \
                    orphanet_epidemiology, orphanet_clinical_description, \
                    orphanet_management_and_treatment, mayo_symptoms, \
                    mayo_causes, mayo_risk_factors, mayo_complications, \
                    mayo_prevention, mayo_see_doc in csv_reader:

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

                # mondo_id (e.g. '8019')
                if mondo_id != '':
                    mondo_id_literal = Literal(mondo_id)
                    self._g.add((node_uri, has_mondo_id, mondo_id_literal))

                # mondo_name (e.g. 'mullerian aplasia and hyperandrogenism')
                if mondo_name != '':
                    mondo_name_literal = Literal(mondo_name, 'en')
                    self._g.add((node_uri, has_mondo_name, mondo_name_literal))

                # group_id_bert (e.g. '13924_12592_14672_13460_12591_12536_30861_8146_8148_32846_13459_44329_14544_9805_49223_9804_14086_8147_13515_14029_12581_19019')
                #   -> ignored

                # group_name_bert (e.g. 'osteogenesis imperfecta', 'autosomal recessive nonsyndromic deafness')
                if group_name_bert != '':
                    group_name_bert_literal = Literal(group_name_bert, 'en')
                    self._g.add((node_uri, has_group_name_bert, group_name_bert_literal))

                # mondo_definition (e.g. 'Deficiency of the glycoprotein WNT4, ...')
                if mondo_definition != '':
                    mondo_definition_literal = Literal(mondo_definition, 'en')
                    self._g.add((node_uri, has_mondo_definition, mondo_definition_literal))

                # umls_description (e.g. 'Deficiency of the glycoprotein wnt4, ...')
                if umls_description != '':
                    umls_description_literal = Literal(umls_description, 'en')
                    self._g.add((node_uri, has_umls_description, umls_description_literal))

                # orphanet_definition (e.g. 'A rare syndrome with 46,XX disorder ...')
                if orphanet_definition != '':
                    orphanet_definition_literal = Literal(orphanet_definition, 'en')
                    self._g.add((node_uri, has_orphanet_definition, orphanet_definition_literal))

                # orphanet_prevalence (e.g. '<1/1000000') -> ignored

                # orphanet_epidemiology (e.g. 'Only 5 cases have been described to date.',
                # 'It has been reported in less than 10 families.', 'The prevalence of cherubism is unknown and ...')
                #   -> ignored

                # orphanet_clinical_description (e.g. 'Radiographs show bowing of long bones, platyspondyly and ...',
                # 'At birth, clinical features are similar to those of classical EI with erythroderma, blistering and ...')
                if orphanet_clinical_description != '':
                    orphanet_clinical_description_literal = Literal(orphanet_clinical_description, 'en')
                    self._g.add((node_uri, has_orphanet_clinical_description, orphanet_clinical_description_literal))

                # orphanet_management_and_treatment (e.g. 'Clinical and radiographic monitoring is recommended during
                # the growth phase ...', 'No curative or palliative options exist for HJMD. However, ...')
                #   -> ignored

                # mayo_symptoms (e.g. 'People with myoclonus often describe their signs and symptoms as jerks, shakes
                # or spasms that are...', 'The signs of craniosynostosis are usually noticeable at birth, but ...')
                #   -> ignored

                # mayo_causes (e.g. 'Myoclonus may be caused by a variety of underlying problems. Doctors often ...',
                # "Often the cause of craniosynostosis is not known, but sometimes it's related to genetic
                # disorders. ...")
                #   -> ignored

                # mayo_risk_factors (e.g. 'If untreated, craniosynostosis may cause, for example: Permanent head and
                # facial deformity, ...', 'Factors that increase your risk of amyloidosis include: Age. Most people
                # diagnosed with amyloidosis are between ages 60 and 70, although ...')
                #   -> ignored

                # mayo_complications (e.g. 'The potential complications of amyloidosis depend on which organs the
                # amyloid deposits affect. Amyloidosis can seriously damage your: Heart. ...', 'Untreated, intestinal
                # obstruction can cause serious, life-threatening complications, including: Tissue death. ...')
                #   -> ignored

                # mayo_prevention (e.g. 'The most effective way to prevent tachycardia is to maintain a healthy heart
                # and reduce your risk of developing heart disease. ...', 'If you have had or you are going to have
                # cancer surgery, ask your doctor whether your procedure will involve your lymph nodes or lymph
                # vessels. Ask if your radiation treatment will be ...')
                #   -> ignored

                # mayo_see_doc (e.g. 'When to see a doctor, If your myoclonus symptoms become frequent and
                # persistent, talk to your doctor ...', "When to see a doctor, Your doctor will routinely monitor your
                # child's head growth at well-child visits. Talk to your pediatrician if ...")
                #   -> ignored

    def to_rdf(self) -> Graph:
        return self._g
