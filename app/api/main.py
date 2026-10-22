"""aurora-orders API.

Module 1 version: accepts orders and logs them. There is no database or queue yet,
so orders are not persisted. Postgres and Redis arrive in Module 2.
"""

import logging
import os
import socket
import uuid
from enum import StrEnum

from fastapi import FastAPI, status
from pydantic import BaseModel, Field

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
log = logging.getLogger("api")

APP_VERSION = os.getenv("APP_VERSION", "dev")
HOSTNAME = socket.gethostname()  # inside Kubernetes this is the pod name

app = FastAPI(title="aurora-orders API", version=APP_VERSION)


class OrderStatus(StrEnum):
    RECEIVED = "RECEIVED"
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"
    FAILED = "FAILED"


class OrderItem(BaseModel):
    sku: str = Field(min_length=1, examples=["COFFEE-500G"])
    qty: int = Field(gt=0, examples=[2])


class OrderIn(BaseModel):
    customer: str = Field(min_length=1, examples=["maria"])
    items: list[OrderItem] = Field(min_length=1)
    zip: str = Field(min_length=5, examples=["01001-000"])


class OrderAccepted(BaseModel):
    id: str
    status: OrderStatus
    served_by: str


@app.post("/orders", status_code=status.HTTP_202_ACCEPTED, response_model=OrderAccepted)
def create_order(order: OrderIn) -> OrderAccepted:
    order_id = str(uuid.uuid4())
    log.info("order received id=%s customer=%s items=%d", order_id, order.customer, len(order.items))
    return OrderAccepted(id=order_id, status=OrderStatus.RECEIVED, served_by=HOSTNAME)


@app.get("/healthz")
def healthz() -> dict[str, str]:
    """Liveness: answers only whether this process is alive."""
    return {"status": "ok"}


@app.get("/version")
def version() -> dict[str, str]:
    return {"version": APP_VERSION, "pod": HOSTNAME}
