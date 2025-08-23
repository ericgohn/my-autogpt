import requests

from backend.data.block import Block, BlockCategory, BlockOutput, BlockSchema
from backend.data.model import SchemaField
from backend.util.request import Requests


class MyFirstBlock(Block):
    """
    Demo block
    """

    class Input(BlockSchema):
        topic: str = SchemaField(description="The topic to summarize, hahhahahaha")

    class Output(BlockSchema):
        summary: str = SchemaField(
            description="Sample text",
        )
        error: str = SchemaField(description="Sample output")

    def __init__(self):
        super().__init__(
            id="58befa6a-b071-42b0-99c1-53d5f970f1c1",
            description="My first block demo",
            categories={BlockCategory.BASIC},
            input_schema=MyFirstBlock.Input,
            output_schema=MyFirstBlock.Output,
            test_input={"topic": "Artificial Intelligence"},
            test_output=[
                ("summary", "AI is the simulation of human intelligence in machines.")
            ],
        )

    async def run(self, input_data: Input, **kwargs) -> BlockOutput:
        """
        Using the security Requests Wrapper
        https://dev-docs.agpt.co/platform/new_blocks/#using-the-secure-requests-wrapper
        """
        try:
            topic = input_data.topic
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"
            response = await Requests().get(url)
            data = response.json()
            yield "summary", data.get("extract", "No summary found.")
        except ValueError as e:
            raise RuntimeError(f"Invalid URL provided: {e}")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Request failed: {e}")
