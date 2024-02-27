import asyncio
import dataclasses

import temporalio.converter
from temporalio.client import Client
from temporalio.common import RetryPolicy

from codec import EncryptionCodec
from worker import GreetingWorkflow


async def main():
    # Connect client
    client = await Client.connect(
        "localhost:7233",
		# Set data_converter here to ensure that workflow inputs and results are
		# encoded as required.
		# TODO Part A: Add a `data_converter` parameter here to use the
        # `EncryptionCodec()` from `data_converter.go`. This overrides the
        # stock behavior. Otherwise, the default data converter will be used.
        # It should look like this:
        # data_converter=dataclasses.replace(
		#   temporalio.converter.default(), payload_codec=EncryptionCodec()
	    # ),
		# TODO Part B: Set the `failure_converter_class` parameter within the
        # `data_converter` block from Part A to the value:
        # `temporalio.converter.DefaultFailureConverterWithEncodedAttributes`.
    )

    # Run workflow
    result = await client.execute_workflow(
        GreetingWorkflow.run,
        "Temporal",
        id=f"encryption-workflow-id",
        task_queue="encryption-task-queue"
    )

if __name__ == "__main__":
    asyncio.run(main())
