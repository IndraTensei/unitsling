#!/usr/bin/env python3
"""Tests for unitsling -- the fun unit converter."""

import pytest
from unitsling import (
    convert, format_result, find_category,
    LENGTH_FACTORS, MASS_FACTORS, VOLUME_FACTORS,
    SPEED_FACTORS, DIGITAL_FACTORS, TIME_FACTORS,
    ENERGY_FACTORS, AREA_FACTORS, POWER_FACTORS,
    PRESSURE_FACTORS, FREQUENCY_FACTORS,
    TEMP_CONVERSIONS, FUN_CONVERSIONS,
)


# --- Length ---

class TestLength:
    def test_miles_to_km(self):
        result = convert(1, "mi", "km")
        assert abs(result - 1.609344) < 0.001

    def test_km_to_miles(self):
        result = convert(100, "km", "mi")
        assert abs(result - 62.1371) < 0.01

    def test_feet_to_meters(self):
        result = convert(1, "ft", "m")
        assert abs(result - 0.3048) < 0.0001

    def test_inches_to_cm(self):
        result = convert(1, "in", "cm")
        assert abs(result - 2.54) < 0.001

    def test_yard_to_meter(self):
        result = convert(1, "yd", "m")
        assert abs(result - 0.9144) < 0.0001

    def test_nanometer_to_meter(self):
        result = convert(1e9, "nm", "m")
        assert abs(result - 1.0) < 0.001

    def test_same_unit(self):
        assert convert(42, "km", "km") == 42


# --- Mass ---

class TestMass:
    def test_kg_to_lb(self):
        result = convert(1, "kg", "lb")
        assert abs(result - 2.20462) < 0.001

    def test_lb_to_kg(self):
        result = convert(1, "lb", "kg")
        assert abs(result - 0.453592) < 0.001

    def test_ounce_to_gram(self):
        result = convert(1, "oz", "g")
        assert abs(result - 28.3495) < 0.01

    def test_tonne_to_kg(self):
        result = convert(1, "t", "kg")
        assert abs(result - 1000.0) < 0.001

    def test_stone_to_kg(self):
        result = convert(1, "st", "kg")
        assert abs(result - 6.35029) < 0.001


# --- Temperature ---

class TestTemperature:
    def test_c_to_f_boiling(self):
        result = convert(100, "C", "F")
        assert abs(result - 212.0) < 0.01

    def test_f_to_c_freezing(self):
        result = convert(32, "F", "C")
        assert abs(result - 0.0) < 0.01

    def test_c_to_k(self):
        result = convert(0, "C", "K")
        assert abs(result - 273.15) < 0.01

    def test_k_to_c(self):
        result = convert(273.15, "K", "C")
        assert abs(result - 0.0) < 0.01

    def test_f_to_k(self):
        result = convert(32, "F", "K")
        assert abs(result - 273.15) < 0.01

    def test_k_to_f(self):
        result = convert(273.15, "K", "F")
        assert abs(result - 32.0) < 0.01


# --- Volume ---

class TestVolume:
    def test_gallon_to_liter(self):
        result = convert(1, "gal", "l")
        assert abs(result - 3.78541) < 0.001

    def test_liter_to_ml(self):
        result = convert(1, "l", "ml")
        assert abs(result - 1000.0) < 0.001

    def test_cup_to_ml(self):
        result = convert(1, "cup", "ml")
        assert abs(result - 236.588) < 0.1


# --- Speed ---

class TestSpeed:
    def test_mach_to_kmph(self):
        result = convert(1, "mach", "kmph")
        assert abs(result - 1234.8) < 1.0

    def test_mph_to_mps(self):
        result = convert(1, "mph", "mps")
        assert abs(result - 0.44704) < 0.001

    def test_c_to_mps(self):
        result = convert(1, "c", "mps")
        assert abs(result - 299792458) < 1.0

    def test_knot_to_mph(self):
        result = convert(1, "knot", "mph")
        assert abs(result - 1.15078) < 0.001


# --- Digital ---

class TestDigital:
    def test_gb_to_mb(self):
        result = convert(1, "GB", "MB")
        assert abs(result - 1000.0) < 0.001

    def test_gib_to_mib(self):
        result = convert(1, "GiB", "MiB")
        assert abs(result - 1024.0) < 0.001

    def test_mib_to_gb(self):
        result = convert(1024, "MiB", "GB")
        assert abs(result - 1.073742) < 0.001

    def test_byte_to_bit(self):
        result = convert(1, "B", "bit")
        assert abs(result - 8.0) < 0.001


# --- Time ---

class TestTime:
    def test_hour_to_minute(self):
        result = convert(1, "hr", "min")
        assert abs(result - 60.0) < 0.001

    def test_day_to_seconds(self):
        result = convert(1, "day", "s")
        assert abs(result - 86400.0) < 0.001

    def test_year_to_days(self):
        result = convert(1, "yr", "day")
        assert abs(result - 365.25) < 0.1

    def test_century_to_years(self):
        result = convert(1, "century", "yr")
        assert abs(result - 100.0) < 0.001


