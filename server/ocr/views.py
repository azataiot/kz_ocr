from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from django.views import View
import sys

sys.path.append('../../models/') #inside server

from ocr import *


class OcrView(View):
    def post(self, request, format=None):
        file_obj = request.FILES.get('file', None)
        if file_obj:
            transcript = transcript(file_obj)
            return JsonResponse({'transcript': transcript}, status=200)
        return JsonResponse({}, status=204)