from django.shortcuts import render
import face_recognition as fr
import numpy as np
from django.http import JsonResponse
from .models import Persona
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def registrarPersona(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        archivo = request.FILES['imagen']

        if not nombre or not archivo:
            return JsonResponse({'mensaje': 'Nombre e imagen son obligatorios'}, status=400)

        imagen = fr.load_image_file(archivo)
        encodings = fr.face_encodings(imagen)

        if not encodings:
            return JsonResponse({'mensaje': 'No se detectó ningún rostro en la imagen'}, status=400)
        
        try:
            encoding = np.array(encodings[0]).tolist()
            persona = Persona(nombre=nombre, imagen=archivo, encoding=encoding)
            persona.save()
            return JsonResponse({'mensaje': f'Persona registrada: {nombre}'}, status=201)
        except Exception as e:
            return JsonResponse({'error': f'Ocurrio un error inesperado: {e}'}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def reconocerPersona(request):
    if request.method == 'POST':
        archivo = request.FILES['imagen']

        if not archivo:
            return JsonResponse({'mensaje': 'Imagen es obligatoria'}, status=400)
        
        imagenDesconocida = fr.load_image_file(archivo)
        encodingsDesconocido = fr.face_encodings(imagenDesconocida)

        if not encodingsDesconocido:
            return JsonResponse({'mensaje': 'No se detectó ningún rostro en la imagen'}, status=400)
        
        encodingDesconocido = encodingsDesconocido[0]

        try: 
            personas = Persona.objects.all()
            for persona in personas:
                if persona.encoding:
                    encondingRegistrado = np.array(eval(persona.encoding))
                    coincidencia = fr.compare_faces([encondingRegistrado], encodingDesconocido)
                    if coincidencia[0]:
                        return JsonResponse({'mensaje': f'Rostro reconocido: {persona.nombre}'}, status=200)
            
            return JsonResponse({'mensaje': 'Rostro no reconocido'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Ocurrio un error inesperado: {e}'}, status=500)
    
    return JsonResponse({'mensaje': 'Método no permitido'}, status=405)