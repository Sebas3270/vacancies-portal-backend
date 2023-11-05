from rest_framework.views import exception_handler

def custom_exception_handler(exec, context):
    response = exception_handler(exec, context)
    exception_class = exec.__class__.__name__
    
    if exception_class == 'AuthenticationFailed':
        response.data = {
            'detail': 'Invalid email or password, try again'
        }

    if exception_class == 'NotAutenticated':
        response.data = {
            'detail': 'Login first to access this resource'
        }

    if exception_class == 'InvalidToken':
        response.data = {
            'detail': 'Auth token is expired, login again'
        }

    return response