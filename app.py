import os
import json
import logging
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from recommendation_engine import JobRecommendationEngine
from job_data import JobDatabase

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key-for-development")

# Initialize recommendation engine and job database
job_db = JobDatabase()
recommendation_engine = JobRecommendationEngine(job_db)

@app.route('/')
def index():
    """Main page for inputting candidate preferences"""
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend_jobs():
    """Process candidate preferences and return job recommendations"""
    try:
        # Get preferences from form or JSON
        if request.is_json:
            preferences = request.get_json()
        else:
            # Handle form data
            preferences = {
                'values': request.form.getlist('values'),
                'role_types': request.form.getlist('role_types'),
                'titles': request.form.getlist('titles'),
                'locations': request.form.getlist('locations'),
                'role_level': request.form.getlist('role_level'),
                'leadership_preference': request.form.get('leadership_preference', ''),
                'company_size': request.form.getlist('company_size'),
                'industries': request.form.getlist('industries'),
                'skills': request.form.getlist('skills'),
                'min_salary': int(request.form.get('min_salary', 0)) if request.form.get('min_salary') else 0
            }
        
        app.logger.debug(f"Received preferences: {preferences}")
        
        # Validate preferences
        if not preferences:
            flash('Please provide your job preferences', 'error')
            return redirect(url_for('index'))
        
        # Get recommendations
        recommendations = recommendation_engine.recommend_jobs(preferences)
        
        app.logger.debug(f"Generated {len(recommendations)} recommendations")
        
        if request.is_json:
            return jsonify(recommendations)
        else:
            return render_template('recommendations.html', 
                                 recommendations=recommendations, 
                                 preferences=preferences)
    
    except ValueError as e:
        app.logger.error(f"ValueError in recommend_jobs: {e}")
        if request.is_json:
            return jsonify({'error': str(e)}), 400
        flash(f'Invalid input: {str(e)}', 'error')
        return redirect(url_for('index'))
    
    except Exception as e:
        app.logger.error(f"Error in recommend_jobs: {e}")
        if request.is_json:
            return jsonify({'error': 'An internal error occurred'}), 500
        flash('An error occurred while processing your request', 'error')
        return redirect(url_for('index'))

@app.route('/api/jobs')
def get_all_jobs():
    """API endpoint to get all available jobs"""
    try:
        jobs = job_db.get_all_jobs()
        return jsonify(jobs)
    except Exception as e:
        app.logger.error(f"Error getting jobs: {e}")
        return jsonify({'error': 'Failed to retrieve jobs'}), 500

@app.route('/api/recommend', methods=['POST'])
def api_recommend():
    """API endpoint for job recommendations"""
    try:
        preferences = request.get_json()
        if not preferences:
            return jsonify({'error': 'No preferences provided'}), 400
        
        recommendations = recommendation_engine.recommend_jobs(preferences)
        return jsonify({
            'recommendations': recommendations,
            'total_count': len(recommendations)
        })
    
    except Exception as e:
        app.logger.error(f"Error in API recommend: {e}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('index.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
