from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from payment.models import Payment
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse

#verify_wishmoney_callback
import hmac
import hashlib
from django.conf import settings



@login_required
def payment_checkout(request):
    """
    Redirect user to Wish Money payment page.
    Only PENDING payments are allowed.
    """
    payment_id = request.session.get('payment_id')

    if not payment_id:
        return redirect('home')

    payment = get_object_or_404(
        Payment,
        id=payment_id,
        user=request.user,
        status='PENDING'
    )

    # Build Wish Money payment URL
    wish_money_url = (
        f"https://wishmoney.com/pay?"
        f"amount={payment.amount}&"
        f"reference={payment.id}&"
        f"callback_url={request.build_absolute_uri(reverse('wishmoney_callback'))}&"
        f"success_url={request.build_absolute_uri(reverse('payment_success'))}"
    )

    return redirect(wish_money_url)



def verify_wishmoney_callback(request):
    """
    Verify that the callback comes from Wish Money.
    """
    signature = request.headers.get("X-Signature")  # check Wish Money docs
    payload = request.body  # raw POST body

    if not signature:
        return False

    expected_signature = hmac.new(
        settings.WISHMONEY_SECRET_KEY.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, expected_signature)





@csrf_exempt
def wishmoney_callback(request):
    """
    Wish Money server calls this endpoint to confirm payment.
    """

    if not verify_wishmoney_callback(request):
        return HttpResponseForbidden("Invalid callback")

    reference = request.POST.get('reference')
    status = request.POST.get('status')

    if not reference or not status:
        return HttpResponse("Missing parameters", status=400)

    try:
        payment = Payment.objects.get(id=reference)
    except Payment.DoesNotExist:
        return HttpResponse("Invalid payment reference", status=400)

    if status.upper() == 'SUCCESS' and payment.status != 'SUCCESS':
        payment.status = 'SUCCESS'
        payment.save()

    return HttpResponse("OK")



@login_required
def payment_success(request):
    """
    User is redirected here after successful payment.
    Then redirect to event activation.
    """
    payment_id = request.session.get('payment_id')

    if not payment_id:
        return redirect('home')

    payment = get_object_or_404(
        Payment,
        id=payment_id,
        user=request.user
    )

    # Only allow redirect if payment is confirmed SUCCESS
    if payment.status != 'SUCCESS':
        return HttpResponseForbidden("Payment not completed")

    # Optional: clear session
    request.session.pop('payment_id', None)

    # Redirect to event activation
    return redirect('my_event_invitation_activate')








# @csrf_exempt
# def wishmoney_callback(request):
#     """
#     Wish Money server calls this endpoint to confirm payment.
#     """
#     reference = request.POST.get('reference')
#     status = request.POST.get('status')

#     if not reference or not status:
#         return HttpResponse("Missing parameters", status=400)

#     try:
#         payment = Payment.objects.get(id=reference)
#     except Payment.DoesNotExist:
#         return HttpResponse("Invalid payment reference", status=400)

#     if status.upper() == 'SUCCESS' and payment.status != 'SUCCESS':
#         payment.status = 'SUCCESS'
#         payment.save()


#     return HttpResponse("OK")