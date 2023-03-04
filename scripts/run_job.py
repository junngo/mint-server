import subprocess
import sys

from pathlib import Path


def run():
    """
    [helper] 배치 잡 실행을 위한 커맨드 실행 스크립트
    """
    job = sys.argv[1]
    base_dir = Path(__file__).resolve().parents[1]

    with open("/tmp/output.log", "a") as output:
        docker_config_path = f"-f {base_dir}/docker-compose.prod.yml"
        command_prefix = f"/usr/local/bin/docker-compose {docker_config_path} exec web python manage.py runjob --job "
        subprocess.call(command_prefix + job, shell=True, stdout=output, stderr=output)


if __name__ == "__main__":
    run()
