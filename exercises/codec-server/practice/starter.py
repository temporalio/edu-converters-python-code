import asyncio
import dataclasses

import temporalio.converter
from temporalio.client import Client

from codec import EncryptionCodec
from worker import GreetingWorkflow


async def main():
    # Connect client
    client = await Client.connect(
        "localhost:7233",
        data_converter=dataclasses.replace(
            temporalio.converter.default(), payload_codec=EncryptionCodec(),
            failure_converter_class=temporalio.converter.DefaultFailureConverterWithEncodedAttributes,
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
