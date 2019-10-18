"""Connect parameters for Adax"""
import logging
import requests
import json

__version__ = '0.1.2'

_LOGGER = logging.getLogger(__name__)

class Adax:
    data = None

    @staticmethod
    def do_api_request(url, params):
        """Do API request."""
        req = requests.post(url, data=params)
        _LOGGER.debug("API request returned %d", req.text)

        if req.status_code != requests.codes.ok:
            _LOGGER.exception("API request returned error %d", req.status_code)
        else:
            _LOGGER.debug("API request returned OK %d", req.text)

        json_data = json.loads(req.content)
        return json_data
