# 🍽️ Ap## 📋 Caratteristiche

- **Interface mobile-friendly**: Ottimizzata per l'uso da smartphone
- **💾 Sistema di Bozze**: Salva e riprendi preventivi in qualsiasi momento
- **🔄 Auto-Save**: Salvataggio automatico durante la compilazione
- **📴 Modalità Offline**: Funziona anche senza connessione internet
- **Menu predefiniti**: Basati sui tuoi documenti di esempio esistenti
- **Elementi personalizzabili**: Aggiungi nuovi piatti e personalizza prezzi
- **Export Word**: Genera documenti .docx nel formato del tuo template con logo aziendale
- **Calcolo automatico**: Calcola automaticamente totali e costi
- **Navigazione semplice**: Interface organizzata in sezioni chiare
- **🐳 Docker Ready**: Pronto per deployment con Docker/Docker Composeivi Catering

Un'applicazione Streamlit in italiano per generare preventivi professionali per eventi di catering.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.49+-red.svg)](https://streamlit.io)

## 📋 Caratteristiche

- **Interface mobile-friendly**: Ottimizzata per l'uso da smartphone
- **Menu predefiniti**: Basati sui tuoi documenti di esempio esistenti
- **Elementi personalizzabili**: Aggiungi nuovi piatti e personalizza prezzi
- **Export Word**: Genera documenti .docx nel formato del tuo template con logo aziendale
- **Calcolo automatico**: Calcola automaticamente totali e costi
- **Navigazione semplice**: Interface organizzata in sezioni chiare
- **� Docker Ready**: Pronto per deployment con Docker/Docker Compose

## 🚀 Quick Start

### 🐳 Con Docker (Raccomandato)
```bash
git clone https://github.com/yourusername/homelette-preventivi.git
cd homelette-preventivi
docker-compose up -d
```
Apri: http://localhost:8501

### 💻 Sviluppo Locale
```bash
git clone https://github.com/yourusername/homelette-preventivi.git
cd homelette-preventivi
pip install -r requirements.txt
streamlit run preventivi_app.py
```

### ⚡ Script automatico
```bash
./avvia_app.sh
```

## 📱 Utilizzo

### 0. 📋 Preventivi Salvati *(Nuovo!)*
- **Salva e Riprendi**: I preventivi si salvano automaticamente durante la compilazione
- **Gestisci Bozze**: Visualizza, carica, duplica o elimina preventivi salvati
- **Lavoro Offline**: Continua a lavorare anche senza connessione internet
- **Template**: Duplica preventivi esistenti come modelli per nuovi eventi

### 1. 📋 Dati Evento
- Inserisci riferimento cliente e destinatario
- Specifica luogo, data e ora dell'evento
- Definisci numero di persone e tipologia servizio
- Configura dettagli come bicchieri, posate, stoviglie

### 2. 🍽️ Menu
- Scegli tra elementi predefiniti (basati sui tuoi documenti)
- Filtra per categoria (Antipasti, Primi, Secondi, Dolci, etc.)
- Aggiungi elementi personalizzati con descrizione e prezzo
- Rimuovi elementi non desiderati

### 3. 💰 Prezzi
- Imposta prezzo per persona
- Definisci costo cameriere
- Visualizza calcolo automatico dei totali
- Aggiungi note aggiuntive

### 4. 📄 Anteprima e Export
- Visualizza anteprima del preventivo
- Scarica documento Word (.docx) professionale
- Reset per nuovo preventivo

## 📋 Menu Predefiniti Inclusi

L'app include tutti gli elementi del tuo documento di esempio:

**Aperitivi & Antipasti:**
- Cocktail di benvenuto
- Prosciutto di Parma e melone
- Pinzimonio di verdure
- Tagliata di frutta fresca

**Pasticceria Salata:**
- Coupelle di brisé con mousse di Bologna
- Cestini di sfoglia con paté di fagiolini
- Fiori di pane (varie tipologie)

**Primi & Secondi:**
- Kedgeree al salmone
- Insalata di pasta mediterranea
- Vitello tonnato
- Caponata

**Dolci:**
- Fantasia di tiramisù
- Spumone alla frutta
- Crema caffè

