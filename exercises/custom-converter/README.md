# Exercise 1: Implement a Custom Data Converter

During this exercise, you will: 

* Output typical payloads from a Temporal Workflow using the default Data Converters
* Implement a Custom Codec that encrypts Workflow output
* Implement a Failure Converter and demonstrate parsing its output

Make your changes to the code in the `practice` subdirectory (look for 
`TODO` comments that will guide you to where you should make changes to 
the code). If you need a hint or want to verify your changes, look at 
the complete version in the `solution` subdirectory.


## Part A: Implement a Custom Codec

1. You can supply a Custom Codec to your Data Converter in a single
   configuration parameter. The example in the Practice subdirectory of this
   exercise is missing that necessary change, meaning that you can run it out of
   the box, and produce JSON output using the Default Data Converter. You'll do
   this first, so you have an idea of the expected output. First, start the
   Worker:

   ```shell
   python worker.py
   ```

   Next, run the Workflow starter:

   ```shell
   python starter.py
   ```

   After that, you can use the `temporal` CLI to show the Workflow result:

   ```shell
   temporal workflow show -w encryption-workflow-id
   ```

   ```
   Progress:
     ID          Time                     Type
      1  2024-02-27T19:51:31Z  WorkflowExecutionStarted
      2  2024-02-27T19:51:31Z  WorkflowTaskScheduled
      3  2024-02-27T19:51:31Z  WorkflowTaskStarted
      4  2024-02-27T19:51:31Z  WorkflowTaskCompleted
      5  2024-02-27T19:51:31Z  WorkflowExecutionCompleted

   Result:
     Status: COMPLETED
     Output: ["Received Plain text input"]
   ```

   You should now have an idea of how this Workflow runs ordinarily — it outputs
   the string "Received Plain text input". In the next step, you'll add a Custom
   Codec.
2. To add a Custom Codec, you don't need to change anything in your Workflow
   code. You only need to add a `data_converter` parameter to `Client.connect()`
   where it is used in both `starter.py` and `worker.py`.
3. Next, take a look in `codec.py`. This contains the Custom Codec code you'll
   be using. The `encode()` function serializes a payload to string format, then
   compresses it Python's
   [cramjam](https://github.com/milesgranger/cramjam/tree/master/cramjam-python)
   library to provide `snappy` compression, wraps the compressed result in
   `bytes()`, and sets the file metadata. The `decode()` function should do the
   same thing in reverse. Add the missing calls to the `decode()` function (you
   can use the `encode()` function as a hint).
4. Now you can re-run the Workflow with your Custom Codec. Stop your Worker
   (with `Ctrl+C` in a blocking terminal) and restart it with `python
   worker.py`, then re-run the workflow with `python starter.py`. Finally,
   get the result again with `temporal workflow show -w encryption-workflow-id`.
   This time, your output will be encoded:

   ```
   ...
   Result:
     Status: COMPLETED
     Output: [encoding binary/snappy: payload encoding is not supported]
   ```

  The `payload encoding is not supported` message is normal — the Temporal
  Cluster itself can't use the `Decode` function directly without a Codec
  Server, which you'll create in the next exercise. In the meantime, you have
  successfully implemented Custom Data Conversion, and in the next step, you'll
  add another feature. 


## Part B: Implement a Failure Converter

1. The next feature you may add is a Failure Converter. Failure messages and
   stack traces are not encoded as codec-capable Payloads by default; you must
   explicitly enable encoding these common attributes on failures. If your
   errors might contain sensitive information, you can encrypt the message and
   stack trace by configuring the default Failure Converter to use your encoded
   attributes, in which case it moves your message and stack_trace fields to a
   Payload that's run through your codec. To do this, you add a
   `failure_converter_class` option to your `Client.connect()` call. Make this
   change to `client.Dial()` where it is used in both `starter.py` and
   `worker.py`, as you did before.
2. To test your Failure Converter, change your Workflow to return an artificial
   error. Change the `GreetingWorkflow()` in `worker.py` to throw an error where
   there isn't one, like so:

   ```python
   async def run(self, name: str) -> str:
      raise ApplicationError("This is designed to fail on purpose")
   ```

   Next, try re-running your Workflow, and it should fail.
3. Run `temporal workflow show -w encryption-workflow-id` to get the status of your
   failed Workflow. Notice that the `Failure:` field should now display an encoded
   result, rather than a plain text error:

   ```
   ...
   Status: FAILED
   Failure: &Failure{Message:Encoded failure,Source:PythonSDK,StackTrace:,Cause:nil,FailureType:Failure_ApplicationFailureInfo,}
   ```


### This is the end of the exercise.

