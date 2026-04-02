"""
NutriScan ChatBot engine — ML prediction only, no GUI.
Used by both the Django web interface (views.py) and the standalone Tkinter app (chatgui.py).
"""
import os
import json
import random
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer

# Paths relative to this file's location (project root)
_BASE = os.path.dirname(os.path.abspath(__file__))

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('wordnet', quiet=True)

# Load model and data once at module level
try:
    from keras.models import load_model
    _model = load_model(os.path.join(_BASE, 'chatbot_model.h5'), compile=False)
    _words = pickle.load(open(os.path.join(_BASE, 'words.pkl'), 'rb'))
    _classes = pickle.load(open(os.path.join(_BASE, 'classes.pkl'), 'rb'))
    _intents = json.loads(open(os.path.join(_BASE, 'intents.json'), encoding='utf-8').read())
    _lemmatizer = WordNetLemmatizer()
    _available = True
    print("[ChatBot] Model loaded successfully")
except Exception as e:
    _available = False
    _model = None
    _words = []
    _classes = []
    _intents = {"intents": []}
    _lemmatizer = WordNetLemmatizer()
    print(f"[ChatBot] Failed to load model: {e}")


def clean_up_sentence(sentence: str) -> list[str]:
    sentence_words = nltk.word_tokenize(sentence)
    return [_lemmatizer.lemmatize(w.lower()) for w in sentence_words]


def bow(sentence: str, words: list[str]) -> np.ndarray:
    sentence_words = clean_up_sentence(sentence)
    bag = [1 if s in sentence_words else 0 for s in words]
    return np.array(bag)


def predict_class(sentence: str) -> list[dict]:
    if not _available:
        return [{"intent": "unknown", "probability": "0"}]
    p = bow(sentence, _words)
    res = _model.predict(np.array([p]))[0]

    # If no strong match, return the highest scoring intent
    results = [[i, r] for i, r in enumerate(res) if r > 0.2]
    results.sort(key=lambda x: x[1], reverse=True)

    if not results:
        best = np.argmax(res)
        if res[best] > 0.05:
            return [{"intent": _classes[best], "probability": str(res[best])}]
        intent_map = _keyword_fallback(sentence.lower().strip())
        if intent_map:
            return [{"intent": intent_map, "probability": "0.5"}]
        return [{"intent": "unknown", "probability": "0"}]

    return [{"intent": _classes[r[0]], "probability": str(r[1])} for r in results]


def _keyword_fallback(sentence: str) -> str:
    """Map keywords in casual conversation to known intent tags."""
    text = sentence.lower()
    if any(w in text for w in ['how are you', 'doing', 'fine', 'good', 'great', 'awesome', 'how r u', 'whats up', 'sup', 'howdy']):
        return 'greeting'
    if any(w in text for w in ['workout', 'exercise', 'fit', 'gym', 'fitness', 'sport']):
        return 'exercise_advice'
    if any(w in text for w in ['water', 'drink', 'dehydrat', 'hydrate', 'thirst']):
        return 'hydration'
    if any(w in text for w in ['lose weight', 'lose fat', 'burn fat', 'slim', 'skinny', 'fat loss']):
        return 'weight_management'
    if any(w in text for w in ['gain weight', 'bulk', 'muscle', 'mass', 'heavy']):
        return 'weight_management'
    if any(w in text for w in ['sleep', 'tired', 'insomnia', 'nap', 'rest', 'bedtime']):
        return 'sleep_advice'
    if any(w in text for w in ['vitamin', 'pill', 'supplement', 'multi']):
        return 'vitamins_supplements'
    if any(w in text for w in ['heart', 'cholesterol', 'cardio']):
        return 'heart_health'
    if any(w in text for w in ['stress', 'anxiet', 'depress', 'mood', 'mental', 'brain', 'sad', 'feel bad']):
        return 'mental_health'
    if any(w in text for w in ['immunity', 'cough', 'cold', 'flu', 'sick', 'illness']):
        return 'immune_support'
    if any(w in text for w in ['allergy', 'allergic', 'intolerance', 'gluten', 'lactose', 'nut']):
        return 'food_allergy'
    if any(w in text for w in ['digest', 'stomach', 'gas', 'bloat', 'gut', 'constipat', 'acid']):
        return 'digestive_health'
    if any(w in text for w in ['meal prep', 'prep', 'cook', 'recipe', 'batch', 'quick meal']):
        return 'meal_prep'
    if any(w in text for w in ['protein', 'supplement', 'whey', 'amino']):
        return 'protein_supplements'
    if any(w in text for w in ['meal', 'timing', 'schedule', 'when to eat', 'when should i eat', 'breakfast time', 'dinner time']):
        return 'meal_timing'
    if any(w in text for w in ['weight', 'progress', 'track', 'scale', 'pounds', 'kg']):
        return 'weight_tracking'
    if any(w in text for w in ['thank', 'thanks', 'appreciate', 'great', 'nice', 'helpful', 'cool', 'awesome']):
        return 'feedback'
    return ''


def get_response(ints: list[dict]) -> str:
    if not ints or ints[0]["intent"] == "unknown":
        return random.choice([
            "Sorry, I didn't quite understand that. Could you rephrase?",
            "I'm not sure I got that. Do you want help with BMI, SMR, or diet plans?",
            "Hmm, I'm not trained for that query yet. Try typing 'BMI', 'SMR', or 'Diet'.",
        ])
    tag = ints[0]["intent"]
    for i in _intents["intents"]:
        if i["tag"] == tag:
            return random.choice(i["responses"])
    return "I didn't quite get that. Could you try again?"


def process_message(message: str) -> str:
    ints = predict_class(message)
    return get_response(ints)
