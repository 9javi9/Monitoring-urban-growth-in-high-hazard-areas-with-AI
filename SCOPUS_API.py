API_KEY = 'Enter_your_API_key'
API_URL = 'https://api.elsevier.com/content/search/scopus'
CSV_NAME = "Name.csv"
def scopus_data(query, count=20, start=0):
    h = {
        'X-ELS-APIKey': API_KEY,
        'Accept': 'application/json'
    }
    p = {
        'query': query,
        'count': count,
        'start': start
    }
    response = requests.get(API_URL, headers=h, params=p)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: 
        {response.status_code}")
    return response.json()

def fetch_all_results(query, count=20):
    start = 0
    all_results = []
    while True:
        data = scopus_data(query, count, start)
        entries = data.get('search-results', {})
        .get('entry', [])
        if not entries:
            break
        all_results.extend(entries)
        start += count
    return all_results

# Define tus palabras claves
query = 'urban growth monitoring AND 
satellite imagery AND artificial intelligence'

# Busac toda la data
all_d = fetch_all_results(query)

# Define filtros
flt_cond = [
    lambda entry: '2013' <= entry
    .get('prism:coverDate', '')[:4] <= '2024',
    lambda entry: entry.get('subtypeDescription')=='Article'
]

def filter_and_store_results(entries, filter_conditions):
    filtered_entries = [entry for entry in entries 
    if all(condition(entry) 
    for condition in filter_conditions)]
    df = pd.DataFrame(filtered_entries)
    return df

# Almacena los resultados en un CSV
filtered_data = filter_and_store_results(all_d, flt_cond)
filtered_data.to_csv(NAME, index=False)
