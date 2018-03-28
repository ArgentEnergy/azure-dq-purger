"""This module purges messages from a Azure service bus dead queue."""
import argparse
import logging

from azure.servicebus import ServiceBusService
import requests

# Turn on logging with level of info
logging.basicConfig(format="%(asctime)s %(levelname)s - %(message)s",
                    level=logging.INFO)
_LOGGER = logging.getLogger("purger")


def run(ins):
    """
    Entry point to the script to purge messages from the dead queue.
    :param ins: command line arguments provided to the script
    :type ins: dict
    """
    try:
        threshold = int(ins["threshold"])
        i = 0

        bus_kn = ins["bus_key_name"]
        bus_kv = ins["bus_key_value"]
        service = ServiceBusService(service_namespace=ins["namespace"],
                                    shared_access_key_name=bus_kn,
                                    shared_access_key_value=bus_kv)
        dead_queue = "{}/$DeadLetterQueue".format(ins["queue"])

        while i < threshold:
            # Gets and removes the message since peek_lock is False
            msg = service.receive_queue_message(dead_queue, peek_lock=False)
            if msg.body is None:
                break
            i += 1
    except ValueError:
        _LOGGER.exception("Received an invalid threshold!")
    except requests.exceptions.ConnectionError:
        _LOGGER.exception("Failed to connect to service bus!")


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("--namespace", required=True,
                        help="The service namespace.")
    PARSER.add_argument("--buskeyname", required=True,
                        help="The bus key name.")
    PARSER.add_argument("--buskeyvalue", required=True,
                        help="The bus key value.")
    PARSER.add_argument("--queue", required=True,
                        help="The queue to query the dead queue.")
    PARSER.add_argument("--get", required=True,
                        help="The amount of messages to retrieve.")
    ARGS = PARSER.parse_args()
    INPUTS = {
        "namespace": ARGS.namespace,
        "bus_key_name": ARGS.buskeyname,
        "bus_key_value": ARGS.buskeyvalue,
        "queue": ARGS.queue,
        "threshold": ARGS.get
    }
    run(INPUTS)
    _LOGGER.info("Finished")
