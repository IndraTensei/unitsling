#!/usr/bin/env python3
"""
unitsling — A blazing-fast unit converter for the terminal.

Converts between hundreds of units across length, mass, temperature,
volume, speed, digital storage, time, energy, and more — plus a
handful of whimsical conversions for fun.

Usage:
    unitsling <value> <from> <to>
    unitsling list                 # list all units
    unitsling categories           # list categories
    unitsling fun                  # show whimsical conversions
    unitsling repl                 # interactive REPL mode

Examples:
    unitsling 100 miles km
    unitsling 212 F C
    unitsling 1 kg lb
    unitsling fun                  # "1 horse = 745.7 watts" etc.
    unitsling repl                 # start interactive session
"""

from __future__ import annotations

import sys
import math
import json
import readline
from typing import Callable

__version__ = "1.2.0"


# ─────────────────────────────────────────────────────────────
# Conversion Registry
# Each category holds conversions defined as functions
# that take a value in the base unit and return the target value.
# Base units: meter (length), kilogram (mass), kelvin (temp),
# liter (volume), m/s (speed), byte (digital), second (time),
# joule (energy), m² (area), watt (power), pascal (pressure),
# hertz (frequency)
# ─────────────────────────────────────────────────────────────

CONVERSIONS: dict[str, dict[str, str]] = {
    "Length": {
        "km": "kilometer", "m": "meter", "cm": "centimeter",
        "mm": "millimeter", "mi": "mile", "ft": "foot", "in": "inch",
        "yd": "yard", "nm": "nanometer", "um": "micrometer",
    },
    "Mass": {
        "kg": "kilogram", "g": "gram", "mg": "milligram",
        "lb": "pound", "oz": "ounce", "t": "tonne", "st": "stone",
        "ton_us": "us_ton", "ton_uk": "uk_ton",
    },
    "Temperature": {
        "C": "celsius", "F": "fahrenheit", "K": "kelvin",
    },
    "Volume": {
        "l": "liter", "ml": "milliliter", "gal": "gallon_us",
        "gal_uk": "gallon_uk", "qt": "quart", "pt": "pint",
        "cup": "cup_us", "floz": "fluid_ounce_us", "tbsp": "tablespoon",
        "tsp": "teaspoon", "m3": "cubic_meter", "ft3": "cubic_foot",
    },
    "Speed": {
        "mps": "meters_per_sec", "kmph": "km_per_hour",
        "mph": "miles_per_hour", "knot": "knot", "fps": "feet_per_sec",
        "mach": "mach_at_sea_level", "c": "speed_of_light",
    },
    "Digital": {
        "B": "byte", "KB": "kilobyte", "MB": "megabyte",
        "GB": "gigabyte", "TB": "terabyte", "PB": "petabyte",
        "KiB": "kibibyte", "MiB": "mebibyte", "GiB": "gibibyte",
        "TiB": "tebibyte", "bit": "bit", "kbit": "kilobit",
        "mbit": "megabit", "gbit": "gigabit",
    },
    "Time": {
        "ns": "nanosecond", "us": "microsecond", "ms": "millisecond",
        "s": "second", "min": "minute", "hr": "hour", "day": "day",
        "week": "week", "mo": "month", "yr": "year",
        "decade": "decade", "century": "century",
    },
    "Energy": {
        "j": "joule", "kj": "kilojoule", "cal": "calorie",
        "kcal": "kilocalorie", "wh": "watt_hour", "kwh": "kilowatt_hour",
        "ev": "electronvolt", "btu": "british_thermal_unit",
        "therm": "therm",
    },
    "Area": {
        "m2": "sq_meter", "km2": "sq_km", "cm2": "sq_cm",
        "ha": "hectare", "acre": "acre", "ft2": "sq_foot",
        "mi2": "sq_mile", "in2": "sq_inch",
    },
    "Power": {
        "W": "watt", "kW": "kilowatt", "MW": "megawatt",
        "hp": "horsepower", "hp_metric": "metric_horsepower",
        "btu_hr": "btu_per_hour",
    },
    "Pressure": {
        "Pa": "pascal", "kPa": "kilopascal", "MPa": "megapascal",
        "bar": "bar", "atm": "atmosphere", "psi": "psi",
        "mmHg": "mm_hg", "torr": "torr",
    },
    "Frequency": {
        "Hz": "hertz", "kHz": "kilohertz", "MHz": "megahertz",
        "GHz": "gigahertz", "THz": "terahertz",
    },
    "Force": {
        "N": "newton", "kN": "kilonewton", "dyn": "dyne",
        "lbf": "pound_force", "kgf": "kilogram_force",
    },
    "Angle": {
        "deg": "degree", "rad": "radian", "grad": "gradian",
        "arcmin": "arcminute", "arcsec": "arcsecond", "rev": "revolution",
    },
}

