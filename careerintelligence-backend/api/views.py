from django.http import JsonResponse

def api_status(request):
    return JsonResponse({
        "project": "Career Intelligence",
        "message": "Backend is running successfully",
        "status": "success"
    })

