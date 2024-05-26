import re
from typing import Dict
import jsonata


def transform_json(input_json: Dict, template: str):
    template = re.sub('[\\n ]', '', template)
    expression = jsonata.transform(template, input_json)
    return expression

