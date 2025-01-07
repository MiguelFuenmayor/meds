from peewee import *

db = SqliteDatabase('db/database.db',
    pragmas={'foreign_keys': 1,
             'synchronous': 0},
    )

 # CAMBIAR LOS REGISTROS PARA COINCIDIR CON LOS CAMBIOS
 # ELIMINADO: MED -> UNIDADES_POR_PAQUETE,
 # AGREGADO: MOVIMIENTOS -> UNIDADES POR PAQUETE
class BaseModel(Model):
    class Meta:
        database = db
        legacy_table_names = False


class TipoMed(BaseModel):
    id = AutoField()
    name = CharField()

    class Meta:
        table_name = "tipo_meds"

class User(BaseModel):
    username = CharField()
    password = CharField()

    class Meta:
        table_name = "users"

class Lote(BaseModel):
    id = AutoField()
    name = CharField()

    class Meta:
        table_name = "lotes"


class Med(BaseModel):
    id = AutoField()
    codigo = CharField()
    nombre = CharField()
    tipo_id = ForeignKeyField(TipoMed, related_name="meds")

    class Meta:
        table_name = "meds"


class Movement(BaseModel):
    id = AutoField()
    med_id = ForeignKeyField(Med, related_name="movements")
    paquetes = IntegerField()
    unidades_por_paquete = IntegerField(null=True)
    entrada_salida = BooleanField()  # if true, entrada, if false, salida
    donador_retirador = CharField()
    lote_id = ForeignKeyField(Lote, related_name="meds")
    fecha_entrega = DateField()
    fecha_vencimiento = DateField()
    fecha_creacion = DateField()

    class Meta:
        table_name = "movements"

db.create_tables([Med, Movement, TipoMed, User, Lote])