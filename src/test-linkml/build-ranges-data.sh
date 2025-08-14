echo "** build OWL file from schema **"
build-owl.sh

echo "** translating data into RDF and merging with OWL file **"
build-data.sh