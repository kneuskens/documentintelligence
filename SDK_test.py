import logging
import requests
import time
from typing import Union, Dict
from config.settings import get_settings
from azure.core.credentials import AzureKeyCredential
# from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.ai.documentintelligence import DocumentIntelligenceClient

class DocumentIntelligenceService:
    """
    A service class for interacting with Azure Document Intelligence API.
    This class provides methods to analyze documents using Azure's Document Intelligence service.
    """

    def __init__(self):
        """
        Initialize the DocumentIntelligenceService with API credentials and endpoint.
        """
        settings = get_settings()
        self.key = settings.document_intelligence.api_key
        self.endpoint = settings.document_intelligence.endpoint
        self.api_version = "2024-02-29-preview"  # Currently only available in East US, West US2, and West Europe
        
        
endpoint=DocumentIntelligenceService().endpoint
Key=DocumentIntelligenceService().key
credential=AzureKeyCredential(Key)
document_analysis_client = DocumentIntelligenceClient(endpoint, credential)

path_to_sample_documents=r"C:\Users\kurt_\OneDrive\Documenten\temp\Senior QA Automation Engineer.pdf"

with open(path_to_sample_documents, "rb") as f:
    poller = document_analysis_client.begin_analyze_document(
        "prebuilt-document", document=f,output_content_format=ContentFormat.MARKDOWN
    )
result = poller.result()

for style in result.styles:
    if style.is_handwritten:
        print("Document contains handwritten content: ")
        print(",".join([result.content[span.offset:span.offset + span.length] for span in style.spans]))

print("----Key-value pairs found in document----")
for kv_pair in result.key_value_pairs:
    if kv_pair.key:
        print(
                "Key '{}' found within '{}' bounding regions".format(
                    kv_pair.key.content,
                    kv_pair.key.bounding_regions,
                )
            )
    if kv_pair.value:
        print(
                "Value '{}' found within '{}' bounding regions\n".format(
                    kv_pair.value.content,
                    kv_pair.value.bounding_regions,
                )
            )

for page in result.pages:
    print("----Analyzing document from page #{}----".format(page.page_number))
    print(
        "Page has width: {} and height: {}, measured with unit: {}".format(
            page.width, page.height, page.unit
        )
    )

    for line_idx, line in enumerate(page.lines):
        words = line.get_words()
        print(
            "...Line # {} has {} words and text '{}' within bounding polygon '{}'".format(
                line_idx,
                len(words),
                line.content,
                line.polygon,
            )
        )

        for word in words:
            print(
                "......Word '{}' has a confidence of {}".format(
                    word.content, word.confidence
                )
            )

    for selection_mark in page.selection_marks:
        print(
            "...Selection mark is '{}' within bounding polygon '{}' and has a confidence of {}".format(
                selection_mark.state,
                selection_mark.polygon,
                selection_mark.confidence,
            )
        )

for table_idx, table in enumerate(result.tables):
    print(
        "Table # {} has {} rows and {} columns".format(
            table_idx, table.row_count, table.column_count
        )
    )
    for region in table.bounding_regions:
        print(
            "Table # {} location on page: {} is {}".format(
                table_idx,
                region.page_number,
                region.polygon,
            )
        )
    for cell in table.cells:
        print(
            "...Cell[{}][{}] has content '{}'".format(
                cell.row_index,
                cell.column_index,
                cell.content,
            )
        )
        for region in cell.bounding_regions:
            print(
                "...content on page {} is within bounding polygon '{}'\n".format(
                    region.page_number,
                    region.polygon,
                )
            )
print("----------------------------------------")
