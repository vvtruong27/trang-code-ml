from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from email_classifier import EmailClassifier
import logging
import os
from datetime import datetime

# Thiết lập logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# CORS configuration
CORS(app, resources={
    r"/*": {
        "origins": ["*"],  # Cho phép tất cả origins trong development
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Khởi tạo classifiers
rule_classifier = None
ml_classifier = None

def init_classifiers():
    """Khởi tạo các classifiers"""
    global rule_classifier, ml_classifier
    
    # Initialize rule-based classifier
    try:
        rule_classifier = EmailClassifier()
        logger.info("✅ Rule-based classifier loaded successfully")
    except Exception as e:
        logger.error(f"❌ Failed to load rule-based classifier: {e}")
        rule_classifier = None
    
    # Initialize ML classifier
    try:
        import sys
        import os
        # Add the models directory to Python path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        models_path = os.path.join(current_dir, '..', 'models')
        sys.path.append(models_path)
        
        from lightweight_email_classifier import LightweightEmailClassifier
        ml_classifier = LightweightEmailClassifier(model_path=models_path)
        logger.info("✅ ML classifier (TF-IDF + LR) loaded successfully")
    except Exception as e:
        logger.error(f"❌ Failed to load ML classifier: {e}")
        ml_classifier = None
    
    return rule_classifier is not None or ml_classifier is not None

# Swagger configuration
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Email Classification API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/')
def home():
    """Trang chủ API"""
    return jsonify({
        'message': 'Email Classification API',
        'version': '1.0.0',
        'classifiers': {
            'rule_based': rule_classifier is not None,
            'ml_classifier': ml_classifier is not None
        },
        'endpoints': {
            'health': '/health',
            'swagger': '/swagger',
            'predict_rule': '/predict/rule',
            'predict_ml': '/predict/ml',
            'predict_batch': '/predict/batch',
            'model_info': '/model_info'
        }
    })

@app.route('/health')
def health_check():
    """Kiểm tra trạng thái API"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'classifiers': {
            'rule_based': rule_classifier is not None,
            'ml_classifier': ml_classifier is not None
        }
    })

@app.route('/model_info')
def model_info():
    """Thông tin về models"""
    return jsonify({
        'models': {
            'rule_based': {
                'type': 'Rule-based Email Classifier',
                'version': '1.0.0',
                'algorithm': 'Pattern-based classification with regex',
                'loaded': rule_classifier is not None
            },
            'ml_classifier': {
                'type': 'TF-IDF + Logistic Regression',
                'version': '1.0.0',
                'algorithm': 'TF-IDF vectorization + Logistic Regression',
                'accuracy': '99.92%',
                'training_time': '3.62 seconds',
                'loaded': ml_classifier is not None
            }
        },
        'categories': {
            '0': 'An toàn',
            '1': 'Nghi ngờ', 
            '2': 'Spam',
            '3': 'Giả mạo'
        },
        'features': ['title', 'content', 'from_email']
    })

@app.route('/predict/rule', methods=['POST', 'OPTIONS'])
def predict_rule():
    """
    Phân loại email sử dụng rule-based approach
    """
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
    
    try:
        if rule_classifier is None:
            return jsonify({
                'success': False,
                'error': 'Rule-based classifier not loaded'
            }), 500
        
        # Lấy dữ liệu từ request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
        
        # Validate required fields
        required_fields = ['title', 'content', 'from_email']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Phân loại email
        import time
        start_time = time.time()
        
        result = rule_classifier.classify_email(data)
        
        processing_time = (time.time() - start_time) * 1000  # Convert to ms
        
        return jsonify({
            'success': True,
            'method': 'rule_based',
            'category': result['category'],
            'confidence': result['confidence'],
            'indicators': result['indicators'],
            'level': result['level'],
            'processing_time': round(processing_time, 2)
        })
        
    except Exception as e:
        logger.error(f"Error in predict_rule: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/predict/ml', methods=['POST', 'OPTIONS'])
def predict_ml():
    """
    Phân loại email sử dụng ML model (TF-IDF + Logistic Regression)
    """
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
    
    try:
        if ml_classifier is None:
            return jsonify({
                'success': False,
                'error': 'ML classifier not loaded'
            }), 500
        
        # Lấy dữ liệu từ request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
        
        # Validate required fields
        required_fields = ['title', 'content', 'from_email']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Phân loại email
        import time
        start_time = time.time()
        
        result = ml_classifier.predict(
            title=data['title'],
            content=data['content'],
            from_email=data['from_email']
        )
        
        processing_time = (time.time() - start_time) * 1000  # Convert to ms
        
        return jsonify({
            'success': True,
            'method': 'ml_classifier',
            'category': result['category'],
            'confidence': result['confidence'],
            'probabilities': result['probabilities'],
            'processing_time': round(processing_time, 2),
            'text_length': result.get('text_length', 0)
        })
        
    except Exception as e:
        logger.error(f"Error in predict_ml: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/predict/batch', methods=['POST', 'OPTIONS'])
def predict_batch():
    """
    Phân loại nhiều email cùng lúc
    """
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return jsonify({'message': 'OK'}), 200
    
    try:
        if rule_classifier is None and ml_classifier is None:
            return jsonify({
                'success': False,
                'error': 'No classifiers loaded'
            }), 500
        
        # Lấy dữ liệu từ request
        data = request.get_json()
        
        if not data or 'emails' not in data:
            return jsonify({
                'success': False,
                'error': 'No emails array provided'
            }), 400
        
        emails = data['emails']
        method = data.get('method', 'rule')  # Default to rule-based
        
        if not isinstance(emails, list):
            return jsonify({
                'success': False,
                'error': 'emails must be an array'
            }), 400
        
        if len(emails) == 0:
            return jsonify({
                'success': False,
                'error': 'emails array cannot be empty'
            }), 400
        
        # Validate each email (both methods require same 3 fields)
        required_fields = ['title', 'content', 'from_email']
        for i, email in enumerate(emails):
            for field in required_fields:
                if field not in email:
                    return jsonify({
                        'success': False,
                        'error': f'Email {i+1} missing required field: {field}'
                    }), 400
        
        # Phân loại batch
        import time
        start_time = time.time()
        
        results = []
        
        if method == 'rule' and rule_classifier:
            for email in emails:
                result = rule_classifier.classify_email(email)
                results.append({
                    'category': result['category'],
                    'confidence': result['confidence'],
                    'indicators': result['indicators'],
                    'level': result['level']
                })
        elif method == 'ml' and ml_classifier:
            for email in emails:
                result = ml_classifier.predict(
                    title=email['title'],
                    content=email['content'],
                    from_email=email['from_email']
                )
                results.append({
                    'category': result['category'],
                    'confidence': result['confidence'],
                    'probabilities': result['probabilities']
                })
        else:
            return jsonify({
                'success': False,
                'error': f'Method {method} not available'
            }), 400
        
        processing_time = (time.time() - start_time) * 1000  # Convert to ms
        
        return jsonify({
            'success': True,
            'method': method,
            'results': results,
            'total_processed': len(results),
            'processing_time': round(processing_time, 2)
        })
        
    except Exception as e:
        logger.error(f"Error in predict_batch: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handler cho 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'available_endpoints': [
            '/',
            '/health',
            '/swagger',
            '/predict/rule',
            '/predict/ml',
            '/predict/batch',
            '/model_info'
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handler cho 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    # Khởi tạo classifiers
    if init_classifiers():
        logger.info("🚀 Starting Email Classification API...")
        app.run(host='0.0.0.0', port=5001, debug=True)
    else:
        logger.error("❌ Failed to start API due to classifier initialization error") 