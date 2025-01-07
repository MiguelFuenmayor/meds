from peewee import fn, JOIN

from database import Med, Movement, TipoMed, User, Lote


def get_movements():
    return (Movement.select(
        Movement.id,
        Med.id,
        Med.codigo,
        Med.nombre,
        Movement.unidades_por_paquete,
        Lote.name.alias('lote'),
        Movement.paquetes,
        Movement.donador_retirador,
        Movement.entrada_salida,
        TipoMed.name.alias('tipo'),
        Movement.fecha_creacion,
        Movement.fecha_vencimiento,
        Movement.fecha_entrega
    )
        .join_from(Movement, Med)
        .join_from(Med, TipoMed)
        .join_from(Movement, Lote)
        .order_by(Movement.id.desc())
        .dicts()
            )

def get_movements_by_id(id):
    data = (Movement.select(
        Movement.id,
        Med.id.alias('med_id'),
        Med.codigo,
        Med.nombre,
        Movement.unidades_por_paquete,
        Lote.id.alias('lote_id'),
        Lote.name.alias('lote'),
        Movement.paquetes,
        Movement.donador_retirador,
        Movement.entrada_salida,
        TipoMed.name.alias('tipo'),
        Movement.fecha_creacion,
        Movement.fecha_vencimiento,
        Movement.fecha_entrega
    )
            .join_from(Movement, Med)
            .join_from(Med, TipoMed)
            .join_from(Movement, Lote)
            .where(Movement.id == id)
    .limit(1)
            .dicts()
            )
    rows = []
    for dat in data:
        rows.append(dat)
    return rows[0]
def get_report_data(date_from, date_to, tipo):
    if tipo == 'TODOS':
        data = (Movement.select(
            Movement.id,
            Med.id,
            Med.codigo,
            Med.nombre,
            Movement.unidades_por_paquete,
            Lote.name.alias('lote'),
            Movement.paquetes,
            Movement.donador_retirador,
            Movement.entrada_salida,
            TipoMed.name.alias('tipo'),
            Movement.fecha_creacion,
            Movement.fecha_vencimiento,
            Movement.fecha_entrega
        )
                .join_from(Movement, Med)
                .join_from(Med, TipoMed)
                .join_from(Movement, Lote)
                .order_by(Movement.id.desc())
                .where((Movement.fecha_entrega >= date_from) & (Movement.fecha_entrega <= date_to))
                .dicts()

                )
    elif tipo == 'SOLO ENTRADAS':
        data = (Movement.select(
            Movement.id,
            Med.id,
            Med.codigo,
            Med.nombre,
            Movement.unidades_por_paquete,
            Lote.name.alias('lote'),
            Movement.paquetes,
            Movement.donador_retirador,
            Movement.entrada_salida,
            TipoMed.name.alias('tipo'),
            Movement.fecha_creacion,
            Movement.fecha_vencimiento,
            Movement.fecha_entrega
        )
                .join_from(Movement, Med)
                .join_from(Med, TipoMed)
                .join_from(Movement, Lote)
                .order_by(Movement.id.desc())
                .where((Movement.fecha_entrega >= date_from) &
                       (Movement.fecha_entrega <= date_to) &
                       (Movement.entrada_salida == True))
                .dicts()

                )

    elif tipo == 'SOLO SALIDAS':
        data = (Movement.select(
            Movement.id,
            Med.id,
            Med.codigo,
            Med.nombre,
            Movement.unidades_por_paquete,
            Lote.name.alias('lote'),
            Movement.paquetes,
            Movement.donador_retirador,
            Movement.entrada_salida,
            TipoMed.name.alias('tipo'),
            Movement.fecha_creacion,
            Movement.fecha_vencimiento,
            Movement.fecha_entrega
        )
                .join_from(Movement, Med)
                .join_from(Med, TipoMed)
                .join_from(Movement, Lote)
                .order_by(Movement.id.desc())
                .where(
                        (Movement.fecha_entrega >= date_from) &
                        (Movement.fecha_entrega <= date_to) &
                        (Movement.entrada_salida == False)
                       )
                .dicts()
                )
    rows = []
    for dat in data:
        rows.append(dat)
    return rows

def earliest_date():
    data = Movement.select(Movement.fecha_entrega).order_by(Movement.id.asc()).limit(1).dicts()
    row = None
    for dat in data:
        row = dat
    return row


def latest_date():
    data = Movement.select(Movement.fecha_entrega).order_by(Movement.id.desc()).limit(1).dicts()
    row = None
    for dat in data:
        row = dat
    return row

