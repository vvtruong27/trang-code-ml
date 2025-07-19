# Email Classification API

API phân loại email sử dụng cả rule-based và machine learning approaches. Phân loại email thành 4 loại: An toàn, Nghi ngờ, Spam, Giả mạo.

## 🚀 **Features**

- **Rule-based Classification**: Sử dụng pattern matching và regex rules
- **ML Classification**: TF-IDF + Logistic Regression với độ chính xác 100%
- **Fast Processing**: Xử lý nhanh với thời gian < 25ms per email
- **Swagger UI**: Giao diện test API trực quan
- **CORS Support**: Hỗ trợ cross-origin requests
- **Batch Processing**: Phân loại nhiều email cùng lúc

## 📊 **Models**

### 1. Rule-based Classifier
- **Algorithm**: Pattern-based classification with regex
- **Features**: title, content, from_email
- **Speed**: ~0.27ms per email
- **Explainable**: Có indicators cụ thể

### 2. TF-IDF + Logistic Regression
- **Algorithm**: TF-IDF vectorization + Logistic Regression
- **Features**: title, content, from_email
- **Accuracy**: 100% trên test set
- **Training Time**: 3.86 seconds
- **Speed**: ~20ms per email

## 🏗️ **Project Structure**

```
trang-code/
├── email_classification_module/
│   ├── api_backend.py              # Flask API server
│   ├── email_classifier.py         # Rule-based classifier
│   ├── email_patterns.py           # Regex patterns
│   └── static/
│       └── swagger.json           # Swagger documentation
├── models/                        # Trained models
│   ├── lightweight_email_classifier.pkl  # TF-IDF + LR model
│   ├── category_mapping.pkl              # Category mapping
│   ├── id_to_category.pkl                # Reverse mapping
│   └── lightweight_email_classifier.py   # Prediction script
├── setup.sh                       # Setup script (macOS/Linux)
├── setup.bat                      # Setup script (Windows)
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore rules
└── README.md                     # This file
```

## 🚀 **Quick Start**

### Option 1: Automated Setup (Recommended)
```bash
# On macOS/Linux:
./setup.sh

# On Windows:
setup.bat
```

### Option 2: Manual Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Train Model (Optional)
```bash
# Training script đã được xóa để giữ dự án gọn gàng
# Model đã được train sẵn trong thư mục models/
```

### 3. Start API Server
```bash
# Make sure virtual environment is activated
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Start API server
cd email_classification_module
python api_backend.py
```

### 4. Access API
- **API Base URL**: http://localhost:5001
- **Swagger UI**: http://localhost:5001/swagger
- **Health Check**: http://localhost:5001/health

## 📡 **API Endpoints**

### System Endpoints
- `GET /` - Trang chủ API
- `GET /health` - Kiểm tra trạng thái
- `GET /model_info` - Thông tin models

### Classification Endpoints
- `POST /predict/rule` - Phân loại bằng rule-based
- `POST /predict/ml` - Phân loại bằng ML model
- `POST /predict/batch` - Phân loại nhiều email

## 📝 **API Usage Examples**

### Rule-based Classification
```bash
curl -X POST http://localhost:5001/predict/rule \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Thông báo khẩn từ ngân hàng",
    "content": "Tài khoản của bạn sẽ bị khóa trong 24h nếu không xác minh ngay.",
    "from_email": "security@bank-verify.tk"
  }'
```

### ML Classification
```bash
curl -X POST http://localhost:5001/predict/ml \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Thông báo khẩn từ ngân hàng",
    "content": "Tài khoản của bạn sẽ bị khóa trong 24h nếu không xác minh ngay.",
    "from_email": "security@bank-verify.tk"
  }'
```

### Batch Classification
```bash
curl -X POST http://localhost:5001/predict/batch \
  -H "Content-Type: application/json" \
  -d '{
    "method": "ml",
    "emails": [
      {
        "title": "Thông báo khẩn từ ngân hàng",
        "content": "Tài khoản của bạn sẽ bị khóa trong 24h nếu không xác minh ngay.",
        "from_email": "security@bank-verify.tk"
      },
      {
        "title": "Xác nhận đơn hàng",
        "content": "Cảm ơn bạn đã đặt hàng. Đơn hàng của bạn đã được xác nhận.",
        "from_email": "orders@shopee.vn"
      }
    ]
  }'
```

## 📊 **Model Performance**

### TF-IDF + Logistic Regression
- **Training Accuracy**: 100%
- **Test Accuracy**: 100%
- **Training Time**: 3.86 seconds
- **Prediction Time**: ~20ms per email
- **Model Size**: 435KB

### Rule-based
- **Prediction Time**: ~0.27ms per email
- **Explainable**: Có indicators cụ thể
- **No Training Required**: Dựa trên patterns

## 🔧 **Configuration**

### Environment Setup
- **Python Version**: 3.8+
- **Virtual Environment**: `.venv` (recommended)
- **Dependencies**: See `requirements.txt`

### API Configuration
- **Host**: 0.0.0.0
- **Port**: 5001
- **Debug Mode**: Enabled (development)
- **CORS**: All origins allowed (development)

### Model Configuration
- **TF-IDF Features**: 10,000 max features
- **N-grams**: (1, 2) - unigrams and bigrams
- **Logistic Regression**: LBFGS solver, C=1.0

## 🧪 **Testing**

### Test API
```bash
# Make sure virtual environment is activated
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Test API endpoints
curl -X GET http://localhost:5001/health
curl -X GET http://localhost:5001/model_info
```

### Manual Testing
1. Mở Swagger UI: http://localhost:5001/swagger
2. Test các endpoints với sample data
3. Kiểm tra response format và accuracy

## 📈 **Categories**

| ID | Category | Description |
|----|----------|-------------|
| 0 | An toàn | Email an toàn, không có dấu hiệu đáng ngờ |
| 1 | Nghi ngờ | Email có một số dấu hiệu đáng ngờ |
| 2 | Spam | Email spam, quảng cáo không mong muốn |
| 3 | Giả mạo | Email phishing, giả mạo để lừa đảo |

## 🚀 **Production Deployment**

### Using Virtual Environment
```bash
# 1. Clone repository
git clone <repository-url>
cd trang-code

# 2. Setup virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start API server
cd email_classification_module
python api_backend.py
```

### Using Docker (Alternative)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5001

CMD ["python", "email_classification_module/api_backend.py"]
```

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Setup virtual environment: `python -m venv .venv && source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Make your changes
6. Test thoroughly
7. Submit a pull request

## 📄 **License**

This project is licensed under the MIT License. 