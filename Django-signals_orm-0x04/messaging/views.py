from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message, MessageHistory


@login_required
def message_history(request, pk: int):
	message = get_object_or_404(Message, pk=pk)
	history_qs = message.history.all().order_by('-changed_at')
	return render(request, 'messaging/message_history.html', {
		'message': message,
		'history': history_qs,
	})
