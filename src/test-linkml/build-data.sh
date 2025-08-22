../scripts/spreadsheet-to-rdf.py -i ASUoccurrence-new-cols.csv -s ../schema/trait-value.yml > data.ttl
robot merge -i traitvalue.ttl -i data.ttl -o ranges-test-data.ttl