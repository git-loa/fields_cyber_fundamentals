
def format_query_url(query: str, year: str, site: str) -> str:
    url_string = ''
    #Your code here
    search_engine = f"https://www.google.com/search?&q="
    formatted_query = query.replace('%', '%25')
    formatted_query = formatted_query.replace('&', '%26').replace('?', '%3F').replace('/','%2F').replace(':','%3A').replace('=','%3D').replace('+', '%2B').replace(',', '%2C').replace(' ', '+')
    before_date = f"{year}/12/31".replace('/', '%2F')
    after_date = f"{year}/01/01".replace('/', '%2F')

    query_components = (
        formatted_query,
        "+site:",
        site,
        "+before:",
        before_date,
        "+after:",
        after_date,
    )

    url_string = ''.join(query_components).replace(':','%3A').replace(':','%3A')
    url_string = search_engine+url_string
    return url_string

# Test the function with the sample queries
queries = [
    ("Cybersecurity: threats, risks & challenges!", "2019", "wired.com"),
    ("Climate change impacts: causes & solutions", "2015", "bbc.com"),
    ("Quantum computing: advancements & applications", "2020", "scientificamerican.com"),
    ("Phishing attack examples: prevention & response", "2021", "krebsonsecurity.com"),
    ("Data science career opportunities: jobs & skills", "2018", "linkedin.com"),
    ("Artificial intelligence in healthcare: benefits & risks", "2017", "forbes.com"),
    ("Latest cybersecurity trends: 2022 overview", "2022", "darkreading.com"),
    ("Machine learning tutorials: beginners & advanced", "2021", "coursera.org"),
    ("Cloud computing security: best practices", "2020", "cloudsecurityalliance.org"),
    ("Big data analytics case studies: success stories", "2016", "dataversity.net")
]

for q, y, s in queries:
    print(format_query_url(q, y, s))

