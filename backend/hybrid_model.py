from sentence_transformers import SentenceTransformer, util

BERT_MODEL = "all-MiniLM-L6-v2"
SIM_THERESHOLD = 0.60

FAQ = [
    {"q": "hi", "a": "Hello! How can I assist you today?"},
    {"q": "what is nlp", "a": "NLP means Natural Language Processing, which helps computers understand human language."},
    {"q": "goodbye", "a": "Goodbye! See you soon."},
    {"q": "what is ai", "a": "AI stands for Artificial Intelligence, which allows machines to learn and make decisions like humans."},
    {"q": "what is machine learning", "a": "Machine learning is a part of AI that allows systems to learn from data."},
    {"q": "types of machine learning", "a": "The main types of machine learning are supervised, unsupervised, and reinforcement learning."},
    {"q": "what is deep learning", "a": "Deep learning is a branch of machine learning that uses neural networks with many layers."},
    {"q": "what is python", "a": "Python is a programming language widely used in AI, backend development, and automation."},
]


print("Loading BERT Model...")
model = SentenceTransformer(BERT_MODEL)

faq_questions = [item["q"] for item in FAQ]
faq_emb = model.encode(faq_questions, convert_to_tensor=True)

def get_reply(query: str) -> str:
  if not query.strip():
    return "Please say something."
  
  # Encode user query
  emb = model.encode(query, convert_to_tensor=True)

  sims = util.cos_sim(emb, faq_emb)[0]

  idx = int(sims.argmax().item())
  score = float(sims[idx])

  print(f"[Similarity: {score:.3f}] → Match: {FAQ[idx]['q']}")

  if score >= SIM_THERESHOLD:
    return FAQ[idx]["a"]
  
  return "I am not sure about that, but you can ask me about AI, Python, BERT or something related!"