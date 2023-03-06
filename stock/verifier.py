import sys
import yaml
import os

from pathlib import Path


class Verifier:
    def __init__(self):
        self.root_path = Path(__file__).resolve().parents[1]
        self.argv = sys.argv
        self.batch_kind = ""
        self.config = {}

    def init_load(self):
        """
        배치 실행 시 입력값 검증 및 필수 데이터 로드
        """
        # 1. config 파일 로드
        # DJANGO_ENV의 따른 prod(실거래) 또는 test(모의 거래)
        work_env = os.environ.get("DJANGO_ENV", "test")

        with open(os.path.join(self.root_path, 'stock_config.yaml'), encoding='UTF-8') as f:
            try:
                conf = yaml.load(f, Loader=yaml.FullLoader)
            except Exception as e:
                raise Exception("[validate] config.yaml 로드 에러")

        self.config = conf[work_env]
        self.config.update({"ENV": work_env})
        self.config.update({"ROOT_PATH": self.root_path})

        # 2. 실행할 배치 종류 검증
        # if len(self.argv) == 1:
        #     # line_notify.SendMessage("[validate] 입력 받은 인자가 없습니다.")
        #     raise Exception("[validate] 입력 받은 인자가 없습니다.")

        # self.batch_kind = self.argv[1]
        # if self.batch_kind not in Batches:
        #     # line_notify.SendMessage("[validate] 배치종류가 존재하지 않습니다. (" + self.batch_kind + ")")
        #     raise Exception("[validate] 배치종류가 존재하지 않습니다. (" + self.batch_kind + ")")
