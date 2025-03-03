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
