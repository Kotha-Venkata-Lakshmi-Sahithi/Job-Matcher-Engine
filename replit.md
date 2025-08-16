# Job Recommendation Engine

## Overview

This is a Flask-based job recommendation engine that matches candidates with job opportunities based on their preferences. The system uses a weighted scoring algorithm to rank job listings according to how well they align with a candidate's specified criteria including skills, job titles, locations, company size, industry, values, and salary requirements. The application features a web interface for inputting preferences and displays ranked job recommendations with match scores.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Web Framework
- **Flask**: Chosen as the lightweight web framework for rapid development and simplicity
- **Template Engine**: Uses Jinja2 templates with a modular base template system for consistent UI
- **Static Assets**: Organized structure with CSS and JavaScript files for frontend functionality

### Frontend Architecture
- **Bootstrap 5**: Dark theme UI framework for responsive design and consistent styling
- **Progressive Enhancement**: JavaScript adds interactivity without breaking core functionality
- **Form-based Input**: Multi-checkbox form system for collecting user preferences
- **Responsive Design**: Mobile-friendly interface with grid-based layouts

### Backend Architecture
- **MVC Pattern**: Clear separation between data (JobDatabase), business logic (JobRecommendationEngine), and presentation (Flask routes)
- **Modular Design**: Core functionality split into dedicated modules:
  - `job_data.py`: Data access layer with sample job database
  - `recommendation_engine.py`: Scoring algorithm and matching logic
  - `app.py`: Web application routes and request handling

### Recommendation Engine
- **Weighted Scoring System**: Configurable weights for different matching criteria (skills 30%, title 20%, location 15%, etc.)
- **Semantic Matching**: Title synonyms dictionary for intelligent job title matching
- **Fuzzy Matching**: String similarity algorithms for flexible text matching
- **Configurable Algorithm**: Ability to adjust weights and scoring parameters

### Data Layer
- **In-Memory Database**: Sample job data stored in Python data structures
- **JSON-based Structure**: Standardized job listing format with required fields
- **Extensible Schema**: Job records include comprehensive metadata for matching

### Scoring Algorithm
- **Multi-criteria Decision Making**: Combines multiple preference dimensions into single match score
- **Normalization**: Ensures consistent scoring across different data types
- **Ranking System**: Sorts results by match score for optimal user experience

## External Dependencies

### Python Packages
- **Flask**: Web framework for HTTP request handling and templating
- **Logging**: Built-in Python logging for debugging and monitoring

### Frontend Libraries
- **Bootstrap 5**: CSS framework loaded via CDN for responsive UI components
- **Font Awesome**: Icon library for enhanced visual elements
- **Custom CSS/JS**: Local assets for application-specific styling and interactions

### Development Tools
- **Debug Mode**: Flask development server with hot reloading
- **Session Management**: Flask sessions for user state management
- **Error Handling**: Flash messaging system for user feedback

### Deployment Considerations
- **Environment Variables**: Session secret configuration via environment
- **Host Configuration**: Configurable host and port for deployment flexibility
- **Static File Serving**: Flask static file handling for CSS/JS assets

Note: The current implementation uses in-memory data storage. The architecture supports future database integration through the JobDatabase class interface.