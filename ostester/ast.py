def FileMetadata(header, **kwargs):
    return {"header": header}


def FunctionTests(function_name, tests, metadata={}):
    return {"function": function_name,
            "tests": tests,
            "metadata": metadata}


def TestCase(declarations, test_arguments, comparison):
    return {"declarations": declarations,
            "arguments": arguments,
            "comparison": comparison}
