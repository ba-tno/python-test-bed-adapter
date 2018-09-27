import unittest
import sys
import json
sys.path.append("..")
from test_bed_adapter.registry.schema_registry import SchemaRegistry
from test_bed_adapter.options.test_bed_options import TestBedOptions
import logging
logging.basicConfig(level=logging.INFO)


class SchemaRegistryTest(unittest.TestCase):

    def test_schema_registry(self):
        options_file = open("config_files_for_testing/test_bed_options_for_tests_consumer.json", encoding="utf8")
        options = json.loads(options_file.read())
        options_file.close()

        test_bed_configuration = TestBedOptions(options)

        schema_registry = SchemaRegistry(test_bed_configuration)
        schema_registry.start_process()

        logging.info("\n\n---------------------\n\n")
        logging.info(schema_registry.keys_schema)
        logging.info(schema_registry.values_schema)
        self.assertGreater(len(schema_registry.keys_schema), 0)
        self.assertGreater(len(schema_registry.values_schema), 0)

if __name__ == '__main__':
    unittest.main()
