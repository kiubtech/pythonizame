# -*- coding: utf-8 -*-
__author__ = 'alex'
import sys
import logging

from django.views.generic import View
from django.http import JsonResponse
from django.shortcuts import render
from django.db import IntegrityError

from pythonizame.apps.mixin import LoginRequiredMixin
from pythonizame.apps.blog.forms import LikeForm, FavoriteForm
from pythonizame.apps.blog.models import LikePost, FavoritePost
from pythonizame.apps.global_functions import create_json_response
from pythonizame.apps.messages_levels import MSG_SUCCESS, MSG_ERROR
from pythonizame.apps.global_functions import format_sys_errors


# Iniciamos el logger para estas vistas
logger = logging.getLogger(__name__)


class AddPostLike(LoginRequiredMixin, View):
    template_name = 'webservices/add_post_like.html'

    def get(self, request):
        form = LikeForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    @staticmethod
    def post(request):
        form = LikeForm(request.POST)
        is_like = False
        if form.is_valid():
            try:
                new_like = form.save(commit=False)
                new_like.created_by = request.user
                new_like.save()
                mensaje = "Like generado correctamente"
                msg_level = MSG_SUCCESS
                is_like = True
            except IntegrityError:
                try:
                    my_like = LikePost.objects.get(post=form.cleaned_data['post'], created_by=request.user)
                    my_like.delete()
                    mensaje = "Se ha eliminado tu like"
                    msg_level = MSG_SUCCESS
                except LikePost.DoesNotExist:
                    msg_level = MSG_ERROR
                    mensaje = "Error al intentar eliminar el like"
            except:
                msg_level = MSG_ERROR
                mensaje = format_sys_errors(sys, with_traceback=True)
        else:
            mensaje = "Error en los datos recibidos"
            msg_level = MSG_ERROR
        try:
            num_likes = LikePost.objects.filter(post__id=request.POST['post']).count()
        except:
            num_likes = 0
        data = create_json_response(message=mensaje, message_level=msg_level, is_like=is_like, num_likes=num_likes)
        return JsonResponse(data, safe=True)


class AddPostFavorite(LoginRequiredMixin, View):
    template_name = 'webservices/add_post_like.html'

    def get(self, request):
        form = FavoriteForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    @staticmethod
    def post(request):
        form = FavoriteForm(request.POST)
        is_favorite = False
        if form.is_valid():
            try:
                new_fav = form.save(commit=False)
                new_fav.created_by = request.user
                new_fav.save()
                mensaje = "Favorito generado correctamente"
                msg_level = MSG_SUCCESS
                is_favorite = True
            except IntegrityError:
                try:
                    new_fav = FavoritePost.objects.get(post=form.cleaned_data['post'], created_by=request.user)
                    new_fav.delete()
                    mensaje = "Se ha eliminado de tus favoritos"
                    msg_level = MSG_SUCCESS
                except LikePost.DoesNotExist:
                    msg_level = MSG_ERROR
                    mensaje = "Error al intentar eliminar de tus favoritos"
            except:
                msg_level = MSG_ERROR
                mensaje = format_sys_errors(sys, with_traceback=True)
        else:
            mensaje = "Error en los datos recibidos"
            msg_level = MSG_ERROR
        data = create_json_response(message=mensaje, message_level=msg_level, is_favorite=is_favorite)
        return JsonResponse(data, safe=True)