# ─────────────────────────────────────────────────────────────
# Factor-based conversions: (from_factor, to_factor)
# value_in_base = value * from_factor
# value_in_target = value_in_base / to_factor
# ─────────────────────────────────────────────────────────────

LENGTH_FACTORS = {
    "km": 1e3, "m": 1.0, "cm": 1e-2, "mm": 1e-3,
    "mi": 1609.344, "ft": 0.3048, "in": 0.0254,
    "yd": 0.9144, "nm": 1e-9, "um": 1e-6,
}

MASS_FACTORS = {
    "kg": 1.0, "g": 1e-3, "mg": 1e-6,
    "lb": 0.45359237, "oz": 0.02834952,
    "t": 1000.0, "st": 6.350293,
    "ton_us": 907.18474, "ton_uk": 1016.0469,
}

VOLUME_FACTORS = {
    "l": 1.0, "ml": 1e-3, "gal": 3.785412, "gal_uk": 4.54609,
    "qt": 0.946353, "pt": 0.473176, "cup": 0.236588,
    "floz": 0.0295735, "tbsp": 0.0147868, "tsp": 0.00492892,
    "m3": 1000.0, "ft3": 28.3168,
}

SPEED_FACTORS = {
    "mps": 1.0, "kmph": 1/3.6, "mph": 0.44704, "knot": 0.514444,
    "fps": 0.3048, "mach": 343.0, "c": 299792458,
}

DIGITAL_FACTORS = {
    "B": 1.0,
    "KB": 1e3, "MB": 1e6, "GB": 1e9, "TB": 1e12, "PB": 1e15,
    "KiB": 1024, "MiB": 1024**2, "GiB": 1024**3, "TiB": 1024**4,
    "bit": 1/8, "kbit": 1e3/8, "mbit": 1e6/8, "gbit": 1e9/8,
}

TIME_FACTORS = {
    "ns": 1e-9, "us": 1e-6, "ms": 1e-3, "s": 1.0,
    "min": 60.0, "hr": 3600.0, "day": 86400.0, "week": 604800.0,
    "mo": 2629800.0, "yr": 31557600.0,
    "decade": 315576000.0, "century": 3155760000.0,
}

ENERGY_FACTORS = {
    "j": 1.0, "kj": 1e3, "cal": 4.184, "kcal": 4184.0,
    "wh": 3600.0, "kwh": 3.6e6, "ev": 1.602176634e-19,
    "btu": 1055.06, "therm": 1.05506e8,
}

AREA_FACTORS = {
    "m2": 1.0, "km2": 1e6, "cm2": 1e-4,
    "ha": 1e4, "acre": 4046.856, "ft2": 0.092903,
    "mi2": 2.58999e6, "in2": 0.00064516,
}

POWER_FACTORS = {
    "W": 1.0, "kW": 1e3, "MW": 1e6,
    "hp": 745.7, "hp_metric": 735.5, "btu_hr": 0.293071,
}

PRESSURE_FACTORS = {
    "Pa": 1.0, "kPa": 1e3, "MPa": 1e6,
    "bar": 1e5, "atm": 101325.0,
    "psi": 6894.76, "mmHg": 133.322, "torr": 133.322,
}

FREQUENCY_FACTORS = {
    "Hz": 1.0, "kHz": 1e3, "MHz": 1e6,
    "GHz": 1e9, "THz": 1e12,
}