def create_med(codigo, nombre, tipo):
    return Med.create(
        codigo=codigo,
        nombre=nombre,
        tipo_id=tipo
    )

def update_med(id, codigo, nombre, tipo_id):
     return Med.update(
        codigo=codigo,
        nombre=nombre,
        tipo_id=tipo_id
    ).where(Med.id == id).execute()


def delete_med(id):
    return Med.delete().where(Med.id == id).execute()

def get_all_med_movements(med_id):
    data = Movement.select(
        Movement.id
    ).where(Movement.med_id == med_id).dicts()
    row = []
    for dat in data:
        row.append(dat)
    return row

def get_meds():
    return (Med.select(
        Med.id,
        Med.codigo,
        Med.nombre,
        Movement.unidades_por_paquete,
        TipoMed.name.alias('tipo'),
        fn.Sum(Movement.paquetes).alias('paquetes')
    ).join_from(Med, TipoMed, JOIN.LEFT_OUTER)
        .join_from(Med, Movement, JOIN.LEFT_OUTER)
        .group_by(Med.id)
        .order_by(Med.id.desc())
            .dicts())

def get_med(id):
    data = (Med.select(
        Med.id,
        Med.codigo,
        Med.nombre,
        TipoMed.name.alias('tipo'),
    ).join_from(Med, TipoMed, JOIN.LEFT_OUTER)
            .where(Med.id == id).dicts())
    row = None
    for d in data:
        row = d
    return row
def get_tipo_meds():
    return TipoMed.select().dicts()

def update_tipo_med(id, name):
    return TipoMed.update(name=name).where(TipoMed.id == id).execute()


def delete_tipo_med(id):
    return TipoMed.delete().where(TipoMed.id == id).execute()


def create_tipo_med(name):
    return TipoMed.create(name=name)


def no_def_lote():
    lote_id, result = Lote.get_or_create(name="No Definido")
    print(lote_id)
    return lote_id.id

def create_movement(med_id, paquetes,
                    donador_retirador, entrada_salida,
                    fecha_entrega, fecha_vencimiento, fecha_creacion,
                    lote_id,
                    unidades_por_paquete):
    return Movement.create(
        med_id=med_id,
        paquetes=paquetes,
        donador_retirador=donador_retirador,
        entrada_salida=entrada_salida,
        fecha_entrega=fecha_entrega,
        fecha_vencimiento=fecha_vencimiento,
        fecha_creacion=fecha_creacion,
        lote_id=lote_id,
        unidades_por_paquete=unidades_por_paquete
    )

def check_lote(name):
    data = Lote.get_or_create(name=name)
    result = []
    for d in data:
        result.append(d)
    return result[0]


def create_lote(name):
    return Lote.create(name=name)


def get_lotes():
    return Lote.select(Lote.id, Lote.name).dicts()


def update_lote(id, name):
    return Lote.update(name=name).where(Lote.id == id).execute()


def update_movement(id, med_id,
                    paquetes, donador_retirador,
                    entrada_salida, fecha_entrega,
                    fecha_vencimiento, fecha_creacion,
                    lote_id, unidades_por_paquete):
    return Movement.update(
        med_id=med_id,
        paquetes=paquetes,
        donador_retirador=donador_retirador,
        entrada_salida=entrada_salida,
        unidades_por_paquete=unidades_por_paquete,
        fecha_entrega=fecha_entrega,
        fecha_vencimiento=fecha_vencimiento,
        fecha_creacion=fecha_creacion,
        lote_id=lote_id
    ).where(Movement.id == id).execute()

def delete_movement(id):
    return Movement.delete().where(Movement.id == id).execute()


def login(username, password):
    return User.select().where(User.username == username, User.password == password).dicts()

def search_totales(data):
    print(data)
    # solve this
    data = Movement.raw(
       " SELECT med.id, med.codigo, "
         "   med.nombre, "
       "     t.name AS 'tipo', "
         "   m.unidades_por_paquete AS 'unidades', "
          "  m.entrada_salida, "
           " m.paquetes AS 'paquetes' "
   " FROM movements m "
    "JOIN meds med ON med.id = m.med_id "
    "LEFT OUTER JOIN tipo_meds t ON t.id = med.tipo_id "
    f" WHERE (med.nombre LIKE '%{data}%') OR (med.codigo LIKE '%{data}%') OR (t.name LIKE '%{data}%') "
    ).dicts()
    rows = []
    for dat in data:
        rows.append(dat)
    print(rows)
    return rows

