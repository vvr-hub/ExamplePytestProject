import pytest
import requests
import jsonschema
import copy
from utils.api_client import APIClient
from jsonschema import ValidationError, Draft7Validator
from uritemplate.template import URITemplate


@pytest.fixture
def api_client():
    return APIClient()


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

# Define and validate JSON schemas
user_schema = {
    "type": "object",
    "properties": {
        "data": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "email": {"type": "string", "format": "email"},
                "first_name": {"type": "string"},
                "last_name": {"type": "string"},
                "avatar": {"type": "string", "format": "uri"},
            },
            "required": ["id", "email", "first_name", "last_name", "avatar"],
        }
    },
    "required": ["data"],
}

list_users_schema = {
    "type": "object",
    "properties": {
        "page": {"type": "integer"},
        "per_page": {"type": "integer"},
        "total": {"type": "integer"},
        "total_pages": {"type": "integer"},
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "email": {"type": "string", "format": "email"},
                    "first_name": {"type": "string"},
                    "last_name": {"type": "string"},
                    "avatar": {"type": "string", "format": "uri"},
                },
                "required": ["id", "email", "first_name", "last_name", "avatar"],
            },
        },
    },
    "required": ["page", "per_page", "total", "total_pages", "data"],
}

resource_schema = {
    "type": "object",
    "properties": {
        "data": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "year": {"type": "integer"},
                "color": {"type": "string"},
                "pantone_value": {"type": "string"},
            },
            "required": ["id", "name", "year", "color", "pantone_value"],
        }
    },
    "required": ["data"],
}

list_resources_schema = {
    "type": "object",
    "properties": {
        "page": {"type": "integer"},
        "per_page": {"type": "integer"},
        "total": {"type": "integer"},
        "total_pages": {"type": "integer"},
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "year": {"type": "integer"},
                    "color": {"type": "string"},
                    "pantone_value": {"type": "string"},
                },
                "required": ["id", "name", "year", "color", "pantone_value"],
            },
        },
    },
    "required": ["page", "per_page", "total", "total_pages", "data"],
}

# Validate schemas to catch errors early
Draft7Validator.check_schema(user_schema)
Draft7Validator.check_schema(list_users_schema)
Draft7Validator.check_schema(resource_schema)
Draft7Validator.check_schema(list_resources_schema)


@pytest.mark.parametrize("user_id", [2, 3, 4])
def test_get_user_contract(api_client, user_id):
    """Ensure response follows expected schema."""
    response = api_client.get(f"/users/{user_id}")
    assert response.status_code == 200
    try:
        DefaultDraft7Validator(user_schema, format_checker=format_checker).validate(response.json())
    except ValidationError as e:
        pytest.fail(f"Schema validation failed for user {user_id}: {e.message}")


def test_list_users_contract(api_client):
    """Ensure response follows expected schema for list of users."""
    response = api_client.get(f"/users")
    assert response.status_code == 200
    try:
        DefaultDraft7Validator(list_users_schema, format_checker=format_checker).validate(response.json())
    except ValidationError as e:
        pytest.fail(f"Schema validation failed: {e.message}")


def test_single_resource_contract(api_client):
    """Ensure response follows expected schema for a single resource."""
    response = api_client.get(f"/unknown/2")
    assert response.status_code == 200
    try:
        DefaultDraft7Validator(resource_schema, format_checker=format_checker).validate(response.json())
    except ValidationError as e:
        pytest.fail(f"Schema validation failed: {e.message}")


def test_list_resources_contract(api_client):
    """Ensure response follows expected schema for list of resources."""
    response = api_client.get(f"/unknown")
    assert response.status_code == 200
    try:
        DefaultDraft7Validator(list_resources_schema, format_checker=format_checker).validate(response.json())
    except ValidationError as e:
        pytest.fail(f"Schema validation failed: {e.message}")


def test_get_user_contract_missing_field(api_client):
    """Test response with a missing field."""
    response = api_client.get(f"/users/2")
    response_json = copy.deepcopy(response.json())  # Safe copy before modification
    if "avatar" in response_json["data"]:
        del response_json["data"]["avatar"]
    with pytest.raises(ValidationError):
        DefaultDraft7Validator(user_schema, format_checker=format_checker).validate(response_json)


def test_get_user_contract_invalid_email():
    """Test response with invalid email format."""
    invalid_email_json = {
        "data": {
            "id": 2,
            "email": "invalid_email",
            "first_name": "Janet",
            "last_name": "Weaver",
            "avatar": "https://reqres.in/img/faces/2-image.jpg",
        }
    }
    with pytest.raises(ValidationError):
        DefaultDraft7Validator(user_schema, format_checker=format_checker).validate(invalid_email_json)

