from . import container, hello, project, user

api_bp = [
    hello.bp,
    project.bp,
    user.bp,
    container.bp
]
