from fastapi import APIRouter, Depends
from ..models import Response
from ..dependencies.verify_token import verify_token

from .. import logger
router = APIRouter(prefix='/test', dependencies=[Depends(verify_token)], tags=['test'])

@router.get('/', response_model=Response, response_model_exclude_unset=True)
def test():
    logger.debug('==============')
    return {
        'abc': 1,
        'code': 0,
        'result': {
            'AB': 1
        }
    }