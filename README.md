# 🎙️ Personal Voice Assistant AI

A **web-based AI-powered personal voice assistant** that understands natural language voice commands, identifies user intent, and performs real-time actions through a fast and responsive interface.

This project was developed as part of **Semester VII – M.Sc. (CA & IT)** using modern AI, NLP, and full-stack web technologies.

---

## 📌 Project Overview

The **Personal Voice Assistant AI** is designed to provide hands-free interaction through voice commands while maintaining privacy and customization.  
Unlike many platform-dependent assistants, this system focuses on **local processing**, **custom intent handling**, and a **lightweight web interface**.

The system integrates:
- **Svelte / SvelteKit** for the frontend  
- **Python FastAPI** for backend APIs  
- **all-MiniLM-L6-v2** for intent detection and language understanding  

---

## 🎯 Objectives

- Enable hands-free interaction using voice commands  
- Accurately understand user intent using **all-MiniLM-L6-v2**  
- Execute real-time actions such as search and responses  
- Provide a fast, minimalistic, and responsive UI  
- Ensure high-performance backend communication via FastAPI  

---

## ❓ Problem Statement

Most existing voice assistants:
- Are platform-dependent  
- Require continuous cloud connectivity  
- Offer limited personalization  
- Raise privacy concerns  

This project aims to build a **fully customizable personal voice assistant** that:
- Processes voice input locally  
- Uses NLP for intent recognition  
- Communicates via a lightweight SvelteKit interface  

---

## 🧠 Key AI Concepts & Terminology

- **NLP (Natural Language Processing)** – Enables machines to understand human language  
- **all-MiniLM-L6-v2** – Lightweight transformer model  
- **Intent Classification** – Determines what action the user wants  
- **Entity Extraction** – Extracts key information like tasks, keywords, or names  

---

## ⚙️ AI Techniques Used

- **all-MiniLM-L6-v2 Model** – Contextual understanding of user commands  
- **Transformers Library** – Pretrained BERT architecture 
- **Web Speech API** – Voice-to-text conversion  

---

## 🛠️ Technology Stack

### Frontend
- Svelte / SvelteKit  
- Tailwind CSS  
- Web Speech API  

### Backend
- Python FastAPI  
- Pydantic  

### AI / NLP
- all-MiniLM-L6-v2 (BERT-based model)  
- Transformers  

---

## 📂 Dataset

- Custom **csv file**

---

## 🔄 System Workflow

1. User gives a **voice command**
2. Voice is converted to text using **Web Speech API**
3. Text is processed by **all-MiniLM-L6-v2**
4. Intent is classified
5. Backend triggers the relevant action
6. Response is sent back to the frontend in real time

---

## 🧪 Testing

### Sample Test Cases

| Test Case | Input | Expected Output | Status |
|---------|------|----------------|--------|
| Voice Recognition | “Hey Assistant, hello” | Assistant replies with greeting | Pass |
| Invalid Command | Random input | “I didn’t understand” | Pass |
| Authentication | Login / Signup | Successful authentication | Pass |
| Forgot Password | OTP-based reset | Password reset flow | Pass |

---

## ⚠️ Challenges Faced

### Problems
- Python voice libraries (`SpeechRecognition`, `pyttsx3`) were not frontend-compatible  

### Solutions
- Shifted voice handling to **Web Speech API**
- Optimized NLP model loading to reduce response latency  

---

## 📈 Key Outcomes

- Fully functional personal voice assistant  
- Accurate intent detection using BERT-based NLP  
- Modular and scalable architecture  
- Fast frontend–backend communication  

---

## 📚 What We Learned

- Practical understanding of NLP and transformer models  
- Integrating SvelteKit with a Python FastAPI backend  
- Handling real-time voice input in web applications  
- Importance of preprocessing and response optimization  

---

## 🚀 Future Enhancements

- Advanced conversational memory  
- Multi-language support  
- Offline intent execution  
- AI-powered personalization  
- Smart task automation  

---

## 👨‍🎓 Project Team

- Shubham Jani (4034)  
- Manav Modi (4051)  
- Pritesh Rathod (4079)  

K. S. School of Business Management & Information Technology  

---

## 🔗 GitHub Repository
👉 https://github.com/rathod-pritesh/ai-voice-assistant  

---
## 📜 License
This project is developed for **academic and learning purposes**.
