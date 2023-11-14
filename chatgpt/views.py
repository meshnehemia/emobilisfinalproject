from openai import OpenAI
from django.shortcuts import render
from django.http import JsonResponse
from openai import AsyncOpenAI

#openai_api_key = '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'
openai_api_key = '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'

def home(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatgpt/chatbot.html')


def ask_openai(message):
    conversation = [
        {"role": "system", "content": "You are a intelligent."},
        {"role": "user", "content": message}
    ]
    client = OpenAI(
        api_key= openai_api_key  # this is also the default, it can be omitted
    )
    # client = AsyncOpenAI()
    response= client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )
    answer = response.choices[0].message.content
    return answer




