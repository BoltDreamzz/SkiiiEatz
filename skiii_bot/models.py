from django.db import models
from django.contrib.postgres.fields import ArrayField

class PDFKnowledgeBase(models.Model):
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='Brainz_pdfs/')
    processed = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class QAPair(models.Model):
    knowledge_base = models.ForeignKey(PDFKnowledgeBase, on_delete=models.CASCADE, related_name='qa_pairs')
    question = models.TextField()
    answer = models.TextField()
    keywords = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Q: {self.question[:50]}..."