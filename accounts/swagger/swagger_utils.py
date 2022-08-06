import os
from drf_yasg import openapi

def make_api_param(name, type, desc, format, default=""):
    param = openapi.Parameter(
        name,
        type,
        description=desc,
        type=format,
        default=default
    )

    return param

login_no_require = [
    make_api_param("system-key", openapi.IN_HEADER, "시스템 키", openapi.TYPE_STRING, default=os.environ.get("SYSTEM_KEY")),
]

login_required = [
    make_api_param("system-key", openapi.IN_HEADER, "시스템 키", openapi.TYPE_STRING, default=os.environ.get("SYSTEM_KEY")),
    make_api_param("Authorization", openapi.IN_HEADER, "jwt", openapi.TYPE_STRING),
]