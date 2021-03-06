import unittest
import sys
import json
import os
import logging
import datetime
import time
logging.basicConfig(level=logging.INFO)
sys.path += [".."]
from test_bed_adapter.options.test_bed_options import TestBedOptions
from test_bed_adapter import TestBedAdapter
from test_bed_adapter.services.time_service import milliseconds_since_epoch


class ProducerExample:
    @staticmethod
    def main(schema_topic, body, use_ssl):
        options = {
            "auto_register_schemas": True,
            # "kafka_host": 'driver-testbed.eu:3501',
            # "schema_registry": 'http://driver-testbed.eu:3502',
            "kafka_host": '127.0.0.1:3501',
            "schema_registry": 'http://localhost:3502',
            "fetch_all_versions": False,
            "from_off_set": True,
            "client_id": 'PYTHON TEST BED ADAPTER PRODUCER',
            "heartbeat_interval": 10,
            "produce": [schema_topic]
        }

        if use_ssl:
            options["use_ssl"] = True
            options["ca_file"] = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                              "sample-ssl-clients", "admin-tool-client-CARoot.pem")
            options["cert_file"] = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                "sample-ssl-clients", "admin-tool-client-certificate.pem")
            options["key_file"] = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                               "sample-ssl-clients", "admin-tool-client-key.pem")

        test_bed_options = TestBedOptions(options)
        test_bed_options.client_id = test_bed_options.client_id + "---" + str(datetime.datetime.now())
        test_bed_adapter = TestBedAdapter(test_bed_options)

        message = {"message": body}
        messages = 1 * [message]

        # This funcion will act as a handler. It only prints the message once it has been sent
        message_sent_handler = lambda message : logging.info("\n\n------\nmessage sent:\n------\n\n" + str(message))

        # Here we add the message to the test bed adapter
        test_bed_adapter.on_sent += message_sent_handler

        test_bed_adapter.initialize()
        test_bed_adapter.producer_managers[schema_topic].send_messages(messages)

        time.sleep(10)

        logging.info("Current date is %s" % test_bed_adapter.time_service.get_trial_date().strftime('%B %d %Y - %H:%M:%S'))
        logging.info("Current elapsed time is %d" % test_bed_adapter.time_service.get_trial_elapsed_time())

        test_bed_adapter.stop()


def parse_json_file(file_name):
    message_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "sample_messages",
                                file_name)
    example_message_file = open(message_path, encoding="utf-8")
    body = json.loads(example_message_file.read())
    example_message_file.close()
    return body


if __name__ == '__main__':
    # Test standard cap
    #ProducerExample().main("standard_cap",
    #                       parse_json_file("example_amber_alert.json"),
    #                       use_ssl=False)

    # Test system large data update
    # ProducerExample().main("system_large_data_update",
    #                        parse_json_file("example_system_large_data_update.json"),
    #                        use_ssl=False)

    # Test system timing
    time_dict = parse_json_file("example_system_timing.json")
    time_dict["updatedAt"] = 0 # milliseconds_since_epoch(datetime.datetime.now())
    time_dict["trialTime"] = 0 # milliseconds_since_epoch(datetime.datetime.now())
    ProducerExample().main("system_timing",
                           time_dict,
                           use_ssl=False)
