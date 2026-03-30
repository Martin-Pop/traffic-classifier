from .core import configuration, ConfigurationField
from .rules import ConfigurationRules as Rules

@configuration
class AppConfiguration:

    analysed_captures_directory = ConfigurationField(
        str,
        Rules.valid_directory,
        default="analysed_captures"
    )

    default_threshold = ConfigurationField(
        float,
        Rules.valid_percentage,
        default=0.4
    )