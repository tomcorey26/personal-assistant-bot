def main(food):
    from googlesearch import search
    from recipe_scrapers import scrape_me
    # google a recipe from allrecipes.com
    query = food + " allrecipes.com"
    # find the desired url
    url = ""
    for i in search(query, tld="com", num=1, stop=1, pause=2):
        url = i
    print("url: ", url)
    # assign scraper to this url
    scraper = scrape_me(url)
    # find the ingredients for the recipe and convert that into a string
    ingredients = str(scraper.ingredients())
    #remove brackets and add line breaks in the string to make it more readable
    ingredients = ingredients[(ingredients.index(",")+2):]
    ingredients = ingredients.replace(",", "\n") #replace commas with line breaks
    ingredients = ingredients.replace("®", "") #remove registered mark for speech purposes
    ingredients = ingredients.replace("[", "") #remove left bracket
    ingredients = ingredients.replace("]", "") #remove right bracket
    ingredients = ingredients.replace("'", "") #remove single quotes

    return ingredients