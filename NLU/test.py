import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, ConceptsOptions

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-03-16',
    iam_apikey='a3jHgMchnTE0W1ZIH3IemDKNUZpuqq6D3_4345HXkLVZ',
    url='https://gateway.watsonplatform.net/natural-language-understanding/api'
)

response = natural_language_understanding.analyze(
    url='www.ibm.com',
    features=Features(concepts=ConceptsOptions(limit=3))).get_result()

print(json.dumps(response, indent=2))