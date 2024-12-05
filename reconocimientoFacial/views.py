from django.shortcuts import render
import face_recognition as fr
import numpy as np
from django.http import JsonResponse
from .models import Personal, RepositorioImagen
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Create your views here.
@csrf_exempt
def registrarPersonal(request):
    if request.method == 'POST':
        v_cod_personal = request.POST.get('v_cod_personal')  # Se asume que el formulario tiene un campo 'v_cod_personal'
        n_num_doc = request.POST.get('n_num_doc')  # Se asume que el formulario tiene un campo 'n_num_doc'
        v_nombre = request.POST.get('v_nombre')  # Se asume que el formulario tiene un campo 'v_nombre'
        v_apellido_paterno = request.POST.get('v_apellido_paterno')  # Se asume que el formulario tiene un campo 'v_apellido_paterno'
        v_apellido_materno = request.POST.get('v_apellido_materno')  # Se asume que el formulario tiene un campo 'v_apellido_materno'
        v_correo_institucional = request.POST.get('v_correo_institucional')  # Se asume que el formulario tiene un campo 'v_correo_institucional'
        n_telefono_contacto = request.POST.get('n_telefono_contacto')  # Se asume que el formulario tiene un campo 'n_telefono_contacto'
        v_disponibilidad = request.POST.get('v_disponibilidad')  # Se asume que el formulario tiene un campo 'v_disponibilidad'
        c_estado = request.POST.get('c_estado')
        imagen_biometrica = request.FILES['imagen_biometrica'] 

        if not v_nombre or not imagen_biometrica:
            return JsonResponse({'mensaje': 'Nombre e imagen son obligatorios'}, status=400)

        imagen = fr.load_image_file(imagen_biometrica)
        encodings = fr.face_encodings(imagen)

        if not encodings:
            return JsonResponse({'mensaje': 'No se detectó ningún rostro en la imagen'}, status=400)
        
        encoding = np.array(encodings[0]).tolist()
        try:
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save(imagen_biometrica.name, imagen_biometrica)
            file_url = fs.url(filename)  # Ruta relativa de la imagen

            # Generar URL pública usando `ngrok`
            ngrok_base_url = 'https://c393-181-176-49-31.ngrok-free.app'
            public_image_url = ngrok_base_url + file_url
        except Exception as e:
            return JsonResponse({'mensaje': f'Error al guardar la imagen: {e}'}, status=500)

        try:
            personal = Personal(
                v_cod_personal=v_cod_personal,
                n_num_doc=n_num_doc,
                v_nombre=v_nombre,
                v_apellido_paterno=v_apellido_paterno,
                v_apellido_materno=v_apellido_materno,
                v_correo_institucional=v_correo_institucional,
                n_telefono_contacto=n_telefono_contacto,
                v_disponibilidad=v_disponibilidad,
                c_estado=c_estado
            )
            personal.save()

            repositorio_imagen = RepositorioImagen(
                imagen_biometrica=public_image_url,  # Guardamos el nombre del archivo o puedes usar el archivo directamente
                personal_n_id_personal=personal  # Relacionamos la imagen con el usuario registrado
            )
            repositorio_imagen.save()  

            return JsonResponse({'mensaje': f'Persona registrada: {v_nombre}'}, status=201)
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