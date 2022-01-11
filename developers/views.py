from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def realtime_view(request, dev1, dev2):

    """
    Check if two developers are connected and what GitHub organizations they have in common
    """
    
    return Response({}, status=status.HTTP_200_OK)

@api_view(["GET"])
def register_view(request, dev1, dev2):

    """
    This endpoint will return all the related information from previous requests to the real-time endpoint
    """
    
    return Response({}, status=status.HTTP_200_OK)