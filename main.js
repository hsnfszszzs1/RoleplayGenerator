function generatePrompt() {
    const params = {
        character_name: document.getElementById('char_name').value,
        personality_traits: document.getElementById('personality').value,
        speech_style: document.getElementById('speech').value,
        setting: document.getElementById('setting').value,
        mood: document.getElementById('mood').value,
        relationship_dynamic: document.getElementById('relationship').value,
        emotional_intensity: document.getElementById('intensity').value + '%',
        sexual_tension: document.getElementById('tension').value,
        power_dynamic: document.getElementById('power').value
    };

    // Simulate calling the Python backend
    const prompt = `You are ${params.character_name}.

PERSONALITY: ${params.personality_traits}
SPEECH STYLE: ${params.speech_style}
SETTING: ${params.setting}
MOOD: ${params.mood}
RELATIONSHIP: ${params.relationship_dynamic}

CURRENT STATE:
- Emotional Intensity: ${params.emotional_intensity}
- Sexual Tension: ${params.sexual_tension}/100
- Power Dynamic: ${params.power_dynamic}

Stay in character. Match the intensity. Never break immersion.`;

    document.getElementById('prompt_output').textContent = prompt;
    document.getElementById('output').style.display = 'block';
}

// Live update sliders
document.addEventListener('DOMContentLoaded', () => {
    const intensity = document.getElementById('intensity');
    const tension = document.getElementById('tension');

    if (intensity) {
        intensity.oninput = () => {
            document.getElementById('intensity_val').textContent = intensity.value;
        };
    }
    if (tension) {
        tension.oninput = () => {
            document.getElementById('tension_val').textContent = tension.value;
        };
    }
});