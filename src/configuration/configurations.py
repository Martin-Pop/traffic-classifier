from .core import configuration, ConfigurationField
from .rules import ConfigurationRules as Rules

@configuration
class AppConfiguration:

    analysed_captures_directory = ConfigurationField(
        str,
        Rules.valid_directory,
        default="analysed_captures"
    )

    model_path = ConfigurationField(
        str,
        (Rules.existing_file, Rules.is_joblib_file),
        default="model/model.joblib"
    )

    window_size_sec = ConfigurationField(
        int,
        Rules.positive_integer,
        default=20
    )

    step_size_sec = ConfigurationField(
        int,
        Rules.positive_integer,
        default=5
    )

    # default_threshold = ConfigurationField(
    #     float,
    #     Rules.valid_percentage,
    #     default=0.4
    # )