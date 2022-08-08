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

get_all_posts = [
    make_api_param("page", openapi.IN_QUERY, "페이지", openapi.TYPE_STRING, default="1"),
    make_api_param("system-key", openapi.IN_HEADER, "시스템 키", openapi.TYPE_STRING, default=os.environ.get("SYSTEM_KEY")),
    make_api_param("Authorization", openapi.IN_HEADER, "jwt", openapi.TYPE_STRING),
]

get_all_comments = [
    make_api_param("page", openapi.IN_QUERY, "페이지", openapi.TYPE_STRING, default="1"),
    make_api_param("system-key", openapi.IN_HEADER, "시스템 키", openapi.TYPE_STRING, default=os.environ.get("SYSTEM_KEY")),
    make_api_param("Authorization", openapi.IN_HEADER, "jwt", openapi.TYPE_STRING),
]

modify_comment = [
    make_api_param("comment_pk", openapi.IN_PATH, "댓글 PK", openapi.TYPE_STRING),
    make_api_param("system-key", openapi.IN_HEADER, "시스템 키", openapi.TYPE_STRING, default=os.environ.get("SYSTEM_KEY")),
    make_api_param("Authorization", openapi.IN_HEADER, "jwt", openapi.TYPE_STRING),
]

login_no_require = [
    make_api_param("system-key", openapi.IN_HEADER, "시스템 키", openapi.TYPE_STRING, default=os.environ.get("SYSTEM_KEY")),
]

login_required = [
    make_api_param("system-key", openapi.IN_HEADER, "시스템 키", openapi.TYPE_STRING, default=os.environ.get("SYSTEM_KEY")),
    make_api_param("Authorization", openapi.IN_HEADER, "jwt", openapi.TYPE_STRING),
]