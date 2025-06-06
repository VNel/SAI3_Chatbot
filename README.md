---

title: "🛡️ Cybersecurity RAG Chatbot"
author: "Carlos Gomez, Nelson Vidovic, Lirim Zahiri, Mouad Medini, Niklaus Joel"
date: "`r format(Sys.Date(), '%d. %B %Y')`"
output:
html\_document:
toc: true
toc\_float: true
number\_sections: true
code\_folding: hide
-------------------

# Einleitung

Ein kontextbasierter Chatbot zur Beantwortung sicherheitsrelevanter Fachfragen auf Basis von **500+ wissenschaftlichen Cybersecurity-Artikeln** (Textformat).
Er liefert **schnelle, faktenbasierte Antworten** – ausschließlich basierend auf vorhandenen Dokumenten.

---

# 📌 Projektteam

Dieses Projekt wurde im Rahmen eines Moduls an der Berner Fachhochschule erstellt von:

* Carlos Gomez
* Nelson Vidovic
* Lirim Zahiri
* Mouad Medini
* Niklaus Joel

---

# ✅ Voraussetzungen (einmalig)

## 1. 🔧 Installiere Python (Version 3.8 oder 3.9)

* Offizielle Website: [https://www.python.org/downloads/](https://www.python.org/downloads/)
* Beim Setup **"Add Python to PATH" aktivieren**
* Danach im Terminal prüfen:

```bash
python --version
```

## 2. 🅿️ Together.ai Account erstellen

* Besuche: [https://www.together.ai](https://www.together.ai)
* Anmeldung z. B. via GitHub
* Nach Login:

  * Profilbild → **API Keys**
  * → **Create API Key**
  * Key kopieren (`sk-...`)
 
  

---

# 🔧 Setup – Schritt für Schritt

## 1. 📁 Projekt klonen

### Git-Variante

```bash
git clone https://github.com/VNel/SAI3_Chatbot.git
cd online_chatbot
```


## 2. 🧪 Virtuelle Umgebung einrichten

* **Windows PowerShell:**

```bash
py -m venv venv
```

* **macOS/Linux:**

```bash
python -m venv venv
```

### Dann aktivieren:

* **Windows PowerShell:**

```bash
.\venv\Scripts\Activate.ps1
```

* **macOS/Linux:**

```bash
source venv/bin/activate
```

---

## 3. 📦 Notwendige Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### Inhalt von `requirements.txt`

```text
faiss-cpu
sentence-transformers
gradio
requests
python-dotenv
```

---

## 4. 🔐 API-Key eintragen

```bash
cp .env.template .env
```

Dann `.env` öffnen und den API Key eintragen:

```env
TOGETHER_API_KEY=sk-abc123xyz456
```

> Ohne `.env` funktioniert die Kommunikation mit Together.ai nicht.

---

## 5. 📚 Vektordatenbank vorbereiten

```bash
python load_data.py
python build_index.py
```

* Erstellt `documents.json` (Text-Chunks)
* Erstellt `index.faiss` (semantischer Suchindex)

---

## 6. 🚀 Webinterface starten

```bash
python web_ui.py
```

Öffnet automatisch:
[http://localhost:7860](http://localhost:7860)

---

# 💬 Funktionen

* Fragen auf Deutsch oder Englisch möglich
* Antworten basieren **nur auf lokalen Texten**
* Kein Halluzinieren
* Transparente Quellenangabe pro Antwort
* Falls keine Info vorhanden → klare Rückmeldung

---

# 🔒 Sicherheit & Datenschutz

| Punkt                         | Status |
| ----------------------------- | ------ |
| API Key bleibt lokal          | ✅      |
| Keine Cloud-Speicherung       | ✅      |
| Kein Login nötig              | ✅      |
| Lokaler Zugriff via localhost | ✅      |

---

# ✅ Fertig! – Funktionscheck

| Muss erfüllt sein            | ✅ |
| ---------------------------- | - |
| Python 3.8 / 3.9 installiert | ✅ |
| Virtuelle Umgebung aktiv     | ✅ |
| `pip install` erfolgreich    | ✅ |
| `.env` mit API Key vorhanden | ✅ |
| `load_data.py` erfolgreich   | ✅ |
| `build_index.py` erfolgreich | ✅ |
| `web_ui.py` gestartet        | ✅ |

---

# 📂 Dateistruktur (Auszug)

```bash
├── clean_data/               # 500 Cybersecurity-Artikel (.txt)
├── vectorstore/             # Vektordatenbank (automatisch generiert)
│   ├── documents.json
│   └── index.faiss
├── .env                     # (von dir erstellt)
├── load_data.py             # Texte verarbeiten
├── build_index.py           # FAISS-Index erstellen
├── query_pipeline.py        # Retrieval-Logik
├── llm_api.py               # API-Anbindung an Together.ai
├── web_ui.py                # Webinterface starten
├── requirements.txt         # Python-Abhängigkeiten
└── README.md                # Diese Anleitung
```

---

# 📎 Hinweis

Dieses Projekt dient ausschließlich der Forschung und Lehre im Rahmen des Studiengangs Wirtschaftsinformatik.
Es ist **nicht** für den produktiven oder kommerziellen Einsatz vorgesehen.