# --- Energy ---

class TestEnergy:
    def test_kcal_to_joule(self):
        result = convert(1, "kcal", "j")
        assert abs(result - 4184.0) < 0.1

    def test_kwh_to_joule(self):
        result = convert(1, "kwh", "j")
        assert abs(result - 3.6e6) < 1.0

    def test_btu_to_joule(self):
        result = convert(1, "btu", "j")
        assert abs(result - 1055.06) < 0.1


# --- Area ---

class TestArea:
    def test_acre_to_m2(self):
        result = convert(1, "acre", "m2")
        assert abs(result - 4046.856) < 0.1

    def test_hectare_to_m2(self):
        result = convert(1, "ha", "m2")
        assert abs(result - 10000.0) < 0.001

    def test_km2_to_m2(self):
        result = convert(1, "km2", "m2")
        assert abs(result - 1e6) < 0.001


# --- Power ---

class TestPower:
    def test_hp_to_watt(self):
        result = convert(1, "hp", "W")
        assert abs(result - 745.7) < 0.1

    def test_kw_to_watt(self):
        result = convert(1, "kW", "W")
        assert abs(result - 1000.0) < 0.001


# --- Pressure ---

class TestPressure:
    def test_atm_to_psi(self):
        result = convert(1, "atm", "psi")
        assert abs(result - 14.6959) < 0.001

    def test_bar_to_pa(self):
        result = convert(1, "bar", "Pa")
        assert abs(result - 100000.0) < 0.001

    def test_psi_to_kpa(self):
        result = convert(1, "psi", "kPa")
        assert abs(result - 6.89476) < 0.001

    def test_mmhg_to_pa(self):
        result = convert(1, "mmHg", "Pa")
        assert abs(result - 133.322) < 0.01

    def test_torr_to_atm(self):
        result = convert(760, "torr", "atm")
        assert abs(result - 1.0) < 0.001


# --- Frequency ---

class TestFrequency:
    def test_ghz_to_mhz(self):
        result = convert(1, "GHz", "MHz")
        assert abs(result - 1000.0) < 0.001

    def test_thz_to_ghz(self):
        result = convert(1, "THz", "GHz")
        assert abs(result - 1000.0) < 0.001

    def test_hz_to_khz(self):
        result = convert(1000, "Hz", "kHz")
        assert abs(result - 1.0) < 0.001

    def test_mhz_to_hz(self):
        result = convert(1, "MHz", "Hz")
        assert abs(result - 1e6) < 0.001


# --- Formatting ---

class TestFormatting:
    def test_zero(self):
        assert format_result(0) == "0"

    def test_normal(self):
        assert format_result(42.5) == "42.5"

    def test_trailing_zeros(self):
        result = format_result(1.500000)
        assert result == "1.5"

    def test_scientific_large(self):
        result = format_result(1e15)
        assert "e+" in result

    def test_scientific_small(self):
        result = format_result(1e-10)
        assert "e-" in result


# --- Category lookup ---

class TestCategory:
    def test_find_length(self):
        assert find_category("km") == "Length"

    def test_find_temp(self):
        assert find_category("F") == "Temperature"

    def test_find_pressure(self):
        assert find_category("psi") == "Pressure"

    def test_find_frequency(self):
        assert find_category("GHz") == "Frequency"

    def test_find_unknown(self):
        assert find_category("foobar") is None


# --- Error handling ---

class TestErrors:
    def test_cross_category_raises(self):
        with pytest.raises(ValueError):
            convert(1, "km", "kg")

    def test_unknown_unit_raises(self):
        with pytest.raises(ValueError):
            convert(1, "foo", "bar")


# --- Whimsical conversions ---

class TestFun:
    def test_coffee_to_loc(self):
        from unitsling import FUN_CONVERSIONS
        fn = FUN_CONVERSIONS["coffee_to_productivity"]["conversions"][("cup", "loc")]
        assert fn(1) == 42
        assert fn(5) == 210

    def test_blue_whale_to_elephant(self):
        from unitsling import FUN_CONVERSIONS
        fn = FUN_CONVERSIONS["blue_whale"]["conversions"][("blue_whale", "elephant")]
        assert fn(1) == 25

    def test_pizza_to_egg(self):
        from unitsling import FUN_CONVERSIONS
        fn = FUN_CONVERSIONS["pizza_to_eggs"]["conversions"][("whole_pizza", "egg")]
        assert fn(1) == 12

    def test_tweet_to_book(self):
        from unitsling import FUN_CONVERSIONS
        fn = FUN_CONVERSIONS["tweets_to_books"]["conversions"][("tweet", "book")]
        assert abs(fn(28000) - 1.0) < 0.01


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
