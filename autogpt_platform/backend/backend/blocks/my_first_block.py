import requests

from backend.data.block import Block, BlockCategory, BlockOutput, BlockSchema
from backend.data.model import SchemaField


class MyFirstBlock(Block):

    class Input(BlockSchema):
        topic: str = SchemaField(description="The topic to summarize")

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
        try:
            topic = input_data.topic
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"
            response = requests.get(url).json()
            yield "summary", response.get("extract", "No summary found.")
        except requests.exceptions.HTTPError as http_err:
            raise RuntimeError(f"Http error occurred: {http_err}")