def get_totales_types():
    data = (Movement.select(TipoMed.id,
                            Med.codigo,
                            TipoMed.name,
                            fn.Count(Med.codigo.distinct()).alias('meds'),
                            Movement.entrada_salida,
                            fn.Sum(Movement.paquetes).alias('paquetes')
                            )
            .join_from(Movement, Med, JOIN.LEFT_OUTER)
            .join_from(Med, TipoMed, JOIN.LEFT_OUTER)
            .group_by(Movement.entrada_salida, TipoMed.id)
            .dicts())

    rows = []
    for dat in data:
        rows.append(dat)
    return rows


def get_totales():
    data = Movement.raw("""
    SELECT med.id, med.codigo, 
            med.nombre, 
            t.name AS 'tipo', 
            m.unidades_por_paquete AS 'unidades', 
            m.entrada_salida, 
            m.paquetes AS 'paquetes'
    FROM movements m
    JOIN meds med ON med.id = m.med_id
    LEFT OUTER JOIN tipo_meds t ON t.id = med.tipo_id
    """).dicts()
    rows = []
    for dat in data:
        rows.append(dat)
    print(rows)
    return rows

def get_full_med(med_code):
    data = Movement.raw(
    "SELECT med.id, med.codigo, "
        "med.nombre, "
        "t.name AS 'tipo', "
        "t.id AS 'tipo_id', "
        "m.unidades_por_paquete AS 'unidades', "
        "m.entrada_salida, "
        "m.paquetes AS 'paquetes' "
    "FROM movements m "
    "JOIN meds med ON med.id = m.med_id "
    "LEFT OUTER JOIN tipo_meds t ON t.id = med.tipo_id "
    f" WHERE med.codigo = '{med_code}'"
    ).dicts()
    rows = []
    for dat in data:
        rows.append(dat)
    print(rows)
    return rows

def check_code(code):
    data = (Med.select(Med.id,
                Med.codigo,
                Med.nombre,
                TipoMed.name,
                TipoMed.id.alias('tipo_id')
                )
                .join_from(Med, TipoMed)
                .where(Med.codigo == code)
                .dicts())
    rows = []
    for dat in data:
        rows.append(dat)
    return rows

def create_lote(name):
    return Lote.create(name=name)

def get_lotes():
    return Lote.select().dicts()

def update_lote(id, name):
    return Lote.update(name=name).where(Lote.id == id).execute()

def delete_lote(id):
    return Lote.delete().where(Lote.id == id).execute()

def search_med(name):
    data =  (Med.select(
        Med.id,
        Med.codigo,
        Med.nombre,
        TipoMed.name.alias('tipo')
    ).join_from(Med, TipoMed)
             .where(
        (Med.nombre.contains(name)) | (Med.codigo.contains(name))
    ).dicts())

    rows = []
    for dat in data:
        rows.append(dat)
    return rows

def search_lote(name):
    data = Lote.select(Lote.name).where(Lote.name.contains(name)).dicts()

    rows = []
    for dat in data:
        rows.append(dat)
    return rows

def search_movement(name):
    data = (Movement.select(
        Movement.id,
        Med.codigo.alias('med_code'),
        Med.nombre.alias('med'),
        Movement.unidades_por_paquete,
        Lote.name.alias('lote'),
        Movement.paquetes,
        Movement.donador_retirador,
        Movement.entrada_salida,
        TipoMed.name.alias('tipo'),
        Movement.fecha_creacion,
        Movement.fecha_vencimiento,
        Movement.fecha_entrega
    ).join_from(Movement, Lote, JOIN.LEFT_OUTER, on=(Lote.id == Movement.lote_id))
             .join_from(Movement, Med, JOIN.LEFT_OUTER, on=(Med.id == Movement.med_id))
             .join_from(Med, TipoMed, JOIN.LEFT_OUTER, on=(TipoMed.id == Med.tipo_id))
             .where(
        (Movement.donador_retirador.contains(name) |
         Med.nombre.contains(name) |
         Lote.name.contains(name) | Movement.unidades_por_paquete.contains(name) | Med.nombre.contains(name) |
         Movement.unidades_por_paquete.contains(name) | Med.codigo.contains(name)
         ))
             .dicts())

    rows = []
    for dat in data:
        rows.append(dat)
    return rows

def search_med_type(name):
    data = (TipoMed.select(
        TipoMed.id,
        TipoMed.name,
        fn.Count(Med.id).alias('productos')
        ).where(TipoMed.name.contains(f"{name}"))
            .join_from(TipoMed, Med, JOIN.LEFT_OUTER)
            .group_by(TipoMed.id)
            .order_by(TipoMed.name)
            .dicts())
    rows = []
    for dat in data:
        rows.append(dat)
    return rows



