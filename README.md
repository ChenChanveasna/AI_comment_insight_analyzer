## Features

- Input a YouTube video URL and retrieve all comments
- Real-time sentiment analysis (positive, negative, neutral)
- Visual charts displaying sentiment distribution
- Summary statistics including total comments and sentiment breakdown
- Common keywords and topic extraction
- Confidence scores for each sentiment prediction
- User attribution and word count tracking
- Clean, responsive web interface

## Purpose

This project was developed as part of an AI Fundamentals final project. It demonstrates practical applications of Artificial Intelligence and Natural Language Processing in analyzing and extracting insights from large volumes of online comments.

---

## Getting Started

### Prerequisites

- **Python 3.8 or higher**
- **pip** (Python package manager)
- A **YouTube Data API Key** (see [Setup Instructions](#obtaining-youtube-api-key))
- Approximately **2GB of free disk space** (for model downloads on first run)
- **Internet connection** (for downloading pre-trained models and accessing YouTube API)

### Requirements

All project dependencies are listed in `requirements.txt`:

```
Flask==3.1.1
python-dotenv==1.0.1
google-api-python-client==2.170.0
transformers==4.44.2
tqdm==4.66.5
torch
```

**Key Dependencies:**
- **Flask**: Web framework for the application server
- **google-api-python-client**: YouTube Data API client
- **transformers**: Hugging Face library for loading pre-trained NLP models
- **torch**: PyTorch deep learning framework (required by transformers)
- **python-dotenv**: Environment variable management
- **tqdm**: Progress bar visualization

### Installation

1. **Clone or download the project:**
   ```bash
   cd AI_comment_insight_analyzer
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   *Note: On first run, the transformers library will automatically download the pre-trained sentiment model (~350MB). This may take a few minutes depending on your internet connection.*

### Configuration

#### Obtaining YouTube API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the **YouTube Data API v3**
4. Create an **API Key** credential
5. Copy your API key

#### Environment Setup

1. Create a `.env` file in the project root directory:
   ```bash
   touch .env  # On Windows, create it manually or use: copy con .env
   ```

2. Add your configuration to `.env`:
   ```
   YOUTUBE_API_KEY=your_api_key_here
   SENTIMENT_MODEL_NAME=finiteautomata/bertweet-base-sentiment-analysis
   FLASK_SECRET_KEY=your_secret_key_here
   ```

   **Configuration Options:**
   - `YOUTUBE_API_KEY`: Your YouTube Data API key (required)
   - `SENTIMENT_MODEL_NAME`: Hugging Face model identifier (optional, defaults to `finiteautomata/bertweet-base-sentiment-analysis`)
   - `FLASK_SECRET_KEY`: Flask session secret (optional, defaults to internal value)

---

## How to Run

### Starting the Application

1. **Activate your virtual environment** (if not already activated):
   ```bash
   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

2. **Run the Flask application:**
   ```bash
   python app.py
   ```

3. **Open in your browser:**
   - Navigate to `http://localhost:5000`
   - You should see the application homepage with a URL input field

4. **Enter a YouTube video URL:**
   - Paste a YouTube URL (e.g., `https://www.youtube.com/watch?v=dQw4w9WgXcQ`)
   - Click "Analyze"
   - Wait for comments to be fetched and analyzed

### Sample YouTube URLs for Testing

- Long videos with many comments typically yield better analysis results
- Music videos, tutorials, and news videos are good test cases

---

## Project Architecture

### Directory Structure

```
AI_comment_insight_analyzer/
├── app.py                    # Main Flask application server
├── analysis.py              # Sentiment analysis engine
├── youtube_comment.py       # YouTube API integration
├── requirements.txt         # Python dependencies
├── .env                     # Configuration (create this file)
├── README.md               # This file
├── LICENSE
│
├── static/
│   ├── css/
│   │   └── style.css       # Frontend styling
│   └── js/
│       └── app.js          # Frontend interactivity
│
└── templates/
    └── index.html          # HTML template
```

### Component Overview

#### 1. **Frontend** (`static/` and `templates/`)
- **index.html**: Main user interface with URL input form
- **style.css**: Responsive styling for desktop and mobile
- **app.js**: Client-side JavaScript for form handling and chart visualization
- **Chart.js**: Library for rendering sentiment distribution graphs

#### 2. **Backend** (`app.py`)
- Flask web server handling HTTP requests
- Route management (`GET /` for page rendering)
- Request validation and error handling
- Coordination between YouTube API and sentiment analysis

#### 3. **YouTube Integration** (`youtube_comment.py`)
- **API Configuration**: Loads YouTube Data API credentials from environment
- **URL Parsing**: Extracts video ID from YouTube URLs using regex
- **Comment Fetching**: Retrieves paginated comment threads via YouTube Data API v3
- **Data Formatting**: Parses API responses into structured comment data

#### 4. **Sentiment Analysis** (`analysis.py`)
- **Model Loading**: Loads pre-trained Hugging Face model (lazy loading with caching)
- **Text Preprocessing**: Tokenization, normalization, and cleaning
- **Classification**: Runs transformer-based sentiment prediction
- **Confidence Scoring**: Provides confidence scores for each prediction
- **Keyword Extraction**: Identifies common tokens and removes stopwords
- **Statistics Generation**: Aggregates sentiment counts and distributions

### Data Flow

```
User Input (URL)
    ↓
YouTube API (fetch comments)
    ↓
Text Preprocessing (cleaning, tokenization)
    ↓
Sentiment Analysis (transformer model)
    ↓
Aggregation & Statistics
    ↓
Visualization (charts, summary)
    ↓
Display Results
```

---

## Pre-trained Model Details

### Sentiment Analysis Model

The project uses **Hugging Face's Transformers Library** with a pre-trained BERT-based sentiment analysis model.

**Default Model:** `finiteautomata/bertweet-base-sentiment-analysis`

**Model Characteristics:**
- **Type**: BERT fine-tuned for sentiment analysis
- **Training Data**: Brazilian Portuguese tweets and English social media
- **Output Classes**: Positive, Negative, Neutral
- **Confidence**: Prediction probability scores (0.0 - 1.0)
- **Model Size**: ~350MB (downloaded on first use)
- **License**: Open-source via Hugging Face Hub

**How It Works:**
1. Comment text is tokenized into subword units
2. Tokens are passed through the BERT encoder
3. Classification layer outputs probability scores for each sentiment class
4. The highest probability class is selected as the prediction
5. Confidence score is the probability of the predicted class

**Performance:**
- Optimized for social media and informal language
- Handles emojis, abbreviations, and casual speech
- Achieves ~90% accuracy on benchmark datasets

**Customization:**
To use a different model, update the `.env` file:
```
SENTIMENT_MODEL_NAME=distilbert-base-uncased-finetuned-sst-2-english
```

Available alternatives from Hugging Face Hub:
- `distilbert-base-uncased-finetuned-sst-2-english` (faster, smaller)
- `roberta-large-mnli` (more robust)
- `nlptown/bert-base-multilingual-uncased-sentiment` (multilingual support)

---

## How the Project Was Built

### Development Approach

1. **Planning Phase**
   - Defined project scope and core features
   - Identified required technologies and APIs
   - Designed system architecture

2. **Backend Development**
   - Set up Flask web framework
   - Integrated YouTube Data API for comment retrieval
   - Implemented sentiment analysis using Hugging Face transformers
   - Added error handling and data validation

3. **Data Processing Pipeline**
   - Created comment preprocessing module
   - Built tokenization and text cleaning functions
   - Developed aggregation and statistics engine
   - Implemented confidence scoring and normalization

4. **Frontend Development**
   - Designed responsive HTML template
   - Created CSS styling for user interface
   - Implemented JavaScript for interactivity
   - Integrated Chart.js for data visualization

5. **Integration & Testing**
   - Connected frontend to backend API
   - Tested with various YouTube videos
   - Validated sentiment predictions
   - Optimized performance

### Key Design Decisions

- **Pre-trained Models**: Used Hugging Face's pre-trained BERT model to leverage existing research and reduce training time
- **Flask Framework**: Chose Flask for its simplicity and flexibility
- **Environment Variables**: Used .env for secure credential management
- **Lazy Model Loading**: Model is loaded once and cached to improve performance
- **Client-side Visualization**: Charts rendered in browser to reduce server load

---

## Building & Deployment

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py

# Application will be available at http://localhost:5000
```

### Production Deployment

For production deployment, consider:

1. **Use a production WSGI server** (e.g., Gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Set environment variables securely** (don't commit .env to version control)

3. **Use a reverse proxy** (e.g., Nginx) for better performance

4. **Enable HTTPS/SSL** for security

5. **Monitor API rate limits** from YouTube Data API

6. **Cache results** to reduce API calls and improve responsiveness

---

## Troubleshooting

### Common Issues

**"YOUTUBE_API_KEY is missing"**
- Ensure `.env` file exists in the project root
- Verify the API key is correctly set in `.env`
- Restart the Flask application

**"Invalid YouTube URL"**
- Ensure URL is a valid YouTube video link
- Supported formats: `youtube.com/watch?v=...` and `youtu.be/...`

**"Module not found" errors**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again
- Check Python version is 3.8+

**Slow analysis on first run**
- The sentiment model downloads on first use (~350MB)
- Subsequent runs will be much faster
- Ensure stable internet connection

**API Rate Limiting**
- YouTube API has daily quota limits
- Each comment fetch consumes quota
- Monitor usage in Google Cloud Console

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | HTML, CSS, JavaScript, Chart.js |
| **Backend** | Python, Flask 3.1.1 |
| **NLP/ML** | Hugging Face Transformers, PyTorch |
| **APIs** | YouTube Data API v3 |
| **Data Processing** | Pandas, NLTK stopwords |
| **Utilities** | python-dotenv, tqdm |

---

## Project Scope

This project focuses on practical and straightforward functionality:
- ✅ YouTube comment analysis
- ✅ Sentiment classification (positive/negative/neutral)
- ✅ Keyword extraction and statistics
- ✅ Visual representation of results
- ✅ Confidence scoring

Intentionally kept lightweight and realistic for a student team project while demonstrating core AI/NLP concepts.

---

## Future Improvements

Potential enhancements for future versions:
- Export results to CSV/PDF
- Advanced topic detection and clustering
- Support for additional social media platforms (Twitter, Instagram, TikTok)
- Multi-language support
- Aspect-based sentiment analysis
- Real-time streaming updates
- User accounts and result history
- Comparative analysis between videos
- Fine-tuned models for specific domains

---

## Team Project

This system was built as a university group project for an AI Fundamentals course, with a focus on usefulness, simplicity, and practical implementation of machine learning concepts.
