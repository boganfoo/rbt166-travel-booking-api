from django.http import JsonResponse


def health_check(request):
    """Health check endpoint for monitoring."""
    return JsonResponse({"status": "healthy", "service": "rbt166-travel-booking-api"})

