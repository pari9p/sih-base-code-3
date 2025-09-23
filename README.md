# PM Internship Recommendation Engine

A lightweight AI-based recommendation system for the PM Internship Scheme that helps candidates find relevant internships based on their profile, academic background, interests, and location preferences.

## Features

- **Simple Input Form**: Captures education, skills, sector interests, and location
- **AI Recommendations**: Rule-based engine suggesting 3-5 top internships
- **Mobile-Responsive**: Works seamlessly on mobile devices
- **User-Friendly**: Minimal text with visual cues for low digital literacy users
- **Multilingual Support**: Basic structure for regional language adaptation

## Tech Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Data Processing**: Pandas, scikit-learn
- **Deployment**: Lightweight and easily integrable

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Fill out the candidate profile form with:
   - Educational background
   - Skills and interests
   - Preferred sector
   - Location preferences

2. Click "Get Recommendations" to receive 3-5 personalized internship suggestions

3. View detailed internship cards with key information

## Project Structure

```
├── app.py                 # Flask backend application
├── static/
│   ├── css/
│   │   └── style.css     # Responsive styling
│   ├── js/
│   │   └── main.js       # Frontend interactions
│   └── images/           # UI icons and images
├── templates/
│   ├── index.html        # Main application page
│   └── base.html         # Base template
├── data/
│   └── internships.json  # Sample internship data
├── models/
│   └── recommender.py    # Recommendation engine
└── requirements.txt      # Python dependencies
```

## License

This project is developed for educational purposes as part of the PM Internship Scheme initiative.