## 🔧 Personalizzazione

### Modifica Template
Il documento Word generato può essere personalizzato modificando la funzione `create_word_document()` nel file `preventivi_app.py`.

### Aggiungi Nuovi Elementi
Modifica la funzione `get_predefined_menu_items()` per aggiungere nuovi piatti predefiniti.

### Styling Mobile
Il CSS nella funzione main può essere modificato per personalizzare l'aspetto mobile.

## 📁 Struttura File

```
homelette-preventivi/
├── preventivi_app.py          # App principale Streamlit
├── avvia_app.sh              # Script di avvio
├── examine_docs.py           # Script per analizzare documenti Word
├── PREVENTIVO BARBERI LACMUS(2).docx  # Documento di riferimento
├── template_preventivo.dotx   # Template Word
├── .venv/                    # Ambiente virtuale Python
└── README.md                 # Questo file
```

## 🛠️ Dipendenze

- streamlit
- python-docx
- pandas
- datetime

## � Deployment

### ☁️ Cloud Deployment
- **Streamlit Cloud**: Deploy direttamente da GitHub
- **Heroku**: Con un click deployment
- **DigitalOcean**: App Platform ready
- **Google Cloud Run**: Container deployment
- **AWS ECS/Fargate**: Enterprise deployment

Vedi [DEPLOYMENT.md](DEPLOYMENT.md) per istruzioni dettagliate.

### 🐳 Docker
```bash
# Build
docker build -t homelette-preventivi .

# Run
docker run -d -p 8501:8501 homelette-preventivi

# Con Docker Compose
docker-compose up -d
```

## 📄 License

Questo progetto è rilasciato sotto licenza MIT. Vedi [LICENSE](LICENSE) per dettagli.

## �📞 Supporto

Per modifiche o problemi, modifica il file `preventivi_app.py` seguendo la struttura esistente. L'app è progettata per essere facilmente estendibile e personalizzabile.

## 🎯 Funzionalità Principali per Mobile

- Layout responsive
- Navigazione tramite sidebar
- Bottoni full-width
- Text input ottimizzati per touch
- Sezioni organizzate per facilità d'uso

L'app è stata specificamente progettata per essere utilizzata facilmente da smartphone, mantenendo tutte le funzionalità professionali necessarie per la generazione di preventivi.

## 🎨 **Design Professionale del Documento Word**

### **Caratteristiche Avanzate**
- **🖼️ Logo Aziendale**: Include automaticamente il logo Homelette se presente come `homelette_logo.jpg`
- **📝 Subtitle Aziendale**: "Primum manducare, deinde filosofare" in grassetto e colore blu cobalto
- **➖ Linea Decorativa**: Divisore orizzontale elegante sotto l'intestazione
- **🔤 Typography Professionale**: 
  - **Headings**: Arial Black (bold, sans-serif, 28pt)
  - **Testo fisso**: Segoe UI (sans-serif, 10-12pt)
  - **Dati variabili**: Georgia (serif, 11pt)
  - **Sezioni**: Calibri (14-16pt)

## 🛠️ Struttura Progetto

```
homelette-preventivi/
├── preventivi_app.py          # App principale Streamlit
├── avvia_app.sh              # Script di avvio
├── requirements.txt          # Dipendenze Python
├── Dockerfile               # Container configuration
├── docker-compose.yml       # Multi-container deployment
├── .gitignore              # Git ignore rules
├── LICENSE                 # Licenza MIT
├── README.md               # Documentazione
├── DEPLOYMENT.md           # Guida deployment
├── homelette_logo.jpg      # Logo aziendale
└── .venv/                  # Virtual environment
```

### **Come Aggiungere il Logo**
1. Salva l'immagine del logo come `homelette_logo.jpg` nella cartella del progetto
2. L'app utilizzerà automaticamente il logo nei documenti generati
3. Se il logo non è presente, mostrerà solo il testo "HOMELETTE"

### **Test del Documento**
Puoi testare la generazione del documento con:
```bash
cd /home/grigolet/cernbox/personal/code/homelette-preventivi
python test_document.py
```
