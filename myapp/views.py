import pandas as pd
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import Upload
import json

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Leer el archivo excel y convertirlo en DataFrame
            file = request.FILES['file']
            df = pd.read_excel(file, sheet_name=0)

            # Convertir el DataFrame a formato JSON
            file_value = df.to_json(orient='records')

            # Crear y guardar el objeto Upload con los datos del formulario y el valor del archivo
            upload = Upload(
                usuario=form.cleaned_data['usuario'],
                fecha=form.cleaned_data['fecha'],
                laboratorio=form.cleaned_data['laboratorio'],
                cuit=form.cleaned_data['cuit'],
                file=file_value
            )
            upload.save()

            # Redireccionar a la lista de archivos después de guardar exitosamente
            return redirect('file_list')
    else:
        form = UploadFileForm()
    return render(request, 'upload_form.html', {'form': form})

def file_list(request):
    uploads = Upload.objects.all()
    return render(request, 'file_list.html', {'uploads': uploads})

def file_detail(request, pk):
    upload = Upload.objects.get(pk=pk)
    
    # Convertir el JSON almacenado en el campo 'file' de Upload de vuelta a DataFrame
    df = pd.DataFrame(json.loads(upload.file))
    
    # Convertir las columnas relevantes a enteros sin decimales
    integer_columns = ['Cantidad', 'Imp. Total', 'Costo']
    for col in integer_columns:
        if col in df.columns:
            df[col] = df[col].astype(int)

    # Calcular las sumas
    total_cantidad = df['Cantidad'].sum()
    total_imp_total = df['Imp. Total'].sum()
    total_costo = df['Costo'].sum()
    
    return render(request, 'file_detail.html', {
        'upload': upload,
        'dataframe': df,
        'total_cantidad': total_cantidad,
        'total_imp_total': total_imp_total,
        'total_costo': total_costo
    })
