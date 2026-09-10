import sys
from src.exception import CustomException

def divide_num() -> None:
    a =10
    b =0
    result = a/b
    return result

if __name__=="__main__":            ### to execute current file
    try:
        result = divide_num()
        print(result)
    except Exception as e:
        raise CustomException(e ,sys)

    