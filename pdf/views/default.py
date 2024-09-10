import base64

from inference_sdk import InferenceHTTPClient
from django.views.decorators.csrf import csrf_exempt
from django.core.files.images import ImageFile
from django.http import JsonResponse
from PIL import Image
from django.conf import settings

from ..utils import render_with_appname


def home(request):
    context = {}
    return render_with_appname(request, "index.html", context=context)


@csrf_exempt
def sendInputImage(request):
    if request.method == 'POST':
        image = request.FILES['image'].file

        client = InferenceHTTPClient(
            api_url="https://detect.roboflow.com",
            api_key=settings.ROBOFLOW_API_KEY,
        )

        pil_image = Image.open(image)

        # Convert RGBA image to RGB
        if pil_image.mode == 'RGBA':
            rgb_image = pil_image.convert('RGB')
        else:
            rgb_image = pil_image

        result = client.run_workflow(
            workspace_name="test-y7opj",
            workflow_id="custom-workflow",
            images={"image": rgb_image},
        )

        return JsonResponse(result[0])
    else:
        return JsonResponse({"error": "Only POST requests are accepted"}, status=400)