import json
import os
from django.conf import settings
from django.http import HttpResponse, Http404
import requests
from django.core import serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from projects.serializers import ProjectDetailSerializer, ProjectListSerializer
from projects.models import Project


class ProjectCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer


class ProjectListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectListSerializer
    queryset = Project.objects.order_by("sorted_index", "pk").all()


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectDetailSerializer
    queryset = Project.objects.all()

    def delete(self, request, *args, **kwargs):
        try:
            r = requests.post(
                settings.URL_JENKINS,
                data=json.dumps({'id': kwargs.get("pk"), "status": "delete"}), verify=False)
            if r.status_code != 200:
                return Response(r.reason, status=r.status_code)
        except requests.ConnectionError as e:
            return Response({"id": kwargs.get("pk"),
                             "info": "проблема с url jenkins: {}".format(e.request.url)}, status=504)
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        url_check_deploy = "http://localhost:8008/api/v1/projects/checkdeploy"
        """
        data = request.data
        project = Project.objects.get(pk=kwargs.get("pk"))
        if data.get('users_list', None):
            if type(data.get('users_list')) == str:
                lst = json.loads(data.get('users_list'))
            else:
                lst = data.get('users_list')
            project.users_list.set(lst)
        if data.get('name', None):
            project.name = data.get("name")
        if data.get('catalog', None):
            project.catalog = data.get("catalog")
        if data.get('description', None):
            project.description = data.get("description")
        if data.get('sorted_index', None):
            project.sorted_index = data.get("sorted_index")
        if data.get('image', None):
            if data.get("image") == "delete":
                project.image.delete()
            elif data.get("image").name[-3:] in ['jpg', 'png']:
                project.image.delete()
                project.image = data.get("image")
            else:
                return Response({"id": kwargs.get("pk"),
                                 "info": "Правильный формат изображения: jpg или png"}, status=415)
        if data.get('model', None):
            if data.get("model").name[-3:] != 'zip':
                return Response({"id": kwargs.get("pk"),
                                 "info": "Неправильный формат файла"}, status=415)
            project.model = data.get("model")
            project.save()
            data = {
                'id': kwargs.get("pk"),
                'url': project.model.path,
                'Authorization': 'Bearer ' + request.auth
            }
            try:
                r = requests.post(
                    settings.URL_JENKINS,
                    data=json.dumps(data), verify=False)
                if r.status_code != 200:
                    project.model.delete()
                    return Response(r.reason, status=r.status_code)
                else:
                    project.status = 1
            except requests.ConnectionError as e:
                project.model.delete()
                return Response({"id": kwargs.get("pk"),
                                 "info": "проблема с url jenkins: {}".format(e.request.url),
                                 "status": 1}, status=504)
        project.save()
        return self.get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = request.data
        project = Project.objects.get(pk=data.get("id"))
        kwargs["pk"] = data.get("id")
        if data.get("status") == "2":
            project.status = 2
            project.save()
            serialized_obj = serializers.serialize('json', [project])
            return Response(json.loads(serialized_obj), status=200)
        if data.get("status") == "3":
            project.status = 3
            project.url = data.get("url")
            project.model.delete()
            project.save()
            serialized_obj = serializers.serialize('json', [project])
            return Response(json.loads(serialized_obj), status=200)
        if data.get("status") == "4":
            project.status = 4
            project.url = data.get("url")
            project.model.delete()
            project.save()
            serialized_obj = serializers.serialize('json', [project])
            return Response(json.loads(serialized_obj), status=200)
        else:
            serialized_obj = serializers.serialize('json', [project])
            return Response(json.loads(serialized_obj), status=200)


def download(request, path):
    file_path = path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
