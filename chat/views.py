import json
import os

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from dotenv import load_dotenv
from google import genai
from django.views.decorators.csrf import csrf_exempt

# Đọc biến môi trường từ file .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "Không tìm thấy GEMINI_API_KEY trong file .env"
    )

client = genai.Client(api_key=api_key)


def home(request):
    return render(request, "index.html")


@csrf_exempt
@require_POST
def chat_ai(request):
    try:
        data = json.loads(request.body or "{}")
        message = data.get("message", "").strip()

        if not message:
            return JsonResponse(
                {
                    "success": False,
                    "reply": "Bạn chưa nhập câu hỏi.",
                },
                status=400,
            )

        prompt = f"""
Bạn là trợ lý AI thân thiện dành cho sinh viên.

Yêu cầu:
- Luôn trả lời bằng tiếng Việt.
- Trả lời rõ ràng, dễ hiểu và không quá dài.
- Chỉ sử dụng tiếng Anh khi người dùng yêu cầu.
- Không tự tạo thông tin khi không chắc chắn.

Câu hỏi của người dùng:
{message}
"""

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        answer = (
            response.text
            or "Xin lỗi, tôi chưa thể trả lời câu hỏi này."
        )

        return JsonResponse(
            {
                "success": True,
                "reply": answer,
            }
        )

    except json.JSONDecodeError:
        return JsonResponse(
            {
                "success": False,
                "reply": "Dữ liệu gửi lên không hợp lệ.",
            },
            status=400,
        )

    except Exception as error:
        import traceback
        traceback.print_exc()

        return JsonResponse(
            {
                "success": False,
                "reply": f"Lỗi Gemini: {str(error)}",
            },
            status=500,
        )