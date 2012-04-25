'''
Created on Mar 13, 2012

@author: cgueret
'''
from SPARQLWrapper import SPARQLWrapper, Wrapper
STORE='http://192.168.1.69:8080/openrdf-sesame/repositories/SW'

def get_pairs(infer):
	offset = 0
	limit = 100
	total_results = set()
	new_results = -1
	while new_results != 0:
		query_string = """
		PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
		SELECT DISTINCT ?s ?o WHERE {
		?s rdfs:subClassOf ?o.
		FILTER (?s != ?o)
		FILTER (?o != <http://www.w3.org/2000/01/rdf-schema#Resource>)
		} OFFSET %d LIMIT %d
		""" % (offset, limit)
		sparql = SPARQLWrapper(STORE)
		sparql.setReturnFormat(Wrapper.JSON)
		sparql.setQuery(query_string)
		sparql.addCustomParameter('infer', infer)
		results = sparql.query().convert()
		new_results = len(results["results"]["bindings"])
		for result in results["results"]["bindings"]:
			total_results.add((result['s']['value'], result['o']['value']))
		offset = offset + limit
	print "Downloaded %d relations" % len(total_results)
	return total_results


if __name__ == '__main__':
	pairs = get_pairs('true')
	pairs_explicit = get_pairs('false')
	res = []
	for pair in pairs:
		if pair not in pairs_explicit:
			res.append("%s\t%s" % pair)
	f = open('output.csv', 'w')
	for r in sorted(res):
		f.write(r)
		f.write('\n')
	f.close()
	
						