FORCE_FACTORS = {
    "N": 1.0, "kN": 1e3, "dyn": 1e-5,
    "lbf": 4.4482216153, "kgf": 9.80665,
}

ANGLE_FACTORS = {
    "deg": 1.0, "rad": 180 / math.pi, "grad": 0.9,
    "arcmin": 1/60, "arcsec": 1/3600, "rev": 360.0,
}

# ─────────────────────────────────────────────────────────────
# Temperature conversions (special — not factor-based)
# ─────────────────────────────────────────────────────────────

def c_to_f(c: float) -> float: return c * 9/5 + 32
def c_to_k(c: float) -> float: return c + 273.15
def f_to_c(f: float) -> float: return (f - 32) * 5/9
def f_to_k(f: float) -> float: return (f - 32) * 5/9 + 273.15
def k_to_c(k: float) -> float: return k - 273.15
def k_to_f(k: float) -> float: return (k - 273.15) * 9/5 + 32

TEMP_CONVERSIONS: dict[tuple[str, str], Callable[[float], float]] = {
    ("C", "F"): c_to_f, ("C", "K"): c_to_k,
    ("F", "C"): f_to_c, ("F", "K"): f_to_k,
    ("K", "C"): k_to_c, ("K", "F"): k_to_f,
}

# ─────────────────────────────────────────────────────────────
# Whimsical / fun conversions
# ─────────────────────────────────────────────────────────────

FUN_CONVERSIONS = {
    "coffee_to_productivity": {
        "description": "Coffee -> Productivity (lines of code per cup)",
        "conversions": {
            ("cup", "loc"): lambda x: x * 42,  # 42 lines per cup, obviously
            ("cup", "bugs_fixed"): lambda x: x * 3,
            ("cup", "existential_crises"): lambda x: x * 0.5,
        }
    },
    "pizza_to_eggs": {
        "description": "Pizza -> Eggs (calorie equivalent)",
        "conversions": {
            ("slice", "egg"): lambda x: x * 1.5,  # ~450 cal per slice, ~70 per egg
            ("whole_pizza", "egg"): lambda x: x * 12,
        }
    },
    "banana_to_energy": {
        "description": "Bananas -> Energy (kWh equivalent)",
        "conversions": {
            ("banana", "kwh"): lambda x: x * 0.000116,  # ~105 kcal per banana
            ("banana", "joule"): lambda x: x * 439320,
        }
    },
    "cat_to_human_years": {
        "description": "Cat years -> Human years",
        "conversions": {
            ("cat_year", "human_year"): lambda x: x * 4 + 16 if x > 1 else x * 15,
        }
    },
    "dog_to_human_years": {
        "description": "Dog years -> Human years",
        "conversions": {
            ("dog_year", "human_year"): lambda x: x * 7,
        }
    },
    "sneezes_to_energy": {
        "description": "Sneezes -> Energy (joules)",
        "conversions": {
            ("sneeze", "joule"): lambda x: x * 0.00023,  # ~0.23 mJ per sneeze
        }
    },
    "tweets_to_books": {
        "description": "Tweets -> Books (word count equivalent)",
        "conversions": {
            ("tweet", "book"): lambda x: x / 28000,  # 280 words/tweet, 80k words/book
        }
    },
    "olympic_pools": {
        "description": "Olympic swimming pools -> Various",
        "conversions": {
            ("olympic_pool", "bathtub"): lambda x: x * 16.67,  # 2500 m^3 pool, 150L tub
            ("olympic_pool", "beer_keg"): lambda x: x * 14706,
        }
    },
    "blue_whale": {
        "description": "Blue whale -> Various",
        "conversions": {
            ("blue_whale", "elephant"): lambda x: x * 25,  # ~150t whale, ~6t elephant
            ("blue_whale", "school_bus"): lambda x: x * 1.5,
            ("blue_whale", "car"): lambda x: x * 100,
        }
    },
    "pizza_to_moon": {
        "description": "Pizzas stacked -> Distance to the Moon",
        "conversions": {
            ("pizza_stack_km", "moon_distance"): lambda x: x / 384400,
        }
    },
}

