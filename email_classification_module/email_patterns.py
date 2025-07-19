import re

EMAIL_PATTERNS = {
    # Pattern cho email SPAM (category_id = 2)
    "spam": {
        # Pattern cơ bản (dễ nhận biết)
        "basic": {
            "titlePatterns": [
                re.compile(r"GIẢM GIÁ.*[0-9]{2,}%", re.IGNORECASE),
                re.compile(r"CHỈ.*HÔM NAY", re.IGNORECASE),
                re.compile(r"KHUYẾN MÃI.*KHỦNG", re.IGNORECASE),
                re.compile(r"💰|🎉|🔥|⭐|💯"),
                re.compile(r"!!!"),
                re.compile(r"\$\$\$"),
                re.compile(r"CLICK.*NGAY", re.IGNORECASE),
                re.compile(r"FREE|MIỄN PHÍ.*100%", re.IGNORECASE)
            ],
            "contentPatterns": [
                re.compile(r"giảm giá.*[789][0-9]%", re.IGNORECASE),
                re.compile(r"chỉ còn.*[0-9]+.*giờ", re.IGNORECASE),
                re.compile(r"click.*ngay.*link", re.IGNORECASE),
                re.compile(r"bit\.ly|tinyurl|short\.link"),
                re.compile(r"!!!|💰💰💰")
            ],
            "fromDomainPatterns": [
                re.compile(r"promo|deals|sale|offer|discount", re.IGNORECASE),
                re.compile(r"\d{2,}\.net|\.tk|\.ml")
            ]
        },
        # Pattern nâng cao (khó nhận biết hơn)
        "advanced": {
            "titlePatterns": [
                re.compile(r"ưu đãi.*đặc biệt", re.IGNORECASE),
                re.compile(r"thông báo.*khuyến mãi", re.IGNORECASE),
                re.compile(r"cơ hội.*hiếm", re.IGNORECASE)
            ],
            "contentPatterns": [
                re.compile(r"số lượng có hạn", re.IGNORECASE),
                re.compile(r"đăng ký ngay để nhận", re.IGNORECASE),
                re.compile(r"ưu đãi dành riêng cho bạn", re.IGNORECASE)
            ],
            "fromDomainPatterns": [
                re.compile(r"marketing@", re.IGNORECASE),
                re.compile(r"newsletter@", re.IGNORECASE)
            ]
        }
    },
    # Pattern cho email PHISHING (category_id = 3)
    "phishing": {
        "basic": {
            "titlePatterns": [
                re.compile(r"bảo mật|security", re.IGNORECASE),
                re.compile(r"tài khoản.*bị.*khóa", re.IGNORECASE),
                re.compile(r"xác (minh|nhận|thực).*khẩn", re.IGNORECASE),
                re.compile(r"cập nhật.*ngay", re.IGNORECASE)
            ],
            "contentPatterns": [
                re.compile(r"tài khoản.*sẽ bị.*khóa", re.IGNORECASE),
                re.compile(r"xác (minh|nhận).*trong.*[0-9]+.*giờ", re.IGNORECASE),
                re.compile(r"click.*link.*xác (minh|nhận)", re.IGNORECASE),
                re.compile(r"cập nhật.*thông tin.*bảo mật", re.IGNORECASE)
            ],
            "fromDomainPatterns": [
                re.compile(r"[0-9]"),  # Có số trong tên miền (amaz0n)
                re.compile(r"-verification|-security|-account", re.IGNORECASE),
                re.compile(r"\.tk|\.ml|\.ga|\.cf")
            ],
            "brandSpoofing": [
                re.compile(r"amaz[0o]n", re.IGNORECASE),
                re.compile(r"g[0o]{2}gle", re.IGNORECASE),
                re.compile(r"micr[0o]soft", re.IGNORECASE),
                re.compile(r"payp[a@]l", re.IGNORECASE),
                re.compile(r"faceb[0o]{2}k", re.IGNORECASE)
            ]
        },
        "advanced": {
            "titlePatterns": [
                re.compile(r"thông báo từ.*phòng.*kế toán", re.IGNORECASE),
                re.compile(r"yêu cầu xác nhận.*thanh toán", re.IGNORECASE)
            ],
            "contentPatterns": [
                re.compile(r"vui lòng kiểm tra.*đính kèm", re.IGNORECASE),
                re.compile(r"xác nhận.*giao dịch", re.IGNORECASE),
                re.compile(r"để tiếp tục.*vui lòng", re.IGNORECASE)
            ],
            "fromDomainPatterns": [
                re.compile(r"no-?reply@.*\.(info|online|site)", re.IGNORECASE)
            ]
        }
    },
    # Pattern cho email NGHI NGỜ (category_id = 1)
    "suspicious": {
        "basic": {
            "titlePatterns": [
                re.compile(r"khẩn|gấp|urgent", re.IGNORECASE),
                re.compile(r"hạn chót|deadline", re.IGNORECASE),
                re.compile(r"quan trọng.*cập nhật", re.IGNORECASE)
            ],
            "contentPatterns": [
                re.compile(r"vui lòng.*cung cấp", re.IGNORECASE),
                re.compile(r"xác nhận.*thông tin", re.IGNORECASE),
                re.compile(r"truy cập.*link.*bên dưới", re.IGNORECASE),
                re.compile(r"trong vòng.*[0-9]+.*giờ", re.IGNORECASE)
            ],
            "fromDomainPatterns": [
                re.compile(r"\.(info|click|site|online)$", re.IGNORECASE),
                re.compile(r"-system|-admin", re.IGNORECASE)
            ],
            "spellingErrors": [
                re.compile(r"recieve", re.IGNORECASE),  # receive
                re.compile(r"occured", re.IGNORECASE),  # occurred
                re.compile(r"loose", re.IGNORECASE),    # lose
                re.compile(r"there account", re.IGNORECASE),  # their account
            ]
        },
        "advanced": {
            # Email trông chuyên nghiệp nhưng có dấu hiệu nhỏ
            "subtleIndicators": [
                re.compile(r"vui lòng phản hồi sớm", re.IGNORECASE),
                re.compile(r"thông tin này là bảo mật", re.IGNORECASE),
                re.compile(r"không chia sẻ email này", re.IGNORECASE)
            ]
        }
    },
    # Pattern cho email AN TOÀN (category_id = 0)
    "safe": {
        "requiredPatterns": {
            "fromDomainPatterns": [
                re.compile(r"@fpt\.edu\.vn$"),
                re.compile(r"@[a-z]+\.edu\.vn$"),
                re.compile(r"@(gmail|outlook|yahoo)\.com$"),
                re.compile(r"@[a-z]+(corp|company|university)\.(com|vn|edu)$")
            ],
            "professionalGreetings": [
                re.compile(r"^kính (gửi|chào)", re.IGNORECASE),
                re.compile(r"^thân gửi", re.IGNORECASE),
                re.compile(r"^dear", re.IGNORECASE)
            ],
            "professionalClosings": [
                re.compile(r"trân trọng", re.IGNORECASE),
                re.compile(r"best regards", re.IGNORECASE),
                re.compile(r"thân ái", re.IGNORECASE),
                re.compile(r"kính thư", re.IGNORECASE)
            ]
        },
        # Không có các pattern nghi ngờ
        "mustNotHave": {
            "suspiciousWords": [
                re.compile(r"click.*here|nhấp.*vào đây", re.IGNORECASE),
                re.compile(r"verify.*account|xác minh.*tài khoản", re.IGNORECASE),
                re.compile(r"suspended|bị treo", re.IGNORECASE),
                re.compile(r"act now|hành động ngay", re.IGNORECASE)
            ]
        }
    }
} 