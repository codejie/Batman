from fastapi import Header, HTTPException

def verify_token(x_token: str = Header()):
    # logger.debug('x_token = ', x_token)
    return x_token

def verify_admin(x_token: str = Header()):
    if x_token != 'superman':
        raise HTTPException(status_code=400, detail="X-Token invalid.")
    return x_token