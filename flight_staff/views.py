from django.shortcuts import render
from django.views import View


class IndexView(View):
    template_name = "flight_staff/index.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        pass
