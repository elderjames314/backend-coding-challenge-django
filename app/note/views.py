from ast import Not
from cgitb import lookup
from curses import meta
from itertools import product

from django.http import Http404
from rest_framework import authentication, generics, mixins, permissions
from django.shortcuts import get_object_or_404
from yaml import serialize
from .models import Note
from rest_framework.response import Response
from .serializers import NoteSerializer


class NoteMixinView(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        generics.GenericAPIView):

    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        print(serializer.validated_data)
        title = serializer.validated_data.get('title')
        body = serializer.validated_data.get('body') or None
        if body is None:
            body = title
        serializer.save(body=body)

    #def post() #HTTP ->post
note_mixins_view = NoteMixinView.as_view()


def product_alt_view(request, pk=None, *args, **kwargs):
    pass
    method = request.method
    if method == 'GET':
        if pk is not None:
            # detail view
            queryset = Note.objects.filter(pk=pk)
            # obj = get_object_or_404(Note, pk)
            data = NoteSerializer(queryset, many=False).data
            return Response(data)

        else:
            queryset = Note.objects.all()
            data = NoteSerializer(queryset, many=True)
            return Response(data)
        pass
    if method == 'POST':
        serialiser = NoteSerializer(data=request.data)
        if serialiser.is_valid(raise_exception=True):
            instance = serialiser.save()
            return Response(serialiser.data)
        return Response({"message": "invalid data"}, status=400)


class NoteDetailApiView(generics.RetrieveAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


note_detail_view = NoteDetailApiView.as_view()


class NoteUpdateApiView(generics.UpdateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.save()


note_update_view = NoteUpdateApiView.as_view()


class NoteDestroyApiView(generics.DestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        # do something the instance here..
        super().perform_destroy(instance)


note_delete_view = NoteDestroyApiView.as_view()


class NoteCreateApiView(generics.CreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        print(serializer.validated_data)
        title = serializer.validated_data.get('title')
        body = serializer.validated_data.get('body') or None
        if body is None:
            body = title
        serializer.save(body=body)
        # immediately after save, you may decide to send django signal


note_create_view = NoteCreateApiView.as_view()


class NoteListCreateApiView(generics.ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    #authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        print(serializer.validated_data)
        title = serializer.validated_data.get('title')
        body = serializer.validated_data.get('body') or None
        if body is None:
            body = title
        serializer.save(body=body)




note_list_create_view = NoteListCreateApiView.as_view()


class NoteListApiView(generics.ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


note_list_view = NoteListApiView.as_view()

class NoteFilterByTagListApiView(generics.ListAPIView):
    #queryset = Note.objects.all().filter(tags__contains=lookup_field)
    serializer_class = NoteSerializer
    # Note can be view only without authentication
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_url_kwarg = "tag"

    def get_queryset(self):
        uid = self.kwargs.get(self.lookup_url_kwarg)
        notes = Note.objects.filter(tags__contains=uid)
        return notes


note_filter_tags = NoteFilterByTagListApiView.as_view()

