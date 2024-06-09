from linkml.generators.owlgen import OwlSchemaGenerator
import pandas as pd
import yaml
import os
from pyld import jsonld
import json

from linkml_runtime.utils import inference_utils
from linkml_runtime.utils.compile_python import compile_python
from linkml_runtime.utils.inference_utils import infer_all_slot_values
from linkml_runtime.utils.schemaview import SchemaView

from linkml._version import __version__
from linkml.generators.pythongen import PythonGenerator
from linkml.utils import datautils, validation
from linkml.utils.datautils import (
    _get_context,
    _get_format,
    _is_xsv,
    dumpers_loaders,
    get_dumper,
    get_loader,
    infer_index_slot,
    infer_root_class,
)

def json_to_yml(json_):
    j = yaml.safe_load(json_)
    return yaml.dump(j, sort_keys=False)


def main(
        input='./r2.yml', schema='./tv2.yml', 
        # input='./top2.csv', schema='./tv3.yml', 
        input_format='yml', 
        output_format='ttl',
) -> None:
    
    # generate owl to be used with rdf
    gen_owl = OwlSchemaGenerator(schema)
    owl = gen_owl.serialize()

    file_ext = os.path.splitext(input)[-1] # determine file extension

    if file_ext == '.csv':
        df = pd.read_csv(input)
        context = _get_context(schema)
        rdf = jsonld.to_rdf(
                {"@context": json.loads(context), "@graph": df.to_dict(orient="records")},
                {'format': 'application/n-quads'} # must use application/n-quad
        )           
        return rdf
    else:
        # set variables needed for conversion
        sv = SchemaView(schema)
        python_module = PythonGenerator(schema).compile_module()
        target_class = infer_root_class(sv)
        py_target_class = python_module.__dict__[target_class]
        
        
        # create loader and dumper
        loader = get_loader(input_format)
        dumper = get_dumper(output_format)
        
        # set in/out args needed by loader and dumber
        inargs, outargs = {}, {}
        inargs["fmt"] = input_format
        inargs["schema"] = schema
        inargs["schemaview"] = sv
        outargs["schemaview"] = sv
                
        obj = loader.load(source=input, target_class=py_target_class, **inargs)
        return dumper.dumps(obj, **outargs)

    



if __name__ == "__main__":
    print(main())