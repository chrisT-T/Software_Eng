from . import container, file, hello, project, user, login

api_bp = [
    hello.bp,
    project.bp,
    user.bp,
    container.bp,
    file.bp,
    login.bp
]
