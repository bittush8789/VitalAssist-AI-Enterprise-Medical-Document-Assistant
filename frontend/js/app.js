// UI Navigation
function switchView(viewId, element) {
    document.querySelectorAll('.view-section').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
    
    const targetView = document.getElementById(viewId);
    if (targetView) targetView.classList.add('active');
    
    if (element) element.classList.add('active');
}

// Chart.js Initialization for Analytics
document.addEventListener('DOMContentLoaded', () => {
    // Diagnosis Doughnut Chart
    const ctxDiag = document.getElementById('diagnosisChart');
    if(ctxDiag) {
        new Chart(ctxDiag, {
            type: 'doughnut',
            data: {
                labels: ['Hypertension', 'Diabetes Type 2', 'Asthma', 'Anemia', 'Other'],
                datasets: [{
                    data: [35, 25, 15, 10, 15],
                    backgroundColor: ['#1E40AF', '#3B82F6', '#60A5FA', '#93C5FD', '#DBEAFE'],
                    borderWidth: 0
                }]
            },
            options: { cutout: '65%', plugins: { legend: { position: 'right' } } }
        });
    }

    // Volume Line Chart
    const ctxVol = document.getElementById('volumeChart');
    if(ctxVol) {
        new Chart(ctxVol, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Processed Documents',
                    data: [120, 190, 300, 250, 420, 480],
                    borderColor: '#3B82F6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: { plugins: { legend: { display: false } } }
        });
    }
});

// Chatbot Logic
function sendMessage() {
    const inputField = document.getElementById('chat-input');
    const message = inputField.value.trim();
    if(!message) return;

    const chatHistory = document.getElementById('chat-history');
    
    // Add User Message
    const userBubble = document.createElement('div');
    userBubble.className = 'chat-bubble chat-user';
    userBubble.textContent = message;
    chatHistory.appendChild(userBubble);
    
    inputField.value = '';
    chatHistory.scrollTop = chatHistory.scrollHeight;

    // Show typing indicator
    const typingBubble = document.createElement('div');
    typingBubble.className = 'chat-bubble chat-ai typing-indicator';
    typingBubble.innerHTML = '<span></span><span></span><span></span>';
    chatHistory.appendChild(typingBubble);
    chatHistory.scrollTop = chatHistory.scrollHeight;

    // Simulate API Call to Backend
    fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: message })
    })
    .then(res => res.json())
    .then(data => {
        chatHistory.removeChild(typingBubble);
        const aiBubble = document.createElement('div');
        aiBubble.className = 'chat-bubble chat-ai';
        aiBubble.textContent = data.response || "I could not find information in the uploaded medical report.";
        chatHistory.appendChild(aiBubble);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    })
    .catch(err => {
        chatHistory.removeChild(typingBubble);
        const errBubble = document.createElement('div');
        errBubble.className = 'chat-bubble chat-ai text-red-500 border-red-200';
        errBubble.textContent = "Error connecting to AI backend.";
        chatHistory.appendChild(errBubble);
    });
}

// File Upload Logic
const fileInput = document.getElementById('fileInput');
if(fileInput) {
    fileInput.addEventListener('change', function(e) {
        if(e.target.files.length > 0) {
            document.getElementById('processing-status').classList.remove('hidden');
            // Simulate upload progress
            setTimeout(() => {
                document.querySelector('#processing-status p').textContent = "Running LangGraph Multi-Agent Workflow...";
                document.querySelector('#processing-status .bg-blue-600').style.width = "85%";
            }, 1500);
            
            setTimeout(() => {
                document.querySelector('#processing-status p').textContent = "Analysis Complete. Context loaded into RAG Vector Store.";
                document.querySelector('#processing-status .bg-blue-600').style.width = "100%";
                document.querySelector('#processing-status .bg-blue-600').classList.add('bg-green-500');
            }, 3000);
        }
    });
}
