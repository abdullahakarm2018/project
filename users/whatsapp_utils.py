import requests
import logging
from django.http import JsonResponse
from django.conf import settings

logger = logging.getLogger(__name__)

def send_whatsapp_message(request, phoneNumber, otp):
    # تحقق من المدخلات
    if not phoneNumber or not otp:
        logger.error("Phone number and OTP are required.")
        return JsonResponse({"status": "error", "message": "Phone number and OTP are required."}, status=400)

    # بيانات API
    url = settings.WHATSAPP_API_URL
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # بيانات الرسالة
    payload = {
        "messaging_product": "whatsapp",
        "to": phoneNumber,  # رقم الهاتف المستلم
        "type": "template",
        "template": {
            "name": "otp",  # اسم القالب
            "language": {
                "code": "ar"  # لغة القالب (العربية)
            },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": str(otp)  # تحويل OTP إلى نص
                        }
                    ]
                },
                 {
                "type": "button",
                "sub_type": "url",
                "index": 0,  # الفهرس (index) للزر
                "parameters": [
                    {
                        "type": "text",
                        "text": str(otp)   # الرابط المطلوب للزر
                    }
                ]
            }
            ]
        }
    }
    
    try:
        # إرسال الطلب
        logger.info(f"Sending WhatsApp message to {phoneNumber} with OTP: {otp}")
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()
        logger.info(f"API Response: {response_data}")
        
        # التحقق من الاستجابة
        if response.status_code == 200:
            return JsonResponse({"status": "success", "message": "تم إرسال الرسالة بنجاح!"})
        else:
            # إرجاع رسالة الخطأ من API
            error_message = response_data.get("error", {}).get("message", "Unknown error")
            logger.error(f"API Error: {error_message}")
            return JsonResponse({"status": "error", "message": error_message}, status=response.status_code)
    
    except requests.exceptions.RequestException as e:
        # معالجة أخطاء الشبكة
        logger.error(f"Network error: {str(e)}")
        return JsonResponse({"status": "error", "message": f"Network error: {str(e)}"}, status=500)
    except Exception as e:
        # معالجة الأخطاء العامة
        logger.error(f"General error: {str(e)}")
        return JsonResponse({"status": "error", "message": str(e)}, status=500)