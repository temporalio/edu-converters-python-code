# Customizing the Composite Data Converter

This example shows how you can customize the Composite Data Converter by adding an additional Payload Converter. This sample uses the same logic as Exercise #1, but instead of providing a Custom Codec, it provides a new Payload Converter.

## Part A: Add an Additional Payload Converter to the Composite Converter

In `starter.py`, before the `main()` function block, a new Composite Data Converter is initialized as follows:

```python
class IPv4AddressPayloadConverter(temporalio.converter.CompositePayloadConverter):
    def __init__(self) -> None:
        # Just add ours as first before the defaults
        super().__init__(
            IPv4AddressEncodingPayloadConverter(),
            *temporalio.converter.DefaultPayloadConverter.default_encoding_payload_converters,
        )
```

This overrides the default Composite Converter (initialized as `DefaultPayloadConverter.default_encoding_payload_converters`), by prepending a new `IPv4AddressEncodingPayloadConverter()` that will run before the other Payload Converters.

## Part B: Using your customized Composite Converter

As with the Custom Codec example, you can customize your data conversion behaivior by adding a `data_converter` parameter to your `Client.connect()` call.

```python
client = await Client.connect(
    "localhost:7233",
    data_converter=dataclasses.replace(
        temporalio.converter.DataConverter.default, payload_converter_class=IPv4AddressPayloadConverter,
    ),
)
```

## Part C: Defining the Behavior of your new Payload Converter

In this sample, `codec.py` contains a complete implementation of a new Payload Converter. As mentioned, it incorporates `to_payload()` and `from_payload()` calls which perform the actual variable handling and serialization/deserialization to cast your specialized input -- in this case, the internal Python `ipaddress` type -- into a format that Temporal can store.

### This is the end of the sample.