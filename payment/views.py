from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from payment.models import Payment
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse


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


@csrf_exempt
def wishmoney_callback(request):
    """
    Wish Money server calls this endpoint to confirm payment.
    """
    reference = request.POST.get('reference')
    status = request.POST.get('status')

    if not reference or not status:
        return HttpResponse("Missing parameters", status=400)

    try:
        payment = Payment.objects.get(id=reference)
    except Payment.DoesNotExist:
        return HttpResponse("Invalid payment reference", status=400)

    # Only mark SUCCESS if status is 'SUCCESS' from Wish Money
    if status.upper() == 'SUCCESS':
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
