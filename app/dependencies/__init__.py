from fastapi import Header, HTTPException

def verify_token(x_token: str = Header()):
    # logger.debug('x_token = ', x_token)
    return x_token
