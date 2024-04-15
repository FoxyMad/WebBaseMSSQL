from django.contrib.auth.decorators import login_required
from django.db.models import Q
from reportlab.lib.enums import TA_RIGHT, TA_JUSTIFY
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse, FileResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
from .models import technique, types_directory, countries_directory
from docxtpl import DocxTemplate

@login_required
def index(request):
    return render(request, 'main/index.html')
@login_required
def directory(request):

        return render(request, 'main/directory.html')
@login_required
def directory2(request):

    types = types_directory.objects.all()
    return render(request, 'main/directory.html', {"types": types})
@login_required
def directory1(request):
    countries = countries_directory.objects.all()

    return render(request, 'main/directory.html', {"countries": countries})

def premain(request):
    return render(request, 'main/login.html')

@login_required
def copy(request):
    return render(request, 'main/copy.html')

@login_required
def requests(request):
    computers3 = technique.objects.all()
    return render(request, 'main/requests.html', {"computers3": computers3})

@login_required
def tables(request):
    return render(request, 'main/tables.html', )

@login_required
def search(request):

    if request.method == "POST":
            searched = request.POST['searched']
            rec = technique.objects.filter(
                Q(name__icontains=searched) |
                Q(type__icontains=searched) |
                Q(inventory_number=searched))
            return render(request, 'main/search.html', {'searched': searched, 'rec': rec})
    else:
            return render(request, 'main/search.html')
@login_required
def add_object(request):
    computers = technique.objects.all()
    return render(request, 'main/add_object.html', {"computers": computers})

@login_required
def tmplt(request):
    if request.method == "POST":
        computers2 = technique()
        computers2.type = request.POST.get("type")
        computers2.name = request.POST.get("name")
        computers2.amount = request.POST.get("amount")
        computers2.date_of_manufacture = request.POST.get("date_of_manufacture")
        computers2.inventory_number = request.POST.get("inventory_number")
        computers2.manufacture_number = request.POST.get("manufacture_number")
        computers2.residual_value = request.POST.get("residual_value")
        computers2.date_of_purchase = request.POST.get("date_of_purchase")
        computers2.contract_number = request.POST.get("contract_number")
        computers2.country_of_manufacture = request.POST.get("country_of_manufacture")

        return HttpResponseRedirect("/requests")

@login_required
def create(request):
    if request.method == "POST":
        computers1 = technique()
        computers1.type = request.POST.get("type")
        computers1.name = request.POST.get("name")
        computers1.amount = request.POST.get("amount")
        computers1.date_of_manufacture = request.POST.get("date_of_manufacture")
        computers1.inventory_number = request.POST.get("inventory_number")
        computers1.manufacture_number = request.POST.get("manufacture_number")
        computers1.residual_value = request.POST.get("residual_value")
        computers1.date_of_purchase = request.POST.get("date_of_purchase")
        computers1.contract_number = request.POST.get("contract_number")
        computers1.country_of_manufacture = request.POST.get("country_of_manufacture")
        computers1.save()

        doc = DocxTemplate("form_act_priem-peredacha.docx")

        data = {'contract_number': computers1.contract_number,
                'date_of_purchase': computers1.date_of_purchase,
                'id': '1',
                'name': computers1.name,
                'manufacture_number': computers1.manufacture_number,
                'amount': computers1.amount,
                'residual_value': computers1.residual_value}

        response = HttpResponse(content_type="aplication/vnd.openxmlformats-officedocument.wordprocessingml.document")
        response["Content-Disposition"] = 'filename = "Document.docx"'

        doc.render(data)

        doc.save(response)

        return response

    return HttpResponseRedirect("/add_object")

@login_required
def edit(request, id):
    try:
        computers1 = technique.objects.get(id=id)

        if request.method == "POST":
            computers1.name = request.POST.get("name")
            computers1.type = request.POST.get("type")
            computers1.amount = request.POST.get("amount")
            computers1.date_of_manufacture = request.POST.get("date_of_manufacture")
            computers1.inventory_number = request.POST.get("inventory_number")
            computers1.manufacture_number = request.POST.get("manufacture_number")
            computers1.residual_value = request.POST.get("residual_value")
            computers1.date_of_purchase = request.POST.get("date_of_purchase")
            computers1.contract_number = request.POST.get("contract_number")
            computers1.country_of_manufacture = request.POST.get("country_of_manufacture")
            computers1.save()
            return HttpResponseRedirect("/add_object")
        else:
            return render(request, "main/edit.html", {"computers1": computers1})
    except technique.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2")

@login_required
def delete(request, id):
    try:
        computers1 = technique.objects.get(id=id)
        computers1.delete()
        return HttpResponseRedirect("/add_object")
    except technique.DoesNotExist:
        return HttpResponseNotFound("<h2>Object not found</h2>")

@login_required
def print_users(request):

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer,
                                rightMargin=32,
                                leftMargin=32,
                                topMargin=72,
                                bottomMargin=72,
                                pagesize=landscape(letter))
        styles = getSampleStyleSheet()

        elements = []
        pdfmetrics.registerFont(TTFont('DejaVuSerif', 'DejaVuSerif.ttf', 'UTF-8'))
        styles.add(ParagraphStyle(name='ParagraphStyleName', alignment=TA_JUSTIFY, fontName='DejaVuSerif', textwrap=True))
        styles.add(ParagraphStyle(name='TitleStyle', alignment=TA_RIGHT, fontName='DejaVuSerif', fontSize=14, spaceAfter=10))

        computers = technique.objects.all()

        table_title = 'Отчет по таблице "Основые средства"'

        table_names = [[Paragraph('Тип объекта', styles['ParagraphStyleName']),
                        Paragraph('Наименов.', styles['ParagraphStyleName']),
                        Paragraph('Кол-во', styles['ParagraphStyleName']),
                        Paragraph('Инвент. номер', styles['ParagraphStyleName']),
                        Paragraph('Заводской номер', styles['ParagraphStyleName']),
                        Paragraph('Остаточн. стоимость', styles['ParagraphStyleName']),
                        Paragraph('Дата произв.', styles['ParagraphStyleName']),
                        Paragraph('Дата передачи', styles['ParagraphStyleName']),
                        Paragraph('Номер договора', styles['ParagraphStyleName']),
                        Paragraph('Страна произв.', styles['ParagraphStyleName'])]]

        table_data = []
        for i, computer in enumerate(computers):

            table_data.append([computer.type, computer.name, computer.amount, computer.inventory_number,
                               computer.manufacture_number, computer.residual_value,
                               computer.date_of_manufacture, computer.date_of_purchase,
                               computer.contract_number, computer.country_of_manufacture])

            computer_title = Paragraph(table_title, styles['TitleStyle'])
            computer_table1 = Table(table_names, repeatRows=1, colWidths=70)
            computer_table = Table(table_data, colWidths=70)


            computer_table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                                                ('FONT', (0, 0), (-1, -1), 'DejaVuSerif', 8)]))
            computer_table1.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, 0), 0.25, colors.black),
                                                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                                                ('FONT', (0, 0), (-1, -1), 'DejaVuSerif', 8)]))
            elements.append(computer_title)
            elements.append(computer_table1)
            elements.append(computer_table)
            doc.build(elements)

            pdf = buffer.getvalue()
            buffer.seek(0)

        return FileResponse(buffer, as_attachment=True, filename='Doc.pdf')




