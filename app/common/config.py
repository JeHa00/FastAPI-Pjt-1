from dataclasses import dataclass, asdict
from os import path, environ
from typing import List

# notification_api 폴더를 가리켜서 참조를 하도록 한다.  그래서 가리킨 폴더 안에 있는 파일들을 사용한다는 의미다.  
# __file__ 은 현재 수행 중인 파일의 위치를 의미한다.  
# path.abspath(__file__)은 현재 파일의 절대 경로를 반환한다.  
# 이 프로젝트의 폴더가 현재 파일 기준으로 3단계 위에 있으므로, path.dirname()도 3번 덮어씌운다. 
# 절대 경로를 사용하는 이유는 나중에 도커를 사용할 시, 관리하기가 불편하기 때문이다. 


base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))

# dataclass를 사용한 이유는 dictionary로 가져와서 unpacking하고 싶기 때문에
@dataclass
class Config:
    """
    기본 Configuration
    """
    # Config에 기본 url을 입력하여 상속으로 전해져도 되지만, Config에는 이후에 많은 데이터들이 포함되기 때문에, 별도로 하기로 선택한 것이다. 
    # 장고에서 class Config 역할을 하는게 setting.py다.  
    BASE_DIR = base_dir 

    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True  

@dataclass
class LocalConfig(Config):
   PROJ_RELOAD: bool = True 
    

@dataclass
class ProdConfig(Config):
    PROJ_RELOAD: bool = True  


# Converts the dataclass obj to a dict 
@dataclass
class TestConfig(Config):
    DB_URL: str = "mysql+pymysql://travis@localhost/notification_test?charset=utf8mb4"
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    TEST_MODE: bool = True


def conf():
    """
    환경 불러오기
    :return:
    """
    config = dict(prod=ProdConfig, local=LocalConfig, test=TestConfig)
    return config[environ.get("API_ENV", "local")]()
    # switch case..?

