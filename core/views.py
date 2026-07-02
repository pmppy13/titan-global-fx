from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'index.html'

class AboutView(TemplateView):
    template_name = 'about.html'

class ContactView(TemplateView):
    template_name = 'contact.html'

class PlatformsView(TemplateView):
    template_name = 'platforms.html'

class MarketsView(TemplateView):
    template_name = 'markets.html'

class PlansView(TemplateView):
    template_name = 'plans.html'