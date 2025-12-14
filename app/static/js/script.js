// Global state
let isProcessing = false;
let debounceTimer = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log("Game Loaded");
    
    // Load chat history from localStorage
    loadChatHistory();
    
    // Setup image error handling
    const img = document.getElementById('dino-img');
    if (img) {
        img.onerror = () => {
            img.style.display = 'none';
            if (document.getElementById('dino-placeholder')) return;

            const placeholder = document.createElement('div');
            placeholder.id = 'dino-placeholder';
            placeholder.style.width = img.width + 'px';
            placeholder.style.height = img.height + 'px';
            placeholder.style.backgroundColor = '#ddd';
            placeholder.style.borderRadius = '50%';
            placeholder.style.border = '2px solid #aaa';
            img.parentNode.insertBefore(placeholder, img.nextSibling);
        };
    }
    
    // Setup Enter key support for chat input
    const inputField = document.getElementById('user-input');
    if (inputField) {
        inputField.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendAction('chat');
            }
        });
        
        // Focus input on load
        inputField.focus();
    }
    
    // Setup keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Only trigger if not typing in input
        if (document.activeElement === inputField) {
            return;
        }
        
        // Quick action shortcuts
        if (e.key === 'f' || e.key === 'F') {
            e.preventDefault();
            sendAction('feed');
        } else if (e.key === 'p' || e.key === 'P') {
            e.preventDefault();
            sendAction('pet');
        } else if (e.key === 's' || e.key === 'S') {
            e.preventDefault();
            sendAction('sleep');
        }
    });
});

async function sendAction(actionType) {
    // Prevent duplicate requests
    if (isProcessing) {
        console.log("Request already in progress, please wait...");
        return;
    }
    
    // Debounce rapid clicks
    if (debounceTimer) {
        clearTimeout(debounceTimer);
    }
    
    debounceTimer = setTimeout(async () => {
        const inputField = document.getElementById('user-input');
        const userMessage = inputField ? inputField.value.trim() : "";
        
        if (actionType === 'chat' && !userMessage) {
            showNotification("Please enter a message first!", "warning");
            return;
        }

        isProcessing = true;
        setLoadingState(true);
        
        // Add user action to chat history for non-chat actions
        if (actionType !== 'chat') {
            const actionNames = {
                'feed': '🍖 Fed',
                'pet': '🖐️ Petted',
                'sleep': '🌙 Put to sleep'
            };
            addToChatHistory("You", actionNames[actionType] || `Performed ${actionType} action`);
        }
        
        // Clear input for chat action
        if (actionType === 'chat' && inputField) {
            addToChatHistory("You", userMessage);
            inputField.value = "";
        }

        try {
            const response = await fetch('/api/interact', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    action: actionType, 
                    message: userMessage 
                })
            });

            // Check if response is ok
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ error: 'Unknown error' }));
                throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();

            // Validate response data
            if (!data || !data.stats) {
                throw new Error("Invalid response from server");
            }

            updateGameState(data.stats);
            document.getElementById('ai-response').innerText = data.response || "Roar?";
            
            // Always add Dino's response to chat history for all actions
            if (data.response) {
                addToChatHistory("Dino", data.response);
            }
            
            updateDinoImage(data.stats);
            showNotification("Action completed!", "success");

        } catch (error) {
            console.error('Error:', error);
            const errorMessage = error.message || "System Error: Brain disconnected.";
            document.getElementById('ai-response').innerText = errorMessage;
            showNotification(errorMessage, "error");
            
            const img = document.getElementById('dino-img');
            if (img) {
                img.src = "/static/images/dino_normal.png";
            }
        } finally {
            isProcessing = false;
            setLoadingState(false);
        }
    }, 300); // 300ms debounce
}

function updateGameState(stats) {
    document.getElementById('pet-name').innerText = stats.name;
    
    document.getElementById('stat-day').innerText = stats.day;
    document.getElementById('stat-time').innerText = stats.time_phase;

    document.getElementById('bar-hunger').style.width = stats.hunger + "%";
    document.getElementById('bar-mood').style.width = stats.mood + "%";
    document.getElementById('bar-affinity').style.width = stats.affinity + "%";

    document.getElementById('hunger-val').innerText = stats.hunger;
    document.getElementById('mood-val').innerText = stats.mood;
    document.getElementById('affinity-val').innerText = stats.affinity;
    

    if (stats.time_phase === "Night") {
        document.body.style.backgroundColor = "#2c3e50";
    } else {
        document.body.style.backgroundColor = "#f0f0f0";
    }
}

