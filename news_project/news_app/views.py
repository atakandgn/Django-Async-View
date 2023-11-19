# news_app/views.py
from django.shortcuts import render
import httpx
import requests
import time
import aiohttp
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse, JsonResponse
from django.contrib import messages 

secretApiKey = '748f25a23a3b4382b6e401d5b3852d03'

api_key = '98c637c4a52847229f6201402231911 '
city = 'Istanbul'
unit = 'metric'

def homepage(request):
    start_time = time.time()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Homepage Load Time: {elapsed_time} seconds")
    messages.info(request, f"Homepage Load Time: {elapsed_time} seconds") 
    return render(request, 'homepage.html')

# Asenkron Django view
async def async_news(request):
    start_time = time.time()

    async with httpx.AsyncClient() as client:
        parameters = {'country': 'us', 'apiKey' : secretApiKey}
        response = await client.get('https://newsapi.org/v2/top-headlines', params=parameters)
    async_news_data = response.json()
    
    async with httpx.AsyncClient() as client:
        parameters = { 'q': 'bitcoin', 'apiKey' : secretApiKey}
        response = await client.get('https://newsapi.org/v2/everything', params=parameters)
    async_news_data2 = response.json()


    async with httpx.AsyncClient() as client:
        response = await client.get(f'https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&unit={unit}')
        weather_data = response.json()


    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Async News View Load Time: {elapsed_time} seconds")
    
    
    return render(request, 'async_news_list.html', {'async_news_data': async_news_data, 'async_news_data2': async_news_data2, 'weather_data': weather_data, 'elapsed_time': elapsed_time})
    



# Synchronous Django view
def sync_news(request):
    start_time = time.time()

    parameters = {'country': 'us', 'apiKey': secretApiKey}
    api_url = 'https://newsapi.org/v2/top-headlines'
    
    response = requests.get(api_url, params=parameters)
    news_data = response.json()
    
    parameters = {'q': 'bitcoin', 'apiKey': secretApiKey}
    api_url = 'https://newsapi.org/v2/everything'
    
    response = requests.get(api_url, params=parameters)
    news_data2 = response.json()
   
    response = requests.get(f'https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&unit={unit}')
    weather_data = response.json()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Sync News View Load Time: {elapsed_time} seconds")

    return render(request, 'sync_news_list.html', {'news_data': news_data, 'news_data2': news_data2, 'weather_data': weather_data, 'elapsed_time': elapsed_time})

async def async_file_upload_view(request):
    if request.method == 'POST' and request.FILES:
        # Get the file from post request
        uploaded_file = request.FILES['file']
        upload_path = os.path.join('uploads', uploaded_file.name)

        # Save the file to the specified path
        with default_storage.open(upload_path, 'wb') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Dosyanın yüklendiği klasörü kontrol eder
        upload_folder = os.path.join(default_storage.location, 'uploads')
        if os.path.exists(os.path.join(upload_folder, uploaded_file.name)):
            
            return JsonResponse({'status': 'success', 'message': 'File uploaded successfully. The file is in the upload folder.'})
        else:
           
            return JsonResponse({'status': 'error', 'message': 'File upload failed.'})

    return render(request, 'async_file_upload.html')