import chdb
import config
import database
from utils import *
from common import *

@validate_lang_code
def create_intersection(lang_code):
    cfg = flask.g._cfg
    request = flask.request.get_json()
    page_ids = request['page_ids']
    int_id, npages = '', 0
    if page_ids:
        int_id, page_ids = database.create_intersection(
            lang_code, page_ids, cfg.intersection_max_size,
            cfg.intersection_expiration_days)
    return flask.jsonify(int_id = int_id, page_ids = page_ids)
