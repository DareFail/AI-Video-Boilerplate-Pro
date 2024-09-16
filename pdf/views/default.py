from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from deleteYourPDF import (
    pdfToImagePages,
    cropRotateImage,
    imageToText_Roboflow,
)

from ..utils import render_with_appname


def home(request):
    context = {}
    return render_with_appname(request, "index.html", context=context)


def example(request):
    context = {}
    return render_with_appname(request, "example.html", context=context)


@csrf_exempt
def runStep(request):

    if request.method == "POST":
        command = request.POST.get("command", "")

        if command == "pdfToImagePages":
            file = request.FILES["file"].file

            listOfImagePages = pdfToImagePages(file=file, page_number=1)

            return JsonResponse(
                {
                    "result": listOfImagePages[0],
                }
            )

        elif command == "ocr":
            image = request.POST.get("image", "")

            text = imageToText_Roboflow(
                file=image, api_key=settings.ROBOFLOW_API_KEY
            )

            return JsonResponse(
                {
                    "result": text,
                }
            )

        elif command == "cropRotate":
            image = request.POST.get("image", "")
            x = int(request.POST.get("x", 0))
            y = int(request.POST.get("y", 0))
            width = int(request.POST.get("width", 1))
            height = int(request.POST.get("height", 1))
            rotation = int(request.POST.get("rotation", 0))

            croppedAndRotatedImage = cropRotateImage(
                file=image,
                x=x,
                y=y,
                width=width,
                height=height,
                rotation_degrees=rotation,
                expand_for_rotation=True,
            )

            return JsonResponse(
                {
                    "result": croppedAndRotatedImage,
                }
            )

    else:
        return JsonResponse(
            {"error": "Only POST requests are accepted"}, status=400
        )
