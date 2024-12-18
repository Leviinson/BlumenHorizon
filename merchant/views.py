import logging
import os

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
import stripe
import stripe.error
import stripe.webhook


@api_view(["POST"])
def stripe_webhook(request: Request):
    logger = logging.getLogger("django_stripe")
    try:
        payload = request.body
        sig_header = request.headers.get('STRIPE_SIGNATURE')
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, os.getenv("STRIPE_WEBHOOK_SECRET")
            )
        except ValueError as e:
            logger.debug(e, stack_info=True)
            return Response("Invalid payload", status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            logger.debug(e, stack_info=True)
            return Response("Invalid signature", status.HTTP_400_BAD_REQUEST)
        
        event_dict = event.to_dict()
        logger.info(event_dict)
    except Exception as e:
        logger.debug(e, stack_info=True)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(status=status.HTTP_200_OK)
