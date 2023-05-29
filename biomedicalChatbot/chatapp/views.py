from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from chatbot import response, predict_disease

@csrf_exempt
def process_text(request):
    history = "none"
    if request.method == 'POST':
        input_text = request.POST.get('input_text')
        history = predict_disease(input_text, history)
        output_text = response(input_text, history)
        return HttpResponse(output_text)
    else:
        return HttpResponse('Invalid request')
