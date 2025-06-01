from utils.random_utils import seat_types, cabin_classes, baggage_options, fare_classes, change_policies, \
    wifi_availability, entertainment_options, cancellation_policies


def addComponent(base_price, component_and_per):
    result = {}
    total_price = base_price
    for key, value in component_and_per.items():
        result[key] = {
            "name": value["name"],
            "price": round(base_price * value.get("percent", 0) / 100, 2)
        }
        total_price += round(base_price * value.get("percent", 0) / 100, 2)
    return {'components': result, 'total_price': total_price}


def forRecommeded(base_price, other_component=None):
    if other_component is None:
        other_component = {}
    fare_options = []
    # Option 1
    comp1 = {
        'seat_types': {"name": seat_types[0], "percent": 0},
        'cabin_classes': {"name": cabin_classes[0], "percent": 0},
        'baggage_options': {"name": baggage_options[0], "percent": 0},
        'fare_classes': {"name": fare_classes[0], "percent": 0},
    }
    comp1.update(other_component)
    fare_options.append(addComponent(base_price, comp1))
    # Option 2
    comp2 = {
        'change_policies': {"name": change_policies[0], "percent": 1},
        'wifi_availability': {"name": wifi_availability[0], "percent": 1},
        'fare_classes': {"name": fare_classes[1], "percent": 0},
    }
    comp2.update(other_component)
    fare_options.append(addComponent(base_price, comp2))
    return {
        'fareOptions': fare_options,
        'fareType': 'Recommended',
        'image': 'https://s1.travix.com/blog/ai/airplane-multiple-seats-small.jpg'
    }

def forValueOne(base_price, other_component=None):
    if other_component is None:
        other_component = {}
    fare_options = []
    # Option 1
    comp1 = {
        'seat_types': {"name": seat_types[1], "percent": 2},
        'cabin_classes': {"name": cabin_classes[1], "percent": 1},
        'cancellation_policies': {"name": cancellation_policies[0], "percent": 0},
        'baggage_options': {"name": baggage_options[1], "percent": 3},
        'wifi_availability': {"name": wifi_availability[1], "percent": 1},
        'fare_classes': {"name": fare_classes[2], "percent": 1},
    }
    comp1.update(other_component)
    fare_options.append(addComponent(base_price, comp1))
    # Option 2
    comp2 = {
        'seat_types': {"name": seat_types[2], "percent": 4},
        'cabin_classes': {"name": cabin_classes[2], "percent": 2},
        'baggage_options': {"name": baggage_options[2], "percent": 6},
        'wifi_availability': {"name": wifi_availability[1], "percent": 1},
        'fare_classes': {"name": fare_classes[3], "percent": 2},
    }
    comp2.update(other_component)
    fare_options.append(addComponent(base_price, comp2))
    return {
        'fareOptions': fare_options,
        'fareType': 'Value One',
        'image': 'https://s1.travix.com/blog/et/etihad-airways-economy-small.jpg'
    }

def forExpensiveOnbe(base_price, other_component=None):
    if other_component is None:
        other_component = {}
    fare_options = []
    # Option 1
    comp1 = {
        'seat_types': {"name": seat_types[3], "percent": 8},
        'cabin_classes': {"name": cabin_classes[3], "percent": 6},
        'cancellation_policies': {"name": cancellation_policies[2], "percent": 7},
        'baggage_options': {"name": baggage_options[3], "percent": 3},
        'wifi_availability': {"name": wifi_availability[1], "percent": 1},
        'entertainment_options': {"name": entertainment_options[0], "percent": 2},
        'fare_classes': {"name": fare_classes[4], "percent": 5},
    }
    comp1.update(other_component)
    fare_options.append(addComponent(base_price, comp1))
    # Option 2
    comp2 = {
        'seat_types': {"name": seat_types[3], "percent": 8},
        'cabin_classes': {"name": cabin_classes[3], "percent": 6},
        'baggage_options': {"name": baggage_options[3], "percent": 8},
        'wifi_availability': {"name": wifi_availability[1], "percent": 1},
        'entertainment_options': {"name": entertainment_options[1], "percent": 5},
        'fare_classes': {"name": fare_classes[4], "percent": 5},
    }
    comp2.update(other_component)
    fare_options.append(addComponent(base_price, comp2))
    # Option 3
    comp3 = {
        'entertainment_options': {"name": entertainment_options[2], "percent": 6},
        'fare_classes': {"name": fare_classes[5], "percent": 7},
    }
    comp3.update(other_component)
    fare_options.append(addComponent(base_price, comp3))
    return {
        'fareOptions': fare_options,
        'fareType': 'Expensive',
        'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRahR9JwFnrjOC5ozRgjajNvIJIiO_RKjnrrg&s'
    }