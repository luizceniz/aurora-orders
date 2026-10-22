"""aurora-orders worker.

Module 1 version: simulates processing in a loop. The Redis queue arrives in Module 2.

What already matters here is the graceful shutdown: Kubernetes sends SIGTERM before
killing a pod (rolling update, node drain, scale down). The worker finishes the current
order and exits cleanly instead of being cut in the middle of the work.
"""

import logging
import os
import signal
import socket
import time
from types import FrameType

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
log = logging.getLogger("worker")

POD = socket.gethostname()
PROCESSING_SECONDS = float(os.getenv("PROCESSING_SECONDS", "2"))

running = True


def handle_sigterm(signum: int, frame: FrameType | None) -> None:
    global running
    log.info("SIGTERM received on %s: finishing current order, then exiting", POD)
    running = False


def process_order(order_number: int) -> None:
    log.info("processing order #%d on %s", order_number, POD)
    time.sleep(PROCESSING_SECONDS)  # simulates stock check, shipping calculation, etc.
    log.info("order #%d processed", order_number)


def main() -> None:
    signal.signal(signal.SIGTERM, handle_sigterm)
    log.info("worker started on %s", POD)

    order_number = 0
    while running:
        order_number += 1
        process_order(order_number)

    log.info("worker stopped cleanly after %d orders", order_number)


if __name__ == "__main__":
    main()
