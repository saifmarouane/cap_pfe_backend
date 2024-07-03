import time

from kittycad.api.ai import create_text_to_cad, get_text_to_cad_model_for_user
from kittycad.client import ClientFromEnv
from kittycad.models.api_call_status import ApiCallStatus
from kittycad.models.file_export_format import FileExportFormat
from kittycad.models.text_to_cad_create_body import TextToCadCreateBody
import os
os.environ['KITTYCAD_API_TOKEN'] = '018e3c81-5e1a-79af-81bd-e22025157d64'
# Create our client.
client = ClientFromEnv()



def kittycad_prompt(prompt):
    # Prompt the API to generate a 3D model from text.
    response = create_text_to_cad.sync(
        client=client,
        output_format=FileExportFormat.STEP,
        body=TextToCadCreateBody(
            prompt=prompt,
        ),
    )

    # Polling to check if the task is complete
    while response.completed_at is None:
        # Wait for 5 seconds before checking again
        time.sleep(5)

        # Check the status of the task
        response = get_text_to_cad_model_for_user.sync(
            client=client,
            id=response.id,
        )

    if response.status == ApiCallStatus.FAILED:
        # Print out the error message
        print(f"Text-to-CAD failed: {response.error}")

    elif response.status == ApiCallStatus.COMPLETED:
        # Print out the names of the generated files
        print(f"Text-to-CAD completed and returned {len(response.outputs)} files:")
        for name in response.outputs:
            print(f"  * {name}")

        # Save the STEP data as text-to-cad-output.step
        final_result = response.outputs["source.step"]
        with open("text-to-cad-output.step", "w", encoding="utf-8") as output_file:
            output_file.write(final_result.get_decoded().decode("utf-8"))
            print(f"Saved output to {output_file.name}")