# ─────────────────────────────────────────────────────────────
# Core conversion engine
# ─────────────────────────────────────────────────────────────

def find_category(unit: str) -> str | None:
    """Find which category a unit belongs to."""
    for cat, units in CONVERSIONS.items():
        if unit in units:
            return cat
    return None


def convert_factor(value: float, from_unit: str, to_unit: str, factors: dict) -> float:
    """Convert using factor tables."""
    base = value * factors[from_unit]
    return base / factors[to_unit]


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """Main conversion dispatcher."""
    if from_unit == to_unit:
        return value

    # Temperature
    if (from_unit, to_unit) in TEMP_CONVERSIONS:
        return TEMP_CONVERSIONS[(from_unit, to_unit)](value)

    # Factor-based
    factor_tables = {
        "Length": LENGTH_FACTORS,
        "Mass": MASS_FACTORS,
        "Volume": VOLUME_FACTORS,
        "Speed": SPEED_FACTORS,
        "Digital": DIGITAL_FACTORS,
        "Time": TIME_FACTORS,
        "Energy": ENERGY_FACTORS,
        "Area": AREA_FACTORS,
        "Power": POWER_FACTORS,
        "Pressure": PRESSURE_FACTORS,
        "Frequency": FREQUENCY_FACTORS,
        "Force": FORCE_FACTORS,
        "Angle": ANGLE_FACTORS,
    }

    from_cat = find_category(from_unit)
    to_cat = find_category(to_unit)

    if from_cat and to_cat and from_cat == to_cat:
        return convert_factor(value, from_unit, to_unit, factor_tables[from_cat])

    raise ValueError(
        f"Cannot convert '{from_unit}' to '{to_unit}'. "
        f"They may be in different categories or unknown units."
    )


def format_result(value: float) -> str:
    """Format a number nicely -- avoid excessive decimals."""
    if value == 0:
        return "0"
    if abs(value) >= 1e9 or abs(value) < 1e-4:
        return f"{value:.6e}"
    # Strip trailing zeros
    formatted = f"{value:.6f}".rstrip("0").rstrip(".")
    return formatted


def list_units():
    """Print all available units grouped by category."""
    print("\nAvailable Units by Category\n")
    for cat, units in CONVERSIONS.items():
        print(f"  {cat}:")
        for abbr, full in units.items():
            print(f"    {abbr:<12} {full}")
        print()


def list_categories():
    """Print all categories."""
    print("\nCategories:\n")
    for cat in CONVERSIONS:
        print(f"  - {cat}")
    print()


def show_fun():
    """Print whimsical conversions."""
    print("\nWhimsical Conversions\n")
    for key, data in FUN_CONVERSIONS.items():
        print(f"  {data['description']}")
        for (fu, tu), fn in data['conversions'].items():
            # Show example with value 1
            result = fn(1)
            print(f"    1 {fu} = {format_result(result)} {tu}")
        print()


def show_fun_convert(value: float, from_unit: str, to_unit: str, json_output: bool = False):
    """Perform a whimsical conversion."""
    for key, data in FUN_CONVERSIONS.items():
        if (from_unit, to_unit) in data["conversions"]:
            result = data["conversions"][(from_unit, to_unit)](value)
            if json_output:
                print(json.dumps({
                    "value": value,
                    "from": from_unit,
                    "to": to_unit,
                    "result": result,
                    "result_formatted": format_result(result),
                    "description": data["description"],
                }))
            else:
                print(f"\n  {format_result(value)} {from_unit} = {format_result(result)} {to_unit}")
                print(f"  ({data['description']})")
            return
    print(f"  Unknown fun conversion: {from_unit} -> {to_unit}")
    print("  Run 'unitsling fun' to see available whimsical conversions.")


# ─────────────────────────────────────────────────────────────
# Interactive REPL mode
# ─────────────────────────────────────────────────────────────

