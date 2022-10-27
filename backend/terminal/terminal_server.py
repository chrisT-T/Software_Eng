import docker
import tornado


def create_docker_pty(container_id='ee44d43ade04376eb44e9db9c028ed8e857474d4a4c59a55e5661ee9062d82a3'):

    exec_cmd = [
        '/bin/bash'
    ]

    docker_apiclient = docker.APIClient()

    execid = docker_apiclient.exec_create(container_id, exec_cmd, tty=True, stdin=True)
    output = docker_apiclient.exec_start(execid, socket=True, tty=True)
    print(execid)
    print(output)


if __name__ == '__main__':
    create_docker_pty()
