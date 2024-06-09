DOCDIR = docs
SRC = src
SOURCE_SCHEMA_DIR = src/schema

# --- schema documentation --- #
gendoc: $(DOCDIR)
# copy existing files if they exist 
# note: there is no space after the ',' in ($(wildcard src/docs/*.md),)
# condition is the true if the wildcard returns non-empty content (i.e, not equal)
ifneq ($(wildcard src/docs/*.md),)
	cp src/docs/*.md docs/
endif
ifneq ($(wildcard src/docs/images/*.*),)
	cp src/docs/images/*.* docs/images 
endif
# generate documentation
	gen-doc -d $(DOCDIR) $(SOURCE_SCHEMA_DIR)/trait-value.yml

## remove docs
clean-docs:
# don't delete README files
	find docs/ -type f -not -name 'README.md' -delete     
	find docs/images/ -type f -not -name 'README.md' -delete     

# --- linkml products --- #
products: jsonld jsonld-context jsonschema owl shacl

jsonld:
	gen-jsonld $(SOURCE_SCHEMA_DIR)/trait-value.yml > jsonld/trait-value.jsonld

jsonld-context:
	gen-jsonld-context $(SOURCE_SCHEMA_DIR)/trait-value.yml > jsonld-context/trait-value.context.jsonld

jsonschema:
	gen-json-schema $(SOURCE_SCHEMA_DIR)/trait-value.yml > jsonschema/trait-value.schema.json

owl:
	gen-owl $(SOURCE_SCHEMA_DIR)/trait-value.yml > owl/trait-value.owl 

shacl:
	gen-shacl $(SOURCE_SCHEMA_DIR)/trait-value.yml > shacl/trait-value.shacl 

## remove products
clean-products:
# don't delete README files
	find jsonschema/ -type f -not -name 'README.md' -delete     
	find jsonld/ -type f -not -name 'README.md' -delete     
	find jsonld-context/ -type f -not -name 'README.md' -delete     
	find shacl/ -type f -not -name 'README.md' -delete     
	find owl/ -type f -not -name 'README.md' -delete     