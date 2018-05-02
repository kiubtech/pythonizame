from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.views.generic import View, DetailView, CreateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django_countries import countries
from django_countries import Countries
from django.template.loader import render_to_string
from .models import JobCategory, Job
from .forms import JobForm
from pythonizame.core.json_settings import json_settings
from pythonizame.apps.security.functions import send_email


settings = json_settings()


class JobbordListView(View):
    template_name = "jobboard_list.html"

    def get_available_countries(self):
        try:
            country_codes = list(set(list(Job.objects.filter(status=1).values_list('country', flat=True))))
        except:
            country_codes = []
        return country_codes

    def get(self, request):
        """
        Devolvemos consulta de publicaciones al usuario
        """
        country_codes = self.get_available_countries()
        kwargs = {'status': 1}
        if 'q' in request.GET and request.GET['q']:
            kwargs['description__icontains'] = request.GET['q']
        partial = request.GET['partial'] if 'partial' in request.GET else None
        full = request.GET['full'] if 'full' in request.GET else None
        if partial != full:
            if partial == "1":
                kwargs['work_schedule'] = 0
            else:
                kwargs['work_schedule'] = 1
        if 'country' in request.GET and request.GET['country'] and request.GET['country'] != "0":
            kwargs['country'] = request.GET['country']
            selected_country = kwargs['country']
        else:
            selected_country = None
        queryset = Job.objects.filter(**kwargs).order_by('-approval_datetime')
        paginator = Paginator(queryset, 5)
        if 'page' in request.GET and request.GET['page']:
            my_page = int(request.GET['page'])
        else:
            my_page = 1
        try:
            object_list = paginator.page(my_page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)
        categories = JobCategory.objects.all()
        ctx = {'object_list': object_list,
               'page_obj': object_list,
               'selected_country': selected_country,
               'available_countries': country_codes,
               'q': request.GET['q'] if 'q' in request.GET else None,
               'full': request.GET['full'] if 'full' in request.GET else None,
               'partial': request.GET['partial'] if 'partial' in request.GET else None,
               'country': request.GET['country'] if 'country' in request.GET else None,
               'categories': categories,
               'countries': countries}
        return render(request, self.template_name, ctx)


class JobbordMyJobsListView(View):
    template_name = "jobboard_my_list.html"

    def get(self, request):
        """
        Devolvemos consulta los jobs de un usuario
        """
        if 'q' in request.GET and request.GET['q']:
            search_words = request.GET['q']
            queryset = Job.objects.filter(created_by=request.user).order_by('-approval_datetime')
        else:
            search_words = ""
            queryset = Job.objects.filter(created_by=request.user).order_by('-approval_datetime')
        paginator = Paginator(queryset, 10)
        if 'page' in request.GET and request.GET['page']:
            my_page = int(request.GET['page'])
        else:
            my_page = 1
        try:
            object_list = paginator.page(my_page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)
        ctx = {'object_list': object_list,
               'page_obj': object_list,
               'queryset': search_words}
        return render(request, self.template_name, ctx)


class JobDetailView(DetailView):
    model = Job
    template_name = 'job_detail.html'

    def get_context_data(self, **kwargs):
        context = super(JobDetailView, self).get_context_data(**kwargs)
        if self.request.user != context['job'].created_by:
            context['job'].num_of_views += 1  # Aumentamos las visitas
            context['job'].save()
        return context


class JobChangeToReviewView(View):

    def get(self, request, job_id):
        job = get_object_or_404(Job, id=job_id, created_by=request.user)
        job.status = 3
        job.save()
        # mandamos un correo para notificar a los administradores que se mandó a revisión un nuevo empleo
        try:
            users = User.objects.filter(is_staff=True)
        except:
            users = None

        for admin in users:
            to_email = admin.email
            contenido = render_to_string("mail/change_status_job_template.html", {'url_server': settings['URL_SERVER'],
                                                                        'username': admin.username,
                                                                        'job': job.title,
                                                                        'status': job.status})
            send_email("Cambio de estatus del empleo", content=contenido, to=to_email, content_type="text/html")

        messages.success(request, _("¡Gracias! Hemos recibido tu solicitud de revisión. Muy pronto "
                                    "te enviaremos una respuesta :D"))
        return HttpResponseRedirect(reverse_lazy('jobboard:my-list'))


class JobAddView(LoginRequiredMixin, View):
    template_name = "job_add.html"
    form = JobForm

    def get(self, request):
        ctx = {'form': self.form}
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            job.save()
            form.save_m2m()
            #mandamos un correo para notificar a los administradores que se agregó un nuevo empleo
            try:
                users = User.objects.filter(is_staff=True)
            except:
                users = None

            for admin in users:
                to_email = admin.email
                contenido = render_to_string("mail/new_job_template.html", {'url_server': settings['URL_SERVER'],
                                                                               'username': admin.username,
                                                                               'job': job.title,
                                                                               'status': job.status})
                send_email("Nuevo registro de empleo", content=contenido, to=to_email, content_type="text/html")

            messages.success(request, _("Guardado correctamente"))

            return HttpResponseRedirect(reverse_lazy('jobboard:my-list'))
        else:
            ctx = {'form': form}
            messages.error(request, _("Verifique la información enviada"))
            return render(request, self.template_name, ctx)


class JobEditView(LoginRequiredMixin, View):
    template_name = "job_edit.html"
    form = JobForm

    def get(self, request, job_id):
        job = get_object_or_404(Job, id=job_id, created_by=request.user)
        form = self.form(instance=job)
        ctx = {'form': form, 'job': job}
        return render(request, self.template_name, ctx)

    def post(self, request, job_id):
        job = get_object_or_404(Job, id=job_id, created_by=request.user)
        form = self.form(request.POST, instance=job)
        if form.is_valid():
            job = form.save(commit=False)
            job.save()
            form.save_m2m()
            messages.success(request, _("Guardado correctamente"))
            return HttpResponseRedirect(reverse_lazy('jobboard:my-list'))
        else:
            ctx = {'form': form}
            messages.error(request, _("Verifique la información enviada"))
            return render(request, self.template_name, ctx)


class JobDeleteView(LoginRequiredMixin, View):

    def get(self, request, job_id):
        job = get_object_or_404(Job, id=job_id, created_by=request.user)
        job.delete()
        messages.success(request, _("Eliminado correctamente"))
        return HttpResponseRedirect(reverse_lazy('jobboard:my-list'))
