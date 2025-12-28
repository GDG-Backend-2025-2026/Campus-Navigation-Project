"""Swagger/OpenAPI configuration for the Campus Navigation API."""

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "School Direction API",
        "description": "Campus Navigation API for finding routes between buildings",
        "version": "1.0.0",
        "contact": {
            "name": "API Support"
        }
    },
    "basePath": "/api/v1",
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Enter your JWT token with 'Bearer ' prefix (e.g., 'Bearer eyJhbGc...')"
        }
    },
    "tags": [
        {"name": "Authentication", "description": "Admin authentication endpoints"},
        {"name": "Buildings", "description": "Building management endpoints"},
        {"name": "Routes", "description": "Route management endpoints"},
        {"name": "System", "description": "System information endpoints"},
        {"name": "Sync", "description": "Offline sync endpoints"}
    ]
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs"
}
