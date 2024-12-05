from django.db import models

class Personal(models.Model):
    n_id_personal = models.BigIntegerField(primary_key=True)
    v_cod_personal = models.CharField(max_length=7, blank=True, null=True)
    v_nombre = models.CharField(max_length=55, blank=True, null=True)
    v_apellido_paterno = models.CharField(max_length=55, blank=True, null=True)
    v_apellido_materno = models.CharField(max_length=55, blank=True, null=True)
    v_correo_institucional = models.CharField(max_length=80, blank=True, null=True)
    n_telefono_contacto = models.BigIntegerField(blank=True, null=True)
    n_num_doc = models.BigIntegerField(blank=True, null=True)
    v_disponibilidad = models.CharField(max_length=15, blank=True, null=True)
    c_estado = models.CharField(max_length=1, default=1)

    class Meta:
        managed = False
        db_table = 'personal'

class Asistencia(models.Model):
    n_id_asistencia = models.BigIntegerField(primary_key=True)
    t_hora_inicio = models.DateTimeField(blank=True, null=True)
    t_hora_fin = models.DateTimeField(blank=True, null=True)
    c_estado = models.CharField(max_length=1, blank=True, null=True)
    d_fecha = models.DateField(blank=True, null=True)
    personal_n_id_personal = models.ForeignKey('Personal', models.DO_NOTHING, db_column='personal_n_id_personal')


class Dependencia(models.Model):
    n_id_dependencia = models.BigIntegerField(primary_key=True)
    v_descripcion = models.CharField(max_length=70, blank=True, null=True)
    v_abreviatura = models.CharField(max_length=70, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dependencia'


class EspacioAula(models.Model):
    n_id_espacio_aula = models.BigIntegerField(primary_key=True)
    n_capacidad = models.BigIntegerField(blank=True, null=True)
    dependencia_n_id_dependencia = models.ForeignKey(Dependencia, models.DO_NOTHING, db_column='dependencia_n_id_dependencia')

    class Meta:
        managed = False
        db_table = 'espacio_aula'


class EspacioAulaPersonal(models.Model):
    n_id_aula_personal = models.BigIntegerField(primary_key=True)
    personal_n_id_personal = models.ForeignKey('Personal', models.DO_NOTHING, db_column='personal_n_id_personal')
    espacio_aula_n_id_espacio_aula = models.ForeignKey(EspacioAula, models.DO_NOTHING, db_column='espacio_aula_n_id_espacio_aula')

    class Meta:
        managed = False
        db_table = 'espacio_aula_personal'


class EspacioTurno(models.Model):
    n_id_espacio_turno = models.BigIntegerField(primary_key=True)
    espacio_aula_n_id_espacio_aula = models.ForeignKey(EspacioAula, models.DO_NOTHING, db_column='espacio_aula_n_id_espacio_aula')
    turno_n_id_turno = models.ForeignKey('Turno', models.DO_NOTHING, db_column='turno_n_id_turno')

    class Meta:
        managed = False
        db_table = 'espacio_turno'


class Evento(models.Model):
    n_id_evento = models.BigIntegerField(primary_key=True)
    v_cod_evento = models.CharField(max_length=7, blank=True, null=True)
    v_nombre = models.CharField(max_length=90, blank=True, null=True)
    d_fecha_inicio = models.DateField(blank=True, null=True)
    d_fecha_fin = models.DateField(blank=True, null=True)
    c_estado = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'evento'


class LogReconocimiento(models.Model):
    n_id_log_reconocimiento = models.BigIntegerField(primary_key=True)
    v_evento = models.CharField(max_length=55, blank=True, null=True)
    v_tabla = models.CharField(max_length=55, blank=True, null=True)
    cl_row_data = models.TextField(blank=True, null=True)
    d_fec_registro = models.DateField(blank=True, null=True)
    d_fec_actividad = models.DateField(blank=True, null=True)
    v_ip_usuario = models.CharField(max_length=55, blank=True, null=True)
    personal_n_id_personal = models.ForeignKey('Personal', models.DO_NOTHING, db_column='personal_n_id_personal', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log_reconocimiento'


class Reporte(models.Model):
    n_id_reporte = models.BigIntegerField(primary_key=True)
    v_tipo_reporte = models.CharField(max_length=70, blank=True, null=True)
    d_fecha_generacion = models.DateTimeField(blank=True, null=True)
    evento_n_id_evento = models.ForeignKey(Evento, models.DO_NOTHING, db_column='evento_n_id_evento')

    class Meta:
        managed = False
        db_table = 'reporte'


class RepositorioImagen(models.Model):
    n_id_rep_imagen = models.BigIntegerField(primary_key=True)
    imagen_biometrica = models.ImageField(upload_to='personal/')
    personal_n_id_personal = models.ForeignKey(Personal, models.DO_NOTHING, db_column='personal_n_id_personal')

    class Meta:
        managed = False
        db_table = 'repositorio_imagen'


class TipoPersonal(models.Model):
    n_id_tipo_personal = models.BigIntegerField(primary_key=True)
    v_descripcion = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipo_personal'


class Turno(models.Model):
    n_id_turno = models.BigIntegerField(primary_key=True)
    t_hora_inicio = models.DateTimeField(blank=True, null=True)
    t_hora_fin = models.DateTimeField(blank=True, null=True)
    d_fecha = models.DateField(blank=True, null=True)
    c_estado = models.CharField(max_length=1, blank=True, null=True)
    evento_n_id_evento = models.ForeignKey(Evento, models.DO_NOTHING, db_column='evento_n_id_evento')

    class Meta:
        managed = False
        db_table = 'turno'


# Create your models here.
class Persona(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    imagen = models.ImageField(upload_to='personas/')
    encoding = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.nombre