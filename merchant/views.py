import logging
from pprint import pprint

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response


@api_view(["POST"])
def stripe_webhook(request: Request):
    try:
        pprint(request.data)
    except Exception as e:
        logger = logging.getLogger("stripe")
        logger.debug(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(status=status.HTTP_200_OK)
