# views.py

import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .forms import UploadFileForm
from .models import Upload
import json
import os
from datetime import datetime, timedelta

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Leer el archivo excel y convertirlo en DataFrame
            file = request.FILES['file']
            try:
                df = pd.read_excel(file, sheet_name=0)
            except Exception as e:
                form.add_error('file', f'Error al leer el archivo: {e}')
            else:
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
    upload = get_object_or_404(Upload, pk=pk)
    
    # Convertir el JSON almacenado en el campo 'file' de Upload de vuelta a DataFrame
    df = pd.DataFrame(json.loads(upload.file))
    
    # Asegurarse de que la columna IdQuantio existe
    if 'IdQuantio' not in df.columns:
        return render(request, 'file_detail.html', {
            'error': 'El archivo cargado no contiene una columna IdQuantio.'
        })
    
    # Convertir las columnas relevantes a enteros sin decimales
    integer_columns = ['Cantidad', 'Imp. Total', 'Costo']
    for col in integer_columns:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].astype(int)

    # Calcular las sumas
    total_cantidad = df['Cantidad'].sum() if 'Cantidad' in df.columns else 0
    total_imp_total = df['Imp. Total'].sum() if 'Imp. Total' in df.columns else 0
    total_costo = df['Costo'].sum() if 'Costo' in df.columns else 0

    # Cargar datos desde base.json
    base_path = os.path.join(settings.STATIC_ROOT, 'base.json')
    with open(base_path, 'r') as f:
        base_data = json.load(f)
    base_df = pd.DataFrame(base_data)

    # Asegurarse de que la columna SKU existe en base_df
    if 'SKU' not in base_df.columns:
        return render(request, 'file_detail.html', {
            'error': 'El archivo base.json no contiene una columna SKU.'
        })

    # Renombrar la columna SKU a IdQuantio en base_df para el cruce
    base_df.rename(columns={'SKU': 'IdQuantio'}, inplace=True)

    # Filtrar los registros de los últimos 10 días
    today = datetime.now()
    ten_days_ago = today - timedelta(days=10)
    base_df['Fecha'] = pd.to_datetime(base_df['Fecha'])
    recent_base_df = base_df

    # Calcular la completitud para cada IdQuantio en df
    completitud = {}
    for id_quantio in df['IdQuantio']:
        df_cantidad = df[df['IdQuantio'] == id_quantio]['Cantidad'].sum()
        if 'IdQuantio' in recent_base_df.columns:
            recent_cantidad = recent_base_df[recent_base_df['IdQuantio'] == id_quantio]['Cantidad'].sum()
        else:
            recent_cantidad = 0
        
        if df_cantidad > 0:
            completitud[id_quantio] = (recent_cantidad / df_cantidad) * 100
        else:
            completitud[id_quantio] = 0

    # Agregar la columna de completitud a df
    df['Completitud'] = df['IdQuantio'].map(completitud).round(2).astype(str) + '%'

    return render(request, 'file_detail.html', {
        'upload': upload,
        'dataframe': df,
        'total_cantidad': total_cantidad,
        'total_imp_total': total_imp_total,
        'total_costo': total_costo
    })
