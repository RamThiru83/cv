# Public-edition data loader for the automatic CV rebuild.
# All CV content comes from the published cv_data.json (CV_JSON); nothing private is stored here.
import os, json
_p = os.environ.get('CV_JSON', 'cv_data.json')
_j = json.load(open(_p, encoding='utf-8'))
globals().update(_j)
CHAPTERS = ['Essential Diagnostics List 2019-20 for the World Health Organization, South-East Asia Region (co-author).']
TRAINING = [['EpiCap pedagogy workshop: analytic epidemiology for causal inference, teaching for learning',
  'Bergen, Norway; 16-23 February 2024',
  'University of Bergen'],
 ['Fundamental concepts in medical statistics with applications to RCTs (co-facilitator)',
  'Kampala, Uganda; 7-13 June 2023',
  'University of Bergen; Makerere University'],
 ['Advanced epidemiology and causal inference', 'Bergen, Norway; 25-29 April 2022', 'University of Bergen'],
 ['Introduction to modern epidemiology and clinical research methodology', 'Bergen, Norway; 20-22 April 2022', 'University of Bergen'],
 ['Short course series on environmental exposure assessment', 'PHFI, Gurugram; Oct and Dec 2018', 'ISEE, PHFI, CCDC'],
 ['NIH-ICMR-THSTI course on principles and practice of clinical research', 'Hyderabad; 16-21 April 2018', 'NIH, USA and ICMR'],
 ['Data Science specialisation (online)', 'June-September 2017', 'Johns Hopkins Bloomberg School of Public Health']]

# Publications used in the short formats (matched by title so the list can grow without breaking)
KEY_TITLES = ['Incidence of and risk factors for small vulnerable newborns in north India: a secondary analysis of a prospective pregnancy cohort',
 'Development and external validation of Indian population-specific Garbhini-GA2 model for estimating gestational age in second and third trimesters',
 'Effectiveness of ChAdOx1 nCoV-19 vaccine against SARS-CoV-2 infection during the delta (B.1.617.2) variant surge in India: a test-negative, '
 'case-control study and a mechanistic study of post-vaccination immune responses',
 'Clinical and experimental evidence suggest omicron variant of SARS-CoV-2 is inherently less pathogenic than delta variant independent of previous '
 'immunity',
 'Prediction of spontaneous preterm birth in the second trimester: current models, limitations, and the way forward',
 'Prediction models for gestational diabetes mellitus: diagnostic utility of clinical and biochemical markers',
 'Deciphering mechanisms leading to preterm birth through post-GWAS integration of multi-omics data',
 'Genetic variants associated with spontaneous preterm birth in women from India: a prospective cohort study',
 'Association between gestational weight gain and adverse pregnancy outcomes: cohort analysis from South Asia and sub-Saharan Africa',
 'Gestational weight gain trajectories in GARBH-Ini pregnancy cohort in North India and a comparative analysis with global references']
_titles = [p[1] for p in PUBS]
KEY_PUB_IDX = [_titles.index(t) for t in KEY_TITLES if t in _titles]
