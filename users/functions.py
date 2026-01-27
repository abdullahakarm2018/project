from django.conf import settings
from django.http import JsonResponse
import requests


def send_whatsapp_message(request,phoneNumber,otp):
    # بيانات API
   
    url = settings.WHATSAPP_API_URL
    headers = {
        "Authorization": settings.WHATSAPP_API_TOKEN,
        "Content-Type": "application/json"
    }
    
    # بيانات الرسالة
    payload = {
        "messaging_product": "whatsapp",
        "to": phoneNumber,  # استبدل برقم الهاتف المستلم
        "type": "template",
        "template":  { "name": "otp", "language": { "code": "ar" }, "components": [
            {
                "type": "body",
        "parameters":[{"type": "text",
            "text": otp},]}] }
    }
    
    try:
        # إرسال الطلب
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()
        
        # التحقق من الاستجابة
        if response.status_code == 200:
            return JsonResponse({"status": "success", "message": "تم إرسال الرسالة بنجاح!"})
        else:
            return JsonResponse({"status": "error", "message": response_data}, status=400)
    
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
    