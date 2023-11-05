from django.http import JsonResponse

def handler404(request, exception):
    message = ('Route not found')
    response = JsonResponse(data={'detail': message})
    response.status_code = 404
    return response

def handler500(request):
    message = ('Internal server error, call administrator')
    response = JsonResponse(data={'detail': message})
    response.status_code = 500
    return response