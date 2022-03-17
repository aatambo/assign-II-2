import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views import View
from django.views.generic import CreateView, ListView

from .models import Csv
from .utils import format_results, run_apriori


class CsvCreateView(CreateView):
    """
    creates a form view for posts
    """

    model = Csv
    fields = ["csv", "min_support"]
    template_name = "csv_upload.html"

    def get_success_url(self):
        """redirect to when form is valid"""
        return reverse("csv-detail", kwargs={"pk": self.object.pk})


class CsvListView(ListView):
    """view for products list"""

    model = Csv
    template_name = "csv_list.html"
    context_object_name = "csvs"


class CsvDetailView(View):
    """detail view for products including list and form views for reviews"""

    template_name = "csv_detail.html"

    def get(self, request, pk, *args, **kwargs):
        """handle HTTP GET"""
        csv = get_object_or_404(Csv, pk=pk)
        file = csv.csv
        file = "media/" + str(file)
        file = open(file, "r")
        content = file.read()
        min_sup = csv.min_support

        file_records = []
        for line in content.split("\n"):
            line = line.strip().rstrip(",")  # Remove trailing comma
            record = frozenset(list(map(str.strip, line.split(",")[1:])))
            file_records.append(record)

        start = datetime.datetime.now()
        items = run_apriori(file_records, min_sup)
        end = datetime.datetime.now()
        program_run_time = str((end - start))
        result = format_results(items)
        total_item = len(items)

        context = {
            "csv": csv,
            "items": items,
            "result": result,
            "total_item": total_item,
            "program_run_time": program_run_time,
        }

        return render(request, self.template_name, context)
