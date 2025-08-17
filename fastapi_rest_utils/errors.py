"""Error handling utilities for fastapi-rest-utils viewsets."""


class MissingSchemaConfigError(NotImplementedError):
    """Raised when required schema configuration is missing from schema_config."""

    def __init__(self, view_name: str, config_key: str, required_key: str | None = None) -> None:
        """Initialize the error with view name and missing configuration details."""
        if required_key:
            msg = f"{view_name}: schema_config['{config_key}']['{required_key}'] must be set."
        else:
            msg = f"{view_name}: schema_config['{config_key}'] must be set."
        super().__init__(msg)
