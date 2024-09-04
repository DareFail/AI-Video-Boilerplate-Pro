import boto3
import base64

from inference_sdk import InferenceHTTPClient

from celery import shared_task
from django.conf import settings
from ..models import CatLoaf


@shared_task
def rate_loaf(unique_name):

    rate_loaf = CatLoaf.objects.filter(unique_name=unique_name).first()
    rate_loaf.is_rating = True
    rate_loaf.save()

    try:

        # Roboflow Stuff
        client = InferenceHTTPClient(
            api_url="https://detect.roboflow.com",
            api_key=settings.ROBOFLOW_API_KEY,
        )

        result = client.run_workflow(
            workspace_name="test-y7opj",
            workflow_id="rate-my-loaf",
            images={"image": rate_loaf.image_url_user},
        )

        openai_text = result[0]["openai"]["raw_output"]
        only_cat_filter_predictions = result[0]["only_cat_filter_predictions"][
            "predictions"
        ]
        blemiesh_1_predictions = result[0]["blemiesh_1_predictions"][
            "predictions"
        ]
        blemish_1_image = result[0]["blemish_1_image"]
        blemiesh_2_predictions = result[0]["blemiesh_2_predictions"][
            "predictions"
        ]
        blemish_2_image = result[0]["blemish_2_image"]
        cat_image_original = result[0]["cat_image_original"]
        first_cat = result[0]["first_cat"]["predictions"]

        # S3 Stuff
        session = boto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        s3 = session.resource("s3")
        s3_bucket = "rateloaf"

        file_extension = rate_loaf.image_url_user.split(".")[-1]

        key_name_cat_image_original = (
            unique_name + "_cat_image_original." + file_extension
        )
        byte_content_cat_image_original = base64.b64decode(cat_image_original)

        key_name_blemish_1_image = (
            unique_name + "_blemish_1_image." + file_extension
        )
        byte_content_blemish_1_image = base64.b64decode(blemish_1_image)

        key_name_blemish_2_image = (
            unique_name + "_blemish_2_image." + file_extension
        )
        byte_content_blemish_2_image = base64.b64decode(blemish_2_image)

        s3.Bucket(s3_bucket).put_object(
            Key=key_name_cat_image_original,
            Body=byte_content_cat_image_original,
        )
        s3.Bucket(s3_bucket).put_object(
            Key=key_name_blemish_1_image, Body=byte_content_blemish_1_image
        )
        s3.Bucket(s3_bucket).put_object(
            Key=key_name_blemish_2_image, Body=byte_content_blemish_2_image
        )

        print(openai_text)

        rate_loaf.unique_name = unique_name
        rate_loaf.description = openai_text
        rate_loaf.only_cat_filter = len(only_cat_filter_predictions)
        rate_loaf.blemish_pass_1 = len(blemiesh_1_predictions)
        rate_loaf.blemish_pass_2 = len(blemiesh_2_predictions)
        rate_loaf.image_url_original = (
            "https://rateloaf.s3.amazonaws.com/" + key_name_cat_image_original
        )
        rate_loaf.image_url_blemish_1 = (
            "https://rateloaf.s3.amazonaws.com/" + key_name_blemish_1_image
        )
        rate_loaf.image_url_blemish_2 = (
            "https://rateloaf.s3.amazonaws.com/" + key_name_blemish_2_image
        )
        rate_loaf.is_rated = True
        rate_loaf.has_cat_outline = len(first_cat) > 0
        rate_loaf.save()

        return rate_loaf

    except Exception as e:
        print("Failed to upload to S3. Error: ", str(e))
        return None
