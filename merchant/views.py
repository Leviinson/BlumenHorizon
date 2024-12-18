from pprint import pprint

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response


@api_view(["POST"])
def stripe_webhook(request: Request):
    pprint(request.data)
    return Response(status=status.HTTP_200_OK)

