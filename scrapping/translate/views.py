from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from googletrans import Translator
from docx import Document
from summa.summarizer import summarize
from summa.keywords import keywords

def scrape_and_save(request):
    if request.method == 'POST':
        url = request.POST.get('url')

        if not url:
            error_message = 'URL is required.'
            return render(request, 'result.html', {'error_message': error_message})

        try:
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                text_content = soup.get_text()

                translator = Translator()
                translated_text = translator.translate(text_content, src='mr', dest='en').text

                # Generate summary
                summary = summarize(translated_text)
                print(summary)

                # Extract keywords
                extracted_keywords = keywords(translated_text).split('\n')
                print(extracted_keywords)

                return render(request, 'result.html', {'url': url, 'scraped_text': text_content, 'translated_text': translated_text, 'summary': summary, 'keywords': extracted_keywords})
            else:
                error_message = 'Failed to fetch data from the website. Please enter a valid URL.'
                return render(request, 'result.html', {'error_message': error_message})
        except Exception as e:
            error_message = f'An error occurred: {str(e)}'
            return render(request, 'result.html', {'error_message': error_message})

    return render(request, 'scrape_form.html')
