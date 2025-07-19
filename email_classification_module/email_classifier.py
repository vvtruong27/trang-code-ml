import re
from email_patterns import EMAIL_PATTERNS
import logging

# Thiết lập logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailClassifier:
    """
    Phân loại email dựa trên rule-based approach
    Categories: An toàn (0), Nghi ngờ (1), Spam (2), Giả mạo (3)
    """
    
    def __init__(self):
        self.patterns = EMAIL_PATTERNS
        logger.info("✅ Email classifier initialized successfully")
    
    def classify_email(self, email_data):
        """
        Phân loại email dựa trên các dấu hiệu nhận biết
        
        Args:
            email_data (dict): Email cần phân loại với keys:
                - title: Tiêu đề email
                - content: Nội dung email  
                - from_email: Email người gửi
                
        Returns:
            dict: Kết quả phân loại với category, confidence, indicators, level
        """
        title = email_data.get('title', '')
        content = email_data.get('content', '')
        from_email = email_data.get('from_email', '')
        
        # Khởi tạo kết quả với giá trị mặc định
        result = {
            'category': 'An toàn',
            'confidence': 0,
            'indicators': [],
            'level': 'basic'
        }
        
        # Kiểm tra từng loại email theo thứ tự ưu tiên
        # 1. Kiểm tra Phishing trước (nguy hiểm nhất)
        phishing_check = self._check_phishing(title, content, from_email)
        if phishing_check['isPhishing']:
            return {
                'category': 'Giả mạo',
                'confidence': phishing_check['confidence'],
                'indicators': phishing_check['indicators'],
                'level': phishing_check['level']
            }
        
        # 2. Kiểm tra Spam
        spam_check = self._check_spam(title, content, from_email)
        if spam_check['isSpam']:
            return {
                'category': 'Spam',
                'confidence': spam_check['confidence'],
                'indicators': spam_check['indicators'],
                'level': spam_check['level']
            }
        
        # 3. Kiểm tra Nghi ngờ
        suspicious_check = self._check_suspicious(title, content, from_email)
        if suspicious_check['isSuspicious']:
            return {
                'category': 'Nghi ngờ',
                'confidence': suspicious_check['confidence'],
                'indicators': suspicious_check['indicators'],
                'level': suspicious_check['level']
            }
        
        # 4. Kiểm tra An toàn
        safe_check = self._check_safe(title, content, from_email)
        if safe_check['isSafe']:
            return {
                'category': 'An toàn',
                'confidence': safe_check['confidence'],
                'indicators': ['Email từ nguồn tin cậy', 'Không có dấu hiệu đáng ngờ'],
                'level': 'basic'
            }
        
        # Nếu không rõ ràng, mặc định là Nghi ngờ với confidence thấp
        return {
            'category': 'Nghi ngờ',
            'confidence': 0.3,
            'indicators': ['Không thể xác định rõ ràng'],
            'level': 'basic'
        }
    
    def _check_phishing(self, title, content, from_email):
        """Kiểm tra email Phishing (Giả mạo)"""
        patterns = self.patterns['phishing']
        indicators = []
        match_count = 0
        level = 'basic'
        
        # Kiểm tra domain giả mạo trong email gửi
        domain = from_email.split('@')[1] if '@' in from_email else ''
        
        # Kiểm tra brand spoofing (ví dụ: Amaz0n, G00gle)
        for brand_pattern in patterns['basic']['brandSpoofing']:
            if brand_pattern.search(from_email) or brand_pattern.search(content):
                indicators.append('Giả mạo thương hiệu với ký tự số thay chữ')
                match_count += 2  # Trọng số cao cho brand spoofing
        
        # Kiểm tra phishing domains (.tk, .ml, .ga, .cf)
        for phish_domain in patterns['basic']['fromDomainPatterns']:
            if phish_domain.search(domain):
                indicators.append(f'Domain đáng ngờ: {domain}')
                match_count += 2
        
        # Kiểm tra title patterns
        for pattern in patterns['basic']['titlePatterns']:
            if pattern.search(title):
                indicators.append('Tiêu đề có dấu hiệu phishing')
                match_count += 1
        
        # Kiểm tra content patterns
        for pattern in patterns['basic']['contentPatterns']:
            if pattern.search(content):
                indicators.append('Nội dung yêu cầu xác minh khẩn cấp')
                match_count += 1
        
        # Kiểm tra advanced patterns nếu có
        if 'advanced' in patterns and match_count < 3:
            level = 'advanced'
            # Kiểm tra các dấu hiệu tinh vi hơn
            if re.search(r'phòng.*kế.*toán', from_email, re.IGNORECASE) or \
               re.search(r'accounting', from_email, re.IGNORECASE):
                indicators.append('Giả danh phòng ban nội bộ')
                match_count += 1
        
        confidence = min(match_count * 0.25, 1)
        
        return {
            'isPhishing': match_count >= 2,
            'confidence': confidence,
            'indicators': indicators,
            'level': level
        }
    
    def _check_spam(self, title, content, from_email):
        """Kiểm tra email Spam"""
        patterns = self.patterns['spam']
        indicators = []
        match_count = 0
        level = 'basic'
        
        # Kiểm tra basic spam patterns
        # 1. Title với giảm giá, viết hoa, emoji
        for pattern in patterns['basic']['titlePatterns']:
            if pattern.search(title):
                if re.search(r'[0-9]{2,}%', title, re.IGNORECASE):
                    indicators.append('Quảng cáo giảm giá lớn')
                elif re.search(r'!!!', title):
                    indicators.append('Sử dụng nhiều dấu chấm than')
                elif re.search(r'💰|🎉|🔥', title):
                    indicators.append('Sử dụng emoji spam')
                match_count += 1
        
        # 2. Content patterns
        for pattern in patterns['basic']['contentPatterns']:
            if pattern.search(content):
                if re.search(r'bit\.ly|tinyurl', content):
                    indicators.append('Chứa link rút gọn đáng ngờ')
                    match_count += 2  # Trọng số cao cho shortened links
                else:
                    indicators.append('Nội dung spam điển hình')
                    match_count += 1
        
        # 3. From domain patterns
        domain = from_email.split('@')[1] if '@' in from_email else ''
        for pattern in patterns['basic']['fromDomainPatterns']:
            if pattern.search(domain):
                indicators.append('Domain spam thương mại')
                match_count += 1
        
        # Kiểm tra advanced spam (marketing tinh vi)
        if 'advanced' in patterns and match_count < 2:
            level = 'advanced'
            for pattern in patterns['advanced']['contentPatterns']:
                if pattern.search(content):
                    indicators.append('Marketing email với trigger tâm lý')
                    match_count += 1
        
        confidence = min(match_count * 0.3, 1)
        
        return {
            'isSpam': match_count >= 2,
            'confidence': confidence,
            'indicators': indicators,
            'level': level
        }
    
    def _check_suspicious(self, title, content, from_email):
        """Kiểm tra email Nghi ngờ"""
        patterns = self.patterns['suspicious']
        indicators = []
        match_count = 0
        level = 'basic'
        
        # 1. Kiểm tra title patterns (khẩn, gấp, urgent)
        for pattern in patterns['basic']['titlePatterns']:
            if pattern.search(title):
                indicators.append('Tạo áp lực thời gian trong tiêu đề')
                match_count += 1
        
        # 2. Kiểm tra content patterns
        for pattern in patterns['basic']['contentPatterns']:
            if pattern.search(content):
                if re.search(r'trong vòng.*[0-9]+.*giờ', content, re.IGNORECASE):
                    indicators.append('Yêu cầu hành động trong thời gian ngắn')
                elif re.search(r'vui lòng.*cung cấp', content, re.IGNORECASE):
                    indicators.append('Yêu cầu cung cấp thông tin')
                else:
                    indicators.append('Nội dung có dấu hiệu đáng ngờ')
                match_count += 1
        
        # 3. Kiểm tra domain patterns
        domain = from_email.split('@')[1] if '@' in from_email else ''
        for pattern in patterns['basic']['fromDomainPatterns']:
            if pattern.search(domain):
                indicators.append(f'Domain không chính thức: {domain}')
                match_count += 1
        
        # 4. Kiểm tra lỗi chính tả (spelling errors)
        if 'spellingErrors' in patterns['basic']:
            full_text = title + ' ' + content
            for error_pattern in patterns['basic']['spellingErrors']:
                if error_pattern.search(full_text):
                    indicators.append('Có lỗi chính tả đáng ngờ')
                    match_count += 1
                    break
        
        confidence = min(match_count * 0.35, 1)
        
        return {
            'isSuspicious': match_count >= 2,
            'confidence': confidence,
            'indicators': indicators,
            'level': level
        }
    
    def _check_safe(self, title, content, from_email):
        """Kiểm tra email An toàn"""
        patterns = self.patterns['safe']
        safe_score = 0
        
        # 1. Kiểm tra domain tin cậy
        domain = from_email.split('@')[1] if '@' in from_email else ''
        for pattern in patterns['requiredPatterns']['fromDomainPatterns']:
            if pattern.search(from_email):
                safe_score += 2  # Domain tin cậy có trọng số cao
                break
        
        # 2. Kiểm tra lời chào chuyên nghiệp
        for pattern in patterns['requiredPatterns']['professionalGreetings']:
            if pattern.search(content):
                safe_score += 1
                break
        
        # 3. Kiểm tra lời kết chuyên nghiệp
        for pattern in patterns['requiredPatterns']['professionalClosings']:
            if pattern.search(content):
                safe_score += 1
                break
        
        # 4. Đảm bảo KHÔNG có các từ nghi ngờ
        has_suspicious_words = False
        for pattern in patterns['mustNotHave']['suspiciousWords']:
            if pattern.search(content) or pattern.search(title):
                has_suspicious_words = True
                break
        
        # Email an toàn nếu:
        # - Có domain tin cậy (score >= 2) VÀ
        # - Không có từ nghi ngờ VÀ
        # - Có ít nhất 1 yếu tố chuyên nghiệp khác
        is_safe = safe_score >= 3 and not has_suspicious_words
        confidence = min(safe_score * 0.25, 1) if is_safe else 0
        
        return {
            'isSafe': is_safe,
            'confidence': confidence
        }
    
    def analyze_email(self, email_data):
        """Phân tích chi tiết một email và in kết quả"""
        title = email_data.get('title', '')
        from_email = email_data.get('from_email', '')
        
        logger.info('\n=== PHÂN TÍCH EMAIL ===')
        logger.info(f'Tiêu đề: {title}')
        logger.info(f'Từ: {from_email}')
        logger.info('---')
        
        result = self.classify_email(email_data)
        
        logger.info('KẾT QUẢ PHÂN LOẠI:')
        logger.info(f'- Loại: {result["category"]}')
        logger.info(f'- Độ tin cậy: {result["confidence"]*100:.0f}%')
        logger.info(f'- Level: {result["level"]}')
        logger.info('- Dấu hiệu nhận biết:')
        for indicator in result['indicators']:
            logger.info(f'  • {indicator}')
        logger.info('======================\n')
        
        return result 