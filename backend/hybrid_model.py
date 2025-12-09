from sentence_transformers import SentenceTransformer, util
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import webbrowser
import numpy as np

df = pd.read_csv("assistant_dataset.csv", encoding="ISO-8859-1")

questions = df["Question"].tolist()
intents = df["Intent"].tolist()
answers = df["Answer"].tolist()

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Encoding dataset...")
question_embeddings = model.encode(questions)

X_train, X_test, y_train, y_test = train_test_split(
    question_embeddings, intents, test_size=0.2, random_state=42
)

clf = LogisticRegression(max_iter=2000)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
model_accuracy = accuracy_score(y_test, y_pred) * 100

print("Assistant Ready!")

def google_search(query):
  url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
  webbrowser.open(url)

def youtube_search(query):
  url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
  webbrowser.open(url)

def get_reply(query):

  emb = model.encode([query])
  predicted_intent = clf.predict(emb)[0]
  print("Predicted Intent:", predicted_intent)

  sims = util.cos_sim(model.encode(query, convert_to_tensor=True), 
                      model.encode(questions, convert_to_tensor=True))[0]
  
  best_score = float(sims.max())
  idx = int(sims.argmax().item())
  answer = answers[idx]

  print("Similarity Score:", best_score)

  q = query.lower()

  if predicted_intent == "GoogleSearch" or "search" in q or "google" in q or "search for" in q:
    google_search(query)
    return f"{query} on Google."
  
  if predicted_intent == "YouTubeSearch" or "youtube" in q or "playlist" in q:
    youtube_search(query)
    return f"{query} on YouTube."
  
  if ("what is" in q or
      "who is" in q or
      "define" in q or
      "tell me about" in q):
    
    if best_score >= 0.60:
      return answer
    else:
      return "I don't know this yet, but I'm still learning!"
    
  if best_score >= 0.60:
    return answer

def get_accuracy():
    return round(model_accuracy, 2)
