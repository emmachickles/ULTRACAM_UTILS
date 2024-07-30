import json

with open('paths.json', 'r') as f:
    paths = json.load(f)

import sys
sys.path.insert(0, paths['lightcurve_directory'])
from time_utils import BJDConvert
