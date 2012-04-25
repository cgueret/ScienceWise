#!/bin/bash

# Remove previous data
rm -f triples.nt

# Export data using the mappings
for mapping in 'articles' 'concepts' 'authors'; do
	~/tmp/d2r-server-0.7/dump-rdf -m sw-mapping-$mapping.n3 -b http://data.sciencewise.info/ >> triples.nt
done

# Add the ontology
rapper -i guess -o ntriples sw-vocabulary.owl >> triples.nt

# Export the data to OWLIM (use verbose to force closing the connection at the end)
curl -v -T triples.nt -H "Content-Type: text/plain;charset=UTF-8" http://localhost:8080/openrdf-sesame/repositories/SW/statements

