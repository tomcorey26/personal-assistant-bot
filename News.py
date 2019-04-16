import newspaper

def getTheNews(newsSource="http://www.bbc.com"):
    source = newspaper.build(newsSource, memoize_articles=False)

    articleTitles = []
    articleAuthors = []

    for i in range(3):
        article = source.articles[i]
        article.download()
        article.parse()
        articleTitles.append(article.title)
        articleAuthors.append(article.authors)
    
    articles = [articleTitles, articleAuthors]

    return articles