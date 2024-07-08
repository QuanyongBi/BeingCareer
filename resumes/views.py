import logging

from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from utils.chatgptHelper import generate_resume_content
from .models import Resume
from .serializers import ResumeSerializer
import uuid

logger = logging.getLogger(__name__)


# Api endpoints for user related resumes operations
# GET: return a list of resumes for the request user.
# POST: create a new resume input based on input data.
class ResumeApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        resumes = Resume.objects.filter(user=request.user)
        serializer = ResumeSerializer(resumes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # TODO: template_related features not implemented yet.
    def post(self, request):
        data = request.data
        user = request.user
        # template_id = data.get('template_id')
        initial_resume_content = data.get('resume_content')
        if not initial_resume_content:
            return Response({"error": "Invalid data, not containing template_id or resume_json"}, status=status.HTTP_400_BAD_REQUEST)

        generated_resume_content = generate_resume_content(initial_resume_content)
        data['content'] = generated_resume_content
        print(data['content'])
        data['user'] = user.id

        serializer = ResumeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Api endpoints for specific resume operations
# GET: return a specific resume based on the uid
# PUT: update a specific resume based on the uid
# DELETE: delete a specific resume based on the uid
class ResumeDetailApiView(APIView):
    permission_classes = [IsAuthenticated]

    # Helper function to retrieve a certain resume
    # Retrieved resume's user FK must correspond to the current user.
    def get_resume(self, uid, user):
        try:
            return Resume.objects.get(uid=uid, user=user)
        except Resume.DoesNotExist:
            return None

    def get(self, request, uid):
        resume = self.get_resume(uid, request.user)
        if not resume:
            return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ResumeSerializer(resume)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, uid):
        resume = self.get_resume(uid, request.user)
        if not resume:
            return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ResumeSerializer(resume, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uid):
        resume = self.get_resume(uid, request.user)
        if not resume:
            return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)
        resume.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

