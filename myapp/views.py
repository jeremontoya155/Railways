import pandas as pd
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import Upload
import json

from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import Upload
import pandas as pd
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
    return render(request, 'upload.html', {'form': form})



def file_list(request):
    uploads = Upload.objects.all()
    return render(request, 'file_list.html', {'uploads': uploads})

def file_detail(request, pk):
    upload = Upload.objects.get(pk=pk)
    
    # Convertir el JSON almacenado en el campo 'file' de Upload de vuelta a DataFrame
    df = pd.DataFrame(json.loads(upload.file))
    
    # Calcular las sumas, comprobando si las columnas existen
    total_cantidad = df['Cantidad'].sum() if 'Cantidad' in df.columns else 0
    total_imp_total = df['Imp. Total'].sum() if 'Imp. Total' in df.columns else 0
    total_costo = df['Costo'].sum() if 'Costo' in df.columns else 0
    
    return render(request, 'file_detail.html', {
        'upload': upload,
        'dataframe': df,
        'total_cantidad': total_cantidad,
        'total_imp_total': total_imp_total,
        'total_costo': total_costo
    })
