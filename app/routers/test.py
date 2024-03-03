from fastapi import APIRouter, Depends, Body
from .dependencies import verify_token

from .. import logger
router = APIRouter(prefix='/test') #, dependencies=[Depends(verify_token)], tags=['test'])

from pandas import DataFrame
from pydantic import BaseModel, ConfigDict
from typing import Dict

class MyType(BaseModel):
    # model_config = ConfigDict(arbitrary_types_allowed=True)
    result: Dict

@router.get('/')#, response_model=Response, response_model_exclude_unset=True)
def test():

    p = DataFrame(
        {
            'a': [1, 0],
            'b': [3, 4]
        }
    )

    logger.debug(p)

    my = MyType(result=p.to_dict())
    logger.debug(my)

    logger.debug('==============')
    d = DataFrame(p.to_dict())
    print(d)
    return my
# {
#         'abc': 1,
#         'code': 0,
#         'result': {
#             'AB': 1
#         }
#     }


# @router.post('/ta')
# def ta(body = Body()):
    