"""
Support for the Adax wifi heaters using API.
For more details about this platform, please refer to the documentation at

"""
import logging
import sys
import time
import requests
import json
import voluptuous as vol
from .connect import Adax
from .parameters import set_param, get_static

from homeassistant.components.climate import ClimateDevice, PLATFORM_SCHEMA
from homeassistant.components.climate.const import SUPPORT_TARGET_TEMPERATURE, HVAC_MODE_OFF, HVAC_MODE_HEAT
from homeassistant.const import (
    TEMP_CELSIUS, ATTR_TEMPERATURE, PRECISION_WHOLE)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DEFAULT_TEMP = 20

SUPPORT_FLAGS = SUPPORT_TARGET_TEMPERATURE

ZONE_URL = 'https://heater.azurewebsites.net/sheater-client-api/rest/zones/list/' + str(get_static("account_id"))
TEMP_URL = 'https://heater.azurewebsites.net/sheater-client-api/rest/zones/'

# ---------------------------------------------------------------


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Adax thermostat."""

    _LOGGER.debug("Adding component: adax_climate ...")

    params = set_param("static", "zone_signature")
    _LOGGER.debug("URL: " + str(ZONE_URL) + ", PARAMS: " + str(params))

    devices_json = Adax.do_api_request(ZONE_URL, params)

    for zone in devices_json[1]:
     z_id = int(zone["id"])
     z_entity = "climate.adax_" + str(zone["id"])
     z_name = str(zone["name"])
     z_state = round(float(zone["currentTemperature"] + zone["temperatureCalibration"]) / 100, 2)
     z_target =  round(float(zone["targetTemperature"]) / 100, 2)
     z_window = bool(zone["openWindow"])
     z_maxtemp = round(float(zone["upperTemperatureLimit"]) / 100, 2)
     z_mintemp = round(float(zone["lowerTemperatureLimit"]) / 100, 2)

     add_entities([AdaxDevice(z_id, z_name, z_state, z_target, z_window, z_maxtemp, z_mintemp)])

     _LOGGER.debug("adax: Zone " + str(z_id) + " added with name " + str(z_name) + "! Current temp is " + str(z_state))


class AdaxDevice(ClimateDevice):
    """Representation of a heater."""

    def __init__(self, id, name, state, target, window, maxtemp, mintemp):
        """Initialize the heater."""
        self._entity_id = "climate.adax_" + str(id)
        self._current_temperature = state
        self._name = name
        self._id = id
        self._state = state
        self._target_temperature = int(target)
        self._open_window = window
        self._max_temp = maxtemp
        self._min_temp = mintemp
        self.update()

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_TARGET_TEMPERATURE

    @property
    def entity_id(self):
        """Return the name of the device"""
        return self._entity_id

    @property
    def name(self):
        """Return the name of the device, if any."""
        return self._name

    @property
    def should_poll(self):
        """Polling is required."""
        return True

    @property
    def hvac_mode(self):
        if self._target_temperature == 0:
            return HVAC_MODE_OFF
        else:
            return HVAC_MODE_HEAT

    @property
    def hvac_modes(self):
        """HVAC modes."""
        return [HVAC_MODE_HEAT, HVAC_MODE_OFF]

    def set_hvac_mode(self, hvac_mode):
        """Set new target hvac mode."""
        if hvac_mode == HVAC_MODE_OFF:
            temperature = int(0)
            target_temp = int(0)
        elif hvac_mode == HVAC_MODE_HEAT:
            temperature = int(DEFAULT_TEMP)
            target_temp = int(temperature * 100)

        SET_URL = TEMP_URL + str(self._id) + "/target_temperature/" + str(get_static("account_id")) + "/" + str(target_temp)
        _LOGGER.debug("API URL: " + SET_URL)

        params = set_param(self._id, temperature)
        _LOGGER.debug("API params: " + str(params))

        response_json = Adax.do_api_request(SET_URL, params)
        _LOGGER.debug(str(response_json))

        self.schedule_update_ha_state(force_refresh=True)

    @property
    def temperature_unit(self):
        """Return the unit of measurement which this device uses."""
        return TEMP_CELSIUS

    @property
    def min_temp(self):
        """Return the minimum temperature."""
        return self._min_temp

    @property
    def max_temp(self):
        """Return the maximum temperature."""
        return self._max_temp

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._state

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._target_temperature

    @property
    def target_temperature_step(self):
        """Return the supported step of target temperature."""
        return PRECISION_WHOLE

    def set_temperature(self, **kwargs):
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return
        self._set_temperature(temperature)

    def _set_temperature(self, temperature, mode_int=None):
        """Set new target temperature, via API commands."""
        target_temp = int(temperature * 100)

        SET_URL = TEMP_URL + str(self._id) + "/target_temperature/" + str(get_static("account_id")) + "/" + str(target_temp)
        _LOGGER.debug("API URL: " + SET_URL)

        params = set_param(self._id, temperature)
        _LOGGER.debug("API params: " + str(params))

        response_json = Adax.do_api_request(SET_URL, params)
        _LOGGER.debug(str(response_json))

        self.schedule_update_ha_state(force_refresh=True)

    @property
    def device_state_attributes(self):
        """Return the attribute(s) of the device"""
        return {
            "window_open": self._open_window
        }

    def _get_data(self):
        """Get the data of the device."""
        params = set_param("static", "zone_signature")

        devices_json = Adax.do_api_request(ZONE_URL, params)

        for zone in devices_json[1]:
            if zone["id"] == self._id:
                self._name = str(zone["name"])
                self._state = round(float(zone["currentTemperature"] + zone["temperatureCalibration"]) / 100, 2)
                self._target_temperature =  round(float(zone["targetTemperature"]) / 100, 2)
                self._open_window = bool(zone["openWindow"])
                self._max_temp = round(float(zone["upperTemperatureLimit"]) / 100, 2)
                self._min_temp = round(float(zone["lowerTemperatureLimit"]) / 100, 2)

                _LOGGER.debug("Updating adax zone " + str(self._name) + ": Current temp is " + str(self._state))

    def update(self):
        """Get the latest data."""
        self._get_data()
#        return True
