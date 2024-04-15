import sys

from django.core import management
from django.shortcuts import render


def dump_base(request):

    management.call_command("dumpdata", "-o", "db.json")

    return render(request, 'main/copy.html')

def load_base(request):

    management.call_command("loaddata", "db.json")

    return render(request, 'main/copy.html')