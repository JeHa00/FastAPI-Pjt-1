# 0. Introduction

> 1. [config.py 설명](#1-configpy-설명)
> 2. [main.py 설명](#2-mainpy-설명)

- FastAPI 설치: `pip install fastapi uvicorn --user`


- 로컬 서버 실행: `uvicorn main:app --reload`

- `http://127.0.0.1:8000/docs` 를 입력하면 API swagger가 바로 나온다. 


- 변경하려는 파일 구조

    - Project Folder
        - venv folder
        - app folder
            - database
            - router
            - common  
                - config.py
                - consts.py  
            - main.py  
    

# 1. config.py 설명

## base_dir

```python
from os import path

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
```

-  notification_api 폴더 즉, 프로젝트 폴더를 가리켜서 참조하여, 그 안에 있는 파일들을 사용한다는 의미다.  
- \_\_file\_\_ 은 현재 수행 중인 파일의 위치를 의미한다.  
- `path.abspath(__file__)` 은 현재 파일의 절대 경로를 반환한다.  
- 이 프로젝트의 폴더가 현재 파일 기준으로 3단계 위에 있으므로, path.dirname()도 3번 덮어씌운다. 
- 절대 경로를 사용하는 이유는 나중에 도커를 사용할 시, 관리하기가 불편하기 때문이다. 

<br>

## class Config

```python
@dataclass
class Config:
    BASE_DIR = base_dir 

    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True 
```

- Config에 기본 url을 입력하여 상속으로 전해져도 되지만, Config에는 이후에 많은 데이터들이 포함되기 때문에, 별도로 한다.  
- 장고에서 이 class Config 역할을 하는게 setting.py 다. 

<br>

## LocalConfig와 ProdConfig

```python
@dataclass
class LocalConfig(Config):
   PROJ_RELOAD: bool = True 


@dataclass
class ProdConfig(Config):
    PROJ_RELOAD: bool = True  
```
    
- 두 Config 모두 상속을 받았기 때문에, 실제로는 `class Config`에 있는 클래스 변수도 가지고 있다. 

<br>

## dataclass를 사용한 이유

> dictionary로 가져오고 싶기 때문에, dataclass를 사용한다.  

- 보여주기 위해 아래 함수를 정의한다. 

```python
def abc(DB_ECHO = None, DB_POOL_RECYCLE = None, **kwargs):
    print(DB_ECHO, DB_POOL_RECYCLE)
```

- abc(**LocalConfig())로 언팩킹을 해도 풀어져서 출력되지 않는다.   
- 그래서 dictionary unpacking을 사용하기 위해서 `dataclass.asdict`를 사용한다.  

```python
> from dataclasses import dataclass, asdict
> args = asdict(LocalConfig()) 
> print(args)
{'DB_POOL_RECYCLE': 900, 'DB_ECHO': True, 'PROJ_RELOAD': True}

> abc(LocalConfig())
True 900
```

- asdict에 대한 공식문서

> Converts the dataclass obj to a dict (by using the factory function dict_factory).   
> Each dataclass is converted to a dict of its fields, as name:   
> value pairs. dataclasses, dicts, lists,  and tuples are recursed into.


<br>


## def conf()

운영체제에 등록되어 있는 모든 환경 변수는 `os` module의 `environ`이라는 속성을 통해서 접근이 가능하다.  
이 속성은 마치 파이썬 딕셔너리를 사용하듯이 사용할 수 있다.  

- `os.envirion['key']`를 하면 key 값이 존재하지 않을 경우, Error가 발생되기 때문에 예외처리를 해야한다.   
- 그래서 `os.envirion.get('key','key2')`을 사용하는데, 첫 번째 인자가 없을 경우에는 key2를 사용하라는 의미다. 

```python
# API_ENV를 찾지 못하면 local을 사용한다는 의미이고 즉 LocalConfig를 사용한다는 의미다.  

def conf():
    config = dict(prod = ProdConfig, local = LocalConfig, test = TestConfig)
    return config[environ.get("API_ENV", "local")]()
```

- 또한, python에서는 switch 문이 없기 때문에 이처럼 dictionary를 사용하여 매핑하는 방식으로 처리한다. 이 방식으로 잘 사용하고 있다.
    - 파이썬은 이 스위치문이 필요없어서 이와 관련된 논의는 폐기되었다. 
    - [dictionary로 사용하는 것으로 인한 문제점](https://peps.python.org/pep-3103/#when-to-freeze-the-dispatch-dict)


<br>

---


# 2. main.py 설명

