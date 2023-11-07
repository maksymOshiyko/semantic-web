from SPARQLWrapper import SPARQLWrapper, JSON

endpoint = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
sparql = SPARQLWrapper(endpoint)
sparql.setQuery("""
SELECT DISTINCT ?companyLabel ?employeeCount
WHERE {
  ?company wdt:P31 wd:Q4830453 . 
  ?company wdt:P159/wdt:P131* wd:Q212 . 
  ?company wdt:P1128 ?employeeCount . 

  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" }
}
ORDER BY DESC(?employees)
""")

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
  companyName = result["companyLabel"]["value"]
  employeeCount = result["employeeCount"]["value"]
  print(f"{companyName} - {employeeCount}")