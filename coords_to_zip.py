from uszipcode import SearchEngine

search = SearchEngine(simple_zipcode=True)

zipcode = search.by_zipcode("02881")

zip_dict = zipcode.to_dict()

latitude = zip_dict["lat"]
longitude = zip_dict["lng"]
