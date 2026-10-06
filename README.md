# FIH Buddy 📚🤖

> **Status: 🚧 Early development.** The repository currently holds only a starter `main.py`. This README describes the planned design.

**FIH Buddy** is a planned AI study companion for Amrita students taking **Foundations of Indian Heritage (FIH)**. It will answer syllabus questions concisely, generate instant mock exams, and support hands-free use through **speech-to-text** and **text-to-speech**.

---

## ✨ Planned Features

- 💬 **Conversational Q&A:** short, to-the-point answers on FIH topics
- 📝 **Instant mock exams:** generated question sets with answer review
- 🎙️ **Voice input:** ask questions by speaking (speech-to-text)
- 🔊 **Voice output:** answers read aloud (text-to-speech)

---

## 🏗️ Architecture & Concepts (planned)

```
User (voice / text)
   │
   ├─► Speech-to-Text ──┐
   │                    ▼
   └──────────────► Chatbot core (LLM + FIH course knowledge / prompts)
                        │
                        ├─► Q&A mode ──────► concise answer
                        └─► Mock-exam mode ─► question generation + evaluation
                        │
                        ▼
                 Text-to-Speech ──► spoken response
```

**Concepts:** conversational AI / LLM chatbot · prompt engineering for exam-style question generation · retrieval of course material (RAG) · speech recognition (STT) · speech synthesis (TTS)

---

## ⚙️ Getting Started

```bash
git clone https://github.com/God-Gamer-Manyu/FIH_Buddy.git
cd FIH_Buddy
python main.py
```

Requires **Python 3.8+**. Setup steps will be expanded as features are implemented.

## 🛠️ Tech Stack

`Python` (with LLM, STT and TTS integrations planned)

## 👤 Author

**Rtamanyu N J**, [@God-Gamer-Manyu](https://github.com/God-Gamer-Manyu)
