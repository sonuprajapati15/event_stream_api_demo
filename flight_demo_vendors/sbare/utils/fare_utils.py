from utils.random_utils import seat_types, cabin_classes, baggage_options, fare_classes, change_policies, wifi_availability, entertainment_options, cancellation_policies

def addComponent(base_price, component_and_per):
    result = {}
    total_price = base_price
    for key, value in component_and_per.items():
        result[key] = {
            "name": value["name"],
            "price": round(base_price * value.get("percent", 0) / 100, 2)
        }
        total_price +=round(base_price * value.get("percent", 0) / 100, 2)
    return {'components': result, 'total_price': total_price}

def forRecommeded(base_price, other_component=None):
    if other_component is None:
        other_component = {}
    fare_options = []
    component_and_per_1 = {
        'seat_types': {"name": seat_types[0], "percent": 0},
        'cabin_classes': {"name": cabin_classes[0], "percent": 0},
        'baggage_options': {"name": baggage_options[0], "percent": 0},
        'fare_classes': {"name": fare_classes[0], "percent": 0},
    }
    component_and_per_1.update(other_component)
    fare_options.append(addComponent(base_price, component_and_per_1))
    component_and_per_2 = {
        'change_policies': {"name": change_policies[0], "percent": 1},
        'wifi_availability': {"name": wifi_availability[0], "percent": 1},
        'fare_classes': {"name": fare_classes[1], "percent": 0},
    }
    component_and_per_2.update(other_component)
    component_and_per_1.update(component_and_per_2)
    fare_options.append(addComponent(base_price, component_and_per_1))
    fare_type = {
        'fareOptions': fare_options,
        'fareType': 'Recommended'
    }
    return fare_type

def forValueOne(base_price, other_component=None):
    if other_component is None:
        other_component = {}
    fare_options = []
    component_and_per_1 = {
        'seat_types': {"name": seat_types[1], "percent": 2},
        'cabin_classes': {"name": cabin_classes[1], "percent": 1},
        'cancellation_policies': {"name": cancellation_policies[0], "percent": 0},
        'baggage_options': {"name": baggage_options[1], "percent": 3},
        'wifi_availability': {"name": wifi_availability[1], "percent": 1},
        'fare_classes': {"name": fare_classes[2], "percent": 1},
    }
    component_and_per_1.update(other_component)
    fare_options.append(forRecommeded(base_price, component_and_per_1))
    component_and_per_2 = {
        'seat_types': {"name": seat_types[2], "percent": 4},
        'cabin_classes': {"name": cabin_classes[2], "percent": 2},
        'baggage_options': {"name": baggage_options[2], "percent": 6},
        'wifi_availability': {"name": wifi_availability[1], "percent": 1},
        'fare_classes': {"name": fare_classes[3], "percent": 2},
    }
    component_and_per_1.update(component_and_per_2)
    fare_options.append(forRecommeded(base_price, component_and_per_1))
    fare_type = {
        'fareOptions': fare_options,
        'fareType': 'Value One'
    }
    return fare_type

def forExpensiveOnbe(base_price, other_component=None):
    if other_component is None:
        other_component = {}
    fare_options = []
    component_and_per_1 = {
        'seat_types': {"name": seat_types[3], "percent": 8},
        'cabin_classes': {"name": cabin_classes[3], "percent": 6},
        'cancellation_policies': {"name": cancellation_policies[2], "percent": 7},
        'baggage_options': {"name": baggage_options[3], "percent": 3},
        'wifi_availability': {"name": wifi_availability[1], "percent": 1},
        'entertainment_options': {"name": entertainment_options[0], "percent": 2},
        'fare_classes': {"name": fare_classes[4], "percent": 5},
    }
    component_and_per_1.update(other_component)
    fare_options.append(forValueOne(base_price, component_and_per_1))
    component_and_per_2 = {
        'seat_types': {"name": seat_types[3], "percent": 8},
        'cabin_classes': {"name": cabin_classes[3], "percent": 6},
        'baggage_options': {"name": baggage_options[3], "percent": 8},
        'wifi_availability': {"name": wifi_availability[1], "percent": 1},
        'entertainment_options': {"name": entertainment_options[1], "percent": 5},
        'fare_classes': {"name": fare_classes[4], "percent": 5},
    }
    component_and_per_1.update(component_and_per_2)
    fare_options.append(forValueOne(base_price, component_and_per_1))
    component_and_per_3 = {
        'entertainment_options': {"name": entertainment_options[2], "percent": 6},
        'fare_classes': {"name": fare_classes[5], "percent": 7},
    }
    component_and_per_1.update(component_and_per_3)
    fare_options.append(forValueOne(base_price, component_and_per_1))
    fare_type = {
        'fareOptions': fare_options,
        'fareType': 'Expensive'
    }
    return fare_type