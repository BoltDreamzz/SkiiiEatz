from django.urls import path
from . import views

app_name = 'skiii_bot'

urlpatterns = [
    path('api/upload-pdf/', views.upload_pdf, name='upload_pdf'),
    path('api/process-pdf/', views.process_pdf, name='process_pdf'),
    path('api/chat/', views.chat, name='chat'),
    path('api/knowledge-status/', views.knowledge_status, name='knowledge_status'),
    path('api/train-qa/', views.train_qa, name='train_qa'),]