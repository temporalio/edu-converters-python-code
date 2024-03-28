import asyncio
import dataclasses
from datetime import timedelta

import temporalio.converter
from temporalio import workflow
from temporalio.client import Client
from temporalio.worker import Worker
from temporalio.exceptions import ApplicationError

from codec import EncryptionCodec


@workflow.defn(name="Workflow")
class GreetingWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        # TODO Part B: Raise an ApplicationError before returning output here.
        return f"Hello, {name}"


interrupt_event = asyncio.Event()


async def main():
    # Connect client
    client = await Client.connect(
        "localhost:7233",
		# Set data_converter here to ensure that workflow inputs and results are
		# encoded as required.
		# TODO Part A: Add a `data_converter` parameter here to use the
        # `EncryptionCodec()` from `codec.py`. This overrides the stock
        # behavior. Otherwise, the default data converter will be used.
        # It should look like this:
        # data_converter=dataclasses.replace(
		#   temporalio.converter.default(), payload_codec=EncryptionCodec()
	    # ),
		# TODO Part B: Set the `failure_converter_class` parameter within the
        # `data_converter` block from Part A to the value:
        # `temporalio.converter.DefaultFailureConverterWithEncodedAttributes`.
    )

    # Run a worker for the workflow
    async with Worker(
        client,
        task_queue="encryption-task-queue",
        workflows=[GreetingWorkflow],
    ):
        # Wait until interrupted
        print("Worker started, ctrl+c to exit")
        await interrupt_event.wait()
        print("Shutting down")


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        interrupt_event.set()
        loop.run_until_complete(loop.shutdown_asyncgens())
