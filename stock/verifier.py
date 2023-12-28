import yaml
import os

from pathlib import Path


class Verifier:
    def __init__(self):
        self.root_path = Path(__file__).resolve().parents[1]
        self.batch_kind = ""
        self.config = {}

    def init_load(self):
        """
        Load Required Data
        """
        work_env = os.environ.get("DJANGO_ENV", "prod")
        config_path = os.path.join(self.root_path, 'stock_config.yaml')
        token_path = Path(__file__).resolve().parents[2]

        with open(config_path, encoding='UTF-8') as f:
            try:
                conf = yaml.load(f, Loader=yaml.FullLoader)
            except Exception as e:
                raise Exception("[validate] config.yaml load error")

        self.config = conf[work_env]
        self.config.update({"WORK_ENV": work_env})
        self.config.update({"ROOT_PATH": self.root_path})
        self.config.update({"TOKEN": os.path.join(token_path, self.config['TOKEN_FILE'])})
