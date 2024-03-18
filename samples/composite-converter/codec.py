from temporalio.api.common.v1 import Payload
from temporalio.converter import EncodingPayloadConverter
import ipaddress

class IPv4AddressEncodingPayloadConverter(EncodingPayloadConverter):
    @property
    def encoding(self) -> str:
        return "text/ipv4-address"

    def to_payload(self, value):
        if isinstance(value, ipaddress.IPv4Address):
            return Payload(
                metadata={"encoding": self.encoding.encode()},
                data=str(value).encode(),
            )
        else:
            return None

    def from_payload(self, payload: Payload):
        assert type(payload) is ipaddress.IPv4Address
        return ipaddress.IPv4Address(payload.data.decode())