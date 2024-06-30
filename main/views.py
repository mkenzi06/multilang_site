from django.shortcuts import render
from .models import Article
import openai
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM

import torch

# from chatterbot import ChatBot
# from chatterbot.trainers import ChatterBotCorpusTrainer
def home(request):
    return render(request, 'main/home.html')
def articles_list(request):
    articles = Article.objects.all().order_by('date')
    return render(request, 'main/articles_list.html', {'articles': articles})
def chatbot(request):
    return render(request, 'main/blogchatbot.html')
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")

@csrf_exempt
@require_http_methods(["POST"])
def chatbot_view(request):
    user_input = request.POST.get('Value')
    if not user_input:
        return JsonResponse({"response": "Please provide a question."})

    # Tokenize the user input and generate a response
    input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")
    chat_history_ids = model.generate(input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    
    # Decode the generated response
    response = tokenizer.decode(chat_history_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
    
    return JsonResponse({"response": response})


# Charger le modèle de langage
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")

def search_articles(query, articles):
    # Générer un résumé pour chaque article et vérifier la pertinence par rapport à la requête
    relevant_articles = []
    for article in articles:
        inputs = tokenizer.encode("summarize: " + article.content, return_tensors="pt", max_length=512, truncation=True)
        summary_ids = model.generate(inputs, max_length=150, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        
        if query.lower() in summary.lower():
            relevant_articles.append(article)

    return relevant_articles

@csrf_exempt
@require_http_methods(["POST"])
def search_view(request):
    query = request.POST.get('query', '')
    if not query:
        return JsonResponse({"response": "Please provide a search query."})

    articles = Article.objects.all()
    relevant_articles = search_articles(query, articles)
    
    response_data = [{"title": article.title, "content": article.content} for article in relevant_articles]

    return JsonResponse({"response": response_data})
# chatbot = ChatBot('MyBot')
# trainer = ChatterBotCorpusTrainer(chatbot)
# trainer.train('chatterbot.corpus.english')
# @csrf_exempt
# @require_http_methods(["POST"])
# def chatbot_view(request):
#     user_input = request.POST.get('question', '').strip()
    
#     if not user_input:
#         return JsonResponse({"response": "Please provide a question."})
    
#     # Générer une réponse avec le chatbot
#     response = chatbot.get_response(user_input)
#     answer = str(response)
    
#     return JsonResponse({"response": answer})
# chatbot_pipeline = pipeline('conversational', model='facebook/blenderbot-400M-distill')

# @csrf_exempt
# @require_http_methods(["POST"])
# def chatbot_view(request):
#     # Récupération de la question depuis la requête POST
#     user_input = request.POST.get('Value', '').strip()
#     print(user_input)
    
#     if not user_input:
#         return JsonResponse({"response": "Please provide a question."})
    
#     try:
#         # Générer une réponse avec le modèle
#         response = chatbot_pipeline(user_input)
        
#         # Assurez-vous que response est correctement formatée
#         if isinstance(response, list) and response:
#             answer = response[0]['generated_text']
#         elif isinstance(response, dict) and 'generated_text' in response:
#             answer = response['generated_text']
#         else:
#             raise ValueError("Invalid response format from chatbot_pipeline")
        
#         # Log pour vérification
#         print(f"Input: {user_input}, Answer: {answer}")
        
#         # Retourner la réponse du chatbot sous forme de JSON
#         return JsonResponse({"response": answer})
    
#     except Exception as e:
#         # Gérer les exceptions, par exemple si le modèle ne peut pas générer de réponse
#         return JsonResponse({"response": str(e)})
# @csrf_exempt
# @require_http_methods(["POST"]) # type: ignore
# def chatbot_view(request):
#     user_input = request.POST.get('question', '')
#     print(user_input)
#     openai.api_key = "sk-proj-InmbAt7eYVSfjyI3DvGAT3BlbkFJEPD5d1ZKjUpc3BwIgTEQ"
#     response = openai.Completion.create(
#         engine="gpt-3.5-turbo",  
#         prompt=user_input,
#         max_tokens=150
#     )
#     answer = response.choices[0].text.strip()
#     return JsonResponse({"response": answer})
