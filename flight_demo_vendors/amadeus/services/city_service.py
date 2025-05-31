from vendors.mongo_client import search_cities_by_keyword

def search_cities_by_keyword_service(keyword, from_param):
    return search_cities_by_keyword(keyword, from_param)