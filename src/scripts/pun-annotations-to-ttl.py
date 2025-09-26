#!/usr/bin/env python3
"""Reads the annotations in a LinkML schema and converts punning annotations into OWL."""

import click
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.linkml_model.meta import \
    Definition, SlotDefinition, ClassDefinition, EnumDefinition, Annotation
from typing import Text


def parse_prefixes(view:SchemaView) -> Text:
    """Uses the schema view to create turtle prefixes.

    Args:
        view (SchemaView): SchemaView object

    Returns:
        Text: Sting containing turtle prefixes; e.g., "@prefix linkml: <https://w3id.org/linkml/> ."
    """
    ttl_str = ""
    prefix_dict = view.schema.prefixes

    # check for often used prefixes
    prefix_keys = prefix_dict.keys()
    if 'rdf' not in prefix_keys:
        ttl_str += "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n"
    if 'rdfs' not in prefix_keys:
        ttl_str += "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"
    if 'owl' not in prefix_keys:
        ttl_str += "@prefix owl: <http://www.w3.org/2002/07/owl#> .\n"
    if 'linkml' not in prefix_keys:
        ttl_str += "@prefix linkml: <https://w3id.org/linkml/> .\n"
    if 'skos' not in prefix_keys:
        ttl_str += "@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n"
    if 'xsd' not in prefix_keys:
        ttl_str += "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n"
    if 'obo' not in prefix_keys:
        ttl_str += "@prefix obo: <http://purl.obolibrary.org/obo/> .\n"

    # check the default prefix has been mapped to a uri
    # note: if the default prefix is not specified, it may be a uri
    if (view.schema.default_prefix not in prefix_keys) \
            and (view.schema.default_prefix[0:4] != 'http') : 
        
        # determine if '/' needs to be appended
        temp_uri = view.schema.id
        if temp_uri[-1] not in ['/', '#']:
            temp_uri += "/"
        ttl_str += f"@prefix {view.schema.default_prefix} <{temp_uri}> .\n"

    # build turle prefix statments
    for _, prefix_obj in prefix_dict.items(): 
        ttl_str += f"@prefix {prefix_obj.prefix_prefix}: <{prefix_obj.prefix_reference}> .\n"
    return ttl_str


def parse_element_uri(view:SchemaView, element:Definition, include_prefixes:bool) -> Text:
    """extract the URI from the schema element and inserts <> around the URI if necessary

    Args:
        view (SchemaView): schema view object
        element (Definition): schema element with the URI
        include_prefixes (bool): 
            flag that determines if prefixes created with output
            if true: CURIEs are used identifiers
            if false: full URIs are used as identifiers

    Returns:
        Text: element's URI
    """
    if include_prefixes:
        uri = view.get_uri(element, expand=False)
    else:
        uri = view.get_uri(element, expand=True)
    
    # check for 'http' uri
    if uri[0:4] == 'http':
        uri = f"<{uri}>"
    # print(view.get_uri(element, expand=True))
    return uri


def parse_annotation(annotation:Annotation, uri:Text) -> Text:
    """Finds the punning in the annotations and creates corresponding RDF statements for punning.

    Args:
        annotation (Annotation): the Annotation object for an element
        uri (Text): the URI of the element

    Returns:
        Text: turtle statements of the punning information specified by the annotations
    """
    ttl_str = ""

    # parse annotatons
    tag = annotation.tag.lower().strip()
    value = annotation.value.strip()
    if tag in ["pun_as"]:
        ttl_str += f"{uri} {value} . "
    if tag in ["pun_type"]:
        ttl_str += f"{uri} rdf:type {value} . "
    if tag in ["pun_subclass_of", "pun_subclassof", "pun_as_subclass", "pun_as_subclass_of", "pun_as_subclass"]:
        ttl_str += f"{uri} rdf:type owl:Class; rdfs:subClassOf {value} . "
    if tag in ["pun_subproperty_of", "pun_subpropertyof",  "pun_as_subproperty", "pun_as_subproperty_of",  "pun_as_subpropertyof"]:
        ttl_str += f"{uri} rdfs:subPropertyOf {value} . "

    return ttl_str


def parse_annotations(view:SchemaView, element:Definition, include_prefixes:bool) -> Text:
    """iterates over annotations defined for an element and created turtle statements as needed

    Args:
        view (SchemaView): schema view object
        element (Definition): the element being examined for annotations
        include_prefixes (bool): 
            flag that determines if prefixes created with output
            if true: CURIEs are used identifiers
            if false: full URIs are used as identifiers

    Returns:
        Text: turtle statements based on annotation informaton
    """
    # print('-----', type(element), type(element) == SlotDefinition)
    ttl_str = ""
    # return ttl_str
    uri = parse_element_uri(view, element, include_prefixes)

    # parse annotatons
    for _, annotation in element.annotations.items():
        ttl_str += parse_annotation(annotation, uri)
        if len(ttl_str) > 0:
            ttl_str += "\n" # add blank line for readabilty

    return ttl_str


def parse_slot_annotations(view:SchemaView, include_prefixes:bool) -> Text:
    """Uses schema view to create turtle from the slot annotations.

    Args:
        view (SchemaView): SchemaView object
        include_prefixes (bool): 
            flag that determines if prefixes created with output
            if true: CURIEs are used identifiers
            if false: full URIs are used as identifiers

    Returns:
        Text: String containing turtle for the slots.
    """
    ttl_str = ""
    slot_keys = view.all_slots().keys()

    for slot in slot_keys:
        element = view.get_slot(slot)
        
        ttl_str += parse_annotations(view, element, include_prefixes)
        if len(ttl_str) > 0:
            ttl_str += "\n" # add blank line for readabilty

    return ttl_str.rstrip()


def main(view:SchemaView, include_prefixes:bool):
    """Uses schema view to create turtle statements.

    Args:
        view (SchemaView): SchemaView object
        include_prefixes (bool): 
            flag that determines if prefixes created with output
            if true: CURIEs are used identifiers
            if false: full URIs are used as identifiers

    Returns:
        None: Output is the result of printing turtle statements.
    """
    if include_prefixes:
        prefixes_ttl = parse_prefixes(view)
        print(prefixes_ttl)

    annotations_ttl = parse_slot_annotations(view, include_prefixes)
    print(annotations_ttl)


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(
        help="""
        Reads the annotations in a LinkML schema (with a .yml or yaml extenstion) and converts punning annotations into OWL.\n
        e.g., pun-annotations-to-ttl.py myschema.yaml

        By default, the prefixes (e.g., "@prefix ex: <http://example.com#>") are output, and enities are identified using a CURIE (e.g., "ex:entity1").
        This is needed inorder to merge the output with other ontology files.

        To turn off this behavior, use the --no-include-prefixes flag, and entities are identified using the full URI (e.g., "<http://example.com#entity1>").
        """,
        context_settings=CONTEXT_SETTINGS)
@click.argument ('schema')
# @click.option('-s', '--schema', help="linkml schema file (.yml or .yaml) to parse")
@click.option('--include-prefixes/--no-include-prefixes',
              default=True,
              help="flag of whether to include prefixes [default: --include-prefixes]")
def cli(schema, include_prefixes): 
    view = SchemaView(schema) 
    main(view, include_prefixes)


if __name__ == "__main__":
    cli()