function updateDinoImage(stats) {
    const img = document.getElementById('dino-img');
    
    let imgSrc = "/static/images/dino_normal.png"; 

    if (stats.time_phase === "Night") {
        imgSrc = "/static/images/dino_sleep.png"; 
    } 
    else if (stats.hunger < 20) {
        imgSrc = "/static/images/dino_hungry.png";
    } 
    else if (stats.mood > 80) {
        imgSrc = "/static/images/dino_happy.png"; 
    }

    if (!img.src.includes(imgSrc)) {
        img.src = imgSrc;
    }
}

function addToChatHistory(sender, text) {
    const history = document.getElementById('chat-history');
    if (!history) return;
    
    const p = document.createElement('p');
    p.className = `chat-message ${sender.toLowerCase()}`;
    p.innerHTML = `<strong>${sender}:</strong> <span class="message-text">${escapeHtml(text)}</span>`;
    history.appendChild(p);
    history.scrollTop = history.scrollHeight;
    
    // Save to localStorage
    saveChatHistory();
}

function loadChatHistory() {
    try {
        const saved = localStorage.getItem('dino_chat_history');
        if (saved) {
            const messages = JSON.parse(saved);
            const history = document.getElementById('chat-history');
            if (history && messages.length > 0) {
                messages.forEach(msg => {
                    const p = document.createElement('p');
                    p.className = `chat-message ${msg.sender.toLowerCase()}`;
                    p.innerHTML = `<strong>${msg.sender}:</strong> <span class="message-text">${escapeHtml(msg.text)}</span>`;
                    history.appendChild(p);
                });
                history.scrollTop = history.scrollHeight;
            }
        }
    } catch (error) {
        console.error("Failed to load chat history:", error);
    }
}

function saveChatHistory() {
    try {
        const history = document.getElementById('chat-history');
        if (!history) return;
        
        const messages = [];
        const messageElements = history.querySelectorAll('.chat-message');
        
        messageElements.forEach(msgEl => {
            const sender = msgEl.querySelector('strong')?.textContent || 'Unknown';
            const text = msgEl.querySelector('.message-text')?.textContent || '';
            if (sender && text) {
                messages.push({ sender, text });
            }
        });
        
        // Keep only last 50 messages to avoid localStorage size limits
        const messagesToSave = messages.slice(-50);
        localStorage.setItem('dino_chat_history', JSON.stringify(messagesToSave));
    } catch (error) {
        console.error("Failed to save chat history:", error);
    }
}

function clearChatHistory() {
    const history = document.getElementById('chat-history');
    if (history) {
        history.innerHTML = '';
        localStorage.removeItem('dino_chat_history');
        showNotification("Chat history cleared!", "success");
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function setLoadingState(loading) {
    const buttons = document.querySelectorAll('button');
    const inputField = document.getElementById('user-input');
    const img = document.getElementById('dino-img');
    
    buttons.forEach(btn => {
        btn.disabled = loading;
        btn.style.opacity = loading ? '0.6' : '1';
        btn.style.cursor = loading ? 'not-allowed' : 'pointer';
    });
    
    if (inputField) {
        inputField.disabled = loading;
    }
    
    if (img) {
        if (loading) {
            img.src = "/static/images/dino_thinking.png";
            img.style.opacity = "0.75";
            img.classList.add('thinking');
        } else {
            img.style.opacity = "1";
            img.classList.remove('thinking');
        }
    }
    
    // Update loading indicator in response bubble
    const responseBubble = document.getElementById('ai-response');
    if (responseBubble && loading) {
        responseBubble.innerHTML = '<span class="loading-dots">...</span>';
    }
}

function showNotification(message, type = 'info') {
    // Remove existing notification
    const existing = document.getElementById('notification');
    if (existing) {
        existing.remove();
    }
    
    const notification = document.createElement('div');
    notification.id = 'notification';
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => notification.classList.add('show'), 10);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}