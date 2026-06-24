# unitsling

> _Fire-and-forget unit conversions -- serious ones and silly ones._

**unitsling** is a blazing-fast, zero-dependency terminal unit converter. Whether you're converting miles to kilometers or blue whales to elephants, it's got you covered. All from the comfort of your terminal.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/version-1.1.0-orange)

---

## Features

- **120+ standard units** across 12 real-world categories
- **Temperature support** with proper offset handling (C, F, K)
- **Digital storage** including both decimal (KB, MB) and binary (KiB, MiB) prefixes
- **Zero dependencies** -- just Python 3.8+, nothing else
- **Whimsical mode** -- convert coffee to code, pizza to eggs, blue whales to elephants
- **Smart formatting** -- scientific notation for extreme values, clean decimals for normal ones
- **Interactive REPL** -- run `unitsling repl` for a conversational conversion session
- **Self-documenting** -- built-in help, unit listing, and category browser

## Categories

| Category   | Example Units                          |
|------------|----------------------------------------|
| Length     | km, m, cm, mm, mi, ft, in, yd, nm, um |
| Mass       | kg, g, mg, lb, oz, t, st, ton_us      |
| Temperature| C, F, K                                |
| Volume     | l, ml, gal, qt, pt, cup, floz, m3     |
| Speed      | mps, kmph, mph, knot, mach, c         |
| Digital    | B, KB, MB, GB, TB, KiB, MiB, GiB, bit |
| Time       | ns, ms, s, min, hr, day, week, yr     |
| Energy     | j, kj, cal, kcal, wh, kwh, ev, btu    |
| Area       | m2, km2, ha, acre, ft2, mi2           |
| Power      | W, kW, MW, hp, btu/hr                 |
| Pressure   | Pa, kPa, bar, atm, psi, mmHg, torr    |
| Frequency  | Hz, kHz, MHz, GHz, THz                 |

## Installation

### Quick run (no install)

```bash
git clone https://github.com/IndraTensei/unitsling.git
cd unitsling
python3 unitsling.py 100 miles km
```

### Install to PATH

```bash
git clone https://github.com/IndraTensei/unitsling.git
cd unitsling
chmod +x unitsling.py
sudo cp unitsling.py /usr/local/bin/unitsling
```

Now use it from anywhere:

```bash
unitsling 100 miles km
```

## Usage

### Basic conversion

```bash
unitsling <value> <from_unit> <to_unit>
```

### Examples

```bash
# Length
unitsling 100 mi km
# -> 100 mi = 160.9344 km

# Temperature
unitsling 212 F C
# -> 212 F = 100 C

# Mass
unitsling 1 kg lb
# -> 1 kg = 2.20462 lb

# Speed
unitsling 1 mach kmph
# -> 1 mach = 1234.8 kmph

# Digital storage
unitsling 1024 MiB GB
# -> 1024 MiB = 1.073742 GB

# Energy
unitsling 1 kcal j
# -> 1 kcal = 4184 J

# Time
unitsling 1 century s
# -> 1 century = 3.15576e+09 s

# Pressure
unitsling 1 atm psi
# -> 1 atm = 14.6959 psi

# Frequency
unitsling 1 GHz MHz
# -> 1 GHz = 1000 MHz
```

### List all units

```bash
unitsling list
```

### List categories

```bash
unitsling categories
```

### Interactive REPL mode

```bash
unitsling repl
```

Then type conversions interactively:

```
unitsling> 100 miles km
  100.0 miles = 160.9344 km
unitsling> 1 atm psi
  1.0 atm = 14.6959 psi
unitsling> quit
Goodbye!
```

### Whimsical conversions

```bash
# See all fun conversions
unitsling fun

# Convert 5 cups of coffee to lines of code
unitsling fun 5 cup loc
# -> 5 cup = 210 loc

# How many elephants in a blue whale?
unitsling fun 1 blue_whale elephant
# -> 1 blue_whale = 25 elephant

# How many eggs in a whole pizza?
unitsling fun 1 whole_pizza egg
# -> 1 whole_pizza = 12 egg
```

### Available whimsical conversions

| Conversion | Meaning |
|------------|---------|
| cup -> loc | Coffee to lines of code |
| cup -> bugs_fixed | Coffee to bugs fixed |
| slice -> egg | Pizza slice to egg calorie equivalent |
| banana -> kwh | Banana energy to kilowatt-hours |
| cat_year -> human_year | Cat years to human years |
| dog_year -> human_year | Dog years to human years |
| blue_whale -> elephant | Blue whales to elephants |
| blue_whale -> car | Blue whales to cars |
| olympic_pool -> bathtub | Olympic pools to bathtubs |
| tweet -> book | Tweets to books (word count) |

## Development

```bash
# Clone
git clone https://github.com/IndraTensei/unitsling.git
cd unitsling

# Run directly
python3 unitsling.py --help

# Run tests
python3 -m pytest tests/
```

## Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-conversion`
3. Add your conversion or fix
4. Add tests for your changes
5. Submit a pull request

Ideas for contributions:
- New unit categories (force, luminosity, etc.)
- More whimsical conversions
- Localization support
- Shell completions

## License

MIT License -- see [LICENSE](LICENSE) for details.

---

Made with coffee and a sense of humor.
