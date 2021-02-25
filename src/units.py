# @author KOOKIIE


def to_km(value, unit):
    if unit == "mm":
        return value / 1000000
    elif unit == "cm":
        return value / 100000
    elif unit == "m":
        return value / 1000
    elif unit == "km":
        return value
    else:
        raise ValueError(f"Invalid unit: {unit}")


def to_mi(value, unit):
    if unit == "ft":
        return value / 5280
    elif unit == "in":
        return value / 63360
    elif unit == "mi":
        return value
    else:
        raise ValueError(f"Invalid unit: {unit}")


def to_kg(value, unit):
    if unit == "g":
        return value / 1000
    elif unit == "kg":
        return value
    else:
        raise ValueError(f"Invalid unit: {unit}")


def to_lbs(value, unit):
    if unit == "oz":
        return value / 16
    elif unit == "lbs":
        return value
    else:
        raise ValueError(f"Invalid unit: {unit}")


def to_ml(value, unit):
    if unit == "l":
        return value / 1000
    elif unit in ("ml", "cc"):
        return value
    else:
        raise ValueError(f"Invalid unit: {unit}")


def to_oz(value, unit):
    if unit == "gallon":
        return value * 128
    elif unit == "pint":
        return value * 16
    elif unit == "oz":
        return value
    else:
        raise ValueError(f"Invalid unit: {unit}")


def c_to_k(value):
    return value + 273.15


def k_to_c(value):
    return value - 273.15


def f_to_k(value):
    return ((value - 32) / 1.8) + 273.15


def k_to_f(value):
    return ((value - 273.15) * 1.8) + 32


def length_si_to_imperial(unit_from, unit_to, source_value):
    # do conversions as km-mi
    source_in_km = to_km(source_value, unit_from)
    source_in_mi = source_in_km * 0.621371192
    if unit_to == "mi":
        output = source_in_mi
    elif unit_to == "ft":
        output = source_in_mi * 5280
        if int(output):
            # if ft component > 1
            output_in_component = (output - int(output)) * 12
            return f"{source_value}*{unit_from}* = {int(output)}*{unit_to}* {output_in_component:.2f}*in* (2dp)"
    elif unit_to == "in":
        output = source_in_mi * 63360
    else:
        return "Invalid units!"
    return f"{source_value}*{unit_from}* = {output:.2f}*{unit_to}* (2dp)"


def length_imperial_to_si(unit_from, unit_to, source_value):
    # do conversions as mi-km
    source_in_mi = to_mi(source_value, unit_from)
    source_in_km = source_in_mi / 0.621371192
    if unit_to == "km":
        output = source_in_km
    elif unit_to == "m":
        output = source_in_km * 1000
        if int(output):
            # if m component > 1
            output_cm_component = (output - int(output)) * 100
            return f"{source_value}*{unit_from}* = {int(output)}*{unit_to}* {output_cm_component:.2f}*cm* (2dp)"
    elif unit_to == "cm":
        output = source_in_km * 100000
        if int(output):
            # if cm component > 1
            output_mm_component = (output - int(output)) * 10
            return f"{source_value}*{unit_from}* = {int(output)}*{unit_to}* {output_mm_component:.2f}*cm* (2dp)"
    elif unit_to == "mm":
        output = source_in_km * 1000000
    else:
        return "Invalid units!"
    return f"{source_value}*{unit_from}* = {output:.2f}*{unit_to}* (2dp)"


def weight_si_imperial(unit_from, unit_to, source_value):
    # do conversions as kg-lbs
    source_in_kg = to_kg(source_value, unit_from)
    source_in_lbs = source_in_kg / 0.45359237
    if unit_to == "lbs":
        output = source_in_lbs
    elif unit_to == "oz":
        output = source_in_lbs * 16
    else:
        return "Invalid units!"
    return f"{source_value}*{unit_from}* = {output:.2f}*{unit_to}* (2dp)"


def weight_imperial_si(unit_from, unit_to, source_value):
    # do conversions as lbs-kg
    source_in_lbs = to_lbs(source_value, unit_from)
    source_in_kg = source_in_lbs * 0.45359237
    if unit_to == "kg":
        output = source_in_kg
    elif unit_to == "g":
        output = source_in_kg * 1000
    else:
        return "Invalid units!"
    return f"{source_value}*{unit_from}* = {output:.2f}*{unit_to}* (2dp)"


def liquid_imperial_si(unit_from, unit_to, source_value):
    # do conversions as ml-oz
    source_in_ml = to_ml(source_value, unit_from)
    source_in_oz = source_in_ml / 29.57
    if unit_to == "oz":
        output = source_in_oz
    elif unit_to == "pint":
        output = source_in_oz / 16
    elif unit_to == "gallon":
        output = source_in_oz / 128
    else:
        return "Invalid units!"
    return f"{source_value}*{unit_from}* = {output:.2f}*{unit_to}* (2dp)"


def liquid_si_imperial(unit_from, unit_to, source_value):
    # do conversions as oz-ml
    source_in_oz = to_oz(source_value, unit_from)
    source_in_ml = source_in_oz * 29.57
    if unit_to in ("ml", "cc"):
        output = source_in_ml
    elif unit_to == "l":
        output = source_in_ml / 1000
    else:
        return "Invalid units!"
    return f"{source_value}*{unit_from}* = {output:.2f}*{unit_to}* (2dp)"


SI_UNITS = [
    "km",
    "m",
    "cm",
    "mm",
    "kg",
    "g",
    "l",
    "ml",
    "cc",
]


IMPERIAL_UNITS = [
    "mi",
    "ft",
    "in",
    "lbs",
    "oz",
    "pint",
    "gallon",
]
