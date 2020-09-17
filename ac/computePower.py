Temp_levels = ['VC', 'C', 'W', 'H', 'VH'] # very cold,cold,warm,hot,very hot
Humidity_levels = ['VD', 'D', 'N', 'W', 'VW']# very dry,dry,normal,wet,very wet
Power_Levels = ['VL', 'L', 'N', 'H', 'VH']#very low,low,normal,high,very high


def fuzzify_temperature(value):
    if value < 8.0:
        return 'VC'
    elif value >= 9.0 and value < 20.0:
        return 'C'
    elif value >= 20.0 and value < 25.0:
        return 'W'
    elif value >= 26.0 and value < 34.0:
        return 'H'
    else:
        return 'VH'


def fuzzify_humidity(value):
    if value < 2.0:
        return 'VD'
    elif value >= 3.0 and value < 5.0:
        return 'D'
    elif value >= 6.0 and value < 7.0:
        return 'N'
    elif value >= 8.0 and value < 10.0:
        return 'W'
    else:
        return 'VW'


def defuzzify(value):
    if value == 'VL':
        return 50.0
    elif value == 'L':
        return 100.0
    elif value == 'N':
        return 150.0
    elif value == 'H':
        return 200.0
    else:
        return 250.0


def compute_fuzzy_power_amount(temperature_degree_fuzzy, humidity_level_fuzzy):
    rule_map = {
        ('VC', 'VD'): 'H',
        ('VC', 'D'): 'H',
        ('VC', 'N'): 'VH',
        ('VC', 'W'): 'VH',
        ('VC', 'VW'): 'VH',
        ('C', 'VD'): 'N',
        ('C', 'D'): 'H',
        ('C', 'N'): 'H',
        ('C', 'W'): 'VH',
        ('C', 'VW'): 'VH',
        ('W', 'VD'): 'VL',
        ('W', 'D'): 'VL',
        ('W', 'N'): 'VL',
        ('W', 'W'): 'L',
        ('W', 'VW'): 'N',
        ('H', 'VD'): 'N',
        ('H', 'D'): 'N',
        ('H', 'N'): 'H',
        ('H', 'W'): 'H',
        ('H', 'VW'): 'VH',
        ('VH', 'VD'): 'L',
        ('VH', 'D'): 'N',
        ('VH', 'N'): 'H',
        ('VH', 'W'): 'VH',
        ('VH', 'VW'): 'VH',
    }

    fuzzy_output = rule_map.get(
        (temperature_degree_fuzzy, humidity_level_fuzzy))

    if fuzzy_output is None:
        print("Case not covered for given input")
        return "No matchinf rule"
    else:
        return fuzzy_output


def power_in_watts(temperature_degree, humidity_level):
    if humidity_level < 1.0 or humidity_level > 10.0:
        print("Invalid value for humidity level : ", humidity_level)
        return "Invalid input"
    temp_degree_fuzzy = fuzzify_temperature(temperature_degree)
    humidity_level_fuzzy = fuzzify_humidity(humidity_level)
    power_amount_fuzzy = compute_fuzzy_power_amount(
        temp_degree_fuzzy, humidity_level_fuzzy)
    power_amount = defuzzify(power_amount_fuzzy)
    return power_amount
