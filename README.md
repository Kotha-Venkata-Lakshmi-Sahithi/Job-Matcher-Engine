# Job Recommendation Engine

A Flask-based intelligent job recommendation system that matches candidates with job opportunities based on their preferences using weighted scoring algorithms.

## Overview

This application helps job seekers find the most suitable job opportunities by analyzing their preferences across multiple criteria including skills, job titles, locations, company size, industry, values, and salary requirements. The system uses a sophisticated weighted scoring algorithm to rank job listings and provide personalized recommendations.

## Features

### Core Functionality
- **Intelligent Matching Algorithm**: Uses weighted scoring across 7 key criteria
- **Personalized Recommendations**: Tailored job suggestions based on user preferences
- **Match Score Breakdown**: Detailed explanation of why each job matches
- **Responsive Web Interface**: Clean, modern UI built with Bootstrap
- **Real-time Results**: Instant job recommendations upon form submission

### Matching Criteria (Weighted)
- **Skills** (30%): Technical and soft skills matching
- **Job Title** (20%): Role type and seniority level matching with semantic understanding
- **Location** (15%): Geographic preferences including remote options
- **Industry** (10%): Sector and domain matching
- **Company Size** (10%): Organization size preferences
- **Values & Culture** (10%): Company values and culture fit
- **Salary** (5%): Compensation expectations

### Advanced Features
- **Semantic Title Matching**: Understands job title synonyms (e.g., "UX Designer" ≈ "Product Designer")
- **Flexible Location Matching**: Supports remote work and city-based preferences
- **Partial Skills Matching**: Rewards related and similar skills
- **Interactive Job Details**: Modal popups with comprehensive job information
- **Match Statistics**: Summary analytics of recommendations

## Technology Stack

### Backend
- **Flask**: Lightweight Python web framework
- **Python 3.11**: Core programming language
- **Gunicorn**: WSGI HTTP server for production deployment

### Frontend
- **Bootstrap 5**: Responsive CSS framework with dark theme
- **Font Awesome**: Icon library
- **Vanilla JavaScript**: Enhanced user interactions
- **Jinja2**: Template engine

### Architecture
- **MVC Pattern**: Clear separation of concerns
- **Modular Design**: Separated components for maintainability
- **In-memory Database**: Fast job data access (production-ready for database integration)

## Installation

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

### Quick Start

1. **Clone the repository**
```bash
git clone <repository-url>
cd job-recommendation-engine
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set environment variables**
```bash
export SESSION_SECRET="your-secret-key-here"
```

4. **Run the application**
```bash
python main.py
```

5. **Access the application**
Open your browser and navigate to `http://localhost:5000`

### Production Deployment

For production deployment using Gunicorn:

```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

## Usage

### For Job Seekers

1. **Visit the Homepage**: Navigate to the main application URL
2. **Fill Preferences Form**: Select your preferences across different categories:
   - Job titles you're interested in
   - Your key skills
   - Preferred locations (US cities or Indian cities)
   - Employment type (Full-time/Contract)
   - Industry preferences
   - Company size preferences
   - Important values
   - Minimum salary expectations

3. **Get Recommendations**: Submit the form to receive personalized job recommendations
4. **Review Matches**: Browse through ranked job listings with match scores
5. **View Details**: Click on any job to see comprehensive details and match breakdown

### API Endpoints

The application also provides REST API endpoints:

- `GET /api/jobs` - Retrieve all available jobs
- `POST /api/recommend` - Get job recommendations (JSON input/output)

Example API usage:
```bash
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "skills": ["Figma", "UI/UX Design"],
    "titles": ["UI/UX Designer"],
    "locations": ["Remote in USA"],
    "min_salary": 150000
  }'
```

## Project Structure

```
job-recommendation-engine/
├── app.py                  # Flask application and routes
├── main.py                 # Application entry point
├── recommendation_engine.py # Core matching algorithm
├── job_data.py            # Job database management
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Homepage with preferences form
│   └── recommendations.html # Results page
├── static/               # Static assets
│   ├── css/
│   │   └── custom.css    # Custom styling
│   └── js/
│       └── main.js       # JavaScript functionality
└── README.md             # This file
```

## Job Database

The application includes sample jobs from top companies:

### US Companies
- Google, Microsoft, Netflix, Uber, Airbnb, Slack, Tesla, Adobe, Stripe, Zoom, Spotify

### Indian Companies  
- Flipkart, Paytm, Swiggy, Zomato, BYJU'S, Ola, Razorpay, PhonePe, Freshworks, Myntra, InMobi

Each job record includes:
- Job ID and title
- Company name and size
- Location and employment type
- Salary range
- Required skills
- Industry and role level
- Company values promoted
- Experience requirements

## Customization

### Adjusting Match Weights

You can customize the importance of different criteria by modifying the weights in `recommendation_engine.py`:

```python
DEFAULT_WEIGHTS = {
    'skills': 0.30,      # 30% - Technical skills
    'title': 0.20,       # 20% - Job title match
    'location': 0.15,    # 15% - Location preference  
    'industry': 0.10,    # 10% - Industry match
    'company_size': 0.10, # 10% - Company size
    'values': 0.10,      # 10% - Values alignment
    'salary': 0.05       # 5% - Salary match
}
```

### Adding New Jobs

To add new job listings, edit the `_load_sample_jobs()` method in `job_data.py`:

```python
{
    "job_id": "COMPANY-123",
    "title": "Job Title",
    "company": "Company Name",
    "location": "City, Country",
    "salary_range": [min_salary, max_salary],
    "employment_type": "Full-Time",
    "company_size": "Size Category",
    "industry": "Industry Name",
    "required_skills": ["Skill1", "Skill2"],
    "values_promoted": ["Value1", "Value2"],
    "experience_required": "X-Y years",
    "role_level": "Level"
}
```

### Extending Semantic Matching

Add new job title synonyms in `recommendation_engine.py`:

```python
TITLE_SYNONYMS = {
    'ux designer': ['user experience designer', 'product designer'],
    'your_title': ['synonym1', 'synonym2'],
    # Add more synonyms
}
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Make your changes
4. Add tests for new functionality
5. Commit your changes (`git commit -am 'Add new feature'`)
6. Push to the branch (`git push origin feature/new-feature`)
7. Create a Pull Request

## Future Enhancements

- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] User authentication and saved preferences
- [ ] Machine learning-based matching improvements
- [ ] Email notifications for new matching jobs
- [ ] Advanced filtering and sorting options
- [ ] Company and job analytics dashboard
- [ ] Integration with job boards and APIs
- [ ] Resume parsing and automatic preference detection

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For questions, issues, or contributions, please open an issue in the repository or contact the development team.

---

**Built with ❤️ using Flask and modern web technologies**