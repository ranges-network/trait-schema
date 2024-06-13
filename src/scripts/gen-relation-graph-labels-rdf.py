import click
from rdflib import Graph, RDFS, RDF, OWL, URIRef

def main(input:str, output:str) -> None:
    """Uses RDFLIB the extract labels from an ontology.
    Output is of the form <IRI> rdfs:label "label" .

    Args:
        input (str):  name of the ontology file to use
        output (str): name of file to save output
    """
    g = Graph()
    g.parse(input)

    g_labels = Graph()

    # add labels from source graph
    for triple in g.triples((None, RDFS.label, None)):
        if type(triple[0]) == URIRef:
            g_labels.add(triple)

    # add rdf:type assertions
    for triple in  g_labels.triples((None, None, None)):
        g_labels.add((triple[0], RDF.type, OWL.Class))
        g_labels.add((triple[0], RDF.type, OWL.NamedIndividual))

    # save labels graph
    g_labels.serialize(format='ttl', destination=output)
    
    
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i', '--input', help="name of input onotlogy file")
@click.option('-o', '--output', help="name of output file to save labels.")
def cli(input, output):
    """User RDFLIB to extract labels from ontologyh. 
    Output is of the form <IRI> rdfs:label "label" .
    """
    # call main program
    main(input, output)


if __name__ == "__main__":
    cli()