import json
import PyPDF2
import io
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import PDFKnowledgeBase, QAPair
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

@csrf_exempt
@require_POST
def upload_pdf(request):
    try:
        pdf_file = request.FILES['pdf']
        title = request.POST.get('title', pdf_file.name)
        
        # Save the PDF
        knowledge_base = PDFKnowledgeBase.objects.create(
            title=title,
            pdf_file=pdf_file
        )
        
        return JsonResponse({
            'status': 'success',
            'id': knowledge_base.id,
            'title': knowledge_base.title
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@csrf_exempt
@require_POST
def process_pdf(request):
    try:
        data = json.loads(request.body)
        pdf_id = data.get('pdf_id')
        
        knowledge_base = PDFKnowledgeBase.objects.get(id=pdf_id)
        
        # Extract text from PDF
        pdf_text = extract_text_from_pdf(knowledge_base.pdf_file)
        
        # In a real implementation, you would parse Q&A from the PDF
        # For this example, we'll simulate extracted Q&A pairs
        simulated_qa_pairs = [
            {
                'question': 'What is the return policy?',
                'answer': 'Our return policy allows returns within 30 days of purchase.',
                'keywords': ['return', 'policy', 'refund']
            },
            {
                'question': 'How can I contact support?',
                'answer': 'You can contact support 24/7 at support@example.com or call +1 (555) 123-4567.',
                'keywords': ['contact', 'support', 'help']
            },
            {
                'question': 'What payment methods do you accept?',
                'answer': 'We accept Visa, MasterCard, American Express, and PayPal.',
                'keywords': ['payment', 'credit card', 'paypal']
            }
        ]
        
        # Save Q&A pairs
        for qa in simulated_qa_pairs:
            QAPair.objects.create(
                knowledge_base=knowledge_base,
                question=qa['question'],
                answer=qa['answer'],
                keywords=qa['keywords']
            )
        
        knowledge_base.processed = True
        knowledge_base.save()
        
        return JsonResponse({
            'status': 'success',
            'processed': True,
            'qa_count': len(simulated_qa_pairs)
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

@csrf_exempt
@require_POST
def chat(request):
    try:
        data = json.loads(request.body)
        message = data.get('message', '').lower().strip()
        
        # Get all Q&A pairs
        qa_pairs = QAPair.objects.all()
        
        if not qa_pairs.exists():
            return JsonResponse({
                'response': "I haven't been trained with any knowledge yet.",
                'status': 'success'
            })
        
        # Vectorize questions and find the most similar one
        questions = [qa.question for qa in qa_pairs]
        vectorizer = TfidfVectorizer().fit(questions + [message])
        
        question_vectors = vectorizer.transform(questions)
        message_vector = vectorizer.transform([message])
        
        similarities = cosine_similarity(message_vector, question_vectors)
        best_match_idx = np.argmax(similarities)
        best_match_score = similarities[0, best_match_idx]
        
        # Only return answer if similarity score is above threshold
        if best_match_score > 0.5:
            best_answer = qa_pairs[best_match_idx].answer
            return JsonResponse({
                'response': best_answer,
                'status': 'success',
                'confidence': float(best_match_score)
            })
        else:
            return JsonResponse({
                'response': "I'm not sure about that. Could you rephrase your question?",
                'status': 'success',
                'confidence': float(best_match_score)
            })
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'status': 'error'
        }, status=400)
    

from django.http import JsonResponse
from .models import QAPair

def knowledge_status(request):
    qa_count = QAPair.objects.count()
    status = "Loaded" if qa_count > 0 else "Not loaded"
    return JsonResponse({
        'status': status,
        'qa_count': qa_count
    })

@csrf_exempt
@require_POST
def train_qa(request):
    try:
        data = json.loads(request.body)
        question = data.get('question')
        answer = data.get('answer')
        keywords = data.get('keywords', [])
        
        if not question or not answer:
            return JsonResponse({
                'status': 'error',
                'message': 'Question and answer are required'
            }, status=400)
            
        # Create new Q&A pair
        QAPair.objects.create(
            question=question,
            answer=answer,
            keywords=keywords
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Q&A pair added successfully'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)