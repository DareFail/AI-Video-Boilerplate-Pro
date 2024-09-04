import boto3

from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages


from ..tasks import rate_loaf
from ..models import CatLoaf
from ..utils import render_with_appname


def home(request):

    return render_with_appname(request, "index.html")


def uploadloaf(request, unique_name):

    return render_with_appname(request, "index.html")


@csrf_exempt
def checkloaf(request, unique_name):
    rateloaf = CatLoaf.objects.filter(unique_name=unique_name).first()

    if rateloaf:
        if not rateloaf.is_rating:
            rate_loaf.delay(unique_name)

        return JsonResponse(
            {
                "is_rated": rateloaf.is_rated,
            }
        )
    return render_with_appname(request, "index.html")


def rateloaf(request, unique_name):

    rateloaf = CatLoaf.objects.filter(unique_name=unique_name).first()

    if not rateloaf:
        messages.error(request, "There is no cat loaf here :(")
        return render_with_appname(request, "index.html")
    else:
        if not rateloaf.is_rated:
            if not rateloaf.is_rating:
                thisLoaf = rate_loaf(unique_name)

                if thisLoaf is None:
                    messages.error(
                        request, "Your cat loaf may have been too chonky"
                    )
                    return render_with_appname(request, "index.html")

        split_strings = rateloaf.description.split("/10.", 1)
        title_string = split_strings[0] + "/10."
        last_string = (
            split_strings[1].strip() if len(split_strings) > 1 else ""
        )

        context = {
            "loaf": rateloaf,
            "title": title_string,
            "description": last_string,
        }

        return render_with_appname(request, "rate.html", context=context)


@csrf_exempt
def sign_s3(request):

    unique_name = get_random_string(
        6, allowed_chars="abcdefghijklmnopqrstuvwxyz"
    )

    s3_bucket = "rateloaf"

    if request.method == "GET":
        file_name = request.GET.get("file_name", False)
        file_type = request.GET.get("file_type", False)
        file_extension = file_name.split(".")[-1]
        new_file_name = unique_name + "." + file_extension

        if file_name and file_type and len(file_extension) < 6:

            s3 = boto3.client("s3")

            presigned_post = s3.generate_presigned_post(
                Bucket=s3_bucket,
                Key=new_file_name,
                Fields={"Content-Type": file_type},
                Conditions=[
                    {"Content-Type": file_type},
                ],
                ExpiresIn=3600,
            )


            while True:
                try:
                    CatLoaf.objects.create(
                        unique_name=unique_name,
                        image_url_user="https://rateloaf.s3.amazonaws.com/"
                        + new_file_name,
                    )
                    break

                except Exception as e:
                    print("Error: ", str(e))


            return JsonResponse(
                {
                    "data": presigned_post,
                    "unique_name": unique_name,
                    "url": "https://%s.s3.amazonaws.com/%s"
                    % (s3_bucket, new_file_name),
                }
            )

    return JsonResponse(
        {
            "data": "",
        }
    )
