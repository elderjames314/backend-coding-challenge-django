from logging import raiseExceptions
from mailbox import NotEmptyError
from urllib import response
from django.forms.models import model_to_dict
from note.models import Note
from rest_framework.response import Response
from rest_framework.decorators import api_view
from note.serializers import NoteSerializer
from django.http import JsonResponse


# Create your views here.
@api_view(["GET", "POST"])
def api_random_notes(request, *args, **kwargs):
    try:
        instance = Note.objects.all().order_by("?").first()
        data = {}
        if instance:
           # data = model_to_dict(instance, fields=['title', 'body', 'tags'])
             data = NoteSerializer(instance).data
            # print(data)
             return Response(data)
    except:
        pass

@api_view(["POST"])
def add_new_note(request, *args, **kwargs):
    data={}
    serialiser = NoteSerializer(data=request.data)
    if serialiser.is_valid(raise_exception=True):
        instance = serialiser.save()
        return Response(serialiser.data)
    return Response({"message" : "invalid data"}, status=400)

