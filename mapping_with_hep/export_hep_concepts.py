'''
Created on 27 Jan 2012

@author: cgueret
'''
from surf import Store, Session, namespace

def export_csv():
	store = Store(reader='rdflib', writer='rdflib', rdflib_store='IOMemory')
	session = Session(store)
	print 'Load HEP data'
	store.load_triples(source='HEPont.rdf')
	Concept = session.get_class(namespace.SKOS['Concept'])
	all_concepts = Concept.all()
	print 'Found %d concepts' % (len(all_concepts))
	for concept in all_concepts:
		try:
			concept_uri = concept.subject
			concept_prefLabel = concept.skos_prefLabel.first
			print '%s;%s' % (concept_uri, concept_prefLabel)
		except:
			pass
		
if __name__ == '__main__':
	export_csv()
