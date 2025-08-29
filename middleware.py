from flask import request, Request, Response
import json


def authentication_middleware():
    request.headers.get("")
    request.user = "USER BLAYT`!"
    return Response
    # data = request.get_json()
    # data["user"] = "USER BLAYT`!"
    # request._cached_json = data  # Update the cached JSON
    # request._cached_data = json.dumps(data).encode("utf-8")


# def authentication(func):
#     # request.headers.get("Authorization")

#     def wrapper(*args, **kwargs):
#         response: Response = func(*args, **kwargs)
#         response.set_cookie("token", "123")

#     return wrapper


# def authentication(*Args, **Kwargs):
#     def proxy(func):
#         def wrap(*args, **kwargs):
#             response: Response = func(*Args, **Kwargs)
#             response.set_cookie("token", "123")
#             return response

#         return wrap

#     return proxy


class CustomWSGIMiddleware:
    def __init__(self, app):
        self.app = app  # Wraps the Flask app

    def __call__(self, environ, start_response):
        # Modify request before passing it to Flask
        # print(f"!environ", environ)
        # print(f"Incoming request: {environ['REQUEST_METHOD']} {environ['PATH_INFO']}")

        # Process the request with the Flask app
        response = self.app(environ, start_response)

        # Modify response if needed
        return response
