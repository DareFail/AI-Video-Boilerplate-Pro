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

    listOfImagePages = []

    if request.method == 'POST':
        command = request.POST.get('command', '')

        if command == "pdfToImagePages":
            file = request.FILES['file'].file

            listOfImagePages = pdfToImagePages(file, 1)

        '''
        listOfText = []
        listOfImageResults = []
        for imagePage in listOfImagePages:
            image_dimensions = imageWidthHeight(file=imagePage)

            width = image_dimensions["width"]
            height = image_dimensions["height"]

            croppedAndRotatedImage = cropRotateImage(file=imagePage, x=0, y=0, width=width, height=height, rotation_degrees=0)
            listOfText.append(imageToText_Roboflow(file=croppedAndRotatedImage, api_key=settings.ROBOFLOW_API_KEY))
            
            listOfImageResults.append(croppedAndRotatedImage)

        return JsonResponse({
            "pages": listOfImageResults,
            "texts": listOfText,
        })
        '''

        result = ""

        if len(listOfImagePages) > 0:
            result = listOfImagePages[0]

        return JsonResponse({
            "result": result,
        })

        
    else:
        return JsonResponse({"error": "Only POST requests are accepted"}, status=400)


