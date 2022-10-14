from pymeasure.instruments import Instrument
from pymeasure.instruments.validators import strict_discrete_set,\
    strict_range, joined_validators, truncated_range

# Capitalize string arguments to allow for better conformity with other WFG's
def capitalize_string(string: str, *args, **kwargs):
    return string.upper()

# Combine the capitalize function and validator
string_validator = joined_validators(capitalize_string, strict_discrete_set)

import logging

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class EAPSB_9080_360_3U(Instrument):
    """ Represent the EA PSB 9080 360 3U 15 kW
    These are Its limits:
        0-80 V
        0-360 A
        0-15 kW (product A*I mustn't overcame max power)
    """
    def __init__(self, adapter, **kwargs):
        super().__init__(
            adapter, "EA Elektro-Automatik GmbH & Co. KG PSB 9080-360 3U", timeout=10000, **kwargs
        )
        # Configuration changes can necessitate up to 8.8 secs (per datasheet)
        self.check_errors()


    voltage = Instrument.control(":VOLT?", ":VOLT %gV", """
    A floating point property which set voltage 0 to 80V
    """, validator=truncated_range, values=[0, 80])

    current = Instrument.control(":CURR?", ":CURR %gA", """
    A floating point property which set Current 0 to 300A
    """, validator=truncated_range, values=[0, 300])

    power = Instrument.control(":POW?", ":POW %g", """
    A floating point property which set Power 0 to 15000kW
    """, validator=truncated_range, values=[0, 15000])

    output = Instrument.control(":OUTP?", ":OUTP %s", """
    A floating point property which set Power 0 to 15000kW
    """, validator=joined_validators(
            strict_discrete_set, string_validator
        ), values=[["ON", "OFF"],])

    remote = Instrument.control("::SYST:LOCK?", ":SYST:LOCK %s", """
    A floating point property which set Power 0 to 15000kW
    """, validator=joined_validators(
            strict_discrete_set, string_validator
        ), values=[["ON", "OFF"],])