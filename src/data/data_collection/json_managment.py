import json, os
import errno

FOLDER_PATH = '/Users/wesamazaizeh/Desktop/Projects/halal_o_meter/src/data/data_collection/search_json/'


def json_to_file(businesses_id, json_ojb):
    '''
    Takes a bussiness ID and JSON object and creates a file in the search_json
    folder named after the ID
    '''
    with open(FOLDER_PATH + file_id + '.json' ,'w+') as outfile:
        json.dump(json_ojb, outfile)

def file_to_json(business_id='', file_path=''):
    '''
    Take either a business ID or a filepath and returns the corresponding json
    file if it exists
    '''
    if os.path.isfile(file_path):
        data = json.load(file_path)
        return data
    elif business_id:
        try:
            file_path = FOLDER_PATH + business_id + '.json'
            os.path.isfile(file_path)
            data = json.load(file_path)
            return data
        except:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)
    else :
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)
