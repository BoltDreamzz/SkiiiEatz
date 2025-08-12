class Chatbot {
    constructor() {
        this.chatHistory = [];
        this.isTyping = false;
        this.currentKnowledgeBase = null;
        this.initializeElements();
        this.setupEventListeners();
        this.showChatButtonWithDelay();
        this.checkKnowledgeStatus();
        
        // // For development - show admin panel
        // if (window.location.href.includes('localhost')) {
        //     this.elements.adminPanel.classList.remove('hidden');
        // }
        // // For development - show admin panel
        // if (window.location.href.includes('127.0.0.1')) {
        //     this.elements.adminPanel.classList.remove('hidden');
        // }
    }

    initializeElements() {
        this.elements = {
            chatbotButton: document.getElementById('chatbot-button'),
            chatbotModal: document.getElementById('chatbot-modal'),
            closeChat: document.getElementById('close-chat'),
            clearChat: document.getElementById('clear-chat'),
            chatMessages: document.getElementById('chat-messages'),
            userInput: document.getElementById('user-input'),
            sendButton: document.getElementById('send-button'),
            uploadPdf: document.getElementById('upload-pdf'),
            pdfUpload: document.getElementById('pdf-upload'),
            loadingTemplate: document.getElementById('loading-template'),
            knowledgeStatus: document.getElementById('knowledge-status'),
            adminPanel: document.getElementById('admin-panel'),
            adminPdfUpload: document.getElementById('admin-pdf-upload'),
            pdfTitle: document.getElementById('pdf-title'),
            processPdf: document.getElementById('process-pdf'),
            processingStatus: document.getElementById('processing-status')
        };
    }

    setupEventListeners() {
        this.elements.chatbotButton.addEventListener('click', () => this.toggleChat());
        this.elements.closeChat.addEventListener('click', () => this.toggleChat());
        this.elements.clearChat.addEventListener('click', () => this.clearChat());
        this.elements.sendButton.addEventListener('click', () => this.handleUserMessage());
        this.elements.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.handleUserMessage();
        });
        this.elements.uploadPdf.addEventListener('click', () => this.elements.pdfUpload.click());
        this.elements.pdfUpload.addEventListener('change', (e) => this.handlePdfUpload(e));
        
        // Admin panel events
        this.elements.processPdf.addEventListener('click', () => this.processPdf());
    }

    showChatButtonWithDelay() {
        setTimeout(() => {
            this.elements.chatbotButton.classList.remove('opacity-0');
            this.elements.chatbotButton.classList.add('opacity-100');
        }, 5000);
    }

    toggleChat() {
        this.elements.chatbotModal.classList.toggle('hidden');
    }

    clearChat() {
        this.chatHistory = [];
        this.elements.chatMessages.innerHTML = '<div class="text-center text-sm text-gray-500 py-4">Hello skiii ! How far na ?</div>';
    }

    async checkKnowledgeStatus() {
        try {
            const response = await fetch('{% url "chat_bot:knowledge_status" %}');
            if (response.ok) {
                const data = await response.json();
                this.elements.knowledgeStatus.textContent = `Knowledge: ${data.status}`;
                this.elements.knowledgeStatus.className = data.status === 'Loaded' ? 
                    'text-green-600' : 'text-gray-400';
            }
        } catch (error) {
            console.error('Error checking knowledge status:', error);
        }
    }

    async handleUserMessage() {
        const message = this.elements.userInput.value.trim();
        if (!message) return;

        this.addMessageToChat('user', message);
        this.elements.userInput.value = '';

        // Show loading indicator
        this.showLoadingIndicator();

        try {
            const response = await this.sendMessageToBackend(message);
            
            // Remove loading indicator
            this.removeLoadingIndicator();

            // Display response with typing effect
            await this.displayTypingResponse(response);
        } catch (error) {
            this.removeLoadingIndicator();
            this.addMessageToChat('assistant', "Ooops! No vex. Please try again.");
            console.error('Chat error:', error);
        }
    }

    async sendMessageToBackend(message) {
        const response = await fetch('{% url "chat_bot:chat" %}', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCSRFToken(),
            },
            body: JSON.stringify({
                message: message,
                chat_history: this.chatHistory
            })
        });

        if (!response.ok) {
            throw new Error('Omo network no gree. Please try again later.');
        }

        const data = await response.json();
        return data.response;
    }

    addMessageToChat(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `flex mb-4 p-2 ${role === 'user' ? 'justify-end' : 'justify-start'}`;
        
        const bubble = document.createElement('div');
        bubble.className = `${role === 'user' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-800'} rounded-2xl p-3 max-w-xs`;
        bubble.textContent = content;
        
        messageDiv.appendChild(bubble);
        this.elements.chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        this.elements.chatMessages.scrollTop = this.elements.chatMessages.scrollHeight;
        
        // Add to chat history
        this.chatHistory.push({ role, content });
    }

    showLoadingIndicator() {
        const loadingIndicator = this.elements.loadingTemplate.content.cloneNode(true);
        this.elements.chatMessages.appendChild(loadingIndicator);
        this.elements.chatMessages.scrollTop = this.elements.chatMessages.scrollHeight;
    }

    removeLoadingIndicator() {
        const loadingIndicators = document.querySelectorAll('.flex.space-x-2');
        if (loadingIndicators.length > 0) {
            loadingIndicators[loadingIndicators.length - 1].parentElement.parentElement.remove();
        }
    }

    async displayTypingResponse(response) {
        this.isTyping = true;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = 'flex mb-4 justify-start';
        
        const bubble = document.createElement('div');
        bubble.className = 'bg-gray-100 text-gray-800 rounded-2xl p-3 max-w-xs typing-animation';
        bubble.textContent = '';
        
        messageDiv.appendChild(bubble);
        this.elements.chatMessages.appendChild(messageDiv);
        
        // Type out the response character by character
        for (let i = 0; i < response.length; i++) {
            if (!this.isTyping) break; // Allow cancellation
            bubble.textContent = response.substring(0, i + 1);
            await new Promise(resolve => setTimeout(resolve, 20));
        }
        
        bubble.classList.remove('typing-animation');
        this.isTyping = false;
        
        // Scroll to bottom
        this.elements.chatMessages.scrollTop = this.elements.chatMessages.scrollHeight;
        
        // Add to chat history
        this.chatHistory.push({ role: 'assistant', content: response });
    }

    async handlePdfUpload(event) {
        const file = event.target.files[0];
        if (!file) return;
        
        this.showLoadingIndicator();
        this.addMessageToChat('assistant', `Processing your PDF: ${file.name}...`);
        
        const formData = new FormData();
        formData.append('pdf', file);
        
        try {
            const response = await fetch('{% url "chat_bot:upload_pdf" %}', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': this.getCSRFToken(),
                }
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                this.addMessageToChat('assistant', `✔️ PDF "${data.title}" uploaded successfully. Make i check am well...`);
                await this.processPdf(data.id);
            } else {
                this.addMessageToChat('assistant', `🚫 Error: ${data.message}`);
            }
        } catch (error) {
            this.addMessageToChat('assistant', "🚫 No vex! The PDF no gree upload.");
            console.error('Upload error:', error);
        } finally {
            this.removeLoadingIndicator();
        }
    }

    async processPdf(pdfId = null) {
        // If pdfId is not provided, we're using the admin panel
        const isAdminProcess = pdfId === null;
        
        if (isAdminProcess) {
            const file = this.elements.adminPdfUpload.files[0];
            const title = this.elements.pdfTitle.value.trim() || file.name;
            
            if (!file) {
                alert('Please select a PDF file first');
                return;
            }
            
            this.elements.processingStatus.textContent = "Uploading PDF...";
            this.elements.processingStatus.classList.remove('hidden');
            
            const formData = new FormData();
            formData.append('pdf', file);
            formData.append('title', title);
            
            try {
                const uploadResponse = await fetch('{% url "chat_bot:upload_pdf" %}', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': this.getCSRFToken(),
                    }
                });
                
                const uploadData = await uploadResponse.json();
                
                if (uploadData.status === 'success') {
                    this.elements.processingStatus.textContent = "Processing PDF...";
                    pdfId = uploadData.id;
                } else {
                    this.elements.processingStatus.textContent = `🚫 Error: ${uploadData.message}`;
                    return;
                }
            } catch (error) {
                this.elements.processingStatus.textContent = "Upload failed";
                console.error('Upload error:', error);
                return;
            }
        }
        
        try {
            const response = await fetch('{% url "chat_bot:upload_pdf" %}', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken(),
                },
                body: JSON.stringify({
                    pdf_id: pdfId
                })
            });
            
            const data = await response.json();
            
            if (isAdminProcess) {
                if (data.status === 'success') {
                    this.elements.processingStatus.textContent = `Processed successfully! Added ${data.qa_count} Q&A pairs.`;
                    setTimeout(() => {
                        this.elements.processingStatus.classList.add('hidden');
                    }, 3000);
                } else {
                    this.elements.processingStatus.textContent = `Error: ${data.message}`;
                }
            } else {
                if (data.status === 'success') {
                    this.addMessageToChat('assistant', `🥳 PDF processing complete! I don check am ${data.qa_count} new things.`);
                    this.checkKnowledgeStatus();
                } else {
                    this.addMessageToChat('assistant', `🚫 Error: ${data.message}`);
                }
            }
        } catch (error) {
            if (isAdminProcess) {
                this.elements.processingStatus.textContent = "Processing failed";
            } else {
                this.addMessageToChat('assistant', "🚫 No vex, the PDF no gree work.");
            }
            console.error('Processing error:', error);
        }
    }

    getCSRFToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue || '';
    }
}

// Initialize the chatbot when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new Chatbot();
});