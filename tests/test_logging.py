from dpytools.logger.logger import DpLogger

def test_debug_no_arbitrary_data():
    """
    Test that we get the expected structure when constructing
    a debug log.
    """

    # test_mode=True returns the dictionary being logged
    # from the logging statement.
    logger = DpLogger("test-1", test_mode=True)
    logged_dict = logger.debug("Something")

    # Now that "logged_dict" contains the json fields
    # we need to compare them to a https://pypi.org/project/jsonschema/
    # of how a log of this kind should be populated.

    # Example log:
    # {"created_at": "2024-01-15T19:35:29.470825", "namespace": "test-1", "event": "Something", "trace_id": "not-implemented", "span_id": "not-implemented", "severity": 0, "data": {}}

    # Note:
    # Don't manually write json schemas
    # 1.) Use the logger
    # 2.) Careful check the logs match the spec
    # 3.) Use a site like this to get you started and tweak as needed:
    #      https://www.liquid-technologies.com/online-json-to-schema-converter

# Also write a test for:
# - logger.info
# - logger.warning

# And also
# - one of the above with arbitrary data key values
# - one of the above with a "raw" field
    
# Lastly for:
# - error
# - critical ("fatal" in go terms)
# but for these two remember you'd be passing in an error.
    
# And that's it, as long as the logger is constructing logging structures
# that validate against the json schemas we're done.
# NOTE: ignore hpp and auth fields for now, we'll pick those up later. 

    




