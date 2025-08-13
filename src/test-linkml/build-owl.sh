# convert schema to owl and merge with fovt
gen-owl ../schema/trait-value.yml > schema.tmp.ttl
robot merge -I http://purl.obolibrary.org/obo/fovt.owl -i  schema.tmp.ttl -o traitvalue.tmp.ttl 

# convert pun_as annotations to punning statements and merge with trait value ontology
pun-annotations-to-ttl.py ../schema/trait-value.yml > pun.tmp.ttl
robot merge -i traitvalue.tmp.ttl -i pun.tmp.ttl -o traitvalue.ttl