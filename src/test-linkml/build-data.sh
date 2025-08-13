../scripts/spreadsheet-to-rdf.py -i ASUoccurrence-reduced-100.csv -s traitvalue-test.yml > data.ttl
robot merge -i traitvalue.ttl -i data.ttl -o ranges-data.ttl