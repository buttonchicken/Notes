from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import *
from .models import *
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.contrib.auth.models import User
from django.utils import timezone

class CreateNote(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        data = request.data
        try:
            note_data = data['note_data']
            note_obj = Note.objects.create(created_by = request.user, note_data=note_data)
            serializer = NoteSerializer(note_obj)
            return Response({"Success":True, "message":"Note created successfully","note":serializer.data},status = status.HTTP_200_OK)
        except:
            return Response({"Success":False, "message":"Note cannot be empty !!"},status=status.HTTP_400_BAD_REQUEST)

class DeleteNote(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def delete(self,request):
        data = request.data
        try:
            note_obj = Note.objects.filter(note_id = data['note_id'])
            if len(note_obj)==0:
                return Response({"Success":False, "message":"Invalid Note ID"},status=status.HTTP_400_BAD_REQUEST)
            elif note_obj[0].created_by != request.user:
                 return Response({"Success":False, "message":"you cannot delete a note you did not create"},status=status.HTTP_400_BAD_REQUEST)
            else:
                note_obj.delete()
                return Response({"Success":True, "message":"Note deleted !!"},status = status.HTTP_200_OK)
        except Exception as e:
            return Response({"Success":False, "message":"Please enter Note ID"},status=status.HTTP_400_BAD_REQUEST)

class EditNote(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self,request,note_id = None):
        try:
            note_obj = Note.objects.get(note_id = note_id)
            if not note_obj:
                print(note_obj)
                return Response({"Success":False, "message":"Invalid Note ID"},status=status.HTTP_400_BAD_REQUEST)
            elif note_obj.created_by != request.user:
                 return Response({"Success":False, "message":"you cannot edit a note you did not create"},status=status.HTTP_400_BAD_REQUEST)
            else:
                if note_obj.note_data == request.data['note_data']:
                    return Response({"Success":False, "message":"Nothing to update"},status=status.HTTP_400_BAD_REQUEST)
                serializer = NoteEditSerializer(note_obj, data = request.data)
                if serializer.is_valid():
                    serializer.save()
                    NoteHistory.objects.create(note = note_obj, updated_at = datetime.datetime.now(), changed_data = request.data['note_data'])
                    return Response({"Success":True, "message":"Note edited successfully !!"},status = status.HTTP_200_OK)
                else:
                    return Response({"Success":False, "message":"Please enter note data"},status=status.HTTP_400_BAD_REQUEST) 
        except Exception:
            return Response({"Success":False, "message":"Invalid Note ID"},status=status.HTTP_400_BAD_REQUEST)

class GetNote(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,note_id=None):
        try:
            note_obj = Note.objects.filter(note_id = note_id, created_by=request.user)
            if len(note_obj)==0:
                return Response({"Success":False, "message":"Invalid Note ID"},status=status.HTTP_400_BAD_REQUEST)
            else:
                data = NoteSerializer(note_obj[0]).data
                created_at = data['created_at']
                dt = datetime.datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%fZ")
                ist_dt = dt + datetime.timedelta(hours=5, minutes=30)
                formatted_dt = ist_dt.strftime("%d %b %Y %H:%M %p")
                data_to_display = {'Data':data['note_data'],'Created At':formatted_dt}
                return Response({"Success":True, "Payload":data_to_display},status = status.HTTP_200_OK)
        except Exception as e:
            return Response({"Success":False, "message":"Invalid Note ID"},status=status.HTTP_400_BAD_REQUEST)

class ShareNotes(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request,note_id=None):
        data = request.data
        try:
            note_obj = Note.objects.filter(note_id = note_id)
            if len(note_obj)==0:
                return Response({"Success":False, "message":"Invalid Note ID"},status=status.HTTP_400_BAD_REQUEST)
            elif note_obj[0].created_by != request.user:
                 return Response({"Success":False, "message":"you cannot edit a note you did not create"},status=status.HTTP_400_BAD_REQUEST)
            else:
                user_obj = User.objects.get(username = data['username'])
                if not user_obj:
                    return Response({"Success":False, "message":"Invalid username"},status=status.HTTP_400_BAD_REQUEST)
                if SharedNote.objects.filter(shared_with = user_obj, note = note_obj[0]).exists():
                    return Response({"Success":False, "message":"Note already shared !"},status=status.HTTP_400_BAD_REQUEST)
                else:
                    SharedNote.objects.create(shared_by = request.user, shared_with = user_obj, note = note_obj[0])
                    return Response({"Success":True, "message":"Note shared successfully !!"},status = status.HTTP_200_OK)
        except Exception as e:
            return Response({"Success":False, "message":"Something went wrong :("},status=status.HTTP_400_BAD_REQUEST)

class GetNoteHistory(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,note_id=None):
        try:
            note_obj = Note.objects.get(note_id = note_id, created_by=request.user)
            if not note_obj:
                return Response({"Success":False, "message":"Invalid Note ID"},status=status.HTTP_400_BAD_REQUEST)
            note_history = NoteHistory.objects.filter(note=note_obj)
            print(note_history)
            note_history_data = NoteHistorySerializer(note_history,many=True).data
            return Response({"Success":True, "version_history":note_history_data},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"Success":False, "message":"Something went wrong :("},status=status.HTTP_400_BAD_REQUEST)