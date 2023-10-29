import subprocess
import sys

from pathlib import Path


def run():
    """
    [helper] Script to run the command in the product environment
    e.x) python run_job.py [command]
    """
    job = " ".join(sys.argv[1:])
    base_dir = Path(__file__).resolve().parents[1]

    with open("/tmp/output.log", "a") as output:
        docker_config_path = f"-f {base_dir}/docker-compose.prod.yml"
        command_prefix = f"/usr/local/bin/docker-compose {docker_config_path} exec web python manage.py "
        command = command_prefix + job
        subprocess.call(command, shell=True, stdout=output, stderr=output)


if __name__ == "__main__":
    run()
