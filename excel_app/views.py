from django.shortcuts import render, redirect
from .forms import ExcelFileForm
from django.http import HttpResponse
import pandas as pd

def upload_file(request):
    if request.method == 'POST':
        form = ExcelFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = form.save()
            # Procesar el archivo Excel
            df = pd.read_excel(excel_file.file.path)
            df = df.drop_duplicates(subset=[df.columns[0]])
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=processed_file.xlsx'
            df.to_excel(response, index=False)
            return response
    else:
        form = ExcelFileForm()
    return render(request, 'upload.html', {'form': form})
