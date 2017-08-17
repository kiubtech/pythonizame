# -*- coding: utf-8 -*-
__author__ = 'alex'
import uuid
import logging
import traceback

from django.utils.encoding import smart_str

# Iniciamos el logger para estas vistas
logger = logging.getLogger(__name__)


def create_json_response(data=None, message="", message_level='success', url_redirect="", **kwargs):
    """
    Construye la respuesta JSON para que la web pueda reconocer.
    :param data: Información adicional. Ej. Objetos en JSON
    :param message: Mensaje de alerta al usuario
    :param message_level: Opciones: "debug", "info", "success", "warning", "error"
    :param url_redirect:
    :return: Jons data
    """
    body = {'message': {'text': message,
                        'level': str(message_level).lower()},
            'data': data,
            'url_redirect': url_redirect,
    }
    if kwargs:
        for key, value in kwargs.items():
            body[key] = value
    return body


def format_sys_errors(user_sys, with_traceback=False):
    if user_sys:
        etype, value, tb = user_sys.exc_info()
        tipo_error_name = etype.__name__
        error_args = value.args
        if with_traceback:
            mensaje = "{0} {1} {2}".format(tipo_error_name, error_args, traceback.extract_tb(tb))
        else:
            traceback.print_tb(tb)
            mensaje = "{0} {1}".format(tipo_error_name, error_args)
        return mensaje
    else:
        return ""

def form_errors_to_json(form, form_prefix=""):
    if form.errors:
        errors_json = [{"id_field": "id_"+form_prefix+str(k),
                        "name_field": str(k),
                        "error_message": v[0]} for (k, v) in form.errors.items()]
    else:
        errors_json = ""
    return errors_json


def form_errors_to_pupop_msg(form, form_prefix=""):
    """
    Retorna los errores de un formulario de una manera más entendible.
    """
    json_errors = form_errors_to_json(form, form_prefix)
    message_error = ""
    for json_error in json_errors:
        message_error += "%s: %s <br>" % (smart_str(form[json_error['name_field']].label),
                                        smart_str(json_error['error_message']))
    return message_error

def get_cleaned_uuid():
    uuid_ = (str(uuid.uuid1()).replace('-', ''))
    return uuid_
