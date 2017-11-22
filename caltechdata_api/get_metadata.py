import os,json,csv,argparse
import requests
from datacite import DataCiteMDSClient, schema40
from caltechdata_api import decustomize_schema

def get_metadata(ids,production=True):

    if production==True:
        api_url = "https://data.caltech.edu/api/record/"
    else:
        api_url = "https://cd-sandbox.tind.io/api/record"

    r = requests.get(api_url+str(idv))
    metadata = r.json()['metadata']
    metadata = decustomize_schema(metadata)

    try: 
        assert schema40.validate(metadata)
    except AssertionError:
        v = schema40.validator.validate(metadata)
        errors = sorted(v.iter_errors(instance), key=lambda e:e.path)
        for error in errors:
            print(error.message)
        exit()

    return metadata

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=\
    "get_metadata queries the caltechDATA (Invenio 3) API\
    and returns DataCite-compatable metadata")
    parser.add_argument('ids', metavar='ID', type=int, nargs='+',\
    help='The CaltechDATA ID for each record of interest')

    args = parser.parse_args()

    for idv in args.ids:
        metadata = get_metadata(idv)
        outfile = open(str(idv)+'.json','w')
        outfile.write(json.dumps(metadata))
        outfile.close()