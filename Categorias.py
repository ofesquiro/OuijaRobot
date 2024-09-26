from enum import Enum, auto

class Categorias(Enum):
    EXISTENCIALES = "EXISTENCIALES"
    EMOCIONALES = "EMOCIONALES"
    SOCIALES = "SOCIALES"
    FISICAS = "FISICAS"
    SEXUALES = "SEXUALES"
    ECONOMICAS = "ECONOMICAS"
    POLITICAS = "POLITICAS"
    RELIGIOSAS = "RELIGIOSAS"
    CULTURALES = "CULTURALES"
    SALUDOS = "SALUDOS"
    SALUDOSCONPREGUNTA = "SALUDOSCONPREGUNTA"
    HORA = "HORA"
    DIA = "DIA"
    MES = "MES"
    PREPREGUNTA = "PREPREGUNTA"
    ERROR = "ERROR"


def parse_string_to_enum(categoria_str : str):
    try:
        return Categorias(categoria_str)  # Capitalizamos para asegurar que coincida con el valor del Enum
    except ValueError:
        raise ValueError(f"{categoria_str} no es una categoría válida")
