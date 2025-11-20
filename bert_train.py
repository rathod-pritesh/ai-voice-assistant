from transformers import BertTokenizer, BertForSequenceClassification
import torch
import torch.nn.functional as F
import speech_recognition as sr
import pyttsx3

# --- Training data ---
X_train = [
    "search for microsoft",
    "look up weather in delhi on google",
    "find python playlist on youtube",
    "play lo-fi music on youtube",
    "open google",
    "search news on google",
    "what is ai",
    "who are you",
    "tell me a joke",
    "explain quantum computing"
]
y_train = [
    "GoogleSearch",
    "GoogleSearch",
    "YouTubeSearch",
    "YouTubeSearch",
    "GoogleSearch",
    "GoogleSearch",
    "GeneralQuery",
    "GeneralQuery",
    "GeneralQuery",
    "GeneralQuery"
]


# --- Prepare label mappings ---
labels = sorted(set(y_train))
label2id = {label: i for i, label in enumerate(labels)}
id2label = {i: label for label, i in label2id.items()}

# --- Load BERT and tokenizer ---
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForSequenceClassification.from_pretrained(
    "bert-base-uncased", num_labels=len(labels)
)

# --- Tokenize all texts at once ---
inputs = tokenizer(X_train, padding=True, truncation=True, return_tensors="pt")
targets = torch.tensor([label2id[y] for y in y_train])

optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)
model.train()
for _ in range(10):  
    outputs = model(**inputs, labels=targets)
    loss = outputs.loss
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()
print("Training done, final loss:", round(loss.item(), 4))

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    print("🗣️  Speaking:", text)
    engine.setProperty('rate', 170)
    engine.setProperty('volume', 0.8)
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("\n🎤 Speak now..")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("📝 You said:", text)
        return text
    except sr.UnknownValueError:
        print("❌ Sorry, I couldn’t understand that.")
        return None
    except sr.RequestError:
        print("⚠️ Speech service error.")
        return None

# --- Test prediction ---
model.eval()
while True:
    command = listen()
    if command is None:
        continue

    if command.lower() in ["exit", "quit", "stop"]:
        speak("Goodbye!")
        break

    test_inputs = tokenizer(command, return_tensors="pt")
    with torch.no_grad():
        logits = model(**test_inputs).logits
        pred = torch.argmax(F.softmax(logits, dim=1)).item()

    intent = id2label[pred]
    print("🤖 Predicted Intent:", intent)
    speak(f"The intent is {intent}")
