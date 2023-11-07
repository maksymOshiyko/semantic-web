from rdflib import Graph
from collections import defaultdict

graph = Graph()
graph.parse('countrues_info.ttl')

popQuery = """
SELECT ?country ?population
WHERE {
    ?country :country_name ?countryName.
    ?country :population ?population.
}
"""
countryDictionary = defaultdict(int)
for row in graph.query(popQuery):
  countryDictionary[row['country']] = int(row['population'])

continentQuery = """
SELECT ?country ?continent
WHERE {
  ?country :country_name ?countryName.
  ?country :part_of_continent ?continent.
  ?continent :continent_name ?continentName.
}
"""
continentDictionary = defaultdict(list)
for row in graph.query(continentQuery):
  continentDictionary[row['continent']].append((row['country'], countryDictionary[row['country']]))

fiveCountriesByContinent = {}
countriesToSelect = 5
for continent, countries in continentDictionary.items():
  countries.sort(key=lambda x: x[1], reverse=True)
  fiveCountriesByContinent[continent] = countries[:countriesToSelect]

for continentURI, fiveCountries in fiveCountriesByContinent.items():
    continentNameQuery = f"""
    SELECT ?continentName
    WHERE {{
        <{continentURI}> :continent_name ?continentName.
    }}
    """
    for row in graph.query(continentNameQuery):
      name = row['continentName']
      print(name)
    for countryURI, pop in fiveCountries:
      countryNameQuery = f"""
      SELECT ?countryName
      WHERE {{
          <{countryURI}> :country_name ?countryName .
      }}
      """
      for row in graph.query(countryNameQuery):
        name = row['countryName']
        print(f"{name} - {pop}")