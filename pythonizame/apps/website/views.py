from django.shortcuts import render_to_response, RequestContext
from django.views.generic import View
from django.contrib.auth.models import User
# Create your views here.


class IndexMainView(View):
    template_name = 'index_main.html'

    def get(self, request):
        from django.utils import timezone
        num_users = User.objects.filter(is_active=True).count()
        ctx = {'num_users': num_users, 'years': timezone.now().year}
        return render_to_response(self.template_name, ctx, RequestContext(request))
