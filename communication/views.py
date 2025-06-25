from django.shortcuts import render
from django.http import JsonResponse
from .models import Message, FlashMessage, UsefulInfo
from django.contrib.auth.decorators import login_required

@login_required
def list_messages(request):
    messages = Message.objects.filter(recipient=request.user.email)
    return render(request, 'communication/message_list.html', {'messages': messages})

@login_required
def list_flash_messages(request):
    flashes = FlashMessage.objects.all()
    return render(request, 'communication/flash_list.html', {'flashes': flashes})

@login_required
def useful_info(request):
    infos = UsefulInfo.objects.all()
    return render(request, 'communication/useful_info.html', {'infos': infos})

def send_message(request):
    if request.method == 'POST':
        # Logic to send a message to teachers
        # This is a placeholder for actual implementation
        message_content = request.POST.get('content')
        # Assume we save the message to the database
        message = Message(content=message_content)
        message.save()
        return JsonResponse({'status': 'success', 'message': 'Message sent successfully.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})