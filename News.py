import newspaper

def FakeNews(party = "Democrat"):
    if party == "Democrat":
        fake = newspaper.build("http://www.cnn.com", memoize_articles=False)
    elif party == "Republican":
        fake = newspaper.build("http://www.foxnews.com", memoize_articles=False)
    else:
        fake = newspaper.build("http://www.bbc.com", memoize_articles=False)

    for i in range(5):
        article = fake.articles[i]
        print(article.title)
        print("Authors: ")
        for author in article.authors:
            print(author)

FakeNews()