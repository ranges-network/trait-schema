from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.utils.datautils import _get_context

import pandas as pd
import os
import click
from pyld import jsonld
import json


def schema_to_owl(schema:str) -> str:
    """generates an OWL representaiton of the linkml schema

    Args:
        schema (str): path to linkml schema file

    Returns:
        str: OWL/ttl representation of schema
    """
    gen_owl = OwlSchemaGenerator(schema, metaclasses=False)
    owl = gen_owl.serialize()

    return owl


def df_to_rdf(
        df: pd.DataFrame,
        schema: str, 
        
) -> str:
    """transforms dataframe into rdf

    Args:
        df (pd.DataFrame): pandas dataframe holding the data to be transformed
        schema (str): path to linkml schema file

    Returns:
        str: nquads/ttl representaiton of data
    """
    context = _get_context(schema) # generate jsonld context
    rdf = jsonld.to_rdf(
            {"@context": json.loads(context), "@graph": df.to_dict(orient="records")},
            {'format': 'application/n-quads'} # must use application/n-quad
    )        
    
    return rdf


def main(
        input:str, 
        schema:str, 
        output:str, 
        owl_output:str, 
        data_output:str
) -> None:
    """transforms the input file into RDF

    Args:
        input (str): input data file; types: csv|tsv|xlxs
        schema (str): linkml schema file (.yml or .yaml)
        output (str): file to save the RDF data and OWL schema
        owl_output (str): file to save only the OWL schema
        data_output (str): file to save only the RDF data

    Raises:
        Exception: if the extenstion of input data file is not recogized
    """
    # get owl represenation of schema
    if (output is not None) or (owl_output is not None):
        owl = schema_to_owl(schema)

    # file extension of input file
    if (output is not None) or (data_output is not None):
        file_ext = os.path.splitext(input)[-1]

        if file_ext == '.xlsx':
            df = pd.read_excel(input)
        elif file_ext == '.tsv':
            df = pd.read_table(input)
        elif file_ext == '.csv':
            df = pd.read_csv(input)
        else:
            raise Exception("Input file extension not recognized.")
        
        # transform data to ttl/nquads
        rdf = df_to_rdf(df, schema)

    # save owl and rdf
    if output is not None:
        with open(output,"w") as f:
            # f.write(g.serialize(format='ttl'))
            f.write(owl)
        
        with open(output, "a") as f:
            f.write(rdf)

    # save owl only
    if owl_output is not None:
        with open(owl_output, "w") as f:
            f.write(owl)
    
    # save rdf only
    if data_output is not None:
        with open(data_output, "w") as f:
            f.write(rdf)


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i', '--input', help="input data file; types: csv|tsv|xlxs")
@click.option('-s', '--schema', help="linkml schema file (.yml or .yaml)")
@click.option('-o', '--output', 
              help="output file for transformed RDF data and the OWL schema",
              default=None)
@click.option('-oo', '--owl-output', 
              help="output file for OWL schema", 
              default=None)
@click.option('-do', '--data-output', 
              help="output file for RDF data",
              default=None)
def cli(input, schema, output, owl_output, data_output):
    """transforms the input file into RDF"""
    # call main program
    main(input, schema, output, owl_output, data_output)


if __name__ == "__main__":
    cli()