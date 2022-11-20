from . import container, file, hello, project, user

api_bp = [
    hello.bp,
    project.bp,
    user.bp,
    container.bp,
    file.bp
]
