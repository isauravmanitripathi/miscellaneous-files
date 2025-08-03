The code `extract-bullet-point-json.py` will create this json structure:
```json
// 1. INDIVIDUAL EXTRACTED FILES (extracted_filename.json)
// One file per original JSON file
{
  "extraction_info": {
    "source_file": "original_wikipedia_file.json",
    "extraction_timestamp": "2025-08-02T10:30:45.123456",
    "total_sections_in_source": 25,
    "extracted_sections_count": 18,
    "skipped_sections_count": 7
  },
  "sections": [
    {
      "section_number": "1.1",
      "section_name": "Introduction",
      "chapter_name": "Overview",
      "chapter_id": "chapter_1",
      "openai_summarised_points": [
        "• First comprehensive bullet point with key facts and details",
        "• Second bullet point with specific numbers, dates, and statistics",
        "• Third bullet point mentioning organizations, people, and places",
        "• Additional bullet points preserving all substantial information"
      ],
      "metadata": {
        "processed_timestamp": "2025-08-02T10:25:30.789012",
        "openai_model": "gpt-4.1-mini",
        "bullet_points_count": 4
      },
      "source_file": "original_wikipedia_file.json",
      "original_index": 0
    },
    {
      "section_number": "1.2",
      "section_name": "History",
      "chapter_name": "Overview", 
      "chapter_id": "chapter_1",
      "openai_summarised_points": [
        "• Historical development and key milestones",
        "• Important figures and their contributions",
        "• Major events and their impact on the field"
      ],
      "metadata": {
        "processed_timestamp": "2025-08-02T10:26:15.456789",
        "openai_model": "gpt-4.1-mini",
        "bullet_points_count": 3
      },
      "source_file": "original_wikipedia_file.json",
      "original_index": 2
    }
    // ... more sections
  ]
}

// 2. MASTER INDEX FILE (master_index.json)
// Summary of all processed files
{
  "extraction_summary": {
    "extraction_timestamp": "2025-08-02T10:35:00.000000",
    "source_folder": "/path/to/enhanced/json/folder",
    "total_files_processed": 5,
    "total_sections_extracted": 87,
    "total_sections_skipped": 23
  },
  "files": [
    {
      "filename": "wikipedia_file_1.json",
      "extracted_filename": "extracted_wikipedia_file_1.json",
      "sections_count": 18,
      "extraction_info": {
        "source_file": "wikipedia_file_1.json",
        "extraction_timestamp": "2025-08-02T10:30:45.123456",
        "total_sections_in_source": 25,
        "extracted_sections_count": 18,
        "skipped_sections_count": 7
      }
    },
    {
      "filename": "wikipedia_file_2.json",
      "extracted_filename": "extracted_wikipedia_file_2.json", 
      "sections_count": 22,
      "extraction_info": {
        "source_file": "wikipedia_file_2.json",
        "extraction_timestamp": "2025-08-02T10:32:10.654321",
        "total_sections_in_source": 30,
        "extracted_sections_count": 22,
        "skipped_sections_count": 8
      }
    }
    // ... more files
  ]
}

// 3. FLAT DATASET FILE (flat_dataset.json)
// All sections from all files combined in one place
{
  "dataset_info": {
    "creation_timestamp": "2025-08-02T10:35:00.000000",
    "total_sections": 87,
    "source_folder": "/path/to/enhanced/json/folder",
    "description": "Flat dataset containing all extracted Wikipedia sections with AI summaries"
  },
  "sections": [
    {
      "section_number": "1.1",
      "section_name": "Introduction", 
      "chapter_name": "Overview",
      "chapter_id": "chapter_1",
      "openai_summarised_points": [
        "• Comprehensive bullet point from file 1",
        "• Another detailed bullet point with facts",
        "• Final bullet point with specific information"
      ],
      "metadata": {
        "processed_timestamp": "2025-08-02T10:25:30.789012",
        "openai_model": "gpt-4.1-mini", 
        "bullet_points_count": 3
      },
      "source_file": "wikipedia_file_1.json",
      "original_index": 0
    },
    {
      "section_number": "2.1",
      "section_name": "Methodology",
      "chapter_name": "Research Methods",
      "chapter_id": "chapter_2", 
      "openai_summarised_points": [
        "• Research methodology and approach details",
        "• Data collection techniques and procedures",
        "• Analysis methods and statistical approaches"
      ],
      "metadata": {
        "processed_timestamp": "2025-08-02T10:26:45.123456",
        "openai_model": "gpt-4.1-mini",
        "bullet_points_count": 3
      },
      "source_file": "wikipedia_file_1.json", 
      "original_index": 5
    },
    {
      "section_number": "1.1",
      "section_name": "Background",
      "chapter_name": "Introduction",
      "chapter_id": "chapter_1",
      "openai_summarised_points": [
        "• Background information from second file",
        "• Context and historical perspective", 
        "• Relevant prior research and findings"
      ],
      "metadata": {
        "processed_timestamp": "2025-08-02T10:28:20.987654",
        "openai_model": "gpt-4.1-mini",
        "bullet_points_count": 3
      },
      "source_file": "wikipedia_file_2.json",
      "original_index": 0
    }
    // ... ALL sections from ALL files (87 total in this example)
  ]
}

```

Now once the generation of questions are done, the output json structure will look like this  