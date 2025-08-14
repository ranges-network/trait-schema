from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.utils.datautils import _get_context

import pandas as pd
import os
import click
from typing import List

def check_obo(iri:str) -> str:
    """checks if iri begins with "obo:"
    if so, "obo:" is replaced with "http://purl.obolibary.org/obo"

    Args:
        iri (str): IRI formated as string

    Returns:
        str: iri with replaced obo namespace if needed
    """
    iri = iri.strip()
    if iri.startswith('obo:'):
        iri = f"<{iri.replace('obo:', 'http://purl.obolibrary.org/obo/', 1)}>"
    return iri


def load_df(input:str)->pd.DataFrame:
    """Create pandas datafame from input path.

    Args:
        iput (str): path to data

    Raises:
        Exception: if the input file extension is not recognized

    Returns:
        pd.DataFrame: data loaded into a pandas dataframe
    """ 

    file_ext = os.path.splitext(input)[-1]

    if file_ext == '.xlsx':
        df = pd.read_excel(input)
    elif file_ext == '.tsv':
        df = pd.read_table(input)
    elif file_ext == '.csv':
        df = pd.read_csv(input)
    else:
        raise Exception("Input file extension not recognized.")
    
    return df

def prefixes_to_ttl(prefixes:str) -> List:
    """generates prefixes as turtle
    input file 

    Args:
        prefixes (str): path to tabular prefixes file

    Returns:
        List: list of prefixes formatted as turtle
    """
    ttl_list = []

    df = load_df(prefixes)
    for idx in range(len(df)):
        prfx:str = str(df.iloc[idx, 0]).strip()  # prefix
        iri:str = str(df.iloc[idx, 1]).strip() # IRI mapped to prefix

        if iri.startswith('<'):
            ttl = f"@prefix {prfx}: {iri} . \n"
        else:
            ttl = f"@prefix {prfx}: <{iri}> . \n"
        ttl_list.append(ttl)

    return ttl_list


def df_to_rdf(df:pd.DataFrame) -> List:
    """transforms dataframe into rdf

    Args:
        df (pd.DataFrame): pandas dataframe holding the data to be transformed

    Returns:
        List: list of turtle representation of data
    """

    ttl_list = []
    for idx in range(len(df)):
        subject = check_obo(df.iloc[idx, 0])
        predicate = check_obo(df.iloc[idx, 1])
        object = check_obo(df.iloc[idx, 2])

        rdf = f"{subject} {predicate} {object} . \n"
        ttl_list.append(rdf)

    return ttl_list


def main(input:str, prefixes:str=None, output:str=None)-> None:
    """transforms a tabluar file with headers "subject", "predicate", "object" to turtle

    Args:
        input (str): input tabular data file; types: csv|tsv|xlxs
        prefixes (str): path to prefixes file
        output (str): file to save the turtle
    Raises:
        Exception: if the extension of input data file is not recogized
    """
    # get prefixes
    if prefixes is not None:
        prfxs = prefixes_to_ttl(prefixes)

    df = load_df(input)
    statments = df_to_rdf(df)

    # save turtle
    if output is not None:
        with open(output,"w") as f:
            if prefixes is not None and len(prfxs) > 0:
                for prfx in prfxs:
                    f.write(prfx)
        
            if len(statments) > 0:
                for ttl in statments:
                    f.write(ttl)
    else:
        if prefixes is not None and len(prfxs) > 0:
            print(*prfxs, '\n', sep='')
        if len(statments) > 0:
            print(*statments, sep='')



CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i', '--input', help="input tabular data file; types: csv|tsv|xlxs")
@click.option('-p', '--prefixes', 
              help="tabular file containing the prefix information",
              default=None)
@click.option('-o', '--output', 
              help="output file for for the turtle.",
              default=None)
def cli(input, prefixes, output):
    """transforms a tabluar file with headers "subject", "predicate", "object" to turtle
    
    e.g.: python spo-table-to-ttl.py -i input.csv -p prefixes.csv -o out.ttl   
    """
    # call main program
    main(input, prefixes, output)


if __name__ == "__main__":
    cli()