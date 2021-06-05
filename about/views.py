from django.views.generic.base import TemplateView


class AboutMePage(TemplateView):
    template_name = 'about_me.html'


class AboutTechPage(TemplateView):
    template_name = 'about_tech.html'
