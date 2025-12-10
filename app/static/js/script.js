document.addEventListener('DOMContentLoaded', () => {
    console.log("Game Loaded");

    const img = document.getElementById('dino-img');
    if (img) {
        img.onerror = () => {
            img.style.display = 'none'; // Hide broken image icon
            
            // Avoid creating duplicate placeholders
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
});

async function sendAction(actionType) {
    const inputField = document.getElementById('user-input');
    const userMessage = inputField.value;
    
    if (actionType === 'chat' && !userMessage.trim()) return;

    if (actionType === 'chat') {
        addToChatHistory("You", userMessage);
        inputField.value = ""; 
    }

    document.getElementById('ai-response').innerText = "...";
    
    const img = document.getElementById('dino-img');
    img.src = "/static/images/dino_thinking.png"; 
    img.style.opacity = "0.75"; 

    try {
        const response = await fetch('/api/interact', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                action: actionType, 
                message: userMessage 
            })
        });

        const data = await response.json();

        updateGameState(data.stats);
        document.getElementById('ai-response').innerText = data.response;
        addToChatHistory("Dino", data.response);
        updateDinoImage(data.stats);

    } catch (error) {
        console.error('Error:', error);
        document.getElementById('ai-response').innerText = "System Error: Brain disconnected.";
        img.src = "/static/images/dino_normal.png";
        
    } finally {
        document.getElementById('dino-img').style.opacity = "1";
    }
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
    const p = document.createElement('p');
    p.innerHTML = `<strong>${sender}:</strong> ${text}`;
    history.appendChild(p);
    history.scrollTop = history.scrollHeight; 
}