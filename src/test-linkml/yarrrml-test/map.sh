#!/bin/bash
# Usage:
# - run in the directory where this script is located
# - supply the YARRRML file as the one and only argument
#
# Example:
#   ./map.sh rules.yml

YARRRML_FILE=$1
RML_FILE=temp.rml.ttl

yarrrml-parser -i ${YARRRML_FILE} -o ${RML_FILE}
java -jar rmlmapper.jar -m ${RML_FILE}
