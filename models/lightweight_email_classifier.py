#!/usr/bin/env python3
"""
Lightweight Email Classifier for Prediction
Fast and efficient email classification
"""

import pickle
import os
import re
import numpy as np
from datetime import datetime

class LightweightEmailClassifier:
    def __init__(self, model_path='models'):
        """Initialize the classifier"""
        self.model_path = model_path
        
        # Load model
        with open(os.path.join(model_path, 'lightweight_email_classifier.pkl'), 'rb') as f:
            self.pipeline = pickle.load(f)
        
        # Load mappings
        with open(os.path.join(model_path, 'category_mapping.pkl'), 'rb') as f:
            self.category_mapping = pickle.load(f)
        
        with open(os.path.join(model_path, 'id_to_category.pkl'), 'rb') as f:
            self.id_to_category = pickle.load(f)
        
        print("✅ Lightweight classifier loaded successfully")
    
    def preprocess_text(self, text):
        """Preprocess text for prediction"""
        if not text:
            return ""
        
        text = str(text).lower()
        
        # Remove special characters but keep Vietnamese
        text = re.sub(r'[^\w\sàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def predict(self, title, content, from_email="", to_email=""):
        """
        Predict email category
        
        Args:
            title (str): Email subject
            content (str): Email body content
            from_email (str): Sender email (optional)
            to_email (str): Recipient email (optional)
            
        Returns:
            dict: Prediction result with category, confidence, and probabilities
        """
        start_time = datetime.now()
        
        # Preprocess text
        title_clean = self.preprocess_text(title)
        content_clean = self.preprocess_text(content)
        from_email_clean = self.preprocess_text(from_email)
        
        # Combine text (title, content, from_email)
        text_combined = title_clean + ' ' + content_clean + ' ' + from_email_clean
        
        if len(text_combined.strip()) < 5:
            return {
                'category': 'Nghi ngờ',
                'confidence': 0.5,
                'probabilities': {
                    'An toàn': 0.25,
                    'Nghi ngờ': 0.5,
                    'Spam': 0.125,
                    'Giả mạo': 0.125
                },
                'processing_time': 0.001,
                'warning': 'Text too short for reliable classification'
            }
        
        # Make prediction
        try:
            # Get probabilities
            probabilities = self.pipeline.predict_proba([text_combined])[0]
            
            # Get predicted class
            predicted_class = np.argmax(probabilities)
            confidence = probabilities[predicted_class]
            
            # Get category name
            category = self.id_to_category[predicted_class]
            
            # Create probability dict
            prob_dict = {
                self.id_to_category[i]: float(prob)
                for i, prob in enumerate(probabilities)
            }
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return {
                'category': category,
                'confidence': float(confidence),
                'probabilities': prob_dict,
                'processing_time': processing_time,
                'text_length': len(text_combined)
            }
            
        except Exception as e:
            return {
                'category': 'Nghi ngờ',
                'confidence': 0.5,
                'probabilities': {
                    'An toàn': 0.25,
                    'Nghi ngờ': 0.5,
                    'Spam': 0.125,
                    'Giả mạo': 0.125
                },
                'processing_time': 0.001,
                'error': str(e)
            }
    
    def predict_batch(self, emails):
        """
        Predict multiple emails at once
        
        Args:
            emails (list): List of email dicts with 'title' and 'content'
            
        Returns:
            list: List of prediction results
        """
        results = []
        
        for email in emails:
            title = email.get('title', '')
            content = email.get('content', '')
            from_email = email.get('from_email', '')
            to_email = email.get('to_email', '')
            
            result = self.predict(title, content, from_email, to_email)
            results.append(result)
        
        return results

# Example usage
if __name__ == "__main__":
    # Initialize classifier
    classifier = LightweightEmailClassifier()
    
    # Test single prediction
    result = classifier.predict(
        title="Thông báo khẩn từ ngân hàng",
        content="Tài khoản của bạn sẽ bị khóa trong 24h nếu không xác minh ngay."
    )
    
    print("\n📧 Single Prediction Result:")
    print(f"Category: {result['category']}")
    print(f"Confidence: {result['confidence']:.3f}")
    print(f"Processing time: {result['processing_time']:.3f}s")
    print("\nProbabilities:")
    for cat, prob in result['probabilities'].items():
        print(f"  {cat}: {prob:.3f}")
    
    # Test batch prediction
    test_emails = [
        {
            'title': 'GIẢM GIÁ 90% - CHỈ HÔM NAY!!!',
            'content': 'Click ngay để nhận quà tặng miễn phí!'
        },
        {
            'title': 'Kính gửi sinh viên',
            'content': 'Thân gửi các bạn, vui lòng nộp bài tập trước hạn chót.'
        }
    ]
    
    batch_results = classifier.predict_batch(test_emails)
    
    print("\n📧 Batch Prediction Results:")
    for i, result in enumerate(batch_results):
        print(f"Email {i+1}: {result['category']} (confidence: {result['confidence']:.3f})")
