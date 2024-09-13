from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from deleteYourPDF import pdfToImagePages, imageWidthHeight, cropRotateImage, imageToText_Roboflow

from ..utils import render_with_appname


def home(request):
    context = {}
    return render_with_appname(request, "index.html", context=context)


@csrf_exempt
def runStep(request):

    if request.method == 'POST':
        command = request.POST.get('command', '')

        if command == "pdfToImagePages":
            file = request.FILES['file'].file

            listOfImagePages = pdfToImagePages(file=file, page_number=1)

            return JsonResponse({
                "result": listOfImagePages[0],
            })

        elif command == "ocr":
            image = request.POST.get('image', '')

            text = imageToText_Roboflow(file=image, api_key=settings.ROBOFLOW_API_KEY)

            return JsonResponse({
                "result": text,
            })

        
    else:
        return JsonResponse({"error": "Only POST requests are accepted"}, status=400)


