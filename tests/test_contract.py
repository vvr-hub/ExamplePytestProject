import pytest
import jsonschema
import copy
from jsonschema import ValidationError, Draft7Validator
from uritemplate.template import URITemplate
from schemas.api_schemas import (
    user_schema,
    list_users_schema,
    resource_schema,
    list_resources_schema,
)

# Custom format checker for strict URI validation
format_checker = jsonschema.FormatChecker()


@format_checker.checks("uri")
def is_uri(instance):
    try:
        URITemplate(instance)
        return True
    except ValueError:
        return False


def extend_with_default(validator_class):
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for property, subschema in properties.items():
            if "default" in subschema:
                instance.setdefault(property, subschema["default"])

        yield from validate_properties(validator, properties, instance, schema)

    return jsonschema.validators.extend(validator_class, {"properties": set_defaults})


DefaultDraft7Validator = extend_with_default(Draft7Validator)

# Validate API schemas to catch errors early
Draft7Validator.check_schema(user_schema)
Draft7Validator.check_schema(list_users_schema)
Draft7Validator.check_schema(resource_schema)
Draft7Validator.check_schema(list_resources_schema)


def test_get_user_contract(api_client, config_loader, data_loader):
    """Ensure response follows expected schema."""
    user_ids = data_loader.get_data("contract", "user_ids")
    for user_id in user_ids:
        endpoint = config_loader.get_api_endpoints("users_by_id").format(user_id=user_id)
        response = api_client.get(endpoint)
        assert response.status_code == 200
        try:
            DefaultDraft7Validator(user_schema, format_checker=format_checker).validate(response.json())
        except ValidationError as e:
            pytest.fail(f"Schema validation failed for user {user_id}: {e.message}")


def test_list_users_contract(api_client, config_loader):
    """Ensure response follows expected schema for list of users."""
    endpoint = config_loader.get_api_endpoints("users")
    response = api_client.get(endpoint)
    assert response.status_code == 200
    try:
        DefaultDraft7Validator(list_users_schema, format_checker=format_checker).validate(response.json())
    except ValidationError as e:
        pytest.fail(f"Schema validation failed: {e.message}")


def test_single_resource_contract(api_client, config_loader, data_loader):
    """Ensure response follows expected schema for a single resource."""
    resource_id = data_loader.get_data("contract", "resource_id")
    endpoint = config_loader.get_api_endpoints("unknown_by_id").format(resource_id=resource_id)
    response = api_client.get(endpoint)
    assert response.status_code == 200
    try:
        DefaultDraft7Validator(resource_schema, format_checker=format_checker).validate(response.json())
    except ValidationError as e:
        pytest.fail(f"Schema validation failed: {e.message}")


def test_list_resources_contract(api_client, config_loader):
    """Ensure response follows expected schema for list of resources."""
    endpoint = config_loader.get_api_endpoints("unknown")
    response = api_client.get(endpoint)
    assert response.status_code == 200
    try:
        DefaultDraft7Validator(list_resources_schema, format_checker=format_checker).validate(response.json())
    except ValidationError as e:
        pytest.fail(f"Schema validation failed: {e.message}")


def test_get_user_contract_missing_field(api_client, config_loader):
    """Test response with a missing field."""
    endpoint = config_loader.get_api_endpoints("users_by_id").format(user_id=2)
    response = api_client.get(endpoint)
    response_json = copy.deepcopy(response.json())  # Safe copy before modification
    if "avatar" in response_json["data"]:
        del response_json["data"]["avatar"]
    with pytest.raises(ValidationError):
        DefaultDraft7Validator(user_schema, format_checker=format_checker).validate(response_json)


def test_get_user_contract_invalid_email(data_loader):
    """Test response with invalid email format."""
    invalid_email_json = data_loader.get_data("contract", "invalid_email_user")
    with pytest.raises(ValidationError):
        DefaultDraft7Validator(user_schema, format_checker=format_checker).validate(invalid_email_json)
