import logging
import os
from django.conf import settings


#root = '/home/983869/SOP_PROD_V2'
root = "/home/983869/Workspace1/DjangoWK/mysite/Demo/Models"
log_file = root + "/wk.log"
log_file_daily = root + "/log/wk_daily.log"
attachment_model_path = root + "/attachment/model/FINAL6.pkl"
attachment_feature_path = root+ "/attachment/feature/FINAL6.pickle"
bootstrap_servers = 'localhost:9092'
auto_offset_reset = 'latest'
state_code_dictionary = {'AL': 'ALABAMA', 'MO': 'MISSOURI', 'AK': 'ALASKA', 'MT': 'MONTANA', 'AZ': 'ARIZONA',
                         'NE': 'NEBRASKA', 'AR': 'ARKANSAS', 'NV': 'NEVADA', 'CA': 'CALIFORNIA', 'NH': 'NEW HAMPSHIRE',
                         'CO': 'COLORADO', 'NJ': 'NEW JERSEY', 'CT': 'CONNECTICUT', 'NM': 'NEW MEXICO',
                         'DE': 'DELAWARE', 'NY': 'NEW YORK', 'NC': 'NORTH CAROLINA', 'ND': 'NORTH DAKOTA',
                         'GA': 'GEORGIA', 'OH': 'OHIO', 'HI': 'HAWAII', 'OK': 'OKLAHOMA', 'ID': 'IDAHO', 'OR': 'OREGON',
                         'IL': 'ILLINOIS', 'PA': 'PENNSYLVANIA', 'IN': 'INDIANA', 'RI': 'RHODE ISLAND', 'IA': 'IOWA',
                         'SC': 'SOUTH CAROLINA', 'KS': 'KANSAS', 'SD': 'SOUTH DAKOTA', 'KY': 'KENTUCKY',
                         'TN': 'TENNESSEE', 'LA': 'LOUISIANA', 'TX': 'TEXAS', 'ME': 'MAINE', 'UT': 'UTAH',
                         'MD': 'MARYLAND', 'VT': 'VERMONT', 'MA': 'MASSACHUSETTS', 'VA': 'VIRGINIA', 'MI': 'MICHIGAN',
                         'WA': 'WASHINGTON', 'MN': 'MINNESOTA', 'WV': 'WEST VIRGINIA', 'FL': 'FLORIDA',
                         'MS': 'MISSISSIPPI', 'WI': 'WISCONSIN', 'WY': 'WYOMING'}
jurisdiction_model_path = root+ "/jurisdiction/model/Randomforestmodel_model.pkl"
jurisdiction_feature_path = root+"/jurisdiction/feature/feature_set.pickle"
connecticut = "CONNECTICUT"
lawsuit_feature_path = root + '/lawsuit/feature/TfidfModel_LawSuit.pkl'
lawsuit_model_path = root + '/lawsuit/model/RandomForestClassifierModel_LawSuit.pkl'

cs_juri_specialcase = 0.8

MAX_FILL_COUNT = 4

pdf_count =1000

vendor_id = 20655


log_level = logging.INFO
case_model_path = root + '/casenumber/model/RandomForestClassifierModel_CaseNumberV2.pkl'
case_feature_path = root + '/casenumber/feature/CountVectorizerModel_CaseNumberV2.pkl'
case_model_ngram1 = root + '/casenumber/model/RF_model_1gram.pkl'
case_tfidf1 = root + '/casenumber/feature/TFIDF_model_1gram.pkl'
case_model_ngram2 = root + '/casenumber/model/RF_model_2gram.pkl'
case_tfidf2 = root + '/casenumber/feature/TFIDF_model_2gram.pkl'

docpath = root + '/tmpPDFDocs'
'''
error_code1 = "not able to read pdf"
error_code2 = "processing issue"
error_code3 = "mysql insert issue".
error_code4 = "other issues"
'''
error_code1 = 001
error_code2 = 002
error_code3 = 003
error_code4 = 004

error_log_id  = 1


pldf_RFv4= root + '/plfdfd/features/RFv4.pkl'
pldf_text_vectorizer=root + '/plfdfd/features/Text_vectorizer_pltfv4.pkl'
pldf_top_vectorizer=root + '/plfdfd/features/Top_vectorizer_pltfv4.pkl'
pldf_below_vectorizer=root + '/plfdfd/features/Below_vectorizer_pltfv4.pkl'
dftd_text_vectorizer=root + '/plfdfd/features/Text_vectorizer_dftdv4.pkl'
dftd_top_vectorizer=root + '/plfdfd/features/Top_vectorizer_dftdv4.pkl'
dftd_below_vectorizer=root + '/plfdfd/features/Below_vectorizer_dftdv4.pkl'
pldfdftd_text_vectorizer=root + '/plfdfd/features/Text_vectorizer_zerov4.pkl'
pldfdftd_top_vectorizer=root + '/plfdfd/features/Top_vectorizer_zerov4.pkl'
pldfdftd_below_vectorizer=root + '/plfdfd/features/Below_vectorizer_zerov4.pkl'


dftd_filter_RF = root + '/plfdfd/Defendant_filter/RF.pkl'
dftd_filter_text = root + '/plfdfd/Defendant_filter/Text_vectorizer.pkl'
dftd_filter_top = root + '/plfdfd/Defendant_filter/Top_vectorizer.pkl'
dftd_filer_below = root + '/plfdfd/Defendant_filter/Below_vectorizer.pkl'


pltfdftd_model = root + "/plfdfd/models/Randomforestmodel_model_final.pkl"
pltfdftd_feature = root + "/plfdfd/features/feature_set_final.pickle"

pltf_filter_RF = root + '/plfdfd/Plaintiff_filter/RF.pkl'
pltf_filter_text = root + '/plfdfd/Plaintiff_filter/Text_vectorizer.pkl'
pltf_filter_top = root + '/plfdfd/Plaintiff_filter/Top_vectorizer.pkl'
pltf_filer_below = root + '/plfdfd/Plaintiff_filter/Below_vectorizer.pkl'

country_list = root + '/county_list.txt'
