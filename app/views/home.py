from aws_xray_sdk.core import xray_recorder
from django.shortcuts import render
from app.views.helpers import (
    create_jsonable_subjects,
    create_jsonable_submit_types,
)


@xray_recorder.capture('view.home')
def home(request):
    jsonable_subjects = create_jsonable_subjects()
    jsonable_submit_types = create_jsonable_submit_types()

    return render(request, 'home.html', {
        'subjects': jsonable_subjects,
        'submit_types': jsonable_submit_types,
    })
