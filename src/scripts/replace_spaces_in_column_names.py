import os
import click
import pandas as pd

def replace_spaces_in_column_names(
        df:pd.DataFrame,
        replace_char="_"
) -> pd.DataFrame:
    double_char = replace_char + replace_char
    df.columns = df.columns.str.replace('  ', ' ') # replace double spaces
    df.columns = df.columns.str.replace(' ', replace_char)

    # remove odd cases when replace char gets doubled
    df.columns = df.columns.str.replace(double_char, replace_char)
    
    return df

@click.command()
@click.option('-i', '--input', help="input file")
@click.option('-o', '--output', help="output file")
@click.option('-r', '--replace-char', help="char to replace space; default: '_'", default="_")
def cli(input, output, replace_char):
    """replaces spaces in the column names of the input file with the replace-char"""
    # file extension of input file
    file_ext = os.path.splitext(input)[-1]

    if file_ext == '.xlsx':
        df = pd.read_excel(input)
    elif file_ext == '.tsv':
        df = pd.read_table(input)
    elif file_ext == '.csv':
        df = pd.read_csv(input)
    else:
        raise Exception("Input file extension not recognized.")
    
    df = replace_spaces_in_column_names(df, replace_char)

    # file extension of output
    file_ext = os.path.splitext(output)[-1]

    if file_ext == '.xlsx':
        df.to_excel(output, index=False)
    elif file_ext == '.tsv':
        df.to_csv(output, sep='\t')
    elif file_ext == '.csv':
        df.to_csv(output, index=False)
    else:
        raise Exception("Output file extension not recognized.")
    
if __name__ == "__main__":
    cli()