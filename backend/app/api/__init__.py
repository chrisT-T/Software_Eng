from . import container, file, hello, login, project, user

api_bp = [
    hello.bp,
    project.bp,
    user.bp,
    container.bp,
    file.bp,
    login.bp
]
