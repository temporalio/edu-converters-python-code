import asyncio
import dataclasses

import temporalio.converter
from temporalio.client import Client

from codec import IPv4AddressEncodingPayloadConverter
from worker import GreetingWorkflow

class IPv4AddressPayloadConverter(temporalio.converter.CompositePayloadConverter):
    def __init__(self) -> None:
        # Just add ours as first before the defaults
        super().__init__(
            IPv4AddressEncodingPayloadConverter(),
            *temporalio.converter.DefaultPayloadConverter.default_encoding_payload_converters,
        )

async def main():
    # Connect client
    client = await Client.connect(
        "localhost:7233",
        data_converter=dataclasses.replace(
            temporalio.converter.DataConverter.default, payload_converter_class=IPv4AddressPayloadConverter,
        ),
    )

    # Run workflow
    result = await client.execute_workflow(
        GreetingWorkflow.run,
        "Temporal",
        id=f"encryption-workflow-id",
        task_queue="encryption-task-queue",
    )

if __name__ == "__main__":
    asyncio.run(main())
