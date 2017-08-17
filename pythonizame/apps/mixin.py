# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):
    """
    Este mixin impide que entren a las vistas sin logear
    anteponiendo en nombre del mixin asi
    class AdminList(LoginRequiredMixin, ListView):
    """
    @method_decorator(login_required(login_url="/security/login/"))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
