# -*- coding: utf-8 -*-
__author__ = 'alex'
import sys
import logging
import base64

from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render
from django.core.files.base import ContentFile
from django.core.cache import cache

from pythonizame.apps.mixin import LoginRequiredMixin
from pythonizame.apps.global_functions import create_json_response, get_cleaned_uuid
from pythonizame.apps.global_functions import format_sys_errors
from pythonizame.apps.messages_levels import MSG_SUCCESS, MSG_ERROR


# Iniciamos el logger para estas vistas
logger = logging.getLogger(__name__)


class ChangeImageProfile(LoginRequiredMixin, View):
    template_name = 'webservices/change_image_profile.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if 'image_profile' in request.POST:
            type_image_profile = 'image_profile'
        elif 'image_cover_profile' in request.POST:
            type_image_profile = 'image_cover_profile'
        else:
            type_image_profile = None
        if type_image_profile:
            try:
                raw_extension = request.POST[type_image_profile].partition('base64,')[0]  # Obtenemos solamente la extension inicial de los datos
                raw_extension = str(raw_extension).replace(";", "")  # Quitamos la copa del final
                clean_extension = raw_extension.split('/')[1:][0]  # Limpiamos para tener la extension real
                photo = request.POST[type_image_profile].partition('base64,')[2]
                image_data = base64.b64decode(photo)
                if type_image_profile == "image_profile":
                    request.user.userprofile.image.save('%s.%s' % (get_cleaned_uuid(), clean_extension), ContentFile(image_data), save=True)
                    cache_key = 'easy_thumb_alias_cache_%s.%s_%s' % ("user", "avatar", request.user.id)
                    cache.delete(cache_key)  # Eliminamos cache
                else:
                    request.user.userprofile.cover_image.save('%s.%s' % (get_cleaned_uuid(), clean_extension), ContentFile(image_data), save=True)
                    cache_key = 'easy_thumb_alias_cache_%s.%s_%s' % ("user", "cover_image", request.user.id)
                    cache.delete(cache_key)  # Eliminamos cache
                msg_level = MSG_SUCCESS
                mensaje = "Actualizado correctamente"
            except:
                msg_level = MSG_ERROR
                mensaje = format_sys_errors(sys, with_traceback=True)
        else:
            msg_level = MSG_ERROR
            mensaje = "No se recibió ningún tipo de imagen"
        data = create_json_response(message=mensaje, message_level=msg_level)
        return JsonResponse(data, safe=True)


class UsernameValidation(View):

    def post(self, request):
        print(request.POST)
        if 'username' in request.POST:
            try:
                User.objects.get(username=request.POST['username'])
                msg_level = MSG_SUCCESS
                is_available = False
                mensaje = "Nombre de usuario ya ocupado"
            except:
                is_available = True
                msg_level = MSG_SUCCESS
                mensaje = "Nombre de usuario disponible"
        else:
            mensaje = "Error al recibir la información del nombre de usuario"
            is_available = False
            msg_level = MSG_ERROR
        data = create_json_response(message=mensaje, message_level=msg_level, is_available=is_available)
        return JsonResponse(data, safe=True)
