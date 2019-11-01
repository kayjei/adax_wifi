"""Parameter file for Adax integration"""

def get_static(value):
    switcher = {
    "account_id": '',
    "appVersion": '',
    "device": '',
    "os": '',
    "timeOffset": '',
    "timeZone": '',
    "locale": '',
    "zone_signature": ''
    }
    return switcher.get(value,"Key missing")

def get_signature_123456(value):
    switcher = {
    "heat_signature": '',
    0: '', #Set as HVAC_OFF
    5: '',
    6: '',
    7: '',
    8: '',
    9: '',
    10:'',
    11: '',
    12: '',
    13: '',
    14: '',
    15: '',
    16: '',
    17: '',
    18: '',
    19: '',
    20: '',
    21: '',
    22: '',
    23: '',
    24: '',
    25: '',
    26: '',
    27: '',
    28: '',
    29: '',
    30: '',
    31: '',
    32: '',
    33: '',
    34: '',
    35: ''
    }
    return switcher.get(value,"Key missing")

def set_param(zone, value):
    """Section for iOS devices"""
    if 'iOS' in get_static("os"):
        if zone == "static":
            return {"signature": get_static(value), "appVersion": get_static("appVersion"), "device": get_static("device"), 
            "os": get_static("os"), "timeOffset": get_static("timeOffset"), "timeZone": get_static("timeZone")}

        elif zone == 123456:
            return {"signature": get_signature_123456(value), "appVersion": get_static("appVersion"), "device": get_static("device"), 
            "os": get_static("os"), "timeOffset": get_static("timeOffset"), "timeZone": get_static("timeZone")}


    else:
        if zone == "static":
            return {"signature": get_static(value), "appVersion": get_static("appVersion"), "device": get_static("device"), 
            "os": get_static("os"), "timeOffset": get_static("timeOffset"), "timeZone": get_static("timeZone"), "locale": get_static("locale")}

        elif zone == 123456:
            return {"signature": get_signature_123456(value), "appVersion": get_static("appVersion"), "device": get_static("device"), 
            "os": get_static("os"), "timeOffset": get_static("timeOffset"), "timeZone": get_static("timeZone"), "locale": get_static("locale")}