def repl():
    """Interactive REPL for conversions."""
    print("unitsling REPL v1.2.0")
    print("Type 'help' for commands, 'quit' to exit.")
    print("Type a conversion like: 100 miles km")
    print()

    while True:
        try:
            line = input("unitsling> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not line:
            continue

        if line.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        if line.lower() == "help":
            print("  <value> <from> <to>   Convert a value")
            print("  list                  List all units")
            print("  categories            List categories")
            print("  fun                   Show whimsical conversions")
            print("  fun <val> <from> <to> Do whimsical conversion")
            print("  help                  Show this help")
            print("  quit                  Exit REPL")
            continue

        if line.lower() == "list":
            list_units()
            continue

        if line.lower() == "categories":
            list_categories()
            continue

        if line.lower() == "fun":
            show_fun()
            continue

        parts = line.split()

        # fun conversion: fun <value> <from> <to>
        if len(parts) == 4 and parts[0] == "fun":
            try:
                val = float(parts[1])
            except ValueError:
                print(f"  Invalid number: {parts[1]}")
                continue
            show_fun_convert(val, parts[2], parts[3])
            continue

        # standard conversion: <value> <from> <to>
        if len(parts) == 3:
            try:
                value = float(parts[0])
            except ValueError:
                print(f"  Invalid number: {parts[0]}")
                continue
            from_unit = parts[1]
            to_unit = parts[2]
            try:
                result = convert(value, from_unit, to_unit)
                formatted = format_result(result)
                print(f"  {value} {from_unit} = {formatted} {to_unit}")
            except ValueError as e:
                print(f"  {e}")
            continue

        print("  Invalid input. Type 'help' for commands.")


# ─────────────────────────────────────────────────────────────
# CLI entry point
# ─────────────────────────────────────────────────────────────

def print_help():
    print("""
unitsling — The Fun Unit Converter

Usage:
    unitsling <value> <from> <to>     Convert a value
    unitsling list                    List all units
    unitsling categories              List categories
    unitsling fun                     Show whimsical conversions
    unitsling fun <value> <from> <to> Do a whimsical conversion
    unitsling repl                    Start interactive REPL
    unitsling --json                  Emit machine-readable JSON
    unitsling --help                  Show this help
    unitsling --version               Show version

Use --json before a conversion to get JSON output, e.g.:
    unitsling --json 100 miles km

Examples:
    unitsling 100 miles km
    unitsling 212 F C
    unitsling 1 kg lb
    unitsling 1000 MB GB
    unitsling fun 5 cup loc
    unitsling fun 1 blue_whale elephant
    unitsling repl
""")


def main():
    args = sys.argv[1:]

    if not args or args[0] in ("--help", "-h"):
        print_help()
        return

    if args[0] in ("--version", "-v"):
        print(f"unitsling v{__version__}")
        return

    json_output = False
    if "--json" in args:
        json_output = True
        args = [a for a in args if a != "--json"]

    if args[0] == "list":
        list_units()
        return

    if args[0] == "categories":
        list_categories()
        return

    if args[0] == "repl":
        repl()
        return

    if args[0] == "fun":
        if len(args) == 1:
            show_fun()
            return
        if len(args) == 4:
            try:
                val = float(args[1])
            except ValueError:
                print(f"Invalid number: {args[1]}")
                sys.exit(1)
            show_fun_convert(val, args[2], args[3], json_output=json_output)
            return
        print("Usage: unitsling fun <value> <from> <to>")
        sys.exit(1)

    # Standard conversion: value from to
    if len(args) != 3:
        print("Usage: unitsling <value> <from> <to>")
        print("   Run 'unitsling --help' for more info.")
        sys.exit(1)

    try:
        value = float(args[0])
    except ValueError:
        print(f"Invalid number: {args[0]}")
        sys.exit(1)

    from_unit = args[1]
    to_unit = args[2]

    try:
        result = convert(value, from_unit, to_unit)
        formatted = format_result(result)
        if json_output:
            print(json.dumps({
                "value": value,
                "from": from_unit,
                "to": to_unit,
                "result": result,
                "result_formatted": formatted,
            }))
        else:
            print(f"\n  {value} {from_unit} = {formatted} {to_unit}\n")
    except ValueError as e:
        print(f"\n  {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
