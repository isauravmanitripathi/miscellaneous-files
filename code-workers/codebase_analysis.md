# Codebase Analysis Report

**Generated:** 2025-08-04 14:39:32
**Codebase:** `/Users/sauravtripathi/Downloads/auto-reel-video-gen`
**Root Hash:** `a9c8c5b9297d9b9b8d8ea35aa0833fd2475bf9a102f75cb15ae13b7cebd50b7c`

## 📊 Overview

- **Total Files:** 47
- **Total Code Entities:** 2817
  - Classs: 80
  - Functions: 645
  - Imports: 563
  - Variables: 1529

## 📁 File Structure

```
auto-reel-video-gen/
├── insta-download/
│   └── batch_video_normalizer.py [de2abade]
│   └── combine-video.py [de2abade]
│   └── download-insta.py [de2abade]
│   └── file-processor.py [de2abade]
│   └── image-to-video.py [de2abade]
│   └── image-video-encoder.py [de2abade]
│   └── insta-download.py [de2abade]
│   └── pinterest-download.py [de2abade]
├── insta-download/text-video-detection/
│   └── detect-text.py [7e8fceb2]
│   └── easy-text-detection.py [7e8fceb2]
├── src/processors/
│   └── __init__.py [04b1385e]
│   └── audio_processor.py [de2abade]
│   └── canvas_processor.py [de2abade]
│   └── image_processor.py [de2abade]
│   └── mixed_media_processor.py [de2abade]
│   └── multiple_image_processor.py [de2abade]
│   └── sequential_timing.py [eada0f80]
│   └── sound_effects_processor.py [de2abade]
│   └── split_screen_processor.py [3951e41b]
│   └── subtitle_design_manager.py [23996b74]
│   └── subtitle_processor.py [de2abade]
│   └── subtitle_video_processor.py [ff3e4d4d]
│   └── video_filter_processor.py [de2abade]
│   └── video_formatter.py [3951e41b]
│   └── video_generator.py [de2abade]
│   └── video_processor.py [de2abade]
│   └── vocal_processor.py [c4b23121]
├── src/processors/filters/
│   └── __init__.py [6bdc2823]
│   └── artistic_filters.py [d8fca9de]
│   └── brightness_filters.py [d8fca9de]
│   └── color_filters.py [d8fca9de]
│   └── filter_registry.py [de2abade]
│   └── preset_filters.py [3951e41b]
├── src/utils/
│   └── __init__.py [9ec1177e]
│   └── arg_parser.py [f534a72c]
│   └── cache_manager.py [de2abade]
│   └── file_handler.py [de2abade]
│   └── io_operations.py [de2abade]
│   └── queue_manager.py [de2abade]
│   └── temp_file_manager.py [de2abade]
└── combine_video.py [de2abade]
└── convert-audio-file.py [9a98a75d]
└── extract-audio.py [de2abade]
└── extract-code.py [de2abade]
└── file-test.py [de2abade]
└── main.py [de2abade]
└── video-transcribe.py [de2abade]
```

## 🔍 Detailed File Analysis

### 📄 `combine_video.py`

#### Imports
- `json` (line 2) `[ff3e4d4d]`
- `os` (line 1) `[de2abade]`
- `pathlib.Path` (line 4) `[fa6ee8af]`
- `subprocess` (line 3) `[7d8752c4]`
- `typing.Dict` (line 5) `[db5e932b]`
- `typing.Optional` (line 5) `[abdbaea6]`
- `typing.Tuple` (line 5) `[23996b74]`

#### Classes
- **`VideoProcessor`** (lines 7-191) `[90852103]`

#### Functions
- **`__init__(self, input_dir, output_dir)`** (lines 8-13) `[9d766d73]`
- **`check_video_validity(self, video_path)`** (lines 39-56) `[959f9411]`
  - *Check if video is valid and playable*
- **`combine_videos(self, video_files, output_file)`** (lines 115-138) `[b81fc01b]`
  - *Combine standardized videos*
- **`get_video_info(self, video_path)`** (lines 15-37) `[1a80ff87]`
  - *Get detailed video information using ffprobe*
- **`process_videos(self)`** (lines 140-191) `[ded3929a]`
  - *Main processing function*
- **`repair_video(self, input_path, output_path)`** (lines 58-76) `[5d222e09]`
  - *Attempt to repair corrupt video*
- **`standardize_video(self, input_path, output_path)`** (lines 78-113) `[20058394]`
  - *Standardize video to 1080p and target frame rate*

#### Variables
- `cmd` (line 122) `[d66ef4e9]`
- `final_output` (line 185) `[6a12d5da]`
- `info` (line 29) `[1e627adc]`
- `new_width` (line 93) `[1f869007]`
- `original_height` (line 87) `[eceb4e88]`
- `original_width` (line 86) `[4a394e0f]`
- `output_path` (line 175) `[67779b5a]`
- `rate` (line 31) `[f09719c2]`
- `repair_path` (line 162) `[cf2e3618]`
- `result` (line 50) `[d07c0927]`
- `stream` (line 170) `[8c4ad3db]`
- `successful_videos` (line 153) `[ecb830f3]`
- `video_files` (line 142) `[024c6294]`
- `video_path` (line 166) `[11e1229a]`

---

### 📄 `convert-audio-file.py`

#### Imports
- `asyncio` (line 1) `[9a98a75d]`
- `edge_tts` (line 6) `[ad958d77]`
- `os` (line 2) `[de2abade]`
- `pathlib.Path` (line 5) `[fa6ee8af]`
- `pydub.AudioSegment` (line 7) `[a8a62585]`
- `re` (line 3) `[66ec0182]`
- `time` (line 4) `[4f9b8491]`

#### Classes
- **`MarkdownToAudioConverter`** (lines 9-182) `[f3782973]`

#### Functions
- **`__init__(self)`** (lines 10-13) `[7bf516d7]`
- **`clean_text_for_speech(self, text)`** (lines 15-27) `[903a7962]`
  - *Clean markdown text for better speech synthesis*
- **`cleanup_temp_files(self, audio_files)`** (lines 124-133) `[3547b59b]`
  - *Clean up temporary audio files*
- **`combine_audio_files(self, audio_files, output_path)`** (lines 96-122) `[a78c3673]`
  - *Combine multiple audio files into one using pydub*
- **`split_into_paragraphs(self, content)`** (lines 29-55) `[03d3e7ae]`
  - *Split markdown content into paragraphs by empty lines*

#### Variables
- `audio_files` (line 161) `[9a32ad77]`
- `audio_segment` (line 108) `[9ea36f55]`
- `cleaned_text` (line 43) `[f0b15990]`
- `combined` (line 104) `[b80c5a3d]`
- `communicate` (line 61) `[fd8f4aae]`
- `content` (line 150) `[9c602263]`
- `converter` (line 185) `[7b63595f]`
- `current_paragraph` (line 46) `[88a74036]`
- `line` (line 37) `[35ca2df9]`
- `lines` (line 34) `[ec9f7618]`
- `markdown_path` (line 137) `[ed39baed]`
- `output_file` (line 85) `[41e82a93]`
- `output_path` (line 144) `[2b865395]`
- `paragraph_text` (line 42) `[8f8c3fb6]`
- `paragraphs` (line 153) `[bcab9ca9]`
- `success` (line 168) `[aa45e96d]`
- `text` (line 25) `[a288078c]`

---

### 📄 `extract-audio.py`

#### Imports
- `json` (line 199) `[ff3e4d4d]`
- `os` (line 1) `[de2abade]`
- `pathlib.Path` (line 3) `[fa6ee8af]`
- `subprocess` (line 2) `[7d8752c4]`
- `sys` (line 4) `[9e77b374]`

#### Classes
- **`AudioExtractor`** (lines 6-268) `[8d57b402]`

#### Functions
- **`__init__(self)`** (lines 7-16) `[ec3f0f1e]`
- **`check_ffmpeg_installed(self)`** (lines 18-24) `[f9abf4fa]`
  - *Check if ffmpeg is installed*
- **`choose_audio_format(self)`** (lines 79-110) `[d7dfc502]`
  - *Let user choose audio output format*
- **`extract_audio(self, video_path, audio_format)`** (lines 112-188) `[93f0817e]`
  - *Extract audio from video file using ffmpeg*
- **`get_audio_info(self, file_path)`** (lines 190-219) `[c827b349]`
  - *Get audio information from the extracted file*
- **`get_file_path(self)`** (lines 26-77) `[0f719c70]`
  - *Get video file path from user input*
- **`main()`** (lines 271-273) `[3c5d95e2]`
- **`run(self)`** (lines 221-268) `[a83e91f6]`
  - *Main execution function*

#### Variables
- `another` (line 258) `[326a5b0f]`
- `audio_format` (line 242) `[b086c484]`
- `bitrate` (line 208) `[de383b20]`
- `choice` (line 91) `[6ce0dde2]`
- `choice_num` (line 97) `[89ce2735]`
- `cmd` (line 193) `[9b5ab85e]`
- `codec` (line 205) `[9d8d895a]`
- `duration` (line 211) `[af126163]`
- `extractor` (line 272) `[9077cf9b]`
- `file_extension` (line 61) `[497e83cf]`
- `formats` (line 82) `[442239b2]`
- `info` (line 200) `[ce160e8a]`
- `input_dir` (line 118) `[972cca5b]`
- `input_file` (line 116) `[8bd0ea46]`
- `input_name` (line 117) `[555e439f]`
- `output_ext` (line 126) `[c5a114b8]`
- `output_file` (line 251) `[16497a41]`
- `output_path` (line 130) `[a915862a]`
- `overwrite` (line 138) `[c9c904d8]`
- `path` (line 42) `[c36586a1]`
- `proceed` (line 66) `[33aa19c0]`
- `result` (line 197) `[45218fd2]`
- `size_mb` (line 173) `[b33a5d43]`
- `success` (line 247) `[604d23a5]`
- `video_path` (line 237) `[c98d3042]`

---

### 📄 `extract-code.py`

#### Imports
- `os` (line 1) `[de2abade]`
- `pathlib.Path` (line 3) `[fa6ee8af]`
- `sys` (line 2) `[9e77b374]`

#### Functions
- **`create_consolidated_file(input_paths, output_file)`** (lines 73-131) `[ae57a038]`
  - *Create a consolidated text file with all coding files.*
  - *Calls:* is_coding_file, should_ignore_path, scan_directory, read_file_content, should_ignore_path
  - *Called by:* main
- **`is_coding_file(file_path)`** (lines 5-27) `[c8d62ddd]`
  - *Check if a file is a coding file based on its extension.*
  - *Called by:* scan_directory, create_consolidated_file
- **`main()`** (lines 133-165) `[24c41413]`
  - *Calls:* create_consolidated_file
- **`read_file_content(file_path)`** (lines 33-46) `[06e4e970]`
  - *Read file content with error handling for different encodings.*
  - *Called by:* create_consolidated_file
- **`scan_directory(directory_path, base_path)`** (lines 48-71) `[567786d5]`
  - *Recursively scan directory for coding files.*
  - *Calls:* should_ignore_path, is_coding_file, scan_directory
  - *Called by:* create_consolidated_file, scan_directory
- **`should_ignore_path(path)`** (lines 29-31) `[2ef24046]`
  - *Check if a path should be ignored (starts with dot).*
  - *Called by:* scan_directory, create_consolidated_file, create_consolidated_file

#### Variables
- `all_files` (line 75) `[10a5be7c]`
- `coding_extensions` (line 7) `[40f9283f]`
- `coding_files` (line 50) `[3be0b9fd]`
- `content` (line 123) `[ff43267d]`
- `encodings` (line 35) `[41ce7df4]`
- `ext` (line 18) `[01d6f2d2]`
- `filename` (line 21) `[8a77f25f]`
- `found_files` (line 97) `[2b19e974]`
- `input_paths` (line 138) `[9da44060]`
- `output_file` (line 154) `[f21f31ec]`
- `path` (line 142) `[9a2682d0]`
- `relative_path` (line 60) `[cb70530e]`
- `special_files` (line 22) `[9a821187]`

---

### 📄 `file-test.py`

#### Imports
- `os` (line 1) `[de2abade]`
- `sys` (line 2) `[9e77b374]`

#### Functions
- **`collect_python_code(root_folder, output_file)`** (lines 4-46) `[90fda867]`
  - *Recursively finds all .py files in a directory, ignoring hidden folders,*

#### Variables
- `content` (line 39) `[3b53b119]`
- `file_count` (line 13) `[e28c94d6]`
- `file_path` (line 29) `[5ddaf447]`
- `output_filename` (line 60) `[dd772948]`
- `target_path` (line 51) `[332393a1]`
- `total_files` (line 67) `[25061eb5]`

---

### 📄 `insta-download/batch_video_normalizer.py`

#### Imports
- `datetime.datetime` (line 74) `[605c9066]`
- `json` (line 71) `[ff3e4d4d]`
- `os` (line 67) `[de2abade]`
- `pathlib.Path` (line 73) `[fa6ee8af]`
- `shutil` (line 69) `[582f9ff7]`
- `sqlite3` (line 72) `[cc7487a3]`
- `subprocess` (line 68) `[7d8752c4]`
- `time` (line 70) `[4f9b8491]`

#### Functions
- **`add_file_to_database(db_path, file_path, file_type, original_size_mb)`** (lines 224-242) `[db7c5fb4]`
  - *Add a new file to the database.*
  - *Called by:* process_media_files
- **`analyze_video_changes(video_info, target_format)`** (lines 391-454) `[3d99095c]`
  - *Analyze what changes need to be made to normalize the video (excluding resolution).*
  - *Called by:* process_media_files
- **`check_executable(name)`** (lines 76-81) `[f3557bda]`
  - *Checks if an executable is in the PATH.*
  - *Called by:* main, main
- **`check_gpu_support()`** (lines 83-98) `[1d18c549]`
  - *Check if VideoToolbox (Apple Silicon GPU) is available.*
  - *Called by:* main
- **`convert_image_to_video(image_path, output_path, target_format, duration, use_gpu)`** (lines 503-553) `[74f455d8]`
  - *Convert image to video while preserving original resolution.*
  - *Called by:* process_media_files
- **`find_all_media_files(root_path)`** (lines 307-338) `[224fc6a6]`
  - *Recursively find all video and image files in root path and subfolders.*
  - *Called by:* process_media_files
- **`get_file_size_mb(file_path)`** (lines 340-350) `[daad57cc]`
  - *Get file size in MB.*
  - *Called by:* process_media_files, process_media_files, process_media_files
- **`get_file_status(db_path, file_path)`** (lines 163-186) `[39695f75]`
  - *Get the processing status of a file from database.*
  - *Called by:* process_media_files
- **`get_format_presets(use_gpu)`** (lines 712-775) `[dc027248]`
  - *Get predefined format presets with GPU support.*
  - *Called by:* main
- **`get_processing_statistics(db_path)`** (lines 265-305) `[f9e09614]`
  - *Get processing statistics from database.*
  - *Called by:* process_media_files, process_media_files, main
- **`get_video_info(video_path)`** (lines 352-389) `[82d849cb]`
  - *Get detailed information about a video file using ffprobe.*
  - *Called by:* process_media_files
- **`init_database(db_path)`** (lines 100-161) `[51f17fcc]`
  - *Initialize SQLite database for tracking processing progress.*
  - *Called by:* process_media_files
- **`log_processing_message(db_path, file_path, log_type, message)`** (lines 244-263) `[f9584ca7]`
  - *Log a processing message to database.*
  - *Called by:* process_media_files, process_media_files, process_media_files
- **`main()`** (lines 777-898) `[e64a7161]`
  - *Main function with user input.*
  - *Calls:* check_gpu_support, get_format_presets, process_media_files, get_processing_statistics, check_executable, check_executable
- **`normalize_video(input_path, output_path, target_format, use_gpu)`** (lines 456-501) `[537ff48f]`
  - *Normalize video while preserving original resolution.*
  - *Called by:* process_media_files
- **`process_media_files(root_path, target_format, use_gpu, image_duration)`** (lines 555-710) `[06011d8e]`
  - *Process all media files with resume capability.*
  - *Calls:* find_all_media_files, get_processing_statistics, get_processing_statistics, init_database, get_file_size_mb, add_file_to_database, get_file_status, update_file_status, log_processing_message, get_file_size_mb, get_video_info, analyze_video_changes, normalize_video, get_file_size_mb, update_file_status, log_processing_message, update_file_status, update_file_status, log_processing_message, update_file_status, convert_image_to_video
  - *Called by:* main
- **`update_file_status(db_path, file_path, status)`** (lines 188-222) `[9d311a3a]`
  - *Update file status in database.*
  - *Called by:* process_media_files, process_media_files, process_media_files, process_media_files, process_media_files

#### Variables
- `audio_stream` (line 375) `[75d235ae]`
- `base_presets` (line 715) `[bae87484]`
- `changes_needed` (line 393) `[3b695b3d]`
- `choice` (line 851) `[25016d43]`
- `codec_name` (line 419) `[28b6d661]`
- `command` (line 506) `[424758fd]`
- `confirm` (line 890) `[42a57021]`
- `conn` (line 268) `[e7c72e53]`
- `current_audio_codec` (line 424) `[94a05737]`
- `current_channels` (line 426) `[edda29f4]`
- `current_format` (line 450) `[b4ac341d]`
- `current_height` (line 404) `[0f6c09a3]`
- `current_resolution` (line 405) `[a967c07a]`
- `current_sample_rate` (line 425) `[ef33787f]`
- `current_specs` (line 394) `[e7f4d98e]`
- `current_width` (line 403) `[c7fab2fd]`
- `cursor` (line 269) `[4b534c63]`
- `data` (line 365) `[a67a001d]`
- `db_path` (line 814) `[11b56eb3]`
- `duration_input` (line 863) `[b6d44b58]`
- `end_time` (line 544) `[634f2028]`
- `error_count` (line 597) `[b5acbdb5]`
- `error_msg` (line 686) `[fa45bbe4]`
- `ext_lower` (line 327) `[e0a81142]`
- `file_id` (line 254) `[9ede0eeb]`
- `file_name` (line 230) `[2b3029b8]`
- `file_path` (line 325) `[2bc718d8]`
- `file_status` (line 600) `[7b3548f5]`
- `final_output` (line 658) `[5d6ff1ff]`
- `final_size` (line 652) `[09abc85a]`
- `final_stats` (line 701) `[a781bc0c]`
- `has_videotoolbox` (line 88) `[6a219679]`
- `image_duration` (line 871) `[0c777b9e]`
- `image_extensions` (line 310) `[535f7c50]`
- `info` (line 377) `[95811a25]`
- `media_files` (line 566) `[9b65afb1]`
- `message` (line 621) `[c3ccd1a9]`
- `original_size` (line 613) `[d26c2d61]`
- `presets` (line 846) `[95598399]`
- `processed_count` (line 596) `[7dbf28f3]`
- `processing_time` (line 546) `[4e5fb106]`
- `query` (line 215) `[a3add5f1]`
- `relative_path` (line 605) `[f2b71a9e]`
- `reprocess_choice` (line 836) `[261e6343]`
- `result` (line 543) `[ee8c2a4c]`
- `resume_choice` (line 830) `[9d4bea3f]`
- `root_path` (line 807) `[df6dcfa3]`
- `size_bytes` (line 344) `[33311106]`
- `size_change` (line 661) `[2524faf0]`
- `size_change_percent` (line 662) `[0cf6f97a]`
- `size_mb` (line 345) `[d414f715]`
- `start_time` (line 542) `[0a626f09]`
- `stats` (line 819) `[c3612629]`
- `success` (line 620) `[ea54af86]`
- `target_codec` (line 417) `[47e20e33]`
- `target_format` (line 858) `[fd24c83e]`
- `temp_output` (line 617) `[51815e48]`
- `update_fields` (line 195) `[912950ba]`
- `update_values` (line 196) `[5b0d54e9]`
- `use_gpu` (line 797) `[d8dee632]`
- `video_extensions` (line 309) `[87d3854d]`
- `video_stream` (line 373) `[974e189f]`

---

### 📄 `insta-download/combine-video.py`

#### Imports
- `datetime.datetime` (line 8) `[605c9066]`
- `json` (line 4) `[ff3e4d4d]`
- `os` (line 1) `[de2abade]`
- `pathlib.Path` (line 5) `[fa6ee8af]`
- `random` (line 2) `[7e18ed42]`
- `shutil` (line 7) `[582f9ff7]`
- `subprocess` (line 3) `[7d8752c4]`
- `typing.Dict` (line 6) `[db5e932b]`
- `typing.List` (line 6) `[eada0f80]`
- `typing.Tuple` (line 6) `[23996b74]`

#### Classes
- **`VideoGroupCombiner`** (lines 10-436) `[54314f52]`

#### Functions
- **`__init__(self)`** (lines 11-14) `[48cbc42b]`
- **`analyze_and_group_videos(self, video_files)`** (lines 186-221) `[f84dee89]`
  - *Analyze videos and group them by format categories*
- **`categorize_video_format(self, resolution)`** (lines 146-184) `[26a001b7]`
  - *Categorize video format based on resolution*
- **`check_ffmpeg_installed(self)`** (lines 318-325) `[8617a79a]`
  - *Check if ffmpeg and ffprobe are installed*
- **`combine_group_videos(self, group_key, group_data, group_output_dir)`** (lines 267-316) `[13cf19eb]`
  - *Combine videos in a specific group*
- **`create_concat_file(self, video_files, concat_file_path)`** (lines 259-265) `[3f24050f]`
  - *Create a concat file for ffmpeg*
- **`display_group_statistics(self, video_groups)`** (lines 223-257) `[0f5475d4]`
  - *Display statistics for all video groups*
- **`find_all_videos(self, folders)`** (lines 87-100) `[daf43a55]`
  - *Find all video files in the given folders and their subdirectories*
- **`get_folder_paths(self)`** (lines 31-85) `[f7cac760]`
  - *Get multiple folder paths from user input*
- **`get_video_info(self, video_path)`** (lines 102-113) `[d35bad3c]`
  - *Get video information using ffprobe*
- **`get_video_properties(self, video_info)`** (lines 115-144) `[e2b33168]`
  - *Extract video properties from ffprobe output*
- **`main()`** (lines 439-441) `[dbce2fb9]`
- **`run(self)`** (lines 327-436) `[39c40112]`
  - *Main execution function*
- **`setup_output_directory(self)`** (lines 16-29) `[7fddc828]`
  - *Create main output directory with timestamp*

#### Variables
- `category` (line 197) `[e605212e]`
- `cmd` (line 292) `[9f46d305]`
- `codec` (line 132) `[e471396a]`
- `combiner` (line 440) `[34ae8b73]`
- `concat_file` (line 285) `[d492e994]`
- `count` (line 280) `[6344d6da]`
- `duplicate_found` (line 62) `[2a6fd0a5]`
- `escaped_path` (line 264) `[bb75ee2f]`
- `existing_normalized` (line 60) `[07134e9a]`
- `failed_groups` (line 398) `[5c265ca4]`
- `file_path` (line 429) `[096d8ebc]`
- `file_size` (line 142) `[31599bcc]`
- `folders` (line 343) `[c10f912a]`
- `fps` (line 137) `[e7b08187]`
- `group_output_dir` (line 404) `[4190ef08]`
- `height` (line 130) `[ee3a5b87]`
- `indent` (line 424) `[04ad9d4a]`
- `info` (line 192) `[694555d4]`
- `key` (line 200) `[4309169e]`
- `level` (line 423) `[ba50e70d]`
- `normalized_path` (line 55) `[a233bf81]`
- `output_filename` (line 281) `[17da0bf3]`
- `output_path` (line 282) `[c63185a7]`
- `path` (line 52) `[3ef34672]`
- `percentage` (line 238) `[a49ff1b5]`
- `proceed` (line 380) `[1c9726ae]`
- `resolution` (line 279) `[302f6cc5]`
- `result` (line 299) `[46c2387d]`
- `size_mb` (line 430) `[a3ea355b]`
- `sorted_groups` (line 234) `[423ddd66]`
- `status` (line 241) `[149c728f]`
- `subindent` (line 426) `[9fe606a9]`
- `successful_groups` (line 397) `[83faede3]`
- `timestamp` (line 18) `[389892b1]`
- `total_videos` (line 235) `[fa00a207]`
- `video_files` (line 356) `[de18c8ae]`
- `video_groups` (line 365) `[912b197b]`
- `video_path` (line 96) `[adc4a95e]`
- `video_stream` (line 123) `[9b1de7ee]`
- `videos` (line 274) `[5e591ffc]`
- `width` (line 129) `[7ad53270]`

---

### 📄 `insta-download/download-insta.py`

#### Imports
- `os` (line 1) `[de2abade]`
- `shutil` (line 3) `[582f9ff7]`
- `subprocess` (line 2) `[7d8752c4]`

#### Functions
- **`extract_audio_and_repair_videos(input_folder, audio_output_folder)`** (lines 5-94) `[b846e8bc]`
  - *Extracts MP3 audio from videos. If a video is corrupted, it attempts to*

#### Variables
- `audio_bitrate` (line 17) `[0b2e1e4d]`
- `audio_codec` (line 16) `[6aee5d72]`
- `audio_filename` (line 35) `[093a2c04]`
- `audio_output_directory` (line 105) `[e9dbe5a7]`
- `audio_output_path` (line 36) `[f7f3f474]`
- `extract_command` (line 43) `[a2e342c7]`
- `input_directory` (line 102) `[28e14445]`
- `input_path` (line 34) `[e0ea7576]`
- `repair_command` (line 61) `[25ac4aa1]`
- `supported_extensions` (line 28) `[1d31eb71]`
- `temp_video_path` (line 56) `[51cc37f0]`

---

### 📄 `insta-download/file-processor.py`

#### Imports
- `datetime` (line 6) `[ab28f734]`
- `json` (line 3) `[ff3e4d4d]`
- `os` (line 1) `[de2abade]`
- `platform` (line 7) `[817f6e30]`
- `shutil` (line 4) `[582f9ff7]`
- `sqlite3` (line 5) `[cc7487a3]`
- `subprocess` (line 2) `[7d8752c4]`

#### Functions
- **`check_executable(name)`** (lines 9-14) `[f3557bda]`
  - *Checks if an executable is in the PATH.*
  - *Called by:* reencode_video_ffmpeg, extract_audio_ffmpeg, main
- **`extract_audio_ffmpeg(input_video_filepath, output_audio_path, audio_format)`** (lines 154-174) `[395a67ea]`
  - *Extracts audio from a video file using ffmpeg.*
  - *Calls:* check_executable
  - *Called by:* main
- **`get_record_from_db(db_path, original_video_filepath)`** (lines 41-53) `[24ef0a62]`
  - *Fetches a record from the database based on original_video_filepath.*
  - *Called by:* main
- **`init_processing_db(db_path)`** (lines 17-39) `[3a4c19cb]`
  - *Initializes the SQLite database for processed reels.*
  - *Called by:* main
- **`load_json_file(json_path)`** (lines 93-106) `[7cb83bc0]`
  - *Loads a JSON file or returns an empty list if it doesn't exist or is invalid.*
  - *Called by:* main, main, main
- **`main()`** (lines 176-370) `[32ddd0a6]`
  - *Calls:* init_processing_db, check_executable, load_json_file, load_json_file, get_record_from_db, update_or_insert_processed_reel_sqlite, save_json_file, load_json_file, update_or_insert_processed_reel_sqlite, save_json_file, save_json_file, reencode_video_ffmpeg, extract_audio_ffmpeg
- **`reencode_video_ffmpeg(input_filepath, output_video_path, use_gpu)`** (lines 119-152) `[6776bc27]`
  - *Re-encodes a video file using ffmpeg.*
  - *Calls:* check_executable
  - *Called by:* main
- **`save_json_file(json_path, data)`** (lines 108-115) `[20dae4fd]`
  - *Saves the data to a JSON file.*
  - *Called by:* main, main, main
- **`update_or_insert_processed_reel_sqlite(db_path, record_data)`** (lines 56-90) `[ba21a688]`
  - *Inserts or updates a processed reel's metadata in the SQLite database.*
  - *Called by:* main, main

#### Variables
- `all_records` (line 234) `[8a7d5be1]`
- `audio_extract_error_msg` (line 321) `[d595fd41]`
- `base_filename` (line 282) `[7682b182]`
- `command` (line 161) `[6dab7486]`
- `conn` (line 59) `[350ef74b]`
- `current_error` (line 338) `[74abf6c7]`
- `current_record_had_audio_error` (line 317) `[d6c01703]`
- `current_record_had_reencode_error` (line 289) `[4c2b5460]`
- `cursor` (line 60) `[049059f2]`
- `db_entry` (line 266) `[dc647343]`
- `error_in_this_run_count` (line 249) `[ad9937eb]`
- `error_message` (line 174) `[35b01192]`
- `extracted_audio_dir` (line 202) `[9e898732]`
- `extracted_audio_filename` (line 313) `[cdb91752]`
- `extracted_audio_path` (line 314) `[c63483b3]`
- `final_audio_path` (line 315) `[33a1d2d3]`
- `final_reencoded_path` (line 287) `[24cb6c58]`
- `final_status` (line 345) `[2c2ae7c8]`
- `local_processing_json_path` (line 193) `[8f6c577d]`
- `main_output_dir` (line 189) `[cec81c07]`
- `new_error` (line 339) `[20eb9b86]`
- `original_input_json_path` (line 182) `[186e3837]`
- `original_records` (line 220) `[f9328509]`
- `original_video_filepath` (line 253) `[77d1b1c5]`
- `processed_in_this_run_count` (line 247) `[c7824b4e]`
- `processing_db_path` (line 211) `[b2c97db3]`
- `record` (line 48) `[4c5c2bc8]`
- `reencode_error_msg` (line 288) `[39e6849c]`
- `reencoded_video_filename` (line 285) `[a8fa184b]`
- `reencoded_video_path` (line 286) `[1adfacf1]`
- `reencoded_videos_dir` (line 201) `[1fa912eb]`
- `result` (line 165) `[39ac97d5]`
- `should_use_gpu` (line 196) `[fcb99163]`
- `skipped_count` (line 248) `[0d0ad3a7]`
- `use_gpu_input` (line 195) `[de24ff46]`
- `video_to_extract_from` (line 311) `[0409dbc1]`

---

### 📄 `insta-download/image-to-video.py`

#### Imports
- `PIL.Image` (line 3) `[4f84112b]`
- `datetime.datetime` (line 9) `[605c9066]`
- `hashlib` (line 8) `[ada1d9e0]`
- `os` (line 1) `[de2abade]`
- `pathlib.Path` (line 5) `[fa6ee8af]`
- `random` (line 11) `[7e18ed42]`
- `shutil` (line 2) `[582f9ff7]`
- `sqlite3` (line 7) `[cc7487a3]`
- `subprocess` (line 4) `[7d8752c4]`
- `sys` (line 6) `[9e77b374]`
- `uuid` (line 10) `[8b76fbd0]`

#### Classes
- **`ImageVideoProcessor`** (lines 13-539) `[d9bce994]`

#### Functions
- **`__init__(self, output_folder)`** (lines 14-27) `[44961391]`
- **`check_ffmpeg()`** (lines 541-547) `[5080ba2f]`
  - *Check if ffmpeg is available*
  - *Called by:* main
- **`create_video_from_image(self, image_path, output_video_path, duration)`** (lines 396-419) `[6331b286]`
  - *Create a video from an image using ffmpeg*
- **`create_youtube_sized_image(self, image_path, output_path)`** (lines 351-394) `[870f5feb]`
  - *Create a YouTube-sized (1920x1080) image with black background and 20% gap on all sides*
- **`discover_images(self, root_folder, session_id)`** (lines 132-180) `[580c8f56]`
  - *Discover all images and add new ones to database*
- **`get_file_hash(self, file_path)`** (lines 84-94) `[857c189e]`
  - *Generate MD5 hash of file for verification*
- **`get_or_create_session(self, root_folder, processing_mode)`** (lines 96-130) `[36a5bcd7]`
  - *Get existing session or create new one*
- **`get_pending_images(self, session_id, mode)`** (lines 226-251) `[f3c5c043]`
  - *Get list of images that need processing*
- **`get_processing_statistics(self, session_id, mode)`** (lines 182-224) `[54f80c9e]`
  - *Get current processing statistics*
- **`init_database(self)`** (lines 29-82) `[d51834f9]`
  - *Initialize SQLite database with required tables*
- **`main()`** (lines 549-692) `[60fd2ef8]`
  - *Calls:* check_ffmpeg
- **`process_images(self, session_id)`** (lines 421-462) `[6d00c1d0]`
  - *Process all pending images*
- **`randomize_and_rename_files(self, session_id)`** (lines 464-539) `[87dc666a]`
  - *Randomly arrange and rename all processed files with UUIDs*
- **`simple_copy_images(self, session_id)`** (lines 305-349) `[1a79c9dc]`
  - *Simple copy all images to one folder with unique IDs*
- **`update_image_processing_status(self, image_file_id, success, processed_image_path, error_message)`** (lines 271-286) `[91c77d0f]`
  - *Update image processing status in database*
- **`update_simple_copy_status(self, image_file_id, success, copy_path, uuid_assigned, error_message)`** (lines 253-269) `[eacdac2b]`
  - *Update simple copy status in database*
- **`update_video_creation_status(self, image_file_id, success, video_path, error_message)`** (lines 288-303) `[bab3a927]`
  - *Update video creation status in database*

#### Variables
- `background` (line 367) `[141237c1]`
- `base_name` (line 433) `[29853d0b]`
- `choice` (line 561) `[49c4e300]`
- `command` (line 399) `[69191849]`
- `conn` (line 466) `[371e5251]`
- `copied_count` (line 316) `[bd59d092]`
- `copy_path` (line 332) `[87972d0b]`
- `cursor` (line 467) `[857e25d0]`
- `error_message` (line 344) `[4c7cba3f]`
- `existing_images` (line 140) `[d9127d65]`
- `file_extension` (line 328) `[6076dfb7]`
- `file_hash` (line 157) `[e79069a2]`
- `file_path` (line 146) `[f71a4862]`
- `file_size` (line 156) `[b91f5d1d]`
- `files_to_randomize` (line 482) `[b31c54a7]`
- `final_stats` (line 677) `[8222d12e]`
- `gap_percentage` (line 358) `[61377295]`
- `hash_md5` (line 87) `[82fe74d1]`
- `image_extensions` (line 134) `[f454a6e7]`
- `image_file_id` (line 164) `[f7fb466f]`
- `new_filename` (line 331) `[452eddf1]`
- `new_height` (line 378) `[84538c0b]`
- `new_image_name` (line 507) `[527d8c59]`
- `new_image_path` (line 510) `[7ef241b4]`
- `new_images` (line 139) `[21fcd122]`
- `new_video_name` (line 508) `[1405687e]`
- `new_video_path` (line 511) `[fccca454]`
- `new_width` (line 377) `[7c7a92f5]`
- `original_image` (line 365) `[3ac1fc2b]`
- `output_folder` (line 588) `[87e16457]`
- `pending_images` (line 423) `[6b76c6ae]`
- `processed_image_path` (line 434) `[2df16181]`
- `processing_mode` (line 569) `[ce598bf4]`
- `processor` (line 596) `[c7bda6fc]`
- `randomized_count` (line 674) `[87af059e]`
- `resized_image` (line 381) `[0213a689]`
- `result` (line 411) `[240b0681]`
- `results` (line 248) `[bf850b95]`
- `root_folder` (line 580) `[82eb116f]`
- `scale` (line 374) `[3201300d]`
- `scale_height` (line 373) `[d7de1b0f]`
- `scale_width` (line 372) `[2443e5b8]`
- `session_id` (line 125) `[3617828e]`
- `stats` (line 216) `[7032ab3a]`
- `unique_uuid` (line 506) `[006d8ba1]`
- `usable_height` (line 360) `[1f015857]`
- `usable_width` (line 359) `[ba565e16]`
- `uuids` (line 493) `[8be5f264]`
- `video_path` (line 435) `[27db99c2]`
- `x_offset` (line 384) `[7cbea9b2]`
- `y_offset` (line 385) `[922285c3]`
- `youtube_height` (line 355) `[01e445ea]`
- `youtube_width` (line 354) `[fec5c5e4]`

---

### 📄 `insta-download/image-video-encoder.py`

#### Imports
- `json` (line 66) `[ff3e4d4d]`
- `os` (line 62) `[de2abade]`
- `pathlib.Path` (line 67) `[fa6ee8af]`
- `shutil` (line 64) `[582f9ff7]`
- `subprocess` (line 63) `[7d8752c4]`
- `time` (line 65) `[4f9b8491]`

#### Functions
- **`analyze_video_changes(video_info, target_format)`** (lines 115-181) `[f767b81c]`
  - *Analyze what changes need to be made to normalize the video.*
  - *Called by:* process_mixed_media_folder
- **`check_executable(name)`** (lines 69-74) `[f3557bda]`
  - *Checks if an executable is in the PATH.*
  - *Called by:* process_mixed_media_folder, process_mixed_media_folder
- **`combine_videos(video_folder, output_path, video_files)`** (lines 302-363) `[4ea09deb]`
  - *Combine all processed videos into a single video file.*
  - *Calls:* get_file_size_mb
  - *Called by:* process_mixed_media_folder
- **`convert_image_to_video(image_path, output_path, target_format, duration)`** (lines 240-300) `[0cf99609]`
  - *Convert an image to a video of specified duration using FFmpeg.*
  - *Called by:* process_mixed_media_folder
- **`find_media_files(folder_path)`** (lines 377-400) `[d532f157]`
  - *Find all video and image files in the given folder.*
  - *Called by:* process_mixed_media_folder
- **`get_file_size_mb(file_path)`** (lines 365-375) `[daad57cc]`
  - *Get file size in MB.*
  - *Called by:* combine_videos, process_mixed_media_folder, process_mixed_media_folder, process_mixed_media_folder, process_mixed_media_folder
- **`get_format_presets()`** (lines 638-707) `[93ce95ae]`
  - *Get predefined format presets.*
  - *Called by:* main
- **`get_video_info(video_path)`** (lines 76-113) `[82d849cb]`
  - *Get detailed information about a video file using ffprobe.*
  - *Called by:* process_mixed_media_folder
- **`main()`** (lines 709-784) `[fb0ca258]`
  - *Main function with user input.*
  - *Calls:* get_format_presets, process_mixed_media_folder
- **`normalize_video(input_path, output_path, target_format)`** (lines 183-238) `[a0e692d0]`
  - *Normalize video to standard format using FFmpeg.*
  - *Called by:* process_mixed_media_folder
- **`process_mixed_media_folder(folder_path, target_format, image_duration)`** (lines 402-636) `[240d2f73]`
  - *Process all video and image files in the specified folder.*
  - *Calls:* find_media_files, check_executable, check_executable, get_file_size_mb, get_video_info, analyze_video_changes, get_file_size_mb, normalize_video, convert_image_to_video, combine_videos, get_file_size_mb, get_file_size_mb
  - *Called by:* main

#### Variables
- `audio_stream` (line 99) `[fc4ed56a]`
- `base_name` (line 551) `[ce7b9ef2]`
- `changes_needed` (line 117) `[535e8bff]`
- `choice` (line 740) `[4c4e6dc6]`
- `combine_choice` (line 612) `[dc9de7f3]`
- `combined_filename` (line 617) `[b8a8a8ad]`
- `combined_output_path` (line 618) `[5dbde94e]`
- `command` (line 318) `[22c1a827]`
- `confirm` (line 777) `[bfaaf37f]`
- `current_audio_codec` (line 151) `[d06b259d]`
- `current_channels` (line 153) `[d11fd7c2]`
- `current_format` (line 177) `[4786ffc7]`
- `current_height` (line 128) `[b3ce9d69]`
- `current_resolution` (line 129) `[3b589a9a]`
- `current_sample_rate` (line 152) `[9c56a967]`
- `current_specs` (line 118) `[6286f951]`
- `current_width` (line 127) `[753487ff]`
- `data` (line 89) `[556fa111]`
- `duration_input` (line 755) `[d47babc9]`
- `end_time` (line 331) `[f16f1b8b]`
- `error_count` (line 439) `[59b1d80b]`
- `error_msg` (line 356) `[e652aa74]`
- `escaped_path` (line 314) `[bc73e244]`
- `ext_lower` (line 390) `[acfa03a8]`
- `file_path` (line 387) `[dd41d0f2]`
- `filelist_path` (line 308) `[7a45e8d6]`
- `final_output` (line 502) `[acedb05f]`
- `folder_name` (line 616) `[75f61c35]`
- `folder_path` (line 730) `[b0e3650e]`
- `image_duration` (line 763) `[7ff6f0c1]`
- `image_extensions` (line 380) `[b43f09da]`
- `image_filename` (line 541) `[668de11d]`
- `image_files` (line 383) `[0e0ddb63]`
- `info` (line 101) `[51b1770f]`
- `original_size` (line 545) `[b31f65c5]`
- `output_size` (line 337) `[f4ca191b]`
- `presets` (line 733) `[b276c39a]`
- `processed_size` (line 564) `[89d5bc60]`
- `processing_time` (line 336) `[aa2064e0]`
- `result` (line 330) `[042c1550]`
- `size_bytes` (line 369) `[8204c936]`
- `size_change` (line 505) `[800ad690]`
- `size_change_percent` (line 506) `[b5cb5b38]`
- `size_mb` (line 370) `[a07cc8cd]`
- `start_time` (line 329) `[db6edfb2]`
- `successful_count` (line 438) `[6b2e4f6f]`
- `successfully_processed_files` (line 442) `[baf96741]`
- `target_format` (line 750) `[5f54f54d]`
- `temp_output` (line 556) `[f56539d7]`
- `total_original_size` (line 440) `[e9f3c058]`
- `total_processed_size` (line 441) `[6c3071bf]`
- `video_extensions` (line 379) `[239ee235]`
- `video_filename` (line 449) `[150a3c19]`
- `video_files` (line 382) `[af17d8c2]`
- `video_output_filename` (line 552) `[6b4009c2]`
- `video_output_path` (line 553) `[93bc5a88]`
- `video_stream` (line 97) `[6cb140ea]`

---

### 📄 `insta-download/insta-download.py`

#### Imports
- `json` (line 3) `[ff3e4d4d]`
- `os` (line 1) `[de2abade]`
- `re` (line 5) `[66ec0182]`
- `shutil` (line 4) `[582f9ff7]`
- `sqlite3` (line 6) `[cc7487a3]`
- `subprocess` (line 2) `[7d8752c4]`

#### Functions
- **`add_to_centralized_json(json_path, record)`** (lines 102-119) `[41ea861c]`
  - *Adds a new record to the centralized JSON database, avoiding duplicates by video_filepath.*
  - *Calls:* load_centralized_json, save_centralized_json
  - *Called by:* process_downloaded_metadata
- **`check_executable(name)`** (lines 8-13) `[f3557bda]`
  - *Checks if an executable is in the PATH.*
  - *Called by:* reencode_video_with_ffmpeg, download_reels_with_gallery_dl, main, main
- **`download_reels_with_gallery_dl(profile_reels_url, cookies_path, base_download_dir)`** (lines 219-288) `[b07a1a97]`
  - *Downloads reels from an Instagram profile URL using gallery-dl.*
  - *Calls:* extract_profile_name_from_url, check_executable
  - *Called by:* main
- **`extract_profile_name_from_url(url)`** (lines 15-23) `[d615a33d]`
  - *Extracts the Instagram profile name from a typical profile or reels URL.*
  - *Called by:* download_reels_with_gallery_dl
- **`init_sqlite_db(db_path)`** (lines 26-45) `[cc66d8c8]`
  - *Initializes the SQLite database and creates the metadata table if it doesn't exist.*
  - *Called by:* main
- **`insert_reel_metadata_sqlite(db_path, video_filepath, video_url, description, reencoded)`** (lines 47-62) `[f8c0726e]`
  - *Inserts reel metadata into the SQLite database.*
  - *Called by:* process_downloaded_metadata
- **`load_centralized_json(json_path)`** (lines 80-92) `[9a2f1da5]`
  - *Loads the centralized JSON file or returns an empty list if it doesn't exist or is invalid.*
  - *Called by:* add_to_centralized_json
- **`main()`** (lines 346-406) `[3c944971]`
  - *Main function to download Instagram Reels, re-encode videos, and process their metadata.*
  - *Calls:* init_sqlite_db, download_reels_with_gallery_dl, check_executable, check_executable, process_downloaded_metadata, reencode_all_videos
- **`process_downloaded_metadata(downloaded_content_path, db_path, centralized_json_path)`** (lines 290-344) `[6b83c19c]`
  - *Processes downloaded .mp4 files and their corresponding .json metadata.*
  - *Calls:* insert_reel_metadata_sqlite, add_to_centralized_json
  - *Called by:* main
- **`reencode_all_videos(downloaded_content_path, db_path)`** (lines 164-217) `[a40c8461]`
  - *Re-encodes all .mp4 videos in the downloaded content directory.*
  - *Calls:* reencode_video_with_ffmpeg, update_reencoded_status
  - *Called by:* main
- **`reencode_video_with_ffmpeg(input_video_path, output_video_path)`** (lines 122-162) `[6b305f2a]`
  - *Re-encodes a video using FFmpeg with basic settings for compatibility.*
  - *Calls:* check_executable
  - *Called by:* reencode_all_videos
- **`save_centralized_json(json_path, data)`** (lines 94-100) `[dc340d80]`
  - *Saves the data to the centralized JSON file.*
  - *Called by:* add_to_centralized_json
- **`update_reencoded_status(db_path, video_filepath, reencoded)`** (lines 64-77) `[d8142ab8]`
  - *Updates the reencoded status for a video in the database.*
  - *Called by:* reencode_all_videos

#### Variables
- `actual_download_path` (line 274) `[948e86f7]`
- `all_records` (line 104) `[28fe3eb2]`
- `base_name_no_ext` (line 309) `[dd43f03c]`
- `centralized_json_path` (line 386) `[2d627565]`
- `command` (line 241) `[05cfdcf4]`
- `conn` (line 67) `[45929e6a]`
- `cookies_path` (line 369) `[ddc5fc28]`
- `cursor` (line 68) `[20d6a776]`
- `description` (line 323) `[c8d81e1e]`
- `existing_record_index` (line 110) `[4891c5f1]`
- `failed_reencodes` (line 182) `[80ac239f]`
- `final_video_count` (line 281) `[ff8194ee]`
- `input_path` (line 185) `[bde223e9]`
- `match` (line 20) `[cac37590]`
- `metadata` (line 320) `[ac567a2d]`
- `metadata_filename` (line 305) `[b725b46f]`
- `metadata_filename_alt` (line 310) `[9e63ce63]`
- `metadata_filepath` (line 313) `[56ac3a7b]`
- `metadata_filepath_alt` (line 311) `[099c5966]`
- `name_without_ext` (line 192) `[34d9e968]`
- `output_filename` (line 193) `[51def834]`
- `output_path` (line 194) `[5c1d560f]`
- `process` (line 253) `[d517a9e4]`
- `processed_metadata_count` (line 300) `[3e241ba5]`
- `profile_name` (line 228) `[6e1ca495]`
- `profile_reels_url` (line 364) `[6a5b9848]`
- `record` (line 328) `[bd6634a0]`
- `reencode_videos` (line 362) `[d5048635]`
- `result` (line 153) `[a60e85a5]`
- `script_base_output_dir` (line 375) `[ea07eca0]`
- `sqlite_db_path` (line 385) `[8fb0101f]`
- `successful_reencodes` (line 181) `[56c4c16f]`
- `video_filepath` (line 303) `[ddfcb657]`
- `video_files` (line 175) `[673703ba]`
- `video_files_downloaded` (line 280) `[b3e31b5c]`
- `video_url` (line 322) `[abd14b18]`

---

### 📄 `insta-download/pinterest-download.py`

#### Imports
- `json` (line 10) `[ff3e4d4d]`
- `os` (line 8) `[de2abade]`
- `shutil` (line 11) `[582f9ff7]`
- `sqlite3` (line 12) `[cc7487a3]`
- `subprocess` (line 9) `[7d8752c4]`
- `urllib.parse.parse_qs` (line 13) `[4f8180ef]`
- `urllib.parse.urlparse` (line 13) `[355246b6]`

#### Functions
- **`add_to_centralized_json(json_path, record)`** (lines 106-119) `[3fb9876c]`
  - *Adds a new record to the centralized JSON database.*
  - *Calls:* load_centralized_json, save_centralized_json
  - *Called by:* process_pinterest_metadata
- **`check_executable(name)`** (lines 15-20) `[f3557bda]`
  - *Checks if an executable is in the PATH.*
  - *Called by:* download_pinterest_with_gallery_dl, main
- **`download_pinterest_with_gallery_dl(pinterest_url, base_download_dir, max_downloads)`** (lines 121-190) `[8be1a2fa]`
  - *Downloads Pinterest content using gallery-dl.*
  - *Calls:* extract_search_terms_from_url, check_executable
  - *Called by:* main
- **`extract_search_terms_from_url(url)`** (lines 22-33) `[83b7a4a0]`
  - *Extracts search terms from Pinterest search URL.*
  - *Called by:* download_pinterest_with_gallery_dl
- **`init_sqlite_db(db_path)`** (lines 36-57) `[fb76e5c7]`
  - *Initializes the SQLite database and creates the metadata table.*
  - *Called by:* main
- **`insert_pinterest_metadata_sqlite(db_path, video_filepath, metadata)`** (lines 59-81) `[64c73356]`
  - *Inserts Pinterest metadata into the SQLite database.*
  - *Called by:* process_pinterest_metadata
- **`load_centralized_json(json_path)`** (lines 84-96) `[2bc47439]`
  - *Loads the centralized JSON file or returns an empty list.*
  - *Called by:* add_to_centralized_json
- **`main()`** (lines 248-308) `[ec68330e]`
  - *Main function to download Pinterest videos and process metadata.*
  - *Calls:* init_sqlite_db, download_pinterest_with_gallery_dl, check_executable, process_pinterest_metadata
- **`process_pinterest_metadata(downloaded_content_path, db_path, centralized_json_path)`** (lines 192-246) `[7fea087d]`
  - *Processes downloaded Pinterest files and their metadata.*
  - *Calls:* insert_pinterest_metadata_sqlite, add_to_centralized_json
  - *Called by:* main
- **`save_centralized_json(json_path, data)`** (lines 98-104) `[dc340d80]`
  - *Saves the data to the centralized JSON file.*
  - *Called by:* add_to_centralized_json

#### Variables
- `all_records` (line 108) `[ca995a49]`
- `base_name` (line 210) `[9b256149]`
- `base_output_dir` (line 276) `[6a97dc7c]`
- `centralized_json_path` (line 287) `[1a22a5d8]`
- `command` (line 139) `[c61c0f20]`
- `conn` (line 62) `[34ee1e54]`
- `content_files` (line 179) `[ad4fc4e6]`
- `cursor` (line 63) `[c9fe404a]`
- `existing_record_index` (line 114) `[a0b43ec6]`
- `json_filename` (line 211) `[e64f4e8e]`
- `json_filepath` (line 216) `[f5171b84]`
- `max_downloads` (line 272) `[c8ee42de]`
- `metadata` (line 221) `[8de4d548]`
- `parsed_url` (line 28) `[2a1a6933]`
- `pinterest_dir` (line 176) `[2fca9b29]`
- `pinterest_url` (line 259) `[33b9be81]`
- `process` (line 153) `[52eccc0a]`
- `processed_count` (line 201) `[100e9e1d]`
- `query_params` (line 29) `[ed4ca369]`
- `record` (line 227) `[d6cbc37d]`
- `search_term` (line 30) `[2effa5c9]`
- `sqlite_db_path` (line 286) `[70e097f7]`
- `video_filepath` (line 207) `[03553227]`
- `video_files` (line 181) `[5c7dd6cd]`

---

### 📄 `insta-download/text-video-detection/detect-text.py`

#### Imports
- `cv2` (line 1) `[7e8fceb2]`
- `numpy` (line 2) `[d8fca9de]`
- `os` (line 3) `[de2abade]`
- `pathlib.Path` (line 5) `[fa6ee8af]`
- `subprocess` (line 4) `[7d8752c4]`

#### Functions
- **`cleanup_temp_files(temp_dir)`** (lines 234-243) `[4f606f5d]`
  - *Clean up temporary segment files*
  - *Called by:* main
- **`combine_segments(segment_files, output_path)`** (lines 205-232) `[681814f8]`
  - *Combine all segments into final video*
  - *Called by:* main
- **`create_good_segments(text_segments, total_frames, fps)`** (lines 147-171) `[ccfa70fa]`
  - *Create list of good segments (non-text parts) to keep*
  - *Called by:* main
- **`detect_high_contrast_text(gray)`** (lines 47-68) `[5fb4d573]`
  - *Detect text with high contrast against background*
  - *Called by:* detect_overlay_text
- **`detect_overlay_text(video_path)`** (lines 7-45) `[97d57b2e]`
  - *Detect overlay text in videos (like Instagram reels text, captions, branding)*
  - *Calls:* detect_high_contrast_text, detect_stroke_text, detect_uniform_text_blocks
  - *Called by:* main
- **`detect_stroke_text(gray)`** (lines 70-96) `[f503d0c1]`
  - *Detect text with stroke/outline (common in overlay text)*
  - *Called by:* detect_overlay_text
- **`detect_uniform_text_blocks(gray)`** (lines 98-125) `[05ae9716]`
  - *Detect text on uniform backgrounds (like solid color backgrounds)*
  - *Called by:* detect_overlay_text
- **`extract_segments(video_path, good_segments, temp_dir)`** (lines 173-203) `[8f4ddc84]`
  - *Extract good segments as separate video files*
  - *Called by:* main
- **`group_consecutive_frames(frames_with_text)`** (lines 127-145) `[7136d793]`
  - *Group consecutive frames into text segments*
  - *Called by:* main
- **`main()`** (lines 245-369) `[4cb95cba]`
  - *Calls:* detect_overlay_text, group_consecutive_frames, create_good_segments, extract_segments, combine_segments, cleanup_temp_files

#### Variables
- `area` (line 121) `[692083b6]`
- `aspect_ratio` (line 119) `[e5740c15]`
- `blurred` (line 101) `[730f8080]`
- `cap` (line 352) `[895757ea]`
- `cleaned` (line 108) `[08c62fb5]`
- `closed` (line 81) `[e0dfc8e1]`
- `cmd` (line 186) `[339f1f22]`
- `concat_file` (line 212) `[4dfcf6e0]`
- `confirm` (line 323) `[4bfd64a7]`
- `current_time` (line 165) `[12d26a30]`
- `duration` (line 300) `[f4f2334d]`
- `end` (line 142) `[3a3a59e2]`
- `end_time` (line 302) `[ae663765]`
- `final_duration` (line 354) `[f8e7cdeb]`
- `final_frames` (line 353) `[3da0c594]`
- `final_size` (line 364) `[5fb089be]`
- `fps` (line 270) `[45f6d22c]`
- `frame_count` (line 14) `[93679459]`
- `frames_with_text` (line 285) `[150454d3]`
- `good_segments` (line 309) `[bca01378]`
- `gradient` (line 74) `[cde1cb53]`
- `gray` (line 22) `[07e4912d]`
- `kernel` (line 107) `[65222afc]`
- `large_regions` (line 113) `[84d929e3]`
- `original_size` (line 363) `[32b5d2be]`
- `output_path` (line 331) `[fd219acc]`
- `segment_file` (line 181) `[f06fa1ab]`
- `segment_files` (line 341) `[a210c7ba]`
- `segments` (line 132) `[56e395e3]`
- `start` (line 141) `[5cc7db0f]`
- `start_time` (line 301) `[268926a7]`
- `success` (line 348) `[f1728cf6]`
- `temp_dir` (line 332) `[d03dd914]`
- `text_contours` (line 56) `[0c85ceab]`
- `text_detected` (line 33) `[33f64a64]`
- `text_regions` (line 86) `[681236a0]`
- `text_segments` (line 292) `[0917bd26]`
- `thresh` (line 50) `[64979af4]`
- `total_duration` (line 154) `[7e16eb5b]`
- `total_frames` (line 269) `[94af16af]`
- `total_text_duration` (line 298) `[3bcb7543]`
- `video_path` (line 250) `[5a38ad04]`
- `video_path_obj` (line 330) `[8c609e72]`

---

### 📄 `insta-download/text-video-detection/easy-text-detection.py`

#### Imports
- `cv2` (line 1) `[7e8fceb2]`
- `datetime` (line 8) `[ab28f734]`
- `easyocr` (line 2) `[cc5b9a00]`
- `gc` (line 10) `[28a6b0b6]`
- `glob` (line 9) `[8dcc5586]`
- `os` (line 3) `[de2abade]`
- `pathlib.Path` (line 14) `[fa6ee8af]`
- `psutil` (line 11) `[f6b32ab9]`
- `shutil` (line 4) `[582f9ff7]`
- `sqlite3` (line 7) `[cc7487a3]`
- `subprocess` (line 5) `[7d8752c4]`
- `sys` (line 13) `[9e77b374]`
- `torch` (line 6) `[cf1070d3]`
- `traceback` (line 12) `[6a6eacd0]`

#### Classes
- **`Logger`** (lines 34-125) `[424559d9]`

#### Functions
- **`__init__(self)`** (lines 35-36) `[2b4e2e27]`
- **`build_ffmpeg_command(input_path, output_path, segments, width, height)`** (lines 224-263) `[1c190e84]`
  - *Calls:* detect_video_type
  - *Called by:* process_video
- **`cleanup_memory()`** (lines 127-142) `[d8605206]`
  - *Comprehensive memory and GPU cleanup*
  - *Called by:* main, process_video, main, process_video
- **`complete_processing(self, video_id, text_detected, segments, output_path)`** (lines 90-101) `[22e65f02]`
- **`detect_video_type(width, height)`** (lines 213-222) `[7efa2bff]`
  - *Called by:* build_ffmpeg_command, process_video
- **`error_processing(self, video_id, error)`** (lines 103-105) `[62af42c2]`
- **`exec_db(self, query, params, fetch)`** (lines 57-69) `[3d8248d5]`
  - *Calls:* print
- **`expand_buffer(text_frames, total_frames)`** (lines 165-171) `[20cc842c]`
  - *Add buffer around detected text frames*
  - *Called by:* process_video
- **`format_time(seconds)`** (lines 149-151) `[d8e7f9b2]`
  - *Called by:* process_video, process_video, process_video
- **`frames_to_intervals(frames, fps)`** (lines 173-187) `[7a3f3bc8]`
  - *Called by:* process_video
- **`get_error_details(self, folder_id)`** (lines 118-122) `[396bab08]`
  - *Get detailed error information for failed videos*
- **`get_memory_usage()`** (lines 144-147) `[c11dbe96]`
  - *Get current memory usage in MB*
  - *Called by:* process_video, process_video, main, main, process_video
- **`get_pending(self, folder_id)`** (lines 107-109) `[0f268a87]`
- **`get_summary(self, folder_id)`** (lines 111-116) `[d4f3f577]`
- **`get_video_info(path)`** (lines 195-211) `[37c8710a]`
  - *Calls:* print
  - *Called by:* main
- **`init_db(self)`** (lines 38-55) `[47b5617b]`
- **`log_folder(self, path)`** (lines 71-75) `[1b45560d]`
- **`log_video(self, folder_id, path, size, duration)`** (lines 77-84) `[341668f1]`
- **`main()`** (lines 467-598) `[3e52fd80]`
  - *Calls:* print, print, print, print, print, print, print, cleanup_memory, print, print, print, get_video_info, process_video, cleanup_memory, print, get_memory_usage, get_memory_usage
- **`merge_intervals(intervals)`** (lines 153-163) `[7d786bd7]`
  - *Called by:* process_video
- **`preprocess_frame(frame)`** (lines 189-193) `[0ac57239]`
  - *Called by:* process_video
- **`print(self, msg)`** (lines 124-125) `[7623fda3]`
  - *Calls:* print
  - *Called by:* main, main, main, main, main, main, main, print, test_ffmpeg_command, test_ffmpeg_command, process_video, process_video, process_video, process_video, process_video, process_video, process_video, process_video, process_video, process_video, process_video, process_video, main, main, main, get_video_info, test_ffmpeg_command, test_ffmpeg_command, test_ffmpeg_command, process_video, process_video, process_video, process_video, process_video, process_video, process_video, process_video, main, exec_db, process_video, process_video, process_video, process_video, process_video, process_video
- **`process_video(video_path, logger, video_id, replace_original)`** (lines 286-465) `[c2ce1b18]`
  - *Process single video with comprehensive error handling*
  - *Calls:* get_memory_usage, print, print, print, detect_video_type, print, print, print, print, print, print, build_ffmpeg_command, test_ffmpeg_command, print, print, cleanup_memory, get_memory_usage, print, print, expand_buffer, print, print, print, frames_to_intervals, merge_intervals, print, print, print, print, cleanup_memory, print, print, print, print, format_time, get_memory_usage, preprocess_frame, print, print, format_time, format_time
  - *Called by:* main
- **`start_processing(self, video_id)`** (lines 86-88) `[41411443]`
- **`test_ffmpeg_command(cmd, video_path)`** (lines 265-284) `[b69b632b]`
  - *Test FFmpeg command and return detailed error info*
  - *Calls:* print, print, print, print, print
  - *Called by:* process_video

#### Variables
- `BUFFER_FRAMES` (line 18) `[33c56ebb]`
- `DB_FILE` (line 22) `[3f6e61de]`
- `DELETION_THRESHOLD` (line 20) `[fa36b412]`
- `DETECTION_SCALE` (line 19) `[909570e9]`
- `FFMPEG_SETTINGS` (line 24) `[5b7006bf]`
- `FRAME_SKIP` (line 17) `[9bddee1f]`
- `SOCIAL_RATIOS` (line 29) `[f5c6a49e]`
- `VIDEO_EXTENSIONS` (line 21) `[eadc9b0c]`
- `all_text_frames` (line 372) `[e6ca4053]`
- `batch_size` (line 500) `[91837a0f]`
- `cap` (line 316) `[6d8fe9e7]`
- `clean_duration` (line 400) `[bf608ced]`
- `clean_segments` (line 384) `[44082424]`
- `cmd` (line 417) `[d6921f97]`
- `completed_count` (line 543) `[3bc65ebc]`
- `conn` (line 59) `[350ef74b]`
- `current_memory` (line 573) `[06e465b5]`
- `cursor` (line 60) `[049059f2]`
- `deleted_count` (line 544) `[c4ab4d00]`
- `duration` (line 322) `[d9852227]`
- `end` (line 185) `[ced1a54d]`
- `error_msg` (line 453) `[48c8fd3f]`
- `errors` (line 596) `[bf42daf6]`
- `existing` (line 79) `[767838bc]`
- `expanded` (line 167) `[9eca5062]`
- `failed_count` (line 545) `[ddc59d5d]`
- `filter_complex` (line 242) `[94fd3e8d]`
- `final_memory` (line 446) `[3e21a127]`
- `final_path` (line 432) `[fa2e7165]`
- `folder_id` (line 513) `[65cbdf32]`
- `folder_path` (line 480) `[aaff6ff0]`
- `fps` (line 320) `[11bb6c32]`
- `frame_count` (line 338) `[f8db4705]`
- `frame_list` (line 176) `[29a33dad]`
- `frames` (line 202) `[0c627886]`
- `frames_processed` (line 339) `[5ac762f4]`
- `frames_to_check` (line 330) `[accc2848]`
- `gray` (line 192) `[ea289b81]`
- `height` (line 324) `[06569fa7]`
- `info` (line 518) `[e3756012]`
- `initial_memory` (line 291) `[4b658235]`
- `intervals` (line 177) `[81fd3e5f]`
- `last_end` (line 389) `[cd8ed717]`
- `logger` (line 512) `[6eebf14d]`
- `memory_freed` (line 447) `[58ce7074]`
- `merged` (line 157) `[a00465c1]`
- `merged_intervals` (line 382) `[44b18885]`
- `name` (line 78) `[d3697383]`
- `output_path` (line 413) `[9190fcc9]`
- `pause` (line 576) `[24c7dbc6]`
- `pending` (line 534) `[a4fa3dd1]`
- `process` (line 146) `[42152004]`
- `processed` (line 350) `[43fa73ea]`
- `processing_time` (line 95) `[e8ecf863]`
- `progress` (line 359) `[45804204]`
- `progress_interval` (line 340) `[7f317f1f]`
- `ratio` (line 217) `[bb0f0cd9]`
- `reader` (line 311) `[a6692798]`
- `remaining` (line 565) `[357cf213]`
- `replace` (line 485) `[876e6048]`
- `resized` (line 191) `[2c8de748]`
- `result` (line 61) `[f7a9d91f]`
- `results` (line 351) `[a3715572]`
- `scale` (line 239) `[d89dc4d9]`
- `start` (line 185) `[d925c69f]`
- `start_dt` (line 94) `[9f94a27f]`
- `start_time` (line 91) `[8c31ce5f]`
- `status` (line 560) `[172e28da]`
- `success` (line 550) `[52c2f6f6]`
- `summary` (line 586) `[b368c826]`
- `target_aspect` (line 232) `[f47b8748]`
- `test_single` (line 492) `[04197181]`
- `text_frames` (line 337) `[dd180655]`
- `text_intervals` (line 381) `[a9b16d6d]`
- `text_percentage` (line 401) `[a8b20545]`
- `total_frames` (line 321) `[35fe551d]`
- `total_videos` (line 542) `[960626a0]`
- `use_gpu` (line 305) `[8de22c0f]`
- `vid_id` (line 82) `[939fb50d]`
- `video_info` (line 554) `[fb09bb00]`
- `videos` (line 503) `[9d5db9e4]`
- `width` (line 323) `[70b140d9]`

---

### 📄 `main.py`

#### Imports
- `json` (line 9) `[ff3e4d4d]`
- `os` (line 3) `[de2abade]`
- `pathlib.Path` (line 10) `[fa6ee8af]`
- `random` (line 4) `[7e18ed42]`
- `signal` (line 5) `[10f4eea8]`
- `src.processors.audio_processor.analyze_beats` (line 415) `[a94d8f54]`
- `src.processors.canvas_processor.process_video_with_canvas` (line 16) `[f3ec9c5b]`
- `src.processors.split_screen_processor.SplitScreenProcessor` (line 18) `[eaa9cdd6]`
- `src.processors.split_screen_processor.create_split_screen_video` (line 18) `[9bae604c]`
- `src.processors.split_screen_processor.get_audio_preferences` (line 18) `[02584755]`
- `src.processors.split_screen_processor.get_fit_mode` (line 18) `[a1e7657b]`
- `src.processors.subtitle_processor.generate_subtitles` (line 14) `[21a187d2]`
- `src.processors.subtitle_video_processor.add_subtitles_to_video` (line 15) `[896ebeb5]`
- `src.processors.video_formatter.format_menu` (line 17) `[e194616c]`
- `src.processors.video_generator.generate_video` (line 13) `[0259e986]`
- `src.utils.arg_parser.parse_arguments` (line 33) `[5a61eea1]`
- `src.utils.cache_manager.CacheManager` (line 28) `[45d99fb5]`
- `src.utils.io_operations.IOOperations` (line 29) `[5958acd8]`
- `src.utils.queue_manager.QueueManager` (line 27) `[e3007954]`
- `src.utils.queue_manager.queue_manager` (line 27) `[0323b6cc]`
- `src.utils.temp_file_manager.TempFileManager` (line 26) `[ca937778]`
- `src.utils.temp_file_manager.temp_manager` (line 26) `[71efb9f1]`
- `subprocess` (line 8) `[7d8752c4]`
- `sys` (line 6) `[9e77b374]`
- `time` (line 7) `[4f9b8491]`
- `traceback` (line 770) `[6a6eacd0]`

#### Classes
- **`FFmpegUtils`** (lines 38-104) `[1efab01f]`
- **`VideoProcessingManager`** (lines 107-284) `[d2014dcc]`

#### Functions
- **`__init__(self)`** (lines 110-121) `[6fce9d33]`
- **`_initialize_session(self)`** (lines 123-164) `[179c6068]`
  - *Initialize the processing session*
- **`_is_image_file(self, path)`** (lines 249-252) `[342bf839]`
  - *Check if file is an image*
- **`_signal_handler(self, signum, frame)`** (lines 166-171) `[0434c6af]`
  - *Handle shutdown signals gracefully*
- **`check_ffmpeg_installation()`** (lines 42-55) `[f3c171e5]`
  - *Check if FFmpeg is installed and accessible*
- **`check_ffprobe_installation()`** (lines 58-71) `[d15da511]`
  - *Check if FFprobe is installed and accessible*
- **`check_large_project_warning(self, beat_count, estimated_time)`** (lines 265-284) `[b1275eaa]`
  - *Check if project is large and warn user*
- **`cleanup_session(self)`** (lines 173-193) `[1cede130]`
  - *Clean up the processing session*
- **`estimate_processing_time(self, audio_duration, content_type, num_files)`** (lines 254-263) `[e171959e]`
  - *Estimate processing time based on content*
- **`get_additional_media_configuration()`** (lines 507-563) `[f8a32b58]`
  - *Get additional media configuration*
  - *Called by:* get_video_generation_inputs
- **`get_audio_duration(self, audio_path)`** (lines 214-227) `[847f7e15]`
  - *Get audio duration using FFprobe*
- **`get_custom_filters()`** (lines 500-504) `[379a2020]`
  - *Get custom filter configuration*
  - *Called by:* get_filter_configuration
- **`get_filter_configuration()`** (lines 457-475) `[6f5b5959]`
  - *Get filter configuration from user*
  - *Calls:* get_preset_filters, get_custom_filters
  - *Called by:* get_video_generation_inputs
- **`get_preset_filters()`** (lines 478-497) `[3397a705]`
  - *Get preset filter configuration*
  - *Called by:* get_filter_configuration
- **`get_user_inputs()`** (lines 287-316) `[63544f15]`
  - *Get user inputs for video generation*
  - *Calls:* get_video_generation_inputs, handle_subtitles, handle_canvas, handle_formatting, handle_split_screen, handle_combine_videos, get_user_inputs
  - *Called by:* main, get_user_inputs
- **`get_video_duration(self, video_path)`** (lines 209-212) `[d22f217f]`
  - *Get video duration using FFprobe*
- **`get_video_generation_inputs()`** (lines 319-454) `[915adb12]`
  - *Get inputs for video generation*
  - *Calls:* get_filter_configuration, get_additional_media_configuration
  - *Called by:* get_user_inputs
- **`get_video_info_simple(video_path)`** (lines 74-104) `[64d5ab36]`
  - *Get basic video info using FFprobe*
- **`handle_canvas()`** (lines 593-610) `[c8cc1467]`
  - *Handle canvas addition*
  - *Called by:* get_user_inputs
- **`handle_combine_videos()`** (lines 671-729) `[058baf9e]`
  - *Handle video combination*
  - *Called by:* get_user_inputs
- **`handle_formatting()`** (lines 613-625) `[eec644e8]`
  - *Handle video formatting*
  - *Called by:* get_user_inputs
- **`handle_split_screen()`** (lines 628-668) `[eb57bd48]`
  - *Handle split-screen video creation*
  - *Called by:* get_user_inputs
- **`handle_subtitles()`** (lines 566-590) `[c1f847e4]`
  - *Handle subtitle addition*
  - *Called by:* get_user_inputs
- **`is_audio_file(self, path)`** (lines 204-207) `[259f9240]`
  - *Check if file is an audio file*
- **`is_video_file(self, path)`** (lines 195-202) `[02d6018f]`
  - *Check if file is a video using FFprobe*
- **`main()`** (lines 732-775) `[89c5c061]`
  - *Main application entry point*
  - *Calls:* get_user_inputs
- **`validate_input_files(self, audio_path, content_path)`** (lines 229-247) `[5967b269]`
  - *Validate input files*

#### Variables
- `args` (line 740) `[958a2e0c]`
- `audio_duration` (line 369) `[64b2dfca]`
- `audio_extensions` (line 206) `[7293dca3]`
- `audio_path` (line 347) `[10d89ec1]`
- `audio_prefs` (line 655) `[12015412]`
- `available_gb` (line 271) `[ba3f320c]`
- `base_time` (line 256) `[6b01a2b4]`
- `beat_times` (line 417) `[525a85a6]`
- `cache_entries` (line 152) `[2c8e42ba]`
- `cache_hit_rate` (line 153) `[edf04676]`
- `cache_size_mb` (line 151) `[d0a6152b]`
- `cache_stats` (line 179) `[36df3dfb]`
- `change_interval` (line 411) `[c76a6e65]`
- `choice` (line 300) `[3447591a]`
- `cmd` (line 217) `[7bdbb5ee]`
- `concat_file` (line 701) `[4a290dcd]`
- `config` (line 750) `[59b71955]`
- `content_path` (line 348) `[c461b736]`
- `cutting_choice` (line 365) `[6d2398fb]`
- `cutting_mode` (line 366) `[dacbe9c5]`
- `data` (line 223) `[46573293]`
- `disk_info` (line 270) `[e011744a]`
- `duration` (line 538) `[a5790598]`
- `duration_choice` (line 375) `[b1d6eeeb]`
- `errors` (line 231) `[8c549465]`
- `estimated_segments` (line 418) `[6563483e]`
- `estimated_space_gb` (line 272) `[10599aeb]`
- `estimated_time` (line 419) `[c65dbebb]`
- `filter_choice` (line 465) `[66f2cec7]`
- `filter_config` (line 429) `[94af7b1c]`
- `fit_mode` (line 652) `[030a78b1]`
- `format_choice` (line 648) `[9c949875]`
- `freq_choice` (line 395) `[2e4430a2]`
- `frequency` (line 398) `[7308fd16]`
- `frequency_map` (line 397) `[27ca8a64]`
- `image_extensions` (line 251) `[ebc26ea5]`
- `interval_choice` (line 409) `[bca43b9f]`
- `interval_map` (line 410) `[f37ee613]`
- `manager` (line 735) `[e2c9e1bc]`
- `media_choice` (line 516) `[de3aefa4]`
- `media_config` (line 432) `[9ceb6934]`
- `media_path` (line 551) `[38506980]`
- `media_type` (line 548) `[568141f5]`
- `output_name` (line 437) `[7f97cdae]`
- `output_path` (line 582) `[bb9fa0a5]`
- `parse_arguments` (line 35) `[c1760bc1]`
- `placement` (line 549) `[cd87ca8b]`
- `preset_choice` (line 487) `[b44fdc25]`
- `presets` (line 489) `[c340fe89]`
- `queue_stats` (line 180) `[a0db8da8]`
- `response` (line 281) `[dd448cac]`
- `result` (line 222) `[a19e01cd]`
- `segments` (line 267) `[dbf05c5a]`
- `subtitle_json` (line 577) `[16a74d35]`
- `success` (line 758) `[26e61900]`
- `sync_choice` (line 343) `[75e58397]`
- `sync_mode` (line 344) `[db5017d3]`
- `target_size` (line 336) `[407c7b88]`
- `video1_path` (line 632) `[2b250fff]`
- `video2_path` (line 633) `[97303a1e]`
- `video_format` (line 649) `[4a71952f]`
- `video_info` (line 211) `[48ed35bb]`
- `video_path` (line 678) `[b7642f4f]`
- `video_paths` (line 676) `[5641b22e]`
- `video_stream` (line 89) `[b2682d4d]`

---

### 📄 `src/processors/__init__.py`

#### Imports
- `audio_processor.analyze_beats` (line 1) `[04b1385e]`
- `video_generator.generate_video` (line 6) `[6bcd760b]`
- `video_processor.process_video` (line 2) `[c74b770f]`

#### Variables
- `__all__` (line 7) `[12d0ea8e]`

---

### 📄 `src/processors/audio_processor.py`

#### Imports
- `dataclasses.dataclass` (line 10) `[0010e60c]`
- `enum.Enum` (line 11) `[3b3f4ac9]`
- `hashlib` (line 7) `[ada1d9e0]`
- `json` (line 6) `[ff3e4d4d]`
- `librosa` (line 15) `[c4b23121]`
- `logging` (line 12) `[27dced09]`
- `numpy` (line 13) `[d8fca9de]`
- `os` (line 3) `[de2abade]`
- `pathlib.Path` (line 8) `[fa6ee8af]`
- `scipy.ndimage.gaussian_filter1d` (line 16) `[1b5d27bc]`
- `src.utils.cache_manager.CacheManager` (line 21) `[45d99fb5]`
- `src.utils.queue_manager.TaskStatus` (line 20) `[d7680471]`
- `src.utils.queue_manager.queue_manager` (line 20) `[0323b6cc]`
- `src.utils.temp_file_manager.TaskPriority` (line 19) `[0b5c99e9]`
- `src.utils.temp_file_manager.TaskType` (line 19) `[41fc328b]`
- `src.utils.temp_file_manager.temp_manager` (line 19) `[71efb9f1]`
- `threading` (line 5) `[90781f3e]`
- `time` (line 4) `[4f9b8491]`
- `typing.Any` (line 9) `[4ec2ae04]`
- `typing.Dict` (line 9) `[db5e932b]`
- `typing.List` (line 9) `[eada0f80]`
- `typing.Optional` (line 9) `[abdbaea6]`
- `typing.Tuple` (line 9) `[23996b74]`

#### Classes
- **`AnalysisType`** (lines 23-30) `[c5a3609b]`
  - *Inherits from:* Enum
- **`AudioAnalysisResult`** (lines 33-41) `[5f3fb8e7]`
- **`AudioProcessor`** (lines 43-449) `[56ff200b]`

#### Functions
- **`__init__(self)`** (lines 55-90) `[d23bce89]`
- **`analyze_beats(audio_path, sensitivity)`** (lines 456-481) `[ed802181]`
  - *Analyze audio file and detect beat timings (backward compatible function)*
- **`analyze_beats_with_caching(self, audio_path, sensitivity)`** (lines 107-250) `[6e42bd07]`
  - *Analyze audio file and detect beat timings with caching*
- **`analyze_vocal_changes_with_caching(self, audio_path, threshold)`** (lines 252-426) `[80cf769f]`
  - *Analyze audio file and detect vocal changes with caching*
- **`cleanup_audio_cache(max_age_hours)`** (lines 522-529) `[ab2403b9]`
  - *Clean up old audio analysis cache files*
- **`cleanup_cache(self, max_age_hours)`** (lines 442-449) `[8ed89ae6]`
  - *Clean up old cached analysis results*
- **`detect_vocal_changes(audio_path, threshold)`** (lines 484-509) `[4a4d6a32]`
  - *Detect changes in vocal presence in the audio (backward compatible function)*
- **`get_audio_processing_stats()`** (lines 512-519) `[5dd7061c]`
  - *Get audio processing statistics*
- **`get_cache_key(self, audio_path, analysis_type, params)`** (lines 92-101) `[425bcbd2]`
  - *Generate cache key for audio analysis*
- **`get_processing_stats(self)`** (lines 428-440) `[c85b7fdd]`
  - *Get processing statistics*
- **`smooth_signal(self, signal, window_size)`** (lines 103-105) `[0eca3f4f]`
  - *Custom smoothing function using gaussian filter*

#### Variables
- `BEATS` (line 25) `[c3dc4191]`
- `HARMONIC_PERCUSSIVE` (line 30) `[538bc0a0]`
- `ONSET_STRENGTH` (line 29) `[8b3e44d2]`
- `SPECTRAL_FEATURES` (line 28) `[a5d9c13c]`
- `TEMPO` (line 27) `[aee4463b]`
- `VOCAL_CHANGES` (line 26) `[68bb4ef1]`
- `analysis_params` (line 94) `[d716cc48]`
- `audio_processor` (line 453) `[eec148d8]`
- `beat_times` (line 173) `[9f166f4b]`
- `beats` (line 162) `[05ec1cc8]`
- `cache_key` (line 270) `[262662e3]`
- `cached_result` (line 275) `[5704785c]`
- `contrast` (line 315) `[b38140ec]`
- `feature_smooth` (line 326) `[c260e6e6]`
- `feature_sum` (line 325) `[38e6c3e7]`
- `final_cache_key` (line 397) `[e86135a3]`
- `mel_spect` (line 303) `[3756370f]`
- `mel_spect_db` (line 312) `[c502f433]`
- `onset_env` (line 345) `[5c770688]`
- `params` (line 264) `[dc23dacb]`
- `peaks` (line 346) `[a6012b11]`
- `processing_time` (line 357) `[42b3c501]`
- `result` (line 360) `[04e77438]`
- `result_data` (line 384) `[b84675de]`
- `start_time` (line 293) `[6dfdf41d]`
- `temp_file` (line 378) `[6377d60d]`
- `vocal_times` (line 355) `[f9bda5c9]`

---

### 📄 `src/processors/canvas_processor.py`

#### Imports
- `PIL.Image` (line 14) `[4f84112b]`
- `PIL.ImageDraw` (line 14) `[c2831568]`
- `PIL.ImageFont` (line 14) `[0b3f9671]`
- `dataclasses.dataclass` (line 12) `[0010e60c]`
- `json` (line 7) `[ff3e4d4d]`
- `logging` (line 13) `[27dced09]`
- `numpy` (line 9) `[d8fca9de]`
- `os` (line 981) `[de2abade]`
- `pathlib.Path` (line 10) `[fa6ee8af]`
- `psutil` (line 980) `[f6b32ab9]`
- `shutil` (line 498) `[582f9ff7]`
- `src.utils.cache_manager.CacheManager` (line 19) `[45d99fb5]`
- `src.utils.queue_manager.TaskStatus` (line 18) `[d7680471]`
- `src.utils.queue_manager.queue_manager` (line 18) `[0323b6cc]`
- `src.utils.temp_file_manager.TaskPriority` (line 17) `[0b5c99e9]`
- `src.utils.temp_file_manager.TaskType` (line 17) `[41fc328b]`
- `src.utils.temp_file_manager.temp_manager` (line 17) `[71efb9f1]`
- `subprocess` (line 6) `[7d8752c4]`
- `tempfile` (line 8) `[09d25239]`
- `threading` (line 5) `[90781f3e]`
- `time` (line 4) `[4f9b8491]`
- `typing.Any` (line 11) `[4ec2ae04]`
- `typing.Dict` (line 11) `[db5e932b]`
- `typing.List` (line 11) `[eada0f80]`
- `typing.Optional` (line 11) `[abdbaea6]`
- `typing.Tuple` (line 11) `[23996b74]`

#### Classes
- **`CanvasProcessor`** (lines 388-1022) `[2816ec93]`
- **`CanvasResult`** (lines 22-30) `[7d95e41a]`
- **`FFmpegCanvasProcessor`** (lines 42-386) `[4d41ef50]`
- **`TextOverlay`** (lines 33-40) `[8018fc3e]`

#### Functions
- **`__init__(self)`** (lines 402-439) `[f17e3012]`
- **`_convert_color_to_ffmpeg(self, color)`** (lines 366-386) `[1fbfe4ae]`
  - *Convert color to FFmpeg drawtext format*
- **`_convert_color_to_hex(self, color)`** (lines 342-364) `[6fc48e59]`
  - *Convert color name or hex to FFmpeg-compatible hex format*
- **`_create_text_overlays(self, text_prefs)`** (lines 596-633) `[1e14298d]`
  - *Create text overlay configurations from preferences*
- **`_process_canvas_task(self, task_data)`** (lines 867-904) `[726987d6]`
  - *Process a single canvas task*
- **`add_text_overlay(self, video_path, output_path, text_overlays)`** (lines 150-217) `[2255f861]`
  - *Add text overlays to video using FFmpeg drawtext filter*
- **`apply_canvas_effects(self, video_path, output_path, effects)`** (lines 279-340) `[91689735]`
  - *Apply various canvas effects using FFmpeg filters*
- **`apply_canvas_to_video(video_path, canvas_config, output_path)`** (lines 1116-1152) `[4d80ff42]`
  - *Apply canvas to video with specific configuration using FFmpeg*
- **`apply_canvas_with_caching(self, video_path, output_path, canvas_color, margin_size, text_prefs, effects)`** (lines 460-594) `[9e19faad]`
  - *Apply canvas to video with comprehensive caching*
- **`batch_create_canvases(self, canvas_specs, completed_callback)`** (lines 828-865) `[349a55f8]`
  - *Create multiple canvases in batch*
- **`cleanup_session(self)`** (lines 956-975) `[f28d0ce8]`
  - *Clean up canvas processing session*
- **`clear_cache(self)`** (lines 917-925) `[01fb9c6f]`
  - *Clear all cached canvas results*
- **`create_canvas_batch(canvas_specs, timeout)`** (lines 1077-1113) `[ff07497e]`
  - *Create multiple canvases in batch with FFmpeg and disk-based caching*
- **`create_canvas_preset(self, preset_name)`** (lines 721-766) `[2dbcbb09]`
  - *Create canvas configuration from preset*
- **`create_canvas_preset_video(video_path, preset_name, output_path)`** (lines 1155-1194) `[2e82bb3d]`
  - *Apply canvas preset to video using FFmpeg*
- **`create_canvas_with_video(self, video_path, output_path, canvas_color, margin_size, target_size)`** (lines 82-148) `[8df3b940]`
  - *Create canvas around video using FFmpeg overlay filters*
- **`create_rounded_canvas(self, video_path, output_path, canvas_color, margin_size, corner_radius)`** (lines 219-277) `[1e026052]`
  - *Create canvas with rounded corners using FFmpeg*
- **`end_processing_session(self)`** (lines 449-454) `[a4a880fc]`
  - *End current canvas processing session*
- **`estimate_processing_time(self, video_specs)`** (lines 797-826) `[9242a780]`
  - *Estimate processing time for canvas operations*
- **`get_available_presets()`** (lines 1197-1199) `[bbf5519d]`
  - *Get list of available canvas presets*
- **`get_cache_key(self, identifier, params)`** (lines 456-458) `[6f4d9e94]`
  - *Generate cache key for canvas processing*
- **`get_cache_statistics(self)`** (lines 787-795) `[6590fd05]`
  - *Get canvas cache statistics*
- **`get_canvas_usage_stats(self)`** (lines 927-954) `[70bc0beb]`
  - *Get statistics about canvas usage*
- **`get_memory_usage(self)`** (lines 977-1002) `[2c66078e]`
  - *Get current memory usage statistics*
- **`get_performance_stats(self)`** (lines 768-785) `[5d8b921e]`
  - *Get canvas processing performance statistics*
- **`get_preset_description(preset_name)`** (lines 1202-1210) `[609160df]`
  - *Get description of canvas preset*
- **`get_user_preferences(self)`** (lines 635-719) `[fd8a9b27]`
  - *Get canvas preferences from user input*
- **`get_video_info(self, video_path)`** (lines 49-80) `[ab780b5b]`
  - *Get video information using FFprobe*
- **`log_performance_summary(self)`** (lines 1004-1022) `[05b45ac0]`
  - *Log a comprehensive performance summary*
- **`optimize_canvas_cache(self)`** (lines 911-915) `[4a79d540]`
  - *Optimize canvas cache by removing unused entries*
- **`process_video_with_canvas(video_path, output_path)`** (lines 1025-1074) `[afde2e6c]`
  - *Main entry point for processing video with canvas using FFmpeg and disk-based caching*
- **`start_processing_session(self, session_name)`** (lines 441-447) `[8848bdb3]`
  - *Start a new canvas processing session*
- **`validate_canvas_config(config)`** (lines 1213-1246) `[b118696a]`
  - *Validate canvas configuration*
- **`wait_for_batch(self, task_ids, timeout)`** (lines 906-909) `[25aa1e4e]`
  - *Wait for batch of canvas tasks to complete*

#### Variables
- `add_border` (line 704) `[6cc54dbd]`
- `add_effects` (line 698) `[308240ec]`
- `add_rounded` (line 711) `[5d560c0b]`
- `add_text` (line 671) `[fbbbd670]`
- `base_path` (line 1051) `[17129eee]`
- `base_time` (line 811) `[7dc94576]`
- `blur` (line 300) `[d0da8736]`
- `blur_strength` (line 316) `[30405090]`
- `border_color` (line 707) `[b8e79d31]`
- `border_params` (line 308) `[84710550]`
- `border_width` (line 706) `[c437fd26]`
- `bottom_text` (line 691) `[2ea14799]`
- `cache_key` (line 489) `[81998606]`
- `cache_stats` (line 1007) `[098c8e23]`
- `cached_path` (line 492) `[de06619f]`
- `canvas_height` (line 109) `[81613a03]`
- `canvas_params` (line 482) `[e31c665b]`
- `canvas_temp` (line 508) `[4d70f333]`
- `canvas_width` (line 108) `[cc2baec6]`
- `cmd` (line 327) `[86d7fd75]`
- `color` (line 310) `[b3a7f58b]`
- `color_choice` (line 654) `[bce7e670]`
- `color_hex` (line 250) `[f0e002eb]`
- `color_map` (line 374) `[d01639d7]`
- `color_usage` (line 929) `[2105797c]`
- `completed_callback` (line 1097) `[291c8669]`
- `corner_radius` (line 713) `[49abf5d3]`
- `current_video` (line 557) `[a84bb191]`
- `custom_color` (line 658) `[63736304]`
- `data` (line 58) `[d97ec664]`
- `descriptions` (line 1204) `[9bc81ef1]`
- `drawtext_filter` (line 181) `[d292be0d]`
- `effects` (line 701) `[7f0e284e]`
- `effects_temp` (line 545) `[e29ae0b5]`
- `effects_time` (line 817) `[ef739f87]`
- `escaped_text` (line 175) `[54b4162a]`
- `filter_complex` (line 253) `[0f9888d5]`
- `filter_parts` (line 293) `[12801e00]`
- `margin` (line 939) `[e9d8aa78]`
- `margin_range` (line 940) `[005dfd6c]`
- `margin_usage` (line 930) `[4c3e005a]`
- `memory_info` (line 984) `[4f1b47fc]`
- `memory_stats` (line 1008) `[a71b971e]`
- `offset_x` (line 298) `[d0744734]`
- `offset_y` (line 299) `[86a95967]`
- `original_height` (line 239) `[94a2c57e]`
- `original_width` (line 238) `[a1c35951]`
- `output_path` (line 1052) `[4290ab88]`
- `overlays` (line 598) `[044ce63f]`
- `preferences` (line 1043) `[f203ebfa]`
- `preset_config` (line 1172) `[22f9c712]`
- `presets` (line 723) `[b4024be5]`
- `process` (line 983) `[d49e1ea1]`
- `processing_time` (line 881) `[6fab5fbc]`
- `processor` (line 1168) `[de48e460]`
- `result` (line 335) `[1732d6fb]`
- `result_path` (line 872) `[d74832bb]`
- `results` (line 1096) `[74eb2a30]`
- `session_id` (line 452) `[6f831080]`
- `shadow_params` (line 297) `[65d1e98f]`
- `size` (line 822) `[b45e7c8c]`
- `size_factor` (line 823) `[5854174e]`
- `start_time` (line 870) `[0851d5cc]`
- `stats` (line 1006) `[63aeeb2d]`
- `subtitle` (line 684) `[d28ebcf5]`
- `success` (line 548) `[76a3d105]`
- `task_data` (line 844) `[b4edd44e]`
- `task_id` (line 854) `[142e4012]`
- `task_ids` (line 1099) `[bdd67c3d]`
- `temp_files` (line 504) `[2888c6e4]`
- `text_color` (line 178) `[3b816736]`
- `text_overlays` (line 529) `[41fb9747]`
- `text_prefs` (line 1237) `[9ecda0dc]`
- `text_temp` (line 526) `[aef1ce92]`
- `text_time` (line 814) `[a96b9c01]`
- `text_usage` (line 931) `[e4cf9ec3]`
- `title` (line 677) `[298219b0]`
- `total_requests` (line 779) `[47fd6421]`
- `total_time` (line 807) `[e519aad4]`
- `usage_stats` (line 1009) `[31da9c23]`
- `use_canvas` (line 640) `[e43e90e3]`
- `video_filter` (line 325) `[31b7bb56]`
- `video_info` (line 237) `[bc593e48]`
- `video_stream` (line 64) `[2a8b4724]`
- `video_x` (line 246) `[f1ca2f77]`
- `video_y` (line 247) `[9adaf7a2]`
- `width` (line 309) `[de3a4b87]`

---

### 📄 `src/processors/filters/__init__.py`

#### Imports
- `filter_registry.FILTER_REGISTRY` (line 39) `[a78214ef]`
- `filter_registry.discover_filters` (line 39) `[ee0f37c3]`
- `filter_registry.get_all_filters` (line 39) `[bd613e0e]`
- `filter_registry.get_filters_by_category` (line 39) `[cfddc25c]`
- `filter_registry.register_filter` (line 39) `[6bdc2823]`

#### Functions
- **`_initialize_filters()`** (lines 62-69) `[191d1af5]`
  - *Initialize filter discovery when package is imported*

#### Variables
- `__all__` (line 53) `[df8bea70]`
- `__author__` (line 49) `[d1e41172]`
- `__description__` (line 50) `[284c7ac6]`
- `__version__` (line 48) `[e4e3db4d]`
- `discovered_count` (line 65) `[d53b5593]`

---

### 📄 `src/processors/filters/artistic_filters.py`

#### Imports
- `filter_registry.register_filter` (line 14) `[6bdc2823]`
- `moviepy.editor.ImageClip` (line 11) `[87414a47]`
- `moviepy.editor.VideoFileClip` (line 11) `[3951e41b]`
- `moviepy.video.fx.all` (line 12) `[9ae2cd69]`
- `numpy` (line 10) `[d8fca9de]`
- `random` (line 15) `[7e18ed42]`
- `typing.Union` (line 13) `[26723ff1]`

#### Functions
- **`apply_blur(clip, intensity)`** (lines 26-43) `[fddf8c16]`
  - *Apply gaussian blur effect*
- **`apply_edge_detection(clip, intensity)`** (lines 204-255) `[6eb13f09]`
  - *Apply edge detection filter*
  - *Calls:* edge_effect
- **`apply_emboss(clip, intensity)`** (lines 417-459) `[a82723a2]`
  - *Apply emboss effect for 3D relief appearance*
  - *Calls:* emboss_effect
- **`apply_film_grain(clip, intensity)`** (lines 159-193) `[ca87f191]`
  - *Add film grain effect*
  - *Calls:* grain_effect
- **`apply_glow(clip, intensity)`** (lines 356-406) `[b16f4713]`
  - *Apply glow effect to bright areas*
  - *Calls:* glow_effect
- **`apply_mosaic(clip, intensity)`** (lines 306-345) `[366b8573]`
  - *Apply mosaic/pixelation effect*
  - *Calls:* mosaic_effect
- **`apply_posterize(clip, intensity)`** (lines 266-295) `[d6b1a09f]`
  - *Apply posterization effect (reduce color levels)*
  - *Calls:* posterize_effect
- **`apply_sharpen(clip, intensity)`** (lines 54-94) `[6017dae9]`
  - *Apply sharpening filter*
  - *Calls:* sharpen_effect
- **`apply_vignette(clip, intensity)`** (lines 105-148) `[0c27e17d]`
  - *Apply vignette effect (darkened edges)*
  - *Calls:* vignette_effect
- **`edge_effect(get_frame, t)`** (lines 218-253) `[b7500423]`
  - *Called by:* apply_edge_detection
- **`emboss_effect(get_frame, t)`** (lines 431-457) `[a097eeac]`
  - *Called by:* apply_emboss
- **`glow_effect(get_frame, t)`** (lines 370-404) `[44758ed6]`
  - *Called by:* apply_glow
- **`grain_effect(get_frame, t)`** (lines 173-191) `[3969a0d1]`
  - *Called by:* apply_film_grain
- **`mosaic_effect(get_frame, t)`** (lines 320-343) `[5f549096]`
  - *Called by:* apply_mosaic
- **`posterize_effect(get_frame, t)`** (lines 280-293) `[7264a981]`
  - *Called by:* apply_posterize
- **`sharpen_effect(get_frame, t)`** (lines 68-92) `[fc19e4c0]`
  - *Called by:* apply_sharpen
- **`vignette_effect(get_frame, t)`** (lines 119-146) `[d8e79fb5]`
  - *Called by:* apply_vignette

#### Variables
- `avg_color` (line 338) `[3daf62a8]`
- `block` (line 337) `[effbd3bd]`
- `block_size` (line 325) `[2fd79664]`
- `blur_radius` (line 41) `[8b99ef1d]`
- `blurred` (line 73) `[31899a91]`
- `blurred_glow` (line 389) `[7ff26d8b]`
- `bright_mask` (line 375) `[bed5c91c]`
- `bright_mask_3d` (line 382) `[c110a02b]`
- `brightness` (line 374) `[13d4c474]`
- `distance` (line 129) `[c124d8f6]`
- `edges` (line 248) `[8f9e2e33]`
- `emboss_kernel` (line 435) `[a21a9e2d]`
- `embossed` (line 452) `[dfe54377]`
- `frame` (line 432) `[e6cb1541]`
- `glow_layer` (line 378) `[01d47076]`
- `glowing` (line 402) `[b8b9108a]`
- `grainy` (line 189) `[a7c857b1]`
- `gray` (line 225) `[b85e993a]`
- `gx` (line 239) `[381e19b1]`
- `gy` (line 240) `[fcbc8a49]`
- `i_end` (line 333) `[fc5a5f79]`
- `j_end` (line 334) `[41e353a1]`
- `kernel_size` (line 390) `[a89b711a]`
- `levels` (line 284) `[747a5f6d]`
- `max_distance` (line 132) `[ae986948]`
- `mosaic` (line 328) `[6c8e6e77]`
- `noise` (line 183) `[d9317423]`
- `patch` (line 444) `[622c8e78]`
- `posterized` (line 291) `[26181db2]`
- `region` (line 394) `[4c1032f9]`
- `result` (line 455) `[4ecf625e]`
- `sharpened` (line 90) `[8f072904]`
- `sobel_x` (line 229) `[5218e177]`
- `sobel_y` (line 231) `[d0693907]`
- `step` (line 287) `[d2c6b84d]`
- `vignette_mask` (line 141) `[549392af]`
- `vignetted` (line 144) `[44f9432f]`
- `x` (line 124) `[7dee8bc8]`
- `y` (line 125) `[7e4dc342]`

---

### 📄 `src/processors/filters/brightness_filters.py`

#### Imports
- `filter_registry.register_filter` (line 14) `[6bdc2823]`
- `moviepy.editor.ImageClip` (line 11) `[87414a47]`
- `moviepy.editor.VideoFileClip` (line 11) `[3951e41b]`
- `moviepy.video.fx.all` (line 12) `[9ae2cd69]`
- `numpy` (line 10) `[d8fca9de]`
- `typing.Union` (line 13) `[26723ff1]`

#### Functions
- **`apply_auto_levels(clip, intensity)`** (lines 340-376) `[658700a1]`
  - *Automatically adjust levels for optimal brightness and contrast*
  - *Calls:* auto_levels_effect
- **`apply_brighten(clip, intensity)`** (lines 53-70) `[91e4dca4]`
  - *Brighten the video by increasing brightness*
- **`apply_curves(clip, intensity)`** (lines 284-329) `[32beca7b]`
  - *Apply S-curve adjustment for enhanced contrast and color*
  - *Calls:* curves_effect
- **`apply_darken(clip, intensity)`** (lines 25-42) `[a62cc584]`
  - *Darken the video by reducing brightness*
- **`apply_exposure(clip, intensity)`** (lines 194-225) `[d013cc62]`
  - *Simulate exposure adjustment (like camera settings)*
  - *Calls:* exposure_effect
- **`apply_gamma_correction(clip, intensity)`** (lines 155-183) `[e09b4790]`
  - *Apply gamma correction to adjust midtones*
  - *Calls:* gamma_effect
- **`apply_high_contrast(clip, intensity)`** (lines 81-107) `[4b07103b]`
  - *Increase contrast by expanding tonal range*
  - *Calls:* contrast_effect
- **`apply_low_contrast(clip, intensity)`** (lines 118-144) `[2a2bc207]`
  - *Reduce contrast for a softer look*
  - *Calls:* low_contrast_effect
- **`apply_shadow_highlight(clip, intensity)`** (lines 236-273) `[8aad2709]`
  - *Lift shadows and/or pull down highlights*
  - *Calls:* shadow_highlight_effect
- **`auto_levels_effect(get_frame, t)`** (lines 354-374) `[d73e57c6]`
  - *Called by:* apply_auto_levels
- **`contrast_effect(get_frame, t)`** (lines 95-105) `[dabc7fa8]`
  - *Called by:* apply_high_contrast
- **`curves_effect(get_frame, t)`** (lines 298-327) `[6aa8b035]`
  - *Called by:* apply_curves
- **`exposure_effect(get_frame, t)`** (lines 208-223) `[446aeb2c]`
  - *Called by:* apply_exposure
- **`gamma_effect(get_frame, t)`** (lines 169-181) `[fb93ec30]`
  - *Called by:* apply_gamma_correction
- **`low_contrast_effect(get_frame, t)`** (lines 132-142) `[548570df]`
  - *Called by:* apply_low_contrast
- **`shadow_highlight_effect(get_frame, t)`** (lines 250-271) `[ba99b700]`
  - *Called by:* apply_shadow_highlight

#### Variables
- `brightness_factor` (line 68) `[facd7e60]`
- `contrast_factor` (line 136) `[0106b5f2]`
- `corrected` (line 179) `[d00e65c0]`
- `curve_strength` (line 306) `[b394baac]`
- `exposed` (line 221) `[65c42a23]`
- `exposure_multiplier` (line 215) `[130b0007]`
- `frame` (line 355) `[a7769e92]`
- `gamma` (line 176) `[1609f6b2]`
- `highlight_mask` (line 258) `[30a990fe]`
- `highlight_pull` (line 265) `[b3eb856f]`
- `highlights` (line 317) `[528f6726]`
- `max_val` (line 359) `[1eb89fa6]`
- `midpoint` (line 312) `[d2bf18bf]`
- `min_val` (line 358) `[3d9adfec]`
- `normalized` (line 302) `[35389a06]`
- `result` (line 372) `[7d338e1e]`
- `s_curve` (line 309) `[9206e9a5]`
- `shadow_lift` (line 261) `[f606af0d]`
- `shadow_mask` (line 257) `[e0ee260b]`
- `shadows` (line 313) `[6efedde0]`
- `stretched` (line 366) `[fb898b6d]`

---

### 📄 `src/processors/filters/color_filters.py`

#### Imports
- `filter_registry.register_filter` (line 15) `[6bdc2823]`
- `moviepy.editor.ImageClip` (line 12) `[87414a47]`
- `moviepy.editor.VideoFileClip` (line 12) `[3951e41b]`
- `moviepy.video.fx.all` (line 13) `[9ae2cd69]`
- `numpy` (line 11) `[d8fca9de]`
- `typing.Union` (line 14) `[26723ff1]`

#### Functions
- **`apply_color_temperature(clip, intensity)`** (lines 188-221) `[02399001]`
  - *Adjust color temperature*
  - *Calls:* temperature_effect
- **`apply_desaturate(clip, intensity)`** (lines 106-134) `[e76af9dc]`
  - *Reduce color saturation*
  - *Calls:* desaturate_effect
- **`apply_grayscale(clip, intensity)`** (lines 26-49) `[33e1bd2d]`
  - *Convert clip to grayscale with adjustable intensity*
  - *Calls:* blend_frames
- **`apply_invert(clip, intensity)`** (lines 337-362) `[29b93346]`
  - *Invert colors with adjustable intensity*
  - *Calls:* invert_effect
- **`apply_saturate(clip, intensity)`** (lines 145-177) `[bcbb9808]`
  - *Increase color saturation*
  - *Calls:* saturate_effect
- **`apply_sepia(clip, intensity)`** (lines 60-95) `[2f495094]`
  - *Apply sepia tone effect*
  - *Calls:* sepia_effect
- **`apply_tint(clip, intensity, tint_color)`** (lines 232-274) `[2cd33586]`
  - *Apply color tint overlay*
  - *Calls:* tint_effect
- **`apply_vintage_colors(clip, intensity)`** (lines 285-326) `[ea4b56ec]`
  - *Apply vintage color grading effect*
  - *Calls:* vintage_effect
- **`blend_frames(get_frame, t)`** (lines 44-47) `[68965d5e]`
  - *Called by:* apply_grayscale
- **`desaturate_effect(get_frame, t)`** (lines 120-132) `[e4b3e540]`
  - *Called by:* apply_desaturate
- **`invert_effect(get_frame, t)`** (lines 351-360) `[5559e517]`
  - *Called by:* apply_invert
- **`saturate_effect(get_frame, t)`** (lines 159-175) `[a6f89830]`
  - *Called by:* apply_saturate
- **`sepia_effect(get_frame, t)`** (lines 74-93) `[9bf32e9a]`
  - *Called by:* apply_sepia
- **`temperature_effect(get_frame, t)`** (lines 202-219) `[de160ff8]`
  - *Called by:* apply_color_temperature
- **`tint_effect(get_frame, t)`** (lines 248-272) `[12ba0acd]`
  - *Called by:* apply_tint
- **`vintage_effect(get_frame, t)`** (lines 299-324) `[434ff391]`
  - *Called by:* apply_vintage_colors

#### Variables
- `blended` (line 260) `[a1d8e593]`
- `frame` (line 352) `[5228a2ef]`
- `gray` (line 317) `[4c191222]`
- `gray_frame` (line 46) `[8001ec89]`
- `gray_rgb` (line 318) `[db179525]`
- `grayscale_clip` (line 43) `[b79f48fd]`
- `inverted` (line 355) `[b5ec53a7]`
- `normalized` (line 312) `[7a4405a6]`
- `normalized_frame` (line 256) `[23ba1aa6]`
- `normalized_tint` (line 257) `[4831db2b]`
- `original_frame` (line 45) `[9859cd86]`
- `result` (line 358) `[a31cb259]`
- `saturation_factor` (line 167) `[c43ddfae]`
- `sepia_frame` (line 88) `[1250cda7]`
- `sepia_matrix` (line 78) `[70832134]`
- `shadow_mask` (line 313) `[5b06e34f]`
- `tint_overlay` (line 252) `[cbb3f76a]`

---

### 📄 `src/processors/filters/filter_registry.py`

#### Imports
- `functools.wraps` (line 14) `[cdad882a]`
- `importlib` (line 11) `[856a29a9]`
- `inspect` (line 12) `[c3a743e6]`
- `os` (line 10) `[de2abade]`
- `typing.Any` (line 13) `[4ec2ae04]`
- `typing.Callable` (line 13) `[60ed66b7]`
- `typing.Dict` (line 13) `[db5e932b]`
- `typing.List` (line 13) `[eada0f80]`
- `typing.Optional` (line 13) `[abdbaea6]`

#### Classes
- **`FilterRegistrationError`** (lines 19-21) `[1aae40f9]`
  - *Inherits from:* Exception
- **`FilterValidationError`** (lines 23-25) `[3e2a7073]`
  - *Inherits from:* Exception

#### Functions
- **`apply_filter(filter_id, clip, intensity)`** (lines 178-210) `[42d0306d]`
  - *Apply a filter to a clip*
  - *Calls:* get_filter_by_id
- **`clear_registry()`** (lines 281-285) `[7e83dd19]`
  - *Clear all registered filters (useful for testing)*
- **`decorator(func)`** (lines 90-133) `[2a55674a]`
  - *Calls:* validate_filter_metadata, validate_filter_function
- **`discover_filters()`** (lines 212-256) `[1dde406f]`
  - *Discover and import all filter modules in the filters directory*
- **`get_all_filters()`** (lines 137-139) `[11db2de7]`
  - *Get all registered filters*
- **`get_filter_by_id(filter_id)`** (lines 174-176) `[e325d76a]`
  - *Get a specific filter by its ID*
  - *Called by:* apply_filter
- **`get_filters_by_category(category)`** (lines 141-172) `[ca3b8e38]`
  - *Get filters organized by category*
  - *Called by:* list_available_filters, get_registry_stats
- **`get_registry_stats()`** (lines 287-299) `[184687df]`
  - *Get statistics about the filter registry*
  - *Calls:* get_filters_by_category
- **`list_available_filters()`** (lines 258-279) `[8ad475fc]`
  - *Print a formatted list of all available filters*
  - *Calls:* get_filters_by_category
- **`register_filter(name, category, description, has_intensity, min_intensity, max_intensity, default_intensity, preview_available)`** (lines 61-135) `[ca83131a]`
  - *Decorator to register a filter function with metadata*
  - *Calls:* validate_filter_metadata, validate_filter_function
- **`validate_filter_function(func)`** (lines 50-59) `[76a91e55]`
  - *Validate filter function signature*
  - *Called by:* register_filter, decorator
- **`validate_filter_metadata(metadata)`** (lines 27-48) `[13df60b3]`
  - *Validate filter metadata has required fields*
  - *Called by:* register_filter, decorator
- **`wrapper()`** (lines 130-131) `[63785b32]`

#### Variables
- `args` (line 198) `[9c71a648]`
- `categories` (line 289) `[a1ae97a5]`
- `default` (line 276) `[1957ebc5]`
- `discovered_count` (line 220) `[e99f975f]`
- `filter_category` (line 154) `[cbaae2bf]`
- `filter_files` (line 225) `[6a89ef8d]`
- `filter_func` (line 195) `[41707ff6]`
- `filter_id` (line 114) `[a396be76]`
- `filter_info` (line 191) `[de2856cf]`
- `filter_with_id` (line 164) `[2029a511]`
- `filters_after` (line 241) `[db851b98]`
- `filters_before` (line 234) `[07816f7f]`
- `filters_dir` (line 219) `[57e8ea18]`
- `full_module_name` (line 237) `[515d0ef8]`
- `intensity` (line 203) `[8fbcceff]`
- `intensity_info` (line 277) `[55c07d9d]`
- `max_val` (line 275) `[28448fe7]`
- `metadata` (line 92) `[5418933e]`
- `min_val` (line 274) `[878e3cc2]`
- `new_filters` (line 242) `[67cb12a4]`
- `params` (line 53) `[d81568f5]`
- `required_fields` (line 29) `[6b7694ac]`
- `sig` (line 52) `[5ef214fa]`
- `stats` (line 291) `[d8b9f347]`

---

### 📄 `src/processors/filters/preset_filters.py`

#### Imports
- `artistic_filters.apply_blur` (line 193) `[bfcad2bb]`
- `artistic_filters.apply_edge_detection` (line 655) `[f1e711c8]`
- `artistic_filters.apply_film_grain` (line 706) `[96589ec9]`
- `artistic_filters.apply_glow` (line 706) `[50ff42b6]`
- `artistic_filters.apply_posterize` (line 655) `[697299be]`
- `artistic_filters.apply_sharpen` (line 655) `[e7d42bd2]`
- `artistic_filters.apply_vignette` (line 706) `[d9eeb413]`
- `brightness_filters.apply_auto_levels` (line 555) `[8f4c9000]`
- `brightness_filters.apply_brighten` (line 603) `[fbb2015f]`
- `brightness_filters.apply_darken` (line 705) `[b22b6cfa]`
- `brightness_filters.apply_high_contrast` (line 705) `[3ced8cf7]`
- `brightness_filters.apply_low_contrast` (line 396) `[e7dec35b]`
- `brightness_filters.apply_shadow_highlight` (line 555) `[8a14035d]`
- `color_filters.apply_color_temperature` (line 503) `[290b1021]`
- `color_filters.apply_desaturate` (line 554) `[8ad8a2ff]`
- `color_filters.apply_grayscale` (line 287) `[050bbf51]`
- `color_filters.apply_saturate` (line 704) `[bae87b5e]`
- `color_filters.apply_sepia` (line 90) `[e499eb01]`
- `color_filters.apply_tint` (line 704) `[bea7a51d]`
- `color_filters.apply_vintage_colors` (line 90) `[dbbcc3b6]`
- `filter_registry.register_filter` (line 13) `[6bdc2823]`
- `moviepy.editor.ImageClip` (line 11) `[87414a47]`
- `moviepy.editor.VideoFileClip` (line 11) `[3951e41b]`
- `typing.Union` (line 12) `[26723ff1]`

#### Functions
- **`apply_anime_style(clip, intensity)`** (lines 639-679) `[801a433a]`
  - *Apply anime/cartoon style processing*
- **`apply_cinematic_look(clip, intensity)`** (lines 24-65) `[c7900d3f]`
  - *Apply cinematic look combining multiple effects*
- **`apply_cold_winter(clip, intensity)`** (lines 435-478) `[0ae4b8fc]`
  - *Apply cold winter atmosphere*
- **`apply_cyberpunk(clip, intensity)`** (lines 324-370) `[b15d1895]`
  - *Apply cyberpunk aesthetic*
- **`apply_documentary(clip, intensity)`** (lines 540-577) `[27a04c90]`
  - *Apply documentary-style processing*
- **`apply_dream_sequence(clip, intensity)`** (lines 178-214) `[834c0073]`
  - *Apply dream sequence look*
- **`apply_high_energy(clip, intensity)`** (lines 225-262) `[96f22a1b]`
  - *Apply high energy look*
- **`apply_horror_atmosphere(clip, intensity)`** (lines 127-167) `[25ae3034]`
  - *Apply horror/thriller atmosphere*
- **`apply_instagram_style(clip, intensity)`** (lines 489-529) `[8501b3fc]`
  - *Apply Instagram-style processing*
- **`apply_music_video(clip, intensity)`** (lines 588-628) `[d962f587]`
  - *Apply music video style processing*
- **`apply_noir_style(clip, intensity)`** (lines 273-313) `[d5823853]`
  - *Apply film noir style*
- **`apply_retro_80s(clip, intensity)`** (lines 690-736) `[ba05ae57]`
  - *Apply retro 1980s style*
- **`apply_vintage_film(clip, intensity)`** (lines 76-116) `[68745a98]`
  - *Apply vintage film look*
- **`apply_warm_sunset(clip, intensity)`** (lines 381-424) `[0618cd65]`
  - *Apply warm sunset/golden hour look*
- **`get_all_presets()`** (lines 739-756) `[d79e3f83]`
  - *Return a list of all available preset filters*
- **`get_preset_description(preset_name)`** (lines 758-776) `[921a7a77]`
  - *Get description for a specific preset*

#### Variables
- `descriptions` (line 760) `[b660b3f3]`
- `processed` (line 730) `[48c6c85a]`

---

### 📄 `src/processors/image_processor.py`

#### Imports
- `PIL.Image` (line 15) `[4f84112b]`
- `PIL.ImageEnhance` (line 15) `[6d408e85]`
- `PIL.ImageOps` (line 15) `[960ee6fe]`
- `dataclasses.dataclass` (line 12) `[0010e60c]`
- `json` (line 7) `[ff3e4d4d]`
- `logging` (line 13) `[27dced09]`
- `numpy` (line 14) `[d8fca9de]`
- `os` (line 3) `[de2abade]`
- `pathlib.Path` (line 10) `[fa6ee8af]`
- `random` (line 4) `[7e18ed42]`
- `shutil` (line 130) `[582f9ff7]`
- `src.utils.cache_manager.CacheManager` (line 20) `[45d99fb5]`
- `src.utils.queue_manager.TaskStatus` (line 19) `[d7680471]`
- `src.utils.queue_manager.queue_manager` (line 19) `[0323b6cc]`
- `src.utils.temp_file_manager.TaskPriority` (line 18) `[0b5c99e9]`
- `src.utils.temp_file_manager.TaskType` (line 18) `[41fc328b]`
- `src.utils.temp_file_manager.temp_manager` (line 18) `[71efb9f1]`
- `subprocess` (line 6) `[7d8752c4]`
- `tempfile` (line 8) `[09d25239]`
- `threading` (line 9) `[90781f3e]`
- `time` (line 5) `[4f9b8491]`
- `typing.Dict` (line 11) `[db5e932b]`
- `typing.List` (line 11) `[eada0f80]`
- `typing.Optional` (line 11) `[abdbaea6]`
- `typing.Tuple` (line 11) `[23996b74]`
- `typing.Union` (line 11) `[26723ff1]`

#### Classes
- **`FFmpegImageProcessor`** (lines 43-154) `[b6e89b44]`
- **`ImageProcessingResult`** (lines 23-30) `[e36b0b07]`
- **`ImageSegment`** (lines 33-41) `[65969d13]`
- **`SingleImageProcessor`** (lines 156-519) `[69d2ec8a]`

#### Functions
- **`__init__(self)`** (lines 169-197) `[0ff98b3f]`
- **`apply_image_effects(self, image_path, filter_config)`** (lines 432-499) `[f0514282]`
  - *Apply effects to image using FFmpeg filters*
- **`apply_image_filters(self, image_path, output_path, filter_effects)`** (lines 124-154) `[1f272652]`
  - *Apply filters to image using FFmpeg*
- **`cleanup_session(self)`** (lines 501-515) `[0f62a6b1]`
  - *Clean up current processing session*
- **`create_image_segments(self, image_path, beat_times, duration, target_size, change_interval)`** (lines 273-367) `[bbae224e]`
  - *Create video segments from image synchronized with beat times using FFmpeg*
- **`create_image_with_animation(self, image_path, output_path, duration, target_size, animation_type, fps)`** (lines 80-122) `[164e814f]`
  - *Create animated video from image using FFmpeg filters*
- **`get_cache_key(self, image_path, params)`** (lines 199-201) `[489ce55a]`
  - *Generate cache key for image processing*
- **`get_image_info(image_path)`** (lines 593-613) `[5ca58f93]`
  - *Get image information*
- **`get_processing_stats(self)`** (lines 517-519) `[830d845d]`
  - *Get processing statistics*
- **`image_to_video(self, image_path, output_path, duration, target_size, fps)`** (lines 50-78) `[e2728872]`
  - *Convert image to video using FFmpeg*
- **`preprocess_image(self, image_path, target_size)`** (lines 203-271) `[23639309]`
  - *Preprocess image and save to cache*
- **`process_image(image_path, audio_path, output_path, beat_times, desired_duration, audio_start_time, change_interval, target_size, filter_config)`** (lines 522-564) `[94517fa2]`
  - *Main entry point for single image processing with FFmpeg and temporary file management*
- **`process_single_image(self, image_path, audio_path, output_path, beat_times, desired_duration, audio_start_time, change_interval, target_size, filter_config)`** (lines 369-430) `[761aa4c9]`
  - *Process a single image into a video with FFmpeg*
- **`validate_image_file(image_path)`** (lines 567-590) `[2b0511d4]`
  - *Validate if file is a supported image format*

#### Variables
- `animation_filters` (line 88) `[712a9819]`
- `animation_type` (line 339) `[87aac5d6]`
- `animation_types` (line 311) `[eb170569]`
- `cache_key` (line 325) `[42640db3]`
- `cached_path` (line 328) `[ef694e5c]`
- `canvas` (line 253) `[a925a801]`
- `cmd` (line 136) `[394b75bc]`
- `current_time` (line 295) `[6632645b]`
- `filter_chain` (line 134) `[20b3e79f]`
- `filter_effects` (line 458) `[9d9aa355]`
- `img` (line 234) `[e7362c1e]`
- `img_ratio` (line 237) `[d4d50d96]`
- `new_height` (line 246) `[9cf518d7]`
- `new_width` (line 247) `[4af8f2a5]`
- `output_filename` (line 335) `[d4b8e57f]`
- `output_path` (line 336) `[9d04328d]`
- `preprocess_params` (line 216) `[18d08b0b]`
- `processed_image_path` (line 291) `[1bb00a8b]`
- `processing_time` (line 418) `[ced0e9b9]`
- `processor` (line 540) `[f97396c6]`
- `result` (line 144) `[5f31ec93]`
- `segment_duration` (line 304) `[1d2b771c]`
- `segment_params` (line 318) `[4df4d22b]`
- `segment_paths` (line 396) `[d37e29e2]`
- `segment_timings` (line 294) `[21cc947d]`
- `start_time` (line 391) `[293e34e7]`
- `success` (line 342) `[ca643d38]`
- `target_ratio` (line 238) `[6954d724]`
- `valid_extensions` (line 579) `[ceb95c40]`
- `x_offset` (line 256) `[ec3c89c9]`
- `y_offset` (line 257) `[72b5f7f2]`

---

### 📄 `src/processors/mixed_media_processor.py`

#### Imports
- `dataclasses.dataclass` (line 12) `[0010e60c]`
- `enum.Enum` (line 13) `[3b3f4ac9]`
- `json` (line 7) `[ff3e4d4d]`
- `logging` (line 14) `[27dced09]`
- `os` (line 3) `[de2abade]`
- `pathlib.Path` (line 10) `[fa6ee8af]`
- `shutil` (line 6) `[582f9ff7]`
- `src.utils.cache_manager.CacheManager` (line 19) `[45d99fb5]`
- `src.utils.queue_manager.TaskStatus` (line 18) `[d7680471]`
- `src.utils.queue_manager.queue_manager` (line 18) `[0323b6cc]`
- `src.utils.temp_file_manager.TaskPriority` (line 17) `[0b5c99e9]`
- `src.utils.temp_file_manager.TaskType` (line 17) `[41fc328b]`
- `src.utils.temp_file_manager.temp_manager` (line 17) `[71efb9f1]`
- `subprocess` (line 4) `[7d8752c4]`
- `tempfile` (line 5) `[09d25239]`
- `threading` (line 9) `[90781f3e]`
- `time` (line 8) `[4f9b8491]`
- `typing.Any` (line 11) `[4ec2ae04]`
- `typing.Dict` (line 11) `[db5e932b]`
- `typing.List` (line 11) `[eada0f80]`
- `typing.Optional` (line 11) `[abdbaea6]`
- `typing.Tuple` (line 11) `[23996b74]`
- `video_processor.process_video` (line 730) `[c74b770f]`

#### Classes
- **`MediaFile`** (lines 36-46) `[76393345]`
- **`MediaType`** (lines 21-25) `[ad061643]`
  - *Inherits from:* Enum
- **`MixedMediaProcessor`** (lines 63-681) `[90cda639]`
- **`ProcessingPhase`** (lines 27-33) `[fb2f1631]`
  - *Inherits from:* Enum
- **`ProcessingSession`** (lines 49-61) `[3f075295]`

#### Functions
- **`__init__(self)`** (lines 76-117) `[559a3c9f]`
- **`_check_ffmpeg(self)`** (lines 119-131) `[1e126c9d]`
  - *Check if FFmpeg is available*
- **`analyze_folder(self, folder_path)`** (lines 137-188) `[97093c8e]`
  - *Analyze folder contents and detect media types*
- **`cleanup_session(self)`** (lines 666-670) `[d42f61f9]`
  - *Clean up current processing session*
- **`combine_videos_with_caching(self, video_cache_keys, output_path)`** (lines 410-474) `[1508f1a1]`
  - *Combine multiple videos into one with caching*
- **`convert_image_to_video_with_caching(self, image_path, target_size)`** (lines 246-326) `[656d1589]`
  - *Convert image to video clip with caching*
- **`get_cache_key(self, file_path, processing_params)`** (lines 133-135) `[2b652643]`
  - *Generate cache key for processed file*
- **`get_image_info(self, image_path)`** (lines 223-244) `[ee52c57a]`
  - *Get image information using FFprobe*
- **`get_processing_stats(self)`** (lines 672-681) `[98144cb7]`
  - *Get processing statistics*
- **`get_user_preferences(self)`** (lines 476-513) `[ab9011ee]`
  - *Get user preferences for mixed media processing*
- **`get_video_info(self, video_path)`** (lines 190-221) `[56c91150]`
  - *Get video information using FFprobe*
- **`normalize_video_with_caching(self, video_path)`** (lines 328-408) `[edbccc0e]`
  - *Normalize video with caching (preserves dimensions)*
- **`process_mixed_folder_with_temp_management(self, folder_path, output_path, user_preferences)`** (lines 542-664) `[ce798220]`
  - *Main method to process mixed media folder with temporary file management*
- **`process_mixed_media_folder(folder_path, audio_path, output_path, beat_times, desired_duration, audio_start_time, change_interval, target_size, cutting_mode, sensitivity_choice)`** (lines 684-754) `[cb7b1381]`
  - *Process mixed media folder and then use video processor*
- **`progress_percent(self)`** (lines 60-61) `[f81fa308]`
- **`start_processing_session(self, session_name)`** (lines 515-529) `[a463f9b0]`
  - *Start a new processing session*
- **`update_session_phase(self, phase)`** (lines 537-540) `[412031d5]`
  - *Update current processing phase*
- **`update_session_progress(self, processed_files, failed_files)`** (lines 531-535) `[4a67034a]`
  - *Update session progress*

#### Variables
- `ANALYSIS` (line 29) `[9c3000e8]`
- `CLEANUP` (line 33) `[88776fcf]`
- `COMBINATION` (line 32) `[7545c879]`
- `IMAGE` (line 23) `[02cc141e]`
- `IMAGE_CONVERSION` (line 30) `[7a292874]`
- `UNKNOWN` (line 25) `[2317ba35]`
- `VIDEO` (line 24) `[35edef0f]`
- `VIDEO_NORMALIZATION` (line 31) `[245e0628]`
- `analysis` (line 568) `[c6eae05b]`
- `cache_key` (line 629) `[e63d1ecc]`
- `choice` (line 504) `[68b9b407]`
- `cmd` (line 447) `[502fe6d7]`
- `combined_path` (line 644) `[bf5f9615]`
- `combined_video_path` (line 721) `[c0ce772e]`
- `concat_file` (line 429) `[0d0754d9]`
- `duration` (line 488) `[e61b2a29]`
- `duration_input` (line 485) `[4f1fd087]`
- `file_ext` (line 164) `[9e25d429]`
- `file_size` (line 165) `[410f1db2]`
- `final_cache_key` (line 386) `[60da354d]`
- `first_video_info` (line 586) `[1fd52c76]`
- `image_files` (line 607) `[b7fe3d70]`
- `image_info` (line 274) `[c605787c]`
- `info` (line 233) `[7d084a01]`
- `mixed_processor` (line 707) `[117e14ce]`
- `ordered_files` (line 600) `[e495487e]`
- `ordering` (line 506) `[c0bf9d13]`
- `params` (line 344) `[1f80f096]`
- `prefs` (line 710) `[1dbfbcbf]`
- `processed_cache_keys` (line 590) `[4348ebfc]`
- `result` (line 458) `[171710c2]`
- `session_id` (line 557) `[048e4753]`
- `stream` (line 236) `[ac8be68f]`
- `target_size` (line 588) `[043eb551]`
- `temp_dir` (line 426) `[e805d884]`
- `temp_output` (line 361) `[598127a6]`
- `temp_video_path` (line 434) `[7fea8ed0]`
- `user_preferences` (line 561) `[f5af8e5f]`
- `video_clip` (line 437) `[6ec64de8]`
- `video_files` (line 624) `[92f0cedc]`
- `video_info` (line 339) `[d02f15b1]`
- `video_stream` (line 206) `[5e102357]`

---

### 📄 `src/processors/multiple_image_processor.py`

#### Imports
- `PIL.Image` (line 16) `[4f84112b]`
- `PIL.ImageEnhance` (line 16) `[6d408e85]`
- `PIL.ImageOps` (line 16) `[960ee6fe]`
- `collections.deque` (line 13) `[f4b9d645]`
- `dataclasses.dataclass` (line 14) `[0010e60c]`
- `enum.Enum` (line 12) `[3b3f4ac9]`
- `json` (line 8) `[ff3e4d4d]`
- `logging` (line 15) `[27dced09]`
- `numpy` (line 5) `[d8fca9de]`
- `os` (line 3) `[de2abade]`
- `pathlib.Path` (line 10) `[fa6ee8af]`
- `random` (line 4) `[7e18ed42]`
- `shutil` (line 218) `[582f9ff7]`
- `src.utils.cache_manager.CacheManager` (line 21) `[45d99fb5]`
- `src.utils.queue_manager.TaskStatus` (line 20) `[d7680471]`
- `src.utils.queue_manager.queue_manager` (line 20) `[0323b6cc]`
- `src.utils.temp_file_manager.TaskPriority` (line 19) `[0b5c99e9]`
- `src.utils.temp_file_manager.TaskType` (line 19) `[41fc328b]`
- `src.utils.temp_file_manager.temp_manager` (line 19) `[71efb9f1]`
- `subprocess` (line 7) `[7d8752c4]`
- `threading` (line 9) `[90781f3e]`
- `time` (line 6) `[4f9b8491]`
- `typing.Dict` (line 11) `[db5e932b]`
- `typing.List` (line 11) `[eada0f80]`
- `typing.Optional` (line 11) `[abdbaea6]`
- `typing.Tuple` (line 11) `[23996b74]`
- `typing.Union` (line 11) `[26723ff1]`

#### Classes
- **`AnimationType`** (lines 23-37) `[968774c2]`
  - *Inherits from:* Enum
- **`FFmpegMultiImageProcessor`** (lines 83-237) `[dca98e93]`
- **`ImageProcessingResult`** (lines 49-56) `[b7a76784]`
- **`ImageSegmentInfo`** (lines 73-81) `[1ac38806]`
- **`MultipleImageProcessor`** (lines 239-661) `[2d2f8c81]`
- **`ProcessingSession`** (lines 59-70) `[41e05dab]`
- **`TransitionType`** (lines 39-46) `[49941a21]`
  - *Inherits from:* Enum

#### Functions
- **`__init__(self, batch_size)`** (lines 254-294) `[5fdebe76]`
- **`apply_color_grading(self, image_path, output_path, grading_params)`** (lines 182-237) `[9a06b461]`
  - *Apply color grading to image using FFmpeg*
- **`calculate_image_timing(self, beat_times, total_duration, num_images, change_interval)`** (lines 409-447) `[1c5b5b2d]`
  - *Calculate timing for each image based on beat analysis*
- **`cleanup_session(self)`** (lines 632-646) `[25eb6b81]`
  - *Clean up current processing session*
- **`create_animated_image_segment(self, image_path, output_path, duration, target_size, animation_type, fps)`** (lines 90-142) `[1d890a18]`
  - *Create animated video segment from image using FFmpeg*
- **`create_image_montage(image_paths, output_path, grid_size, target_size, duration)`** (lines 853-939) `[4905eb44]`
  - *Create a video montage showing multiple images simultaneously*
- **`create_image_segments_batch(self, image_paths, image_timings, target_size, use_transitions)`** (lines 449-537) `[da2f82f6]`
  - *Create video segments from images in batches to prevent resource exhaustion*
- **`create_image_slideshow(images_folder, output_path, duration_per_image, target_size, transition_type)`** (lines 768-850) `[d6d67b1d]`
  - *Create a simple slideshow from images (without audio synchronization)*
- **`create_transition_between_images(self, image1_path, image2_path, output_path, transition_duration, transition_type, target_size)`** (lines 144-180) `[2f3276c4]`
  - *Create transition video between two images*
- **`estimate_processing_time(images_folder, desired_duration)`** (lines 747-765) `[cdde705b]`
  - *Estimate processing time for multiple images*
  - *Calls:* get_image_count
- **`get_animation_description(animation_name)`** (lines 953-970) `[695e0187]`
  - *Get description of animation type*
- **`get_available_animations()`** (lines 943-945) `[5bba5acc]`
  - *Get list of available animation types*
- **`get_available_transitions()`** (lines 948-950) `[ebed294f]`
  - *Get list of available transition types*
- **`get_cache_key(self, identifier, params)`** (lines 346-348) `[c9ebed7e]`
  - *Generate cache key for image processing*
- **`get_image_count(images_folder)`** (lines 729-744) `[5fd4d57e]`
  - *Get count of valid images in folder*
  - *Called by:* estimate_processing_time
- **`get_processing_stats(self)`** (lines 648-661) `[c5c7c0d8]`
  - *Get processing statistics*
- **`preprocess_image(self, image_path, target_size)`** (lines 350-407) `[4924957a]`
  - *Preprocess image for consistent quality and format*
- **`process_multiple_images(self, images_folder, audio_path, output_path, beat_times, desired_duration, audio_start_time, change_interval, target_size, cutting_mode, filter_config)`** (lines 539-630) `[fac8ab42]`
  - *Process multiple images into a synchronized video using FFmpeg*
- **`progress_percent(self)`** (lines 69-70) `[5f98a5d8]`
- **`start_processing_session(self, session_name, total_images)`** (lines 296-310) `[995d4beb]`
  - *Start a new processing session*
- **`validate_image_folder(self, folder_path)`** (lines 312-344) `[ba002ec7]`
  - *Validate folder contains images and return sorted list of image paths*
- **`validate_images_folder(images_folder)`** (lines 711-726) `[e7545299]`
  - *Validate if folder contains valid image files*

#### Variables
- `BOUNCE_IN` (line 31) `[6c2bde93]`
- `CROSSFADE` (line 35) `[1bea9800]`
- `CUT` (line 41) `[62a0f15e]`
- `DISSOLVE` (line 43) `[bedd6bc9]`
- `DROP_DOWN` (line 33) `[29c62d6d]`
- `FADE` (line 42) `[895be3f3]`
- `FADE_IN` (line 29) `[280fb9af]`
- `KEN_BURNS` (line 34) `[bd81b1db]`
- `SCALE_IN` (line 30) `[9c12e700]`
- `SLIDE` (line 44) `[6ed0319e]`
- `SLIDE_IN_BOTTOM` (line 28) `[fadada9d]`
- `SLIDE_IN_LEFT` (line 25) `[c98654d2]`
- `SLIDE_IN_RIGHT` (line 26) `[605937e5]`
- `SLIDE_IN_TOP` (line 27) `[34565976]`
- `WIPE` (line 45) `[12d391e7]`
- `WIPE_LEFT` (line 36) `[a9fa06a8]`
- `WIPE_RIGHT` (line 37) `[53133434]`
- `ZOOM` (line 46) `[70c792ef]`
- `ZOOM_IN` (line 32) `[f056f57e]`
- `animation` (line 815) `[87a40acc]`
- `animation_filters` (line 98) `[1b3f7837]`
- `animation_type` (line 498) `[5a259451]`
- `animation_types` (line 455) `[2d4e7a59]`
- `base_time` (line 761) `[73f645f2]`
- `batch_end` (line 462) `[b939591f]`
- `batch_segments` (line 466) `[e709833b]`
- `cache_key` (line 481) `[1411595b]`
- `cached_path` (line 484) `[f650a4a0]`
- `canvas` (line 391) `[e8a25aca]`
- `cell_height` (line 877) `[6e94c416]`
- `cell_width` (line 876) `[847e396a]`
- `cmd` (line 911) `[c4e4f3a2]`
- `col` (line 884) `[9a798c7b]`
- `composite` (line 880) `[ce70f5e3]`
- `current_time` (line 429) `[a511753e]`
- `descriptions` (line 955) `[8b0080a4]`
- `duration` (line 440) `[dd44a2a0]`
- `duration_per_image` (line 421) `[f03c07d0]`
- `file_path` (line 324) `[0b4b2b7e]`
- `filter_chain` (line 222) `[d885e993]`
- `filter_complex` (line 162) `[b86ac796]`
- `filter_effects` (line 186) `[b5132011]`
- `image_count` (line 759) `[85cc6db7]`
- `image_extensions` (line 319) `[690e2706]`
- `image_files` (line 320) `[70774893]`
- `image_index` (line 430) `[1a3eedb4]`
- `image_path` (line 470) `[d98ad760]`
- `image_paths` (line 873) `[3912fb51]`
- `image_time` (line 762) `[f3f9722b]`
- `image_timings` (line 577) `[d1aff92d]`
- `img` (line 893) `[545edbe6]`
- `img_ratio` (line 377) `[6e4d88d6]`
- `invalid_files` (line 321) `[e25d2529]`
- `new_height` (line 384) `[b93b7b61]`
- `new_width` (line 385) `[1e621748]`
- `next_beat_time` (line 437) `[a553a269]`
- `num_segments` (line 588) `[a33c5326]`
- `output_filename` (line 494) `[f49274e3]`
- `output_path` (line 495) `[84ad9456]`
- `params` (line 474) `[47dfdd09]`
- `processed_image` (line 491) `[c86e65b0]`
- `processed_path` (line 369) `[3fc2c054]`
- `processing_time` (line 616) `[9223b473]`
- `processor` (line 785) `[8299ad7a]`
- `progress` (line 533) `[4ea1dfed]`
- `result` (line 923) `[c84c34db]`
- `row` (line 883) `[b1626aa2]`
- `segment_path` (line 805) `[c58d5fdf]`
- `segment_paths` (line 595) `[ed8dfe93]`
- `selected_images` (line 589) `[14d15192]`
- `selected_timings` (line 590) `[9ff66071]`
- `session_id` (line 568) `[c9d6277c]`
- `start_time` (line 423) `[445ad5a4]`
- `stats` (line 650) `[e41d0251]`
- `success` (line 500) `[cd755aaa]`
- `target_ratio` (line 378) `[e3c576ea]`
- `temp` (line 207) `[85791b74]`
- `temp_composite_path` (line 906) `[50ee8fdb]`
- `total_images` (line 459) `[9f6997c3]`
- `transition_filters` (line 152) `[c52f683c]`
- `transition_types` (line 456) `[88b18b02]`
- `x` (line 896) `[6ef1242c]`
- `x_offset` (line 392) `[93cbfe61]`
- `y` (line 897) `[ae2cfd9f]`
- `y_offset` (line 393) `[98cc5e85]`

---

### 📄 `src/processors/sequential_timing.py`

#### Imports
- `random` (line 4) `[7e18ed42]`
- `typing.List` (line 3) `[eada0f80]`
- `typing.Tuple` (line 3) `[23996b74]`

#### Classes
- **`SequentialTimingCalculator`** (lines 6-60) `[c7819977]`

#### Functions
- **`__init__(self, video_duration, total_audio_duration)`** (lines 9-11) `[8b2be876]`
- **`calculate_change_points(self, change_frequency)`** (lines 13-51) `[0ef904f9]`
  - *Calculate change points based on frequency preference*
- **`get_sequential_timing(video_duration, total_audio_duration, change_preference)`** (lines 62-78) `[db876947]`
  - *Main function to get sequential timing based on user preferences*
- **`map_change_preference(self, user_choice)`** (lines 53-60) `[bf4266f4]`
  - *Map user's change preference to frequency setting*

#### Variables
- `base_duration` (line 25) `[cb58cedb]`
- `calculator` (line 76) `[0729651d]`
- `change_points` (line 34) `[f7faaa6a]`
- `current_time` (line 35) `[f54eec54]`
- `duration` (line 44) `[87dbfd46]`
- `frequency` (line 77) `[e060e898]`
- `num_segments` (line 28) `[6360dd3d]`
- `preference_map` (line 55) `[d74bdf8a]`
- `segment_durations` (line 19) `[3f1d16e2]`
- `variation` (line 43) `[b65addc3]`

---

### 📄 `src/processors/sound_effects_processor.py`

#### Imports
- `enum.Enum` (line 7) `[3b3f4ac9]`
- `moviepy.editor.AudioFileClip` (line 5) `[75416f10]`
- `moviepy.editor.CompositeAudioClip` (line 5) `[0146c800]`
- `os` (line 3) `[de2abade]`
- `random` (line 4) `[7e18ed42]`
- `typing.Dict` (line 6) `[db5e932b]`
- `typing.List` (line 6) `[eada0f80]`
- `typing.Optional` (line 6) `[abdbaea6]`
- `typing.Tuple` (line 6) `[23996b74]`

#### Classes
- **`SoundCategory`** (lines 9-14) `[3bf9a6c5]`
  - *Inherits from:* Enum
- **`SoundEffectsProcessor`** (lines 16-282) `[5cdd906d]`

#### Functions
- **`__init__(self)`** (lines 19-35) `[7a6fdfe5]`
- **`_get_sound_preferences(self)`** (lines 88-126) `[fc9fd65e]`
  - *Get detailed sound effect preferences*
- **`_process_audio_duration(self, audio_clip, target_duration)`** (lines 179-235) `[75df4353]`
  - *Process audio to match target duration with proper fade handling*
- **`cleanup_effects(self, effects_list)`** (lines 275-282) `[7878db76]`
  - *Clean up audio clips to free memory*
- **`create_audio_effects_track(self, effects_list, total_duration)`** (lines 237-273) `[402094eb]`
  - *Create composite audio track from all sound effects*
- **`get_sound_for_animation(self, animation_type, animation_duration, sound_prefs)`** (lines 128-177) `[96b3e43c]`
  - *Get appropriate sound effect for animation*
- **`get_user_preferences(self)`** (lines 74-86) `[087e82c0]`
  - *Get user preferences for sound effects*
- **`load_sound_library(self)`** (lines 37-72) `[da123f51]`
  - *Load and categorize all sound effects*

#### Variables
- `AMBIENT` (line 14) `[2b936c24]`
- `IMPACTS` (line 10) `[9694f205]`
- `MAGIC` (line 12) `[5a218a8a]`
- `POPS` (line 13) `[bd43278b]`
- `WHOOSHES` (line 11) `[ce029083]`
- `audio_clip` (line 55) `[b1dbac10]`
- `available_categories` (line 142) `[f4788205]`
- `available_duration` (line 201) `[a988d8eb]`
- `category` (line 145) `[26d2e93f]`
- `category_path` (line 46) `[0b429ca1]`
- `choice` (line 95) `[5313c274]`
- `duration` (line 56) `[dfdc36ec]`
- `effect_clip` (line 252) `[e0974e36]`
- `effects_audio` (line 267) `[14a402bf]`
- `end_time` (line 205) `[f887781a]`
- `file_path` (line 52) `[910dec6c]`
- `max_clip_duration` (line 250) `[0a924583]`
- `original_duration` (line 182) `[929c9aae]`
- `positioned_clip` (line 254) `[bd9bccd2]`
- `positioned_clips` (line 245) `[1c18cd2a]`
- `processed_audio` (line 169) `[57ccc08c]`
- `result` (line 227) `[fadfd47d]`
- `selected_sound` (line 158) `[0654ada3]`
- `sound_mode` (line 100) `[de2de405]`
- `sounds` (line 154) `[1f133157]`
- `start_offset` (line 200) `[05d71c9a]`
- `total_sounds` (line 68) `[96d5ee1b]`
- `volume` (line 118) `[f4b34c11]`
- `volume_choice` (line 110) `[96557af3]`

---

### 📄 `src/processors/split_screen_processor.py`

#### Imports
- `moviepy.editor.AudioFileClip` (line 1) `[75416f10]`
- `moviepy.editor.ColorClip` (line 1) `[071a5536]`
- `moviepy.editor.CompositeAudioClip` (line 1) `[0146c800]`
- `moviepy.editor.CompositeVideoClip` (line 1) `[66154cf9]`
- `moviepy.editor.VideoFileClip` (line 1) `[3951e41b]`
- `os` (line 3) `[de2abade]`
- `traceback` (line 171) `[6a6eacd0]`
- `typing.Dict` (line 2) `[db5e932b]`
- `typing.Tuple` (line 2) `[23996b74]`

#### Classes
- **`SplitScreenProcessor`** (lines 5-187) `[bd060cbc]`

#### Functions
- **`__init__(self)`** (lines 6-16) `[5cea7d4c]`
- **`_crop_video(self, clip, target_size)`** (lines 43-58) `[cc8bf217]`
- **`_fit_video(self, clip, target_size)`** (lines 60-71) `[0d2cd190]`
- **`_stretch_video(self, clip, target_size)`** (lines 40-41) `[c0ff33fa]`
- **`create_split_screen_video()`** (lines 260-320) `[32e4d0e9]`
  - *Calls:* get_fit_mode, get_fit_mode, get_audio_preferences
- **`get_audio_preferences()`** (lines 202-258) `[91a7236a]`
  - *Called by:* create_split_screen_video
- **`get_fit_mode(video_number)`** (lines 189-200) `[d0437719]`
  - *Called by:* create_split_screen_video, create_split_screen_video
- **`process_videos(self, config)`** (lines 73-187) `[50e61423]`
- **`validate_audio_path(self, audio_path)`** (lines 29-38) `[81f6721c]`
- **`validate_video_path(self, video_path)`** (lines 18-27) `[d345e91d]`

#### Variables
- `audio_clips` (line 143) `[56846daa]`
- `audio_config` (line 304) `[30c33bc8]`
- `audio_path` (line 236) `[d32f36e9]`
- `background` (line 117) `[805decf7]`
- `bg_audio` (line 91) `[24e96e5e]`
- `choice` (line 297) `[2a925a5b]`
- `clip_ratio` (line 62) `[db157683]`
- `clips` (line 133) `[96a548dc]`
- `final_audio` (line 150) `[6b87cab9]`
- `final_video` (line 151) `[aeecb84d]`
- `format_choice` (line 270) `[a56c2ff8]`
- `half_height` (line 98) `[7dbf9534]`
- `main_audio` (line 85) `[c55746ea]`
- `max_duration` (line 113) `[8461ca07]`
- `new_height` (line 69) `[33923acd]`
- `new_width` (line 70) `[d17c5f1e]`
- `output_name` (line 306) `[4e8826b4]`
- `output_path` (line 308) `[72caf89b]`
- `position` (line 299) `[c6a75599]`
- `processor` (line 261) `[49f0cd90]`
- `resized` (line 56) `[84c95fa5]`
- `target_ratio` (line 61) `[56bd7ece]`
- `target_size` (line 97) `[2c0ae224]`
- `video1` (line 76) `[b85586a8]`
- `video1_fit_mode` (line 284) `[33b9698e]`
- `video1_path` (line 281) `[705b2b24]`
- `video1_pos` (line 129) `[8a65ffed]`
- `video1_processed` (line 120) `[a92b20b4]`
- `video2` (line 77) `[f29e1951]`
- `video2_fit_mode` (line 290) `[2cc2de02]`
- `video2_path` (line 287) `[f5f5401a]`
- `video2_pos` (line 128) `[33b02c6a]`
- `video2_processed` (line 121) `[e4bf70c4]`
- `video_format` (line 275) `[fcb859a3]`
- `video_target_size` (line 99) `[d54c87e0]`
- `volume` (line 250) `[31ed2aff]`
- `x_offset` (line 51) `[382ad06b]`
- `y_offset` (line 57) `[fdb96bb8]`

---

### 📄 `src/processors/subtitle_design_manager.py`

#### Imports
- `typing.Tuple` (line 3) `[23996b74]`

#### Classes
- **`SubtitleDesignManager`** (lines 5-181) `[9f9abf18]`

#### Functions
- **`__init__(self)`** (lines 6-55) `[7dffc1e6]`
- **`_get_box_color_preference(self)`** (lines 148-160) `[27bb0bdb]`
  - *Get box color preference*
- **`_get_box_opacity_preference(self)`** (lines 162-175) `[f49bc839]`
  - *Get box opacity preference*
- **`_get_box_preference(self)`** (lines 130-146) `[392f2fee]`
  - *Get box preferences*
- **`_get_color_scheme_preference(self)`** (lines 96-112) `[62c5dd5c]`
  - *Get color scheme preferences*
- **`_get_position_preference(self)`** (lines 64-78) `[013eb48e]`
  - *Get subtitle position preference*
- **`_get_size_preference(self)`** (lines 80-94) `[d4d766d2]`
  - *Get font size preference*
- **`_get_static_color_preferences(self)`** (lines 114-128) `[0e763c00]`
  - *Get static color preferences for text and box*
- **`get_text_color(self, word_index)`** (lines 177-181) `[d52c7486]`
  - *Get color for current word based on settings*
- **`get_user_preferences(self)`** (lines 57-62) `[b245ddf7]`
  - *Get all subtitle design preferences from user*

#### Variables
- `choice` (line 171) `[8bb97af1]`
- `color_name` (line 157) `[58ad3388]`
- `opacity_map` (line 169) `[1bb0bd40]`
- `sizes` (line 91) `[dd2acb35]`

---

### 📄 `src/processors/subtitle_processor.py`

#### Imports
- `json` (line 4) `[ff3e4d4d]`
- `logging` (line 8) `[27dced09]`
- `moviepy.editor.VideoFileClip` (line 6) `[3951e41b]`
- `os` (line 3) `[de2abade]`
- `tempfile` (line 7) `[09d25239]`
- `typing.Dict` (line 9) `[db5e932b]`
- `typing.List` (line 9) `[eada0f80]`
- `typing.Optional` (line 9) `[abdbaea6]`
- `typing.Union` (line 9) `[26723ff1]`
- `whisper` (line 5) `[c35eef0b]`

#### Classes
- **`SubtitleProcessor`** (lines 11-223) `[179c3d73]`

#### Functions
- **`__init__(self)`** (lines 12-14) `[ce7d64fb]`
- **`detect_language(self, audio_path)`** (lines 117-126) `[634a4a62]`
  - *Detect language of the audio*
- **`extract_audio_from_video(self, video_path)`** (lines 16-29) `[99c6a216]`
  - *Extract audio from video file and save it temporarily.*
- **`generate_subtitles(video_path, output_json_path)`** (lines 225-233) `[aa51c842]`
  - *Main entry point for generating subtitles.*
- **`get_subtitle_mode(self)`** (lines 92-109) `[759122a7]`
  - *Get user's preferred subtitle mode*
- **`initialize_model(self, model_size)`** (lines 111-115) `[b8a29b5b]`
  - *Initialize the Whisper model*
- **`print_summary(self, output_data)`** (lines 208-223) `[614c3f3d]`
  - *Print summary of generated subtitles*
- **`process_segments_to_phrases(self, segments, max_words_per_phrase)`** (lines 31-61) `[3bf37965]`
  - *Convert segments to phrase-based subtitles with word limit*
- **`process_segments_to_words(self, segments)`** (lines 63-90) `[bc24b513]`
  - *Convert segments to word-based subtitles*
- **`process_transcription(self, result, subtitle_modes)`** (lines 138-166) `[0329a90c]`
  - *Process transcription results into requested formats*
- **`transcribe_audio(self, audio_path)`** (lines 128-136) `[42677ba7]`
  - *Transcribe audio using Whisper*
- **`transcribe_video(self, video_path, output_json_path)`** (lines 168-206) `[64d40b54]`
  - *Transcribe video and save subtitles to a JSON file.*

#### Variables
- `choice` (line 101) `[2923a446]`
- `chunk_duration` (line 49) `[edddd9ec]`
- `chunk_end` (line 51) `[6f3d895d]`
- `chunk_start` (line 50) `[009bc1bb]`
- `chunk_text` (line 46) `[b07cbc72]`
- `chunk_words` (line 45) `[ccf40b1d]`
- `end_time` (line 69) `[d3545fe4]`
- `initial_result` (line 119) `[e29e7605]`
- `output_data` (line 187) `[f1f181d7]`
- `phrase_count` (line 222) `[f02a6b67]`
- `phrase_subtitles` (line 159) `[7cf36276]`
- `phrases` (line 33) `[43978841]`
- `processor` (line 232) `[22947dc8]`
- `result` (line 184) `[79bc8f05]`
- `segment_words` (line 73) `[652f5270]`
- `short_phrase_count` (line 218) `[302defc8]`
- `short_phrase_subtitles` (line 151) `[0339a234]`
- `start_time` (line 68) `[edfbc983]`
- `subtitle_modes` (line 177) `[620e69c1]`
- `temp_audio_path` (line 173) `[47ea9d5d]`
- `text` (line 70) `[5fda7e22]`
- `time_per_word` (line 75) `[fc49f13f]`
- `video` (line 19) `[5aadf0c8]`
- `word` (line 78) `[d002ea22]`
- `word_count` (line 214) `[26702618]`
- `word_end` (line 81) `[73e1b821]`
- `word_start` (line 80) `[af72df96]`
- `word_subtitles` (line 146) `[d1db8b01]`
- `words` (line 41) `[4f44e3cf]`

---

### 📄 `src/processors/subtitle_video_processor.py`

#### Imports
- `json` (line 3) `[ff3e4d4d]`
- `logging` (line 4) `[27dced09]`
- `moviepy.editor.ColorClip` (line 7) `[071a5536]`
- `moviepy.editor.CompositeVideoClip` (line 7) `[66154cf9]`
- `moviepy.editor.TextClip` (line 7) `[d5613d5b]`
- `moviepy.editor.VideoFileClip` (line 7) `[3951e41b]`
- `os` (line 5) `[de2abade]`
- `subtitle_design_manager.SubtitleDesignManager` (line 8) `[6ffc9fda]`
- `typing.Dict` (line 6) `[db5e932b]`
- `typing.List` (line 6) `[eada0f80]`
- `typing.Optional` (line 6) `[abdbaea6]`
- `typing.Tuple` (line 6) `[23996b74]`

#### Classes
- **`SubtitleVideoProcessor`** (lines 10-277) `[bfd0fb81]`

#### Functions
- **`__init__(self)`** (lines 11-25) `[43c9b715]`
- **`add_subtitles_to_video(self, video_path, subtitle_json_path, output_path)`** (lines 202-277) `[d233b7fe]`
  - *Add subtitles to video.*
- **`calculate_text_size(self, text, font_size, font_path, max_width)`** (lines 41-82) `[b7f62cbf]`
  - *Calculate appropriate text size and wrap text if needed.*
  - *Calls:* wrap_text, wrap_text
- **`create_text_clip(self, text, settings, font_path, color, video_size, subtitle_mode)`** (lines 84-136) `[3bb09f5f]`
  - *Create text clip with size adjustment and word wrapping.*
- **`get_font_for_language(self, language)`** (lines 37-39) `[dbfb5c67]`
  - *Get the appropriate font path for a language.*
- **`get_subtitle_mode(self, available_modes)`** (lines 138-160) `[af900156]`
  - *Get user's preferred subtitle display mode.*
- **`hex_to_rgb(self, hex_color)`** (lines 27-35) `[97f86d98]`
  - *Convert hex color string to RGB tuple.*
- **`process_subtitles(self, subtitles, video, design_settings, font_path, subtitle_mode)`** (lines 162-200) `[6de67d35]`
  - *Process subtitles into text clips.*
- **`wrap_text(text, max_chars)`** (lines 43-61) `[87cd041b]`
  - *Called by:* calculate_text_size, calculate_text_size

#### Variables
- `approx_char_width` (line 64) `[60ab010c]`
- `available_choices` (line 148) `[6a5eab72]`
- `available_modes` (line 213) `[1c7734ef]`
- `base_font_size` (line 94) `[4dafc4a9]`
- `base_path` (line 217) `[942101aa]`
- `box` (line 124) `[486be08e]`
- `box_color_rgb` (line 123) `[bddfa85a]`
- `box_height` (line 122) `[9704fa90]`
- `box_width` (line 121) `[26ddab13]`
- `choice` (line 155) `[ab8aa35c]`
- `clips_to_close` (line 205) `[7ea9524b]`
- `current_length` (line 57) `[05705330]`
- `current_line` (line 56) `[87ef11e3]`
- `data` (line 211) `[0c8b51d6]`
- `design_settings` (line 208) `[0f40e56e]`
- `detected_language` (line 235) `[178377d0]`
- `duration` (line 173) `[7e36da8a]`
- `end_time` (line 172) `[0b62848e]`
- `final_video` (line 245) `[a77f025f]`
- `font_path` (line 236) `[531c6ada]`
- `hex_color` (line 29) `[ef9963af]`
- `lines` (line 66) `[1b410148]`
- `margin_x` (line 87) `[776a3c57]`
- `margin_y` (line 88) `[b3efc164]`
- `max_chars` (line 65) `[c0daaf3c]`
- `max_width` (line 89) `[929e1dce]`
- `modes` (line 142) `[e5d73a5d]`
- `output_path` (line 218) `[8edd223d]`
- `padding` (line 120) `[b62c9b01]`
- `processor` (line 285) `[ffe82bd6]`
- `progress` (line 193) `[c86371c0]`
- `start_time` (line 171) `[cc9676b9]`
- `subtitle_clips` (line 239) `[fdce5a7a]`
- `subtitle_mode` (line 214) `[e660216b]`
- `subtitles` (line 230) `[20acd2e8]`
- `test_clip` (line 68) `[d8d02624]`
- `text` (line 170) `[7a7302c9]`
- `text_color` (line 175) `[4f4afd55]`
- `total_subtitles` (line 167) `[fb87b6e9]`
- `txt_clip` (line 188) `[4ba1aca0]`
- `video` (line 222) `[3b99b31d]`
- `video_size` (line 166) `[181a74fe]`
- `words` (line 44) `[9a4a3e2d]`
- `x_pos` (line 134) `[b0d3279b]`
- `y_pos` (line 115) `[fd39ac8a]`

---

### 📄 `src/processors/video_filter_processor.py`

#### Imports
- `filters.filter_registry.apply_filter` (line 23) `[376d639f]`
- `filters.filter_registry.get_all_filters` (line 23) `[71fe9c98]`
- `filters.filter_registry.get_filter_by_id` (line 23) `[3adaa3ff]`
- `filters.filter_registry.get_filters_by_category` (line 23) `[4aa8f553]`
- `filters.filter_registry.get_registry_stats` (line 23) `[4d67a360]`
- `filters.filter_registry.list_available_filters` (line 23) `[d9073869]`
- `logging` (line 16) `[27dced09]`
- `moviepy.editor.ImageClip` (line 15) `[87414a47]`
- `moviepy.editor.VideoFileClip` (line 15) `[3951e41b]`
- `os` (line 915) `[de2abade]`
- `psutil` (line 914) `[f6b32ab9]`
- `src.utils.cache_manager.CacheManager` (line 21) `[45d99fb5]`
- `src.utils.queue_manager.TaskStatus` (line 20) `[d7680471]`
- `src.utils.queue_manager.queue_manager` (line 20) `[0323b6cc]`
- `src.utils.temp_file_manager.TaskPriority` (line 19) `[0b5c99e9]`
- `src.utils.temp_file_manager.TaskType` (line 19) `[41fc328b]`
- `src.utils.temp_file_manager.temp_manager` (line 19) `[71efb9f1]`
- `threading` (line 13) `[90781f3e]`
- `time` (line 12) `[4f9b8491]`
- `typing.Any` (line 14) `[4ec2ae04]`
- `typing.Dict` (line 14) `[db5e932b]`
- `typing.List` (line 14) `[eada0f80]`
- `typing.Optional` (line 14) `[abdbaea6]`
- `typing.Union` (line 14) `[26723ff1]`
- `uuid` (line 778) `[8b76fbd0]`

#### Classes
- **`VideoFilterProcessor`** (lines 32-943) `[0ccd5a89]`

#### Functions
- **`__init__(self)`** (lines 44-87) `[f1eca0cd]`
- **`_initialize_presets(self)`** (lines 89-217) `[71f0ef67]`
  - *Initialize preset filter combinations*
- **`_parse_selection(self, selection, max_options)`** (lines 602-628) `[044fe2d9]`
  - *Parse user selection string into list of indices*
- **`apply_filter_chain(clip, filters)`** (lines 994-1013) `[5a0d37ed]`
  - *Apply a chain of filters to a clip*
- **`apply_filter_chain_cached(self, clip, clip_id, filter_config)`** (lines 317-401) `[5fc5ed82]`
  - *Apply a chain of filters to a clip with disk-based caching*
- **`apply_filters(self, clip, filter_config)`** (lines 630-660) `[e4451d71]`
  - *Apply configured filters to a video clip with disk-based caching*
- **`apply_filters_async(self, clip, clip_id, filter_config, callback)`** (lines 403-443) `[cf9ae663]`
  - *Apply filters asynchronously using the queue system*
- **`apply_preset_filters(clip, preset_name, intensity)`** (lines 951-992) `[1a6ca974]`
  - *Quick function to apply a preset to a clip with disk-based caching*
- **`apply_single_filter_cached(self, clip, clip_id, filter_id, intensity)`** (lines 245-315) `[63c66458]`
  - *Apply a single filter to a clip with disk-based caching*
- **`batch_apply_filters(clips, filter_config, timeout)`** (lines 1015-1040) `[fb93bdfa]`
  - *Apply filters to multiple clips in batch*
- **`cancel_batch(self, task_ids)`** (lines 871-879) `[30dd3e7d]`
  - *Cancel a batch of filter tasks*
- **`cleanup_session(self)`** (lines 881-910) `[9fdf871e]`
  - *Clean up filter processing session*
- **`clear_cache(self)`** (lines 798-805) `[9af27aaf]`
  - *Clear all cached filter results*
- **`create_filter_batch(self, clips, filter_config, callback)`** (lines 836-865) `[e13d326d]`
  - *Process multiple clips with the same filter configuration*
- **`create_filter_processor()`** (lines 947-949) `[b48a8c87]`
  - *Create and return a VideoFilterProcessor instance*
- **`end_processing_session(self)`** (lines 786-796) `[23506968]`
  - *End the current filter processing session*
- **`get_cache_statistics(self)`** (lines 727-733) `[7938fafd]`
  - *Get cache-specific statistics*
- **`get_custom_filters(self)`** (lines 514-600) `[43954c89]`
  - *Get user's custom filter selection*
- **`get_filter_cache_key(self, clip_id, filter_id, intensity, additional_params)`** (lines 219-227) `[b39013c2]`
  - *Generate cache key for filtered clip*
- **`get_filter_chain_cache_key(self, clip_id, filter_config)`** (lines 229-243) `[74b8951a]`
  - *Generate cache key for filter chain result*
- **`get_filter_info(self, filter_id)`** (lines 682-684) `[a295e205]`
  - *Get detailed information about a specific filter*
- **`get_filter_usage_stats(self)`** (lines 815-828) `[69b67524]`
  - *Get statistics about filter usage*
- **`get_memory_usage(self)`** (lines 912-926) `[d0b2fffc]`
  - *Get current memory usage statistics*
- **`get_performance_stats(self)`** (lines 709-725) `[36c49302]`
  - *Get detailed performance statistics*
- **`get_preset_filters(self)`** (lines 445-512) `[e5ef15da]`
  - *Get user's choice of preset filters*
- **`get_stats(self)`** (lines 690-707) `[97fac94b]`
  - *Get processor statistics*
- **`list_all_filters(self)`** (lines 686-688) `[9b906327]`
  - *Print all available filters*
- **`log_performance_summary(self)`** (lines 928-943) `[4f81edcd]`
  - *Log a comprehensive performance summary*
- **`optimize_cache(self)`** (lines 830-834) `[dcbbe844]`
  - *Optimize cache by removing unused entries*
- **`preview_filter(self, clip, filter_id, intensity)`** (lines 662-680) `[54197496]`
  - *Preview a single filter on a clip (for future preview functionality)*
- **`process_filters()`** (lines 418-428) `[66c16607]`
- **`start_processing_session(self, session_name)`** (lines 776-784) `[f9961fa0]`
  - *Start a new filter processing session*
- **`validate_filter_config(self, filter_config)`** (lines 735-774) `[13561d3a]`
  - *Validate a filter configuration*
- **`wait_for_batch(self, task_ids, timeout)`** (lines 867-869) `[e4c49aa5]`
  - *Wait for a batch of filter tasks to complete*
- **`warm_cache(self, common_filters)`** (lines 807-813) `[faf1c93d]`
  - *Warm up cache with commonly used filters*

#### Variables
- `applied_filters` (line 348) `[6bd84786]`
- `base_intensity` (line 495) `[3cbc948c]`
- `cache_key` (line 261) `[ae6d629c]`
- `cache_stats` (line 931) `[4ac4c4ad]`
- `cached_clip` (line 340) `[46749666]`
- `cancelled` (line 873) `[3684f2e4]`
- `chain_cache_key` (line 334) `[67b19a14]`
- `chain_repr` (line 232) `[2ab64981]`
- `choice` (line 456) `[a0a86e9f]`
- `choice_num` (line 457) `[4c2f37fa]`
- `clip_id` (line 853) `[2ed8f5da]`
- `completed_callback` (line 1032) `[0d5c6ee8]`
- `default` (line 576) `[e33aae66]`
- `filter_config` (line 484) `[cf744860]`
- `filter_count` (line 652) `[91410f72]`
- `filter_id` (line 494) `[44e229b2]`
- `filter_info` (line 356) `[efbc1cc6]`
- `filter_options` (line 524) `[7356f38c]`
- `filter_usage` (line 817) `[a65c9cc1]`
- `filtered_clip` (line 285) `[af46787a]`
- `final_intensity` (line 496) `[de60cdf5]`
- `indices` (line 604) `[d6349a74]`
- `intensity` (line 475) `[aaef30f8]`
- `intensity_choice` (line 469) `[7cd90a62]`
- `intensity_info` (line 534) `[25755910]`
- `intensity_input` (line 580) `[912755f1]`
- `intermediate_clip_id` (line 362) `[886cf6f4]`
- `max_val` (line 533) `[70aa4a26]`
- `memory_info` (line 918) `[82a61a6f]`
- `memory_stats` (line 932) `[3e30c163]`
- `min_val` (line 532) `[125bfabe]`
- `num` (line 620) `[f2273362]`
- `option_num` (line 525) `[3a2c2138]`
- `overall_intensity` (line 477) `[92d96601]`
- `params` (line 222) `[2a133857]`
- `part` (line 607) `[f5384c01]`
- `preset_id` (line 971) `[36e47ae5]`
- `preset_info` (line 979) `[475e439a]`
- `preset_list` (line 450) `[c25d6a57]`
- `process` (line 917) `[45eb9875]`
- `processed_clip` (line 363) `[bf45bee0]`
- `processing_time` (line 390) `[42434713]`
- `processor` (line 1029) `[1c5504d3]`
- `result` (line 420) `[2acc3459]`
- `results` (line 1031) `[f42c237c]`
- `saved_cache_key` (line 374) `[e5bd4ce5]`
- `selected_filters` (line 564) `[47cee96d]`
- `selected_indices` (line 553) `[13a61a92]`
- `selected_preset` (line 459) `[726a3ed9]`
- `selection` (line 545) `[63b54362]`
- `session_id` (line 789) `[3bcaabb6]`
- `start_time` (line 346) `[b59cddd0]`
- `stats` (line 793) `[26d6065f]`
- `task_id` (line 855) `[23365c1f]`
- `task_ids` (line 850) `[da2077b3]`

---

### 📄 `src/processors/video_formatter.py`

#### Imports
- `moviepy.editor.ColorClip` (line 1) `[071a5536]`
- `moviepy.editor.CompositeVideoClip` (line 1) `[66154cf9]`
- `moviepy.editor.VideoFileClip` (line 1) `[3951e41b]`
- `os` (line 2) `[de2abade]`
- `random` (line 125) `[7e18ed42]`
- `src.processors.canvas_processor.process_video_with_canvas` (line 4) `[f3ec9c5b]`
- `src.processors.subtitle_processor.generate_subtitles` (line 5) `[21a187d2]`
- `src.processors.subtitle_video_processor.add_subtitles_to_video` (line 6) `[896ebeb5]`
- `typing.Optional` (line 3) `[abdbaea6]`
- `typing.Tuple` (line 3) `[23996b74]`

#### Classes
- **`VideoFormatter`** (lines 8-122) `[00290f0d]`

#### Functions
- **`__init__(self)`** (lines 9-18) `[70acae9f]`
- **`_crop_video(self, clip, target_size)`** (lines 36-51) `[111ad870]`
- **`_fit_video(self, clip, target_size)`** (lines 20-34) `[7cebb096]`
- **`_resize_with_padding(self, clip, target_size)`** (lines 53-61) `[965e2195]`
- **`format_menu()`** (lines 124-275) `[9af638e2]`
- **`format_video(self, input_path, output_path, target_format, fit_mode, add_canvas, add_subtitles)`** (lines 63-122) `[6962017f]`

#### Variables
- `add_canvas` (line 169) `[e73e18ec]`
- `add_subtitles` (line 172) `[6e705e7d]`
- `all_indices` (line 239) `[fce5cda8]`
- `bg` (line 58) `[3f3bd858]`
- `clip_ratio` (line 38) `[a67ea3b8]`
- `current_path` (line 97) `[9f867244]`
- `cut_mode_choice` (line 228) `[d8baf07d]`
- `end_time` (line 246) `[9bfe640f]`
- `final_duration` (line 190) `[9c419267]`
- `fit_mode` (line 164) `[effecd37]`
- `fit_modes` (line 163) `[2e57e6ca]`
- `format_choice` (line 146) `[bc053987]`
- `formatted_video` (line 78) `[9db046b2]`
- `formatter` (line 126) `[6b5389a4]`
- `height_ratio` (line 22) `[b79585d4]`
- `input_path` (line 132) `[c1379785]`
- `max_segments` (line 215) `[ab99479a]`
- `mode_choice` (line 161) `[bc627bc4]`
- `multi_choice` (line 188) `[ce402427]`
- `new_height` (line 48) `[8f257696]`
- `new_width` (line 47) `[90923085]`
- `output_name` (line 138) `[11da8b73]`
- `output_path` (line 139) `[71b189bf]`
- `resized` (line 49) `[80b95d9c]`
- `result_path` (line 176) `[0a78244b]`
- `scale_factor` (line 23) `[b5c911e6]`
- `segment_indices` (line 241) `[ed1cb186]`
- `start_time` (line 245) `[48416534]`
- `sub_count` (line 195) `[f7187e5c]`
- `sub_length` (line 206) `[2d1a0f48]`
- `sub_output_path` (line 251) `[700df5dc]`
- `subclip` (line 256) `[2fd60acc]`
- `subtitle_json` (line 101) `[0ab8708f]`
- `target_format` (line 151) `[b3d62ad8]`
- `target_ratio` (line 37) `[6ca16a35]`
- `target_size` (line 75) `[a7f58bf1]`
- `temp_path` (line 80) `[f1d6c1af]`
- `video` (line 73) `[57947adc]`
- `width_ratio` (line 21) `[70e40848]`
- `x_offset` (line 44) `[79be9bb0]`
- `x_pos` (line 31) `[9496b860]`
- `y_offset` (line 50) `[3d20d36e]`
- `y_pos` (line 59) `[a13d83ab]`

---

### 📄 `src/processors/video_generator.py`

#### Imports
- `dataclasses.dataclass` (line 10) `[0010e60c]`
- `enum.Enum` (line 11) `[3b3f4ac9]`
- `json` (line 7) `[ff3e4d4d]`
- `logging` (line 12) `[27dced09]`
- `os` (line 3) `[de2abade]`
- `pathlib.Path` (line 8) `[fa6ee8af]`
- `random` (line 4) `[7e18ed42]`
- `src.processors.audio_processor.analyze_beats` (line 20) `[a94d8f54]`
- `src.processors.image_processor.process_image` (line 23) `[0860c957]`
- `src.processors.multiple_image_processor.process_multiple_images` (line 24) `[d6bc2eb5]`
- `src.processors.video_processor.process_video` (line 22) `[9f11718c]`
- `src.processors.vocal_processor.detect_vocal_changes` (line 21) `[84d7e9d1]`
- `src.utils.cache_manager.CacheManager` (line 17) `[45d99fb5]`
- `src.utils.queue_manager.TaskStatus` (line 16) `[d7680471]`
- `src.utils.queue_manager.queue_manager` (line 16) `[0323b6cc]`
- `src.utils.temp_file_manager.TaskPriority` (line 15) `[0b5c99e9]`
- `src.utils.temp_file_manager.TaskType` (line 15) `[41fc328b]`
- `src.utils.temp_file_manager.temp_manager` (line 15) `[71efb9f1]`
- `subprocess` (line 6) `[7d8752c4]`
- `time` (line 5) `[4f9b8491]`
- `typing.Dict` (line 9) `[db5e932b]`
- `typing.List` (line 9) `[eada0f80]`
- `typing.Optional` (line 9) `[abdbaea6]`
- `typing.Tuple` (line 9) `[23996b74]`
- `typing.Union` (line 9) `[26723ff1]`

#### Classes
- **`ContentInfo`** (lines 60-66) `[f466ecc7]`
- **`ContentType`** (lines 26-33) `[bafe748f]`
  - *Inherits from:* Enum
- **`FFmpegVideoAnalyzer`** (lines 68-137) `[14f645cd]`
- **`GenerationSession`** (lines 45-57) `[89bc72c9]`
- **`ProcessingPhase`** (lines 35-42) `[d11ffdf0]`
  - *Inherits from:* Enum
- **`VideoGenerator`** (lines 139-677) `[386c12e9]`

#### Functions
- **`__init__(self)`** (lines 152-185) `[bfe2328a]`
- **`add_media_to_video_ffmpeg(self, video_path, output_path, media_path, media_type, placement, duration)`** (lines 346-426) `[5e40c6ba]`
  - *Add image or video to existing video using FFmpeg*
- **`analyze_content_info(self, content_path)`** (lines 258-310) `[a3fb6d91]`
  - *Analyze content and provide detailed information using FFmpeg*
- **`cleanup_session(self)`** (lines 612-628) `[8e860b74]`
  - *Clean up current generation session*
- **`elapsed_time(self)`** (lines 56-57) `[b4b29514]`
- **`generate_video(config)`** (lines 680-705) `[dbbfb7bf]`
  - *Main entry point for video generation with FFmpeg and temporary file management*
- **`generate_video_with_temp_management(self, config)`** (lines 428-610) `[43dd0f21]`
  - *Generate video with comprehensive temporary file management and FFmpeg*
- **`get_content_type(self, path)`** (lines 224-256) `[bf11cfc7]`
  - *Determine the type of content provided with caching*
- **`get_folder_info(self, folder_path)`** (lines 109-137) `[d0209536]`
  - *Analyze folder containing media files*
- **`get_generation_stats(self)`** (lines 630-632) `[8517b032]`
  - *Get generation statistics*
- **`get_video_info(self, video_path)`** (lines 74-107) `[f393839f]`
  - *Get video information using FFprobe*
- **`is_image_file(self, path)`** (lines 219-222) `[e295c92f]`
  - *Check if file is an image*
- **`is_video_file(self, path)`** (lines 210-217) `[d56a3c47]`
  - *Check if file is a video using FFprobe*
- **`optimize_for_content_type(self, content_type, config)`** (lines 312-344) `[bd0332b6]`
  - *Optimize configuration based on content type*
- **`start_generation_session(self, config)`** (lines 187-202) `[ebd8c7f0]`
  - *Start a new video generation session*
- **`update_session_phase(self, phase)`** (lines 204-208) `[d18454d4]`
  - *Update current session phase*
- **`validate_config(self, config)`** (lines 634-677) `[69bf1e5f]`
  - *Validate configuration parameters*

#### Variables
- `AUDIO_ANALYSIS` (line 39) `[943a4b5d]`
- `CONTENT_ANALYSIS` (line 38) `[96b34ac9]`
- `FINALIZATION` (line 42) `[a7186d11]`
- `IMAGE` (line 30) `[4f6475f8]`
- `IMAGE_FOLDER` (line 31) `[6c688411]`
- `INITIALIZATION` (line 37) `[344277ac]`
- `MAIN_PROCESSING` (line 40) `[a4cd8edb]`
- `MEDIA_ADDITION` (line 41) `[f35f5f25]`
- `MIXED_MEDIA` (line 32) `[0b422d44]`
- `UNKNOWN` (line 33) `[e6f7d5fc]`
- `VIDEO` (line 28) `[2ffb9878]`
- `VIDEO_FOLDER` (line 29) `[127734d4]`
- `available_gb` (line 454) `[758fb333]`
- `base_info` (line 372) `[c4e540fc]`
- `beat_times` (line 473) `[0a18a595]`
- `cmd` (line 213) `[e817dba3]`
- `cmd_concat` (line 404) `[5a9031c7]`
- `cmd_image_to_video` (line 374) `[345a6bef]`
- `concat_file` (line 393) `[8bd18162]`
- `content_info` (line 444) `[47e2f0b1]`
- `content_type` (line 246) `[ecb17e69]`
- `data` (line 83) `[55993706]`
- `disk_info` (line 453) `[bdb93dc1]`
- `duration` (line 366) `[0673f357]`
- `estimated_space_gb` (line 455) `[dc11ea4e]`
- `file_ext` (line 121) `[0499e4bc]`
- `file_path` (line 120) `[5a2316e5]`
- `file_size` (line 293) `[48f6263e]`
- `folder_info` (line 277) `[369b9279]`
- `generation_time` (line 594) `[443f7d90]`
- `generator` (line 690) `[0bed0129]`
- `image_extensions` (line 221) `[8c0767c9]`
- `image_files` (line 115) `[a410de3e]`
- `image_time` (line 281) `[4860921c]`
- `media_to_concat` (line 390) `[ab85cfb9]`
- `optimized_config` (line 698) `[b9f6f868]`
- `required_fields` (line 644) `[8031466f]`
- `response` (line 463) `[6b53210c]`
- `result` (line 214) `[9f039eca]`
- `session_id` (line 615) `[84837fd1]`
- `temp_output` (line 569) `[7186a9c2]`
- `temp_video` (line 369) `[6e30cdcb]`
- `timing_points` (line 479) `[78753b5b]`
- `total_size` (line 116) `[bd4843f4]`
- `video_extensions` (line 111) `[8b8a8ac8]`
- `video_files` (line 114) `[8c848499]`
- `video_info` (line 266) `[72723032]`
- `video_stream` (line 89) `[b2682d4d]`
- `video_time` (line 280) `[a04fdd00]`
- `vocal_times` (line 478) `[3aacaf33]`

---

### 📄 `src/processors/video_processor.py`

#### Imports
- `collections.deque` (line 13) `[f4b9d645]`
- `dataclasses.dataclass` (line 11) `[0010e60c]`
- `enum.Enum` (line 12) `[3b3f4ac9]`
- `json` (line 15) `[ff3e4d4d]`
- `logging` (line 14) `[27dced09]`
- `os` (line 3) `[de2abade]`
- `pathlib.Path` (line 9) `[fa6ee8af]`
- `random` (line 4) `[7e18ed42]`
- `sequential_timing.get_sequential_timing` (line 23) `[de951b91]`
- `src.utils.cache_manager.CacheManager` (line 20) `[45d99fb5]`
- `src.utils.queue_manager.TaskStatus` (line 19) `[d7680471]`
- `src.utils.queue_manager.queue_manager` (line 19) `[0323b6cc]`
- `src.utils.temp_file_manager.TaskPriority` (line 18) `[0b5c99e9]`
- `src.utils.temp_file_manager.TaskType` (line 18) `[41fc328b]`
- `src.utils.temp_file_manager.temp_manager` (line 18) `[71efb9f1]`
- `subprocess` (line 7) `[7d8752c4]`
- `tempfile` (line 8) `[09d25239]`
- `threading` (line 6) `[90781f3e]`
- `time` (line 5) `[4f9b8491]`
- `typing.Dict` (line 10) `[db5e932b]`
- `typing.List` (line 10) `[eada0f80]`
- `typing.Optional` (line 10) `[abdbaea6]`
- `typing.Tuple` (line 10) `[23996b74]`
- `typing.Union` (line 10) `[26723ff1]`

#### Classes
- **`FFmpegProcessor`** (lines 72-181) `[86c63f90]`
- **`ProcessingPhase`** (lines 33-40) `[d24f7b88]`
  - *Inherits from:* Enum
- **`ProcessingSession`** (lines 53-61) `[fc005e6d]`
- **`SpeedPatternType`** (lines 25-31) `[8b67b571]`
  - *Inherits from:* Enum
- **`VideoInfo`** (lines 64-70) `[1b3a3e9f]`
- **`VideoProcessor`** (lines 183-614) `[a5ff046d]`
- **`VideoSegment`** (lines 43-50) `[78383098]`

#### Functions
- **`__init__(self, batch_size)`** (lines 195-231) `[1541f319]`
- **`_cache_segment_path(self, cache_key, segment_path)`** (lines 567-570) `[8bf9dc84]`
  - *Cache segment path*
- **`_cleanup_temp_segments(self, segment_paths)`** (lines 572-583) `[456558d7]`
  - *Clean up temporary segment files*
- **`_get_cached_segment_path(self, cache_key)`** (lines 562-565) `[3fe3dcd8]`
  - *Get cached segment path*
- **`_process_random_with_beat_timing(self, video_files, audio_path, output_path, segment_timings, target_size, audio_start_time, desired_duration, filter_config)`** (lines 366-401) `[0960f597]`
  - *Process videos randomly with beat-based timing - FIXED VERSION*
- **`_process_segment_batch(self, batch_segments, target_size)`** (lines 493-529) `[129e6f66]`
  - *Process a batch of video segments*
- **`_process_segments_in_batches(self, segments, output_path, target_size, audio_path, audio_start_time, desired_duration)`** (lines 452-491) `[73f36982]`
  - *Process video segments in batches to prevent resource exhaustion*
- **`_process_sequential_with_beat_timing(self, video_files, audio_path, output_path, segment_timings, target_size, audio_start_time, desired_duration, filter_config)`** (lines 403-450) `[56d4106c]`
  - *Process videos sequentially with beat-based timing - FIXED VERSION*
- **`_process_single_segment(self, segment, target_size, cache_key)`** (lines 531-560) `[0d51887e]`
  - *Process a single video segment using FFmpeg*
- **`calculate_beat_based_segments(self, beat_times, change_interval, desired_duration)`** (lines 259-313) `[bf447254]`
  - *Calculate segment timing based on beats - FIXED VERSION*
- **`cleanup_session(self)`** (lines 585-599) `[a3195357]`
  - *Clean up current processing session*
- **`concatenate_videos(self, video_paths, output_path, audio_path, audio_start)`** (lines 144-181) `[9076c447]`
  - *Concatenate videos and add audio using FFmpeg*
- **`extract_segment(self, video_path, start_time, duration, output_path, target_size)`** (lines 111-142) `[aec882b0]`
  - *Extract and resize video segment using FFmpeg - FIXED ARRAY ISSUE*
- **`get_cache_key(self, segment_id, params)`** (lines 255-257) `[7d6f485c]`
  - *Generate cache key for video segment*
- **`get_processing_stats(self)`** (lines 601-614) `[84cc0c8b]`
  - *Get processing statistics*
- **`get_video_info(self, video_path)`** (lines 78-109) `[b270c674]`
  - *Get video information using FFprobe*
- **`process_video(video_path_or_folder, audio_path, output_path, beat_times, desired_duration, audio_start_time, change_interval, target_size, cutting_mode, sensitivity_choice, filter_config)`** (lines 617-651) `[22dfc4fd]`
  - *Main entry point for video processing with FFmpeg and temporary file management*
- **`process_videos(self, video_path_or_folder, audio_path, output_path, beat_times, desired_duration, audio_start_time, change_interval, target_size, cutting_mode, sensitivity_choice, filter_config)`** (lines 315-364) `[f7837f86]`
  - *Main video processing function with FFmpeg and batch processing*
- **`start_processing_session(self, session_name, total_segments)`** (lines 233-247) `[d317eb88]`
  - *Start a new processing session*
- **`update_session_phase(self, phase)`** (lines 249-253) `[d18454d4]`
  - *Update current session phase*

#### Variables
- `ACCELERATING` (line 28) `[84b2d61a]`
- `ANALYSIS` (line 36) `[e2ef3781]`
- `BATCH_PROCESSING` (line 38) `[6f6d1d4b]`
- `BEAT_SYNC` (line 31) `[0c3f3488]`
- `CONCATENATION` (line 39) `[cd647769]`
- `CONSTANT` (line 27) `[9ff6cee4]`
- `DECELERATING` (line 29) `[293453cd]`
- `FINALIZATION` (line 40) `[a8640892]`
- `INITIALIZATION` (line 35) `[894a6fbb]`
- `RANDOM` (line 30) `[8e918286]`
- `SEGMENTATION` (line 37) `[27c63edf]`
- `batch_end` (line 464) `[3b2a76bd]`
- `batch_paths` (line 470) `[42829c05]`
- `batch_segments` (line 465) `[f3688b93]`
- `beat_times` (line 285) `[c9f8536d]`
- `cache_key` (line 508) `[9ce15f56]`
- `cached_path` (line 511) `[38b905dd]`
- `cleaned_count` (line 574) `[d3584793]`
- `cmd` (line 156) `[817c8c27]`
- `concat_file` (line 149) `[d230a790]`
- `current_video` (line 429) `[b2693992]`
- `current_video_time` (line 428) `[5d6ebb80]`
- `data` (line 87) `[86dc4d7d]`
- `duration` (line 303) `[0c34891d]`
- `end_time` (line 301) `[c945b5ff]`
- `max_start` (line 386) `[e27fef85]`
- `num_segments` (line 277) `[d91ef776]`
- `processed_segment_paths` (line 458) `[5d0c2e16]`
- `processor` (line 638) `[b862168e]`
- `progress` (line 476) `[a8f27300]`
- `result` (line 171) `[b796194b]`
- `scale_filter` (line 126) `[0eb475ef]`
- `segment` (line 436) `[b47736ed]`
- `segment_duration` (line 278) `[fa7a3f5b]`
- `segment_filename` (line 537) `[6a18f04a]`
- `segment_params` (line 502) `[6ff475bb]`
- `segment_path` (line 519) `[6075a562]`
- `segment_timings` (line 341) `[ab9ea4e7]`
- `segments` (line 409) `[6df30471]`
- `selected_video` (line 376) `[dd7805a5]`
- `session_id` (line 346) `[ac817273]`
- `start_time` (line 280) `[77588e07]`
- `stats` (line 603) `[558c6c9b]`
- `success` (line 541) `[664991c5]`
- `total_segments` (line 457) `[3dfc3794]`
- `video_files` (line 328) `[359d91a1]`
- `video_index` (line 410) `[b30aa532]`
- `video_info` (line 431) `[2131c30f]`
- `video_start_time` (line 387) `[89968f63]`
- `video_stream` (line 93) `[5591eca4]`

---

### 📄 `src/processors/vocal_processor.py`

#### Imports
- `librosa` (line 3) `[c4b23121]`
- `numpy` (line 4) `[d8fca9de]`
- `scipy.ndimage.gaussian_filter1d` (line 5) `[1b5d27bc]`

#### Functions
- **`detect_vocal_changes(audio_path, threshold)`** (lines 11-79) `[14f1b38b]`
  - *Detect changes in vocal presence in the audio*
  - *Calls:* smooth_signal
- **`smooth_signal(signal, window_size)`** (lines 7-9) `[33a029b3]`
  - *Custom smoothing function using gaussian filter*
  - *Called by:* detect_vocal_changes

#### Variables
- `contrast` (line 35) `[f1a27cad]`
- `feature_smooth` (line 42) `[03edbc7e]`
- `feature_sum` (line 41) `[547c42b9]`
- `mel_spect` (line 24) `[154fbbde]`
- `mel_spect_db` (line 32) `[811521d3]`
- `onset_env` (line 64) `[a26bd7ad]`
- `peaks` (line 65) `[d69e5776]`
- `vocal_times` (line 74) `[72978528]`
- `vocal_times_list` (line 76) `[d5c19705]`

---

### 📄 `src/utils/__init__.py`

#### Imports
- `file_handler.ensure_output_dir` (line 1) `[434e68b0]`
- `file_handler.validate_file_path` (line 1) `[9ec1177e]`

#### Variables
- `__all__` (line 3) `[fbbedf7d]`

---

### 📄 `src/utils/arg_parser.py`

#### Imports
- `argparse` (line 2) `[f534a72c]`
- `os` (line 3) `[de2abade]`
- `sys` (line 5) `[9e77b374]`
- `typing.Any` (line 4) `[4ec2ae04]`
- `typing.Dict` (line 4) `[db5e932b]`
- `typing.Optional` (line 4) `[abdbaea6]`

#### Functions
- **`create_parser()`** (lines 7-114) `[c1315c54]`
  - *Called by:* parse_arguments
- **`parse_arguments()`** (lines 226-239) `[ab474094]`
  - *Parse command line arguments and return config*
  - *Calls:* create_parser, validate_args
- **`validate_args(args)`** (lines 116-224) `[61c6c674]`
  - *Validate and convert arguments to config dictionary*
  - *Called by:* parse_arguments

#### Variables
- `args` (line 229) `[859f202c]`
- `config` (line 236) `[e606c9cb]`
- `errors` (line 119) `[c696a451]`
- `media_type` (line 186) `[8a1ea5bc]`
- `parser` (line 228) `[fb30be7a]`
- `sensitivity_map` (line 160) `[42a77e70]`

---

### 📄 `src/utils/cache_manager.py`

#### Imports
- `collections.OrderedDict` (line 22) `[c95cd684]`
- `collections.defaultdict` (line 22) `[4152f3fd]`
- `dataclasses.dataclass` (line 20) `[0010e60c]`
- `dataclasses.field` (line 20) `[7cfc6d2d]`
- `datetime.datetime` (line 27) `[605c9066]`
- `datetime.timedelta` (line 27) `[fa21c1b1]`
- `enum.Enum` (line 21) `[3b3f4ac9]`
- `heapq` (line 18) `[dcaa9b42]`
- `json` (line 25) `[ff3e4d4d]`
- `logging` (line 23) `[27dced09]`
- `os` (line 15) `[de2abade]`
- `pathlib.Path` (line 24) `[fa6ee8af]`
- `pickle` (line 26) `[888eeaa6]`
- `random` (line 524) `[7e18ed42]`
- `threading` (line 17) `[90781f3e]`
- `time` (line 16) `[4f9b8491]`
- `typing.Any` (line 19) `[4ec2ae04]`
- `typing.Callable` (line 19) `[60ed66b7]`
- `typing.Dict` (line 19) `[db5e932b]`
- `typing.List` (line 19) `[eada0f80]`
- `typing.Optional` (line 19) `[abdbaea6]`
- `typing.Tuple` (line 19) `[23996b74]`
- `typing.Union` (line 19) `[26723ff1]`
- `weakref` (line 28) `[2b00e696]`

#### Classes
- **`CacheEntry`** (lines 50-89) `[9d5bf133]`
- **`CacheManager`** (lines 118-806) `[799ffed9]`
- **`CachePolicy`** (lines 31-37) `[f812b294]`
  - *Inherits from:* Enum
- **`CacheStats`** (lines 93-115) `[fb8b8165]`
- **`CacheStatus`** (lines 40-46) `[5f348f63]`
  - *Inherits from:* Enum

#### Functions
- **`__init__(self, max_size_bytes, max_entries, policy, default_ttl, enable_persistence, persistence_path, maintenance_interval, enable_stats)`** (lines 131-181) `[8e7dd0b1]`
- **`__post_init__(self)`** (lines 63-67) `[5e0b5896]`
- **`_add_to_policy_structures(self, key, entry)`** (lines 566-578) `[4f8b1dcd]`
  - *Add entry to policy-specific data structures*
- **`_ensure_space(self, required_size)`** (lines 400-412) `[7d9e5b4a]`
  - *Ensure sufficient space is available*
- **`_estimate_size(self, value)`** (lines 656-666) `[6ac8b7e0]`
  - *Estimate memory size of a value*
- **`_evict_adaptive(self, count)`** (lines 499-520) `[0bbfbb0d]`
  - *Evict entries using adaptive policy*
- **`_evict_entries(self, count)`** (lines 414-434) `[3ea2979e]`
  - *Evict entries based on the current policy*
- **`_evict_lfu(self, count)`** (lines 447-465) `[3dd80fa7]`
  - *Evict least frequently used entries*
- **`_evict_lru(self, count)`** (lines 436-445) `[4b847d87]`
  - *Evict least recently used entries*
- **`_evict_random(self, count)`** (lines 522-537) `[9fd68768]`
  - *Evict random entries*
- **`_evict_ttl(self, count)`** (lines 467-497) `[5e68f287]`
  - *Evict entries based on TTL*
- **`_expire_entries(self)`** (lines 608-623) `[10206add]`
  - *Remove expired entries*
- **`_init_policy_structures(self)`** (lines 183-197) `[8d816b5c]`
  - *Initialize data structures for specific cache policies*
- **`_load_persistent_cache(self)`** (lines 708-733) `[bc652786]`
  - *Load cache from persistent storage*
- **`_maintenance_worker(self)`** (lines 209-225) `[62c87934]`
  - *Background maintenance worker*
- **`_optimize_cache(self)`** (lines 625-634) `[d99332ce]`
  - *Optimize cache performance*
- **`_rebuild_frequency_buckets(self)`** (lines 636-644) `[e91e7ccb]`
  - *Rebuild frequency buckets for consistency*
- **`_remove_entry(self, key)`** (lines 539-564) `[75acd1fe]`
  - *Remove an entry and update all data structures*
- **`_remove_from_policy_structures(self, key, entry)`** (lines 598-606) `[6c21cf07]`
  - *Remove entry from policy-specific data structures*
- **`_save_persistent_cache(self)`** (lines 668-706) `[2860d374]`
  - *Save cache to persistent storage*
- **`_start_maintenance(self)`** (lines 199-207) `[75681499]`
  - *Start background maintenance thread*
- **`_update_policy_structures(self, key, entry)`** (lines 580-596) `[1e71601d]`
  - *Update policy-specific data structures on access*
- **`_update_statistics(self)`** (lines 646-654) `[59f987b7]`
  - *Update cache statistics*
- **`add_access_callback(self, callback)`** (lines 749-751) `[9e321001]`
  - *Add callback for cache access events*
- **`add_eviction_callback(self, callback)`** (lines 745-747) `[0ca4501a]`
  - *Add callback for cache eviction events*
- **`age(self)`** (lines 70-72) `[79af89dc]`
  - *Get age of entry in seconds*
- **`clear(self)`** (lines 375-398) `[e28a634e]`
  - *Clear all cache entries*
- **`get(self, key)`** (lines 294-352) `[96cb9631]`
  - *Get an entry from the cache*
- **`get_entries_info(self)`** (lines 771-788) `[6baa7800]`
  - *Get information about all cache entries*
- **`get_statistics(self)`** (lines 753-769) `[58bbe181]`
  - *Get comprehensive cache statistics*
- **`is_expired(self)`** (lines 75-79) `[8a340086]`
  - *Check if entry is expired*
- **`put(self, key, value, size, ttl, priority, metadata)`** (lines 227-292) `[9a144c52]`
  - *Put an entry into the cache*
- **`remove(self, key)`** (lines 354-373) `[3bf91ce8]`
  - *Remove an entry from the cache*
- **`shutdown(self)`** (lines 790-806) `[9accba43]`
  - *Shutdown cache manager*
- **`time_since_access(self)`** (lines 82-84) `[9b2c35fc]`
  - *Get time since last access in seconds*
- **`touch(self)`** (lines 86-89) `[6d18979c]`
  - *Update access time and count*
- **`update_avg_access_time(self, access_time)`** (lines 111-115) `[d9ae8c8e]`
  - *Update average access time*
- **`update_hit_rate(self)`** (lines 106-109) `[e77306a3]`
  - *Update hit rate calculation*
- **`warm_cache(self, keys, loader)`** (lines 735-743) `[e641a276]`
  - *Warm up cache with specific keys*

#### Variables
- `ACTIVE` (line 42) `[04dff8e0]`
- `ADAPTIVE` (line 36) `[913d88ad]`
- `ERROR` (line 46) `[05914a12]`
- `EVICTED` (line 44) `[55f84ecf]`
- `EXPIRED` (line 43) `[632d10be]`
- `LFU` (line 34) `[84216229]`
- `LOADING` (line 45) `[d251a0cb]`
- `LRU` (line 33) `[181e12ec]`
- `RANDOM` (line 37) `[6ea5d18a]`
- `TTL` (line 35) `[de0ed83a]`
- `access_time` (line 341) `[f585ac88]`
- `cache_data` (line 715) `[92b17c24]`
- `current_time` (line 610) `[7a1b0d18]`
- `empty_buckets` (line 632) `[baa61864]`
- `entries_info` (line 773) `[0d2fae9c]`
- `entry` (line 477) `[0405939f]`
- `evicted` (line 428) `[a55507ed]`
- `expired_keys` (line 611) `[490bfab3]`
- `expiry_time` (line 577) `[3c58c5b3]`
- `freq` (line 604) `[aa54cc3c]`
- `key` (line 530) `[7b4c8ad4]`
- `keys` (line 527) `[1563e5e9]`
- `new_buckets` (line 638) `[ed06f78e]`
- `new_freq` (line 589) `[7bc140e9]`
- `old_freq` (line 588) `[5f480035]`
- `oldest_entries` (line 488) `[38cbdea6]`
- `size` (line 247) `[2ea81236]`
- `start_time` (line 304) `[27b78009]`
- `stats` (line 719) `[455fba7c]`
- `strategies` (line 504) `[316b3980]`
- `total_requests` (line 108) `[6953b462]`
- `ttl` (line 251) `[a64d3649]`
- `value` (line 740) `[a434615e]`

---

### 📄 `src/utils/file_handler.py`

#### Imports
- `os` (line 1) `[de2abade]`

#### Functions
- **`ensure_output_dir(file_path)`** (lines 20-26) `[9fa49a63]`
  - *Ensure output directory exists*
- **`validate_file_path(file_path, file_type)`** (lines 3-18) `[96139857]`
  - *Validate if file exists and has correct extension*

#### Variables
- `__all__` (line 28) `[0a49ab72]`
- `directory` (line 24) `[f4041e5a]`
- `valid_extensions` (line 10) `[8bd587dd]`

---

### 📄 `src/utils/io_operations.py`

#### Imports
- `contextlib.contextmanager` (line 28) `[d4651b4c]`
- `dataclasses.dataclass` (line 25) `[0010e60c]`
- `enum.Enum` (line 26) `[3b3f4ac9]`
- `fcntl` (line 19) `[b5544272]`
- `gzip` (line 16) `[f667174a]`
- `hashlib` (line 22) `[ada1d9e0]`
- `logging` (line 27) `[27dced09]`
- `mmap` (line 30) `[1e63722b]`
- `os` (line 14) `[de2abade]`
- `pathlib.Path` (line 23) `[fa6ee8af]`
- `psutil` (line 29) `[f6b32ab9]`
- `shutil` (line 15) `[582f9ff7]`
- `stat` (line 20) `[f9e42ccd]`
- `tempfile` (line 21) `[09d25239]`
- `threading` (line 17) `[90781f3e]`
- `time` (line 18) `[4f9b8491]`
- `typing.Any` (line 24) `[4ec2ae04]`
- `typing.Dict` (line 24) `[db5e932b]`
- `typing.List` (line 24) `[eada0f80]`
- `typing.Optional` (line 24) `[abdbaea6]`
- `typing.Tuple` (line 24) `[23996b74]`
- `typing.Union` (line 24) `[26723ff1]`

#### Classes
- **`CompressionLevel`** (lines 33-37) `[58b5ae23]`
  - *Inherits from:* Enum
- **`DiskSpaceInfo`** (lines 65-70) `[6da5df51]`
- **`FileMetadata`** (lines 51-61) `[c14406ff]`
- **`FileOperation`** (lines 40-47) `[da99b203]`
  - *Inherits from:* Enum
- **`IOOperations`** (lines 73-784) `[71fff7b1]`

#### Functions
- **`__init__(self, base_dir)`** (lines 86-113) `[b9809cf7]`
- **`_calculate_checksum(self, file_path, algorithm)`** (lines 162-176) `[7aada505]`
  - *Calculate file checksum efficiently*
- **`_file_lock(self, file_path)`** (lines 123-130) `[17325618]`
  - *Context manager for file locking*
- **`_get_file_lock(self, file_path)`** (lines 115-120) `[1a1dfc9b]`
  - *Get or create a thread lock for a specific file*
- **`atomic_read(self, file_path, mode)`** (lines 229-259) `[4620d2d9]`
  - *Atomic read operation with error handling*
- **`atomic_write(self, file_path, data, mode, backup)`** (lines 178-227) `[254be2ac]`
  - *Atomic write operation that ensures data integrity*
- **`cleanup_temp_files(self, max_age_hours)`** (lines 698-739) `[bd51d918]`
  - *Clean up temporary files older than specified age*
- **`compress_file(self, source_path, target_path, compression_level)`** (lines 261-310) `[316c4d24]`
  - *Compress a file using gzip compression*
- **`copy_file(self, source_path, target_path, create_dirs, preserve_metadata)`** (lines 489-524) `[497742d6]`
  - *Copy a file with metadata preservation*
- **`create_directory(self, dir_path, mode)`** (lines 526-546) `[708eb1f6]`
  - *Create directory with specified permissions*
- **`decompress_file(self, source_path, target_path)`** (lines 312-353) `[8d9df5d0]`
  - *Decompress a gzip-compressed file*
- **`ensure_disk_space(self, required_bytes, path)`** (lines 396-415) `[5e1dd67d]`
  - *Ensure sufficient disk space is available*
- **`get_disk_space_info(self, path)`** (lines 355-394) `[5425e418]`
  - *Get disk space information for a path*
- **`get_file_metadata(self, file_path)`** (lines 132-160) `[37af5014]`
  - *Get comprehensive metadata for a file*
- **`get_file_size(self, file_path)`** (lines 612-632) `[63413ae0]`
  - *Get file size in bytes*
- **`get_operation_stats(self)`** (lines 662-681) `[081f91ad]`
  - *Get I/O operation statistics*
- **`list_files(self, dir_path, pattern, recursive)`** (lines 578-610) `[dbc58be9]`
  - *List files in directory with optional pattern matching*
- **`move_file(self, source_path, target_path, create_dirs)`** (lines 455-487) `[9d352ce4]`
  - *Move a file atomically*
- **`optimize_storage(self)`** (lines 741-784) `[059d432f]`
  - *Optimize storage by compressing large files*
- **`remove_directory(self, dir_path, recursive)`** (lines 548-576) `[44cd7d94]`
  - *Remove directory*
- **`reset_stats(self)`** (lines 683-696) `[64e096d5]`
  - *Reset operation statistics*
- **`safe_delete(self, file_path, secure)`** (lines 417-453) `[8c7cdc69]`
  - *Safely delete a file with optional secure deletion*
- **`verify_file_integrity(self, file_path, expected_checksum, algorithm)`** (lines 634-660) `[e2ec6dbf]`
  - *Verify file integrity using checksum*

#### Variables
- `APPEND` (line 44) `[fd6d35e9]`
- `BALANCED` (line 36) `[34444cbc]`
- `BEST` (line 37) `[88be1058]`
- `COMPRESS` (line 46) `[ee68ea14]`
- `DECOMPRESS` (line 47) `[a18d6d39]`
- `DELETE` (line 45) `[1ca886f3]`
- `FAST` (line 35) `[4fdc6a9b]`
- `READ` (line 42) `[0e838014]`
- `WRITE` (line 43) `[0f490dfb]`
- `actual_checksum` (line 648) `[c9fc7b52]`
- `age_threshold` (line 707) `[bd999fe6]`
- `backup_path` (line 198) `[cf0cbc28]`
- `bytes_freed` (line 715) `[5a6a631e]`
- `bytes_saved` (line 763) `[b9046d45]`
- `cache_path` (line 749) `[e9a5283d]`
- `checksum` (line 142) `[5e2318d7]`
- `compressed_count` (line 762) `[afcb5b60]`
- `compressed_path` (line 767) `[468e15e4]`
- `compressed_size` (line 770) `[194213d6]`
- `compression_time` (line 293) `[db6bcd03]`
- `current_time` (line 706) `[03c4178c]`
- `data` (line 249) `[585eb135]`
- `decompression_time` (line 342) `[03c19836]`
- `disk_info` (line 378) `[e72405f2]`
- `file_age` (line 724) `[c41d0bc2]`
- `file_size` (line 727) `[299699c4]`
- `files` (line 601) `[d3c69805]`
- `files_removed` (line 714) `[5f1405db]`
- `hash_func` (line 165) `[714c3946]`
- `is_compressed` (line 145) `[46917f1f]`
- `large_files` (line 745) `[bd3a47b8]`
- `lock` (line 125) `[3ee2c829]`
- `original_size` (line 298) `[6b5e7d24]`
- `path` (line 623) `[65db3ade]`
- `ratio` (line 300) `[6e6eeeed]`
- `source` (line 504) `[288f8131]`
- `start_time` (line 324) `[593a3624]`
- `stat_info` (line 139) `[18c47cb3]`
- `target` (line 505) `[c94efe4c]`
- `temp_dirs` (line 709) `[b9d4a2b0]`
- `temp_path` (line 202) `[eeeb2ef9]`
- `usage` (line 376) `[fb51f2e4]`

---

### 📄 `src/utils/queue_manager.py`

#### Imports
- `collections.defaultdict` (line 28) `[4152f3fd]`
- `collections.deque` (line 28) `[f4b9d645]`
- `concurrent.futures.Future` (line 27) `[ef9743bf]`
- `concurrent.futures.ProcessPoolExecutor` (line 27) `[4c633bc0]`
- `concurrent.futures.ThreadPoolExecutor` (line 27) `[107d7d8e]`
- `concurrent.futures.as_completed` (line 27) `[04389600]`
- `dataclasses.dataclass` (line 25) `[0010e60c]`
- `dataclasses.field` (line 25) `[7cfc6d2d]`
- `datetime.datetime` (line 30) `[605c9066]`
- `datetime.timedelta` (line 30) `[fa21c1b1]`
- `enum.Enum` (line 26) `[3b3f4ac9]`
- `heapq` (line 31) `[dcaa9b42]`
- `json` (line 22) `[ff3e4d4d]`
- `logging` (line 29) `[27dced09]`
- `multiprocessing` (line 18) `[23faa645]`
- `os` (line 15) `[de2abade]`
- `pathlib.Path` (line 23) `[fa6ee8af]`
- `pickle` (line 21) `[888eeaa6]`
- `queue` (line 19) `[90665960]`
- `threading` (line 17) `[90781f3e]`
- `time` (line 16) `[4f9b8491]`
- `typing.Any` (line 24) `[4ec2ae04]`
- `typing.Callable` (line 24) `[60ed66b7]`
- `typing.Dict` (line 24) `[db5e932b]`
- `typing.List` (line 24) `[eada0f80]`
- `typing.Optional` (line 24) `[abdbaea6]`
- `typing.Tuple` (line 24) `[23996b74]`
- `typing.Union` (line 24) `[26723ff1]`
- `uuid` (line 20) `[8b76fbd0]`
- `weakref` (line 32) `[2b00e696]`

#### Classes
- **`QueueManager`** (lines 458-1306) `[525f7449]`
- **`QueueStats`** (lines 125-148) `[24b8dc48]`
- **`QueueType`** (lines 55-60) `[e06625c4]`
  - *Inherits from:* Enum
- **`Task`** (lines 80-121) `[702b2a8a]`
- **`TaskPriority`** (lines 46-52) `[de33205c]`
  - *Inherits from:* Enum
- **`TaskQueue`** (lines 151-455) `[11d5503b]`
- **`TaskResult`** (lines 64-76) `[2a14ae41]`
- **`TaskStatus`** (lines 35-43) `[33d7f58a]`
  - *Inherits from:* Enum

#### Functions
- **`__init__(self, persistence_path, enable_persistence, monitoring_interval, max_retry_attempts, retry_backoff_factor)`** (lines 471-520) `[c47b8969]`
- **`__lt__(self, other)`** (lines 103-105) `[88699b39]`
  - *For priority queue ordering*
- **`__post_init__(self)`** (lines 74-76) `[054e5a3c]`
- **`_can_execute_now(self)`** (lines 265-279) `[ed5c08fe]`
  - *Check if we can execute a task now based on rate limiting*
- **`_check_dependent_tasks(self, completed_task_id)`** (lines 738-754) `[522bad87]`
  - *Check for tasks that depend on the completed task*
- **`_cleanup_old_tasks(self)`** (lines 853-882) `[be388604]`
  - *Clean up old completed tasks*
- **`_create_default_queues(self)`** (lines 522-563) `[142b9f03]`
  - *Create default task queues*
- **`_get_queue_for_task(self, task)`** (lines 756-769) `[13213dab]`
  - *Get appropriate queue name for a task*
- **`_handle_task_completion(self, task, result)`** (lines 719-736) `[adc8a138]`
  - *Handle task completion and check for dependent tasks*
- **`_load_persistent_data(self)`** (lines 920-952) `[07c22113]`
  - *Load persistent data*
- **`_log_statistics(self)`** (lines 826-851) `[21acec71]`
  - *Log queue statistics*
- **`_monitoring_worker(self)`** (lines 801-814) `[de9bd756]`
  - *Background worker for monitoring and maintenance*
- **`_persistence_worker(self)`** (lines 816-824) `[c985357f]`
  - *Background worker for data persistence*
- **`_queue_worker(self, queue_name)`** (lines 697-717) `[72c03fee]`
  - *Worker thread for a specific queue*
- **`_retry_task(self, task)`** (lines 771-786) `[d6f9dd8b]`
  - *Retry a failed task with exponential backoff*
- **`_save_persistent_data(self)`** (lines 884-918) `[63389704]`
  - *Save persistent data*
- **`_start_background_workers(self)`** (lines 788-799) `[473b78e5]`
  - *Start background monitoring threads*
- **`age(self)`** (lines 108-110) `[a59b161f]`
  - *Get task age in seconds*
- **`can_execute(self, completed_tasks)`** (lines 119-121) `[7f17dd4b]`
  - *Check if task can be executed based on dependencies*
- **`cancel_task(self, task_id)`** (lines 994-1020) `[d489afb3]`
  - *Cancel a task*
- **`clear_dead_letter_queue(self)`** (lines 1139-1144) `[31b14bdb]`
  - *Clear the dead letter queue*
- **`create_queue(self, name, queue_type, max_workers, max_queue_size, rate_limit)`** (lines 565-614) `[874dff82]`
  - *Create a new task queue*
- **`create_task_chain(self, tasks, chain_name)`** (lines 1218-1250) `[d8b77205]`
  - *Create a chain of dependent tasks*
- **`create_task_group(self, tasks, group_name, wait_for_all)`** (lines 1252-1285) `[ef500b69]`
  - *Create a group of parallel tasks*
- **`execute_task(self, task)`** (lines 281-372) `[ff4c5379]`
  - *Execute a single task*
- **`execution_time(self)`** (lines 113-117) `[e9855ba6]`
  - *Get execution time in seconds*
- **`get_dependent_tasks(self, task_id)`** (lines 1199-1216) `[58ce3152]`
  - *Get tasks that depend on a given task*
- **`get_global_statistics(self)`** (lines 1086-1102) `[59c66ec6]`
  - *Get global statistics across all queues*
- **`get_next_task(self, timeout)`** (lines 231-263) `[4de2d5ae]`
  - *Get the next task to execute*
- **`get_queue_statistics(self)`** (lines 1077-1084) `[b22f4adb]`
  - *Get statistics for all queues*
- **`get_statistics(self)`** (lines 422-440) `[22c0f8e4]`
  - *Get queue statistics*
- **`get_task_dependencies(self, task_id)`** (lines 1186-1197) `[d9b7f7c6]`
  - *Get dependencies for a task*
- **`get_task_result(self, task_id)`** (lines 969-992) `[dccc46cc]`
  - *Get result of a completed task*
- **`get_task_status(self, task_id)`** (lines 954-967) `[f032d9dd]`
  - *Get status of a task*
- **`pause_queue(self, queue_name)`** (lines 1146-1165) `[19d3311e]`
  - *Pause a queue (stop processing new tasks)*
- **`put(self, task)`** (lines 200-229) `[3ad01460]`
  - *Add a task to the queue*
- **`resume_queue(self, queue_name)`** (lines 1167-1184) `[332bcadd]`
  - *Resume a paused queue*
- **`retry_dead_letter_tasks(self, max_tasks)`** (lines 1104-1137) `[2af6f543]`
  - *Retry tasks from dead letter queue*
- **`retry_func()`** (lines 779-783) `[ce15d42e]`
- **`shutdown(self)`** (lines 1287-1306) `[d07fcbae]`
  - *Shutdown the queue manager*
- **`submit_task(self, task_type, func, args, kwargs, queue_name, priority, timeout, max_retries, depends_on, callback, progress_callback, metadata)`** (lines 616-695) `[b872a3c9]`
  - *Submit a task for execution*
- **`update_completion(self, execution_time)`** (lines 138-148) `[5b034800]`
  - *Update stats when a task completes*
- **`wait_for_task(self, task_id, timeout)`** (lines 1022-1047) `[4f02e3ed]`
  - *Wait for a task to complete*
- **`wait_for_tasks(self, task_ids, timeout)`** (lines 1049-1075) `[7a2897b1]`
  - *Wait for multiple tasks to complete*

#### Variables
- `BATCH` (line 60) `[1d00181c]`
- `CANCELLED` (line 41) `[26b6eee1]`
- `COMPLETED` (line 39) `[fa44ba66]`
- `CRITICAL` (line 52) `[cefa4a73]`
- `FAILED` (line 40) `[12f27b20]`
- `HIGH` (line 50) `[f55b9cfb]`
- `LOW` (line 48) `[0a6ecbfe]`
- `NORMAL` (line 49) `[46c9225c]`
- `PENDING` (line 37) `[e2c2ba68]`
- `PROCESS_POOL` (line 58) `[8a3d61eb]`
- `RETRYING` (line 42) `[f1109f96]`
- `RUNNING` (line 38) `[56c38af7]`
- `SEQUENTIAL` (line 59) `[2e1de346]`
- `THREAD_POOL` (line 57) `[27c92333]`
- `TIMEOUT` (line 43) `[8fbfe778]`
- `URGENT` (line 51) `[2c4547e9]`
- `allowed_executions` (line 278) `[23ad6095]`
- `count` (line 1142) `[2cbc7ec3]`
- `current_time` (line 270) `[28362b27]`
- `cutoff_time` (line 855) `[f34139ef]`
- `data` (line 929) `[398fa170]`
- `dependent_tasks` (line 1209) `[4c9c3f5e]`
- `execution_time` (line 344) `[3d83ca29]`
- `future` (line 393) `[5c7cf639]`
- `metadata` (line 1272) `[ffb5f159]`
- `monitor_thread` (line 791) `[cc7f77d9]`
- `old_results` (line 872) `[b2ef0e8d]`
- `old_task_ids` (line 859) `[1b280753]`
- `persist_thread` (line 797) `[390b962a]`
- `persistence_file` (line 923) `[6358a989]`
- `priority_score` (line 217) `[7b709097]`
- `queue` (line 590) `[ef72e129]`
- `queue_manager` (line 1310) `[f0dd2647]`
- `queue_name` (line 1130) `[0b15243e]`
- `queue_stats` (line 1099) `[6c59aa89]`
- `queue_type` (line 657) `[170a9580]`
- `result` (line 1066) `[0c313350]`
- `results` (line 1060) `[965a76fe]`
- `retried` (line 1114) `[d73c9f65]`
- `retry_delay` (line 774) `[508b3385]`
- `retry_thread` (line 785) `[7ad66960]`
- `start_time` (line 1061) `[7656f7de]`
- `stats` (line 838) `[1ed4b94c]`
- `status` (line 1040) `[58691f38]`
- `task` (line 1121) `[ecf52c8f]`
- `task_id` (line 1278) `[4db07d51]`
- `task_ids` (line 1267) `[454b904f]`
- `task_result` (line 398) `[7f38ab26]`
- `tasks_to_queue` (line 740) `[eb776b42]`
- `tasks_to_retry` (line 1117) `[67b7d938]`
- `time_window` (line 147) `[1e3d370a]`
- `total_stats` (line 1088) `[6c6ac06c]`
- `worker_thread` (line 601) `[8ad17ab1]`

---

### 📄 `src/utils/temp_file_manager.py`

#### Imports
- `concurrent.futures.ProcessPoolExecutor` (line 24) `[4c633bc0]`
- `concurrent.futures.ThreadPoolExecutor` (line 24) `[107d7d8e]`
- `concurrent.futures.as_completed` (line 24) `[04389600]`
- `dataclasses.dataclass` (line 22) `[0010e60c]`
- `datetime.datetime` (line 26) `[605c9066]`
- `datetime.timedelta` (line 26) `[fa21c1b1]`
- `enum.Enum` (line 23) `[3b3f4ac9]`
- `hashlib` (line 15) `[ada1d9e0]`
- `io_operations.CompressionLevel` (line 29) `[37cdd933]`
- `io_operations.FileMetadata` (line 29) `[2a197bed]`
- `io_operations.IOOperations` (line 29) `[f38d6f18]`
- `json` (line 17) `[ff3e4d4d]`
- `logging` (line 25) `[27dced09]`
- `multiprocessing` (line 13) `[23faa645]`
- `os` (line 10) `[de2abade]`
- `pathlib.Path` (line 20) `[fa6ee8af]`
- `pickle` (line 16) `[888eeaa6]`
- `queue` (line 14) `[90665960]`
- `shutil` (line 540) `[582f9ff7]`
- `subprocess` (line 18) `[7d8752c4]`
- `tempfile` (line 19) `[09d25239]`
- `threading` (line 12) `[90781f3e]`
- `time` (line 11) `[4f9b8491]`
- `typing.Any` (line 21) `[4ec2ae04]`
- `typing.Callable` (line 21) `[60ed66b7]`
- `typing.Dict` (line 21) `[db5e932b]`
- `typing.List` (line 21) `[eada0f80]`
- `typing.Optional` (line 21) `[abdbaea6]`
- `typing.Tuple` (line 21) `[23996b74]`
- `typing.Union` (line 21) `[26723ff1]`

#### Classes
- **`CacheEntry`** (lines 71-81) `[f73d1ade]`
- **`FFmpegProcessor`** (lines 94-299) `[a14437d6]`
- **`FFmpegResult`** (lines 85-91) `[a3ae7c41]`
- **`Task`** (lines 56-67) `[953ad554]`
- **`TaskPriority`** (lines 47-52) `[58a3c167]`
  - *Inherits from:* Enum
- **`TaskType`** (lines 32-44) `[f32404f2]`
  - *Inherits from:* Enum
- **`TempFileManager`** (lines 302-1057) `[965a352b]`

#### Functions
- **`__init__(self, base_temp_dir, max_cache_size_gb, max_threads, max_processes, enable_compression, compression_threshold_mb)`** (lines 316-387) `[fc49315f]`
- **`__post_init__(self)`** (lines 65-67) `[bea45d16]`
- **`_cache_cleanup_worker(self)`** (lines 458-469) `[30f29f49]`
  - *Background worker for cache maintenance*
- **`_cleanup_cache(self)`** (lines 737-773) `[a4e35095]`
  - *Clean up cache to free space*
- **`_load_cache_index(self)`** (lines 790-806) `[a966e39e]`
  - *Load cache index from disk*
- **`_process_cleanup_task(self, task)`** (lines 932-934) `[8a08ef49]`
  - *Process cleanup task*
- **`_process_compress_task(self, task)`** (lines 936-946) `[88df21bf]`
  - *Process compress task*
- **`_process_decompress_task(self, task)`** (lines 948-957) `[9a8acaff]`
  - *Process decompress task*
- **`_process_ffmpeg_concat_task(self, task)`** (lines 888-899) `[690841e5]`
  - *Process FFmpeg concatenation task*
- **`_process_ffmpeg_extract_task(self, task)`** (lines 874-886) `[6a41234d]`
  - *Process FFmpeg extract task*
- **`_process_ffmpeg_filter_task(self, task)`** (lines 901-912) `[c0d2411d]`
  - *Process FFmpeg filter task*
- **`_process_load_clip_task(self, task)`** (lines 925-930) `[2d6db89d]`
  - *Process load clip task (legacy compatibility)*
- **`_process_save_clip_task(self, task)`** (lines 915-923) `[2c3aa857]`
  - *Process save clip task (legacy compatibility)*
- **`_process_task(self, task)`** (lines 484-507) `[7ad8d6c2]`
  - *Process a single task*
- **`_save_cache_index(self)`** (lines 808-832) `[6844bc7d]`
  - *Save cache index to disk*
- **`_setup_directories(self)`** (lines 389-405) `[84d3161f]`
  - *Set up directory structure*
- **`_setup_logging(self)`** (lines 407-420) `[29939866]`
  - *Set up logging for the temp file manager*
- **`_start_background_workers(self)`** (lines 422-437) `[75422652]`
  - *Start background worker threads*
- **`_statistics_worker(self)`** (lines 471-482) `[d6ab628e]`
  - *Background worker for statistics collection*
- **`_task_processor_worker(self)`** (lines 439-456) `[6fa15381]`
  - *Background worker to process tasks from queues*
- **`_update_statistics(self)`** (lines 775-788) `[057fef22]`
  - *Update statistics*
- **`apply_filters(self, input_path, output_path, filter_chain)`** (lines 224-265) `[9b03468e]`
  - *Apply FFmpeg filter chain to video*
- **`apply_video_filters(self, input_path, output_path, filter_chain, cache_key)`** (lines 694-735) `[a65966b9]`
  - *Apply FFmpeg filters to video*
- **`cleanup_session(self)`** (lines 1027-1057) `[d273daa0]`
  - *Clean up current session*
- **`cleanup_temp_manager()`** (lines 1088-1090) `[d140c8d0]`
  - *Convenience function to cleanup temp manager*
- **`clear_cache(self)`** (lines 854-871) `[84d66bb3]`
  - *Clear entire cache*
- **`concatenate_video_segments(self, segment_paths, output_path, audio_path, audio_start)`** (lines 658-692) `[1107e359]`
  - *Concatenate video segments using FFmpeg*
- **`concatenate_videos(self, video_paths, output_path, audio_path, audio_start)`** (lines 155-222) `[16f86934]`
  - *Concatenate videos using FFmpeg concat demuxer*
- **`extract_segment(self, video_path, start_time, duration, output_path, target_size)`** (lines 101-153) `[9de22d5f]`
  - *Extract video segment using FFmpeg*
- **`extract_video_segment(self, video_path, start_time, duration, cache_key, target_size)`** (lines 610-656) `[db851fdf]`
  - *Extract video segment using FFmpeg and cache the result*
- **`get_cache_key(self, identifier, params)`** (lines 509-516) `[ab2437e3]`
  - *Generate a cache key from identifier and parameters*
- **`get_statistics(self)`** (lines 834-852) `[82d5225d]`
  - *Get current statistics*
- **`get_temp_manager_stats()`** (lines 1083-1085) `[94192d0c]`
  - *Convenience function to get temp manager statistics*
- **`get_video_info(self, video_path)`** (lines 267-299) `[a0bb1ab5]`
  - *Get video information using FFprobe*
- **`load_file_sync(self, cache_key)`** (lines 570-608) `[a2401fcf]`
  - *Load a cached file synchronously*
- **`save_file_sync(self, cache_key, file_path, category)`** (lines 518-568) `[56ed4d82]`
  - *Save a file to cache synchronously (for FFmpeg output files)*
- **`submit_concat_task(self, segment_paths, output_path, audio_path, audio_start, callback, priority)`** (lines 983-1003) `[e7d50849]`
  - *Submit video concatenation task*
- **`submit_extract_task(self, video_path, start_time, duration, cache_key, target_size, callback, priority)`** (lines 960-981) `[468d6359]`
  - *Submit video extraction task*
- **`submit_filter_task(self, input_path, output_path, filter_chain, cache_key, callback, priority)`** (lines 1005-1025) `[49abdfd8]`
  - *Submit video filter task*

#### Variables
- `APPLY_FILTER` (line 37) `[2f02bf5f]`
- `CLEANUP` (line 39) `[1ef9cb8b]`
- `COMPOSITE_VIDEO` (line 38) `[4e190562]`
- `COMPRESS` (line 40) `[bb418cdd]`
- `DECOMPRESS` (line 41) `[71fd35b3]`
- `FFMPEG_CONCAT` (line 43) `[5ddbbf81]`
- `FFMPEG_EXTRACT` (line 42) `[1071a01b]`
- `FFMPEG_FILTER` (line 44) `[57732765]`
- `HIGH` (line 51) `[2887e978]`
- `LOAD_CLIP` (line 35) `[0f5fd8bc]`
- `LOW` (line 49) `[344a2f62]`
- `NORMAL` (line 50) `[4bcd58c7]`
- `PROCESS_ANIMATION` (line 36) `[3c712067]`
- `SAVE_CLIP` (line 34) `[5a489a75]`
- `URGENT` (line 52) `[80b6ea9c]`
- `cache_dir` (line 536) `[b75dc85e]`
- `cache_entry` (line 582) `[4a13261a]`
- `cache_file_path` (line 537) `[6f9f76e5]`
- `cache_stats` (line 837) `[9d769647]`
- `cache_string` (line 515) `[4f73bbcb]`
- `cached_path` (line 711) `[dcb1f50b]`
- `cleanup_worker` (line 430) `[72ba8443]`
- `cmd` (line 270) `[64b9508e]`
- `concat_file` (line 162) `[45457d53]`
- `data` (line 796) `[e60ed946]`
- `ffmpeg_temp_dir` (line 1047) `[c9234a33]`
- `file_path` (line 928) `[e87b6b63]`
- `file_size` (line 544) `[a6a86b1d]`
- `freed_bytes` (line 752) `[80cdbffd]`
- `index_file` (line 811) `[e720aa71]`
- `log_dir` (line 409) `[bd7691a2]`
- `output_filename` (line 632) `[e2227d5f]`
- `output_path` (line 633) `[2d77ddc1]`
- `param_str` (line 512) `[645d2f5e]`
- `processing_time` (line 259) `[ad77d75b]`
- `removed_count` (line 751) `[5a0d8775]`
- `result` (line 715) `[eb892fef]`
- `sorted_entries` (line 745) `[88c1c68b]`
- `start_time_op` (line 227) `[236c0791]`
- `stats_worker` (line 435) `[f51b343a]`
- `success` (line 951) `[4a30ddb9]`
- `task` (line 446) `[5bf8cb4b]`
- `task_id` (line 1009) `[68167057]`
- `task_worker` (line 425) `[547b2d25]`
- `temp_dir` (line 1046) `[72a93f81]`
- `temp_manager` (line 1061) `[7deb8f74]`
- `video_stream` (line 282) `[51107f11]`

---

### 📄 `video-transcribe.py`

#### Imports
- `json` (line 4) `[ff3e4d4d]`
- `moviepy.editor.VideoFileClip` (line 6) `[3951e41b]`
- `os` (line 3) `[de2abade]`
- `tempfile` (line 7) `[09d25239]`
- `whisper` (line 5) `[c35eef0b]`

#### Functions
- **`extract_audio_from_video(video_path)`** (lines 9-26) `[d39c6062]`
  - *Extract audio from video file and save it temporarily.*
  - *Called by:* transcribe_video
- **`main()`** (lines 85-124) `[1e11937b]`
  - *Calls:* transcribe_video
- **`transcribe_video(video_path)`** (lines 28-83) `[9a7df6d2]`
  - *Transcribe video and return word-level transcription.*
  - *Calls:* extract_audio_from_video
  - *Called by:* main

#### Variables
- `base_name` (line 102) `[e9d90157]`
- `end_time` (line 50) `[93a57be3]`
- `model` (line 36) `[196a3efe]`
- `output_path` (line 103) `[9142dc84]`
- `result` (line 39) `[e11c79af]`
- `start_time` (line 49) `[e8829afb]`
- `temp_audio_path` (line 32) `[027d0d70]`
- `text` (line 51) `[866b6360]`
- `time_per_word` (line 57) `[7ae9b7ed]`
- `transcription` (line 46) `[fd2d61ba]`
- `video` (line 12) `[389ee52f]`
- `video_path` (line 91) `[554c0d6d]`
- `word` (line 60) `[0607ff21]`
- `word_end` (line 63) `[71afa769]`
- `word_start` (line 62) `[e25b7488]`
- `words` (line 54) `[ced09822]`

---

## 🔗 Dependency Analysis

### Function Dependencies

**`add_file_to_database`** *(in batch_video_normalizer.py)*
- Called by: process_media_files

**`add_to_centralized_json`** *(in insta-download.py)*
- Calls: load_centralized_json, save_centralized_json
- Called by: process_downloaded_metadata

**`analyze_video_changes`** *(in image-video-encoder.py)*
- Called by: process_mixed_media_folder

**`apply_auto_levels`** *(in brightness_filters.py)*
- Calls: auto_levels_effect

**`apply_color_temperature`** *(in color_filters.py)*
- Calls: temperature_effect

**`apply_curves`** *(in brightness_filters.py)*
- Calls: curves_effect

**`apply_desaturate`** *(in color_filters.py)*
- Calls: desaturate_effect

**`apply_edge_detection`** *(in artistic_filters.py)*
- Calls: edge_effect

**`apply_emboss`** *(in artistic_filters.py)*
- Calls: emboss_effect

**`apply_exposure`** *(in brightness_filters.py)*
- Calls: exposure_effect

**`apply_film_grain`** *(in artistic_filters.py)*
- Calls: grain_effect

**`apply_filter`** *(in filter_registry.py)*
- Calls: get_filter_by_id

**`apply_gamma_correction`** *(in brightness_filters.py)*
- Calls: gamma_effect

**`apply_glow`** *(in artistic_filters.py)*
- Calls: glow_effect

**`apply_grayscale`** *(in color_filters.py)*
- Calls: blend_frames

**`apply_high_contrast`** *(in brightness_filters.py)*
- Calls: contrast_effect

**`apply_invert`** *(in color_filters.py)*
- Calls: invert_effect

**`apply_low_contrast`** *(in brightness_filters.py)*
- Calls: low_contrast_effect

**`apply_mosaic`** *(in artistic_filters.py)*
- Calls: mosaic_effect

**`apply_posterize`** *(in artistic_filters.py)*
- Calls: posterize_effect

**`apply_saturate`** *(in color_filters.py)*
- Calls: saturate_effect

**`apply_sepia`** *(in color_filters.py)*
- Calls: sepia_effect

**`apply_shadow_highlight`** *(in brightness_filters.py)*
- Calls: shadow_highlight_effect

**`apply_sharpen`** *(in artistic_filters.py)*
- Calls: sharpen_effect

**`apply_tint`** *(in color_filters.py)*
- Calls: tint_effect

**`apply_vignette`** *(in artistic_filters.py)*
- Calls: vignette_effect

**`apply_vintage_colors`** *(in color_filters.py)*
- Calls: vintage_effect

**`auto_levels_effect`** *(in brightness_filters.py)*
- Called by: apply_auto_levels

**`blend_frames`** *(in color_filters.py)*
- Called by: apply_grayscale

**`build_ffmpeg_command`** *(in easy-text-detection.py)*
- Calls: detect_video_type
- Called by: process_video

**`calculate_text_size`** *(in subtitle_video_processor.py)*
- Calls: wrap_text, wrap_text

**`check_executable`** *(in image-video-encoder.py)*
- Called by: process_mixed_media_folder, process_mixed_media_folder

**`check_ffmpeg`** *(in image-to-video.py)*
- Called by: main

**`check_gpu_support`** *(in batch_video_normalizer.py)*
- Called by: main

**`cleanup_memory`** *(in easy-text-detection.py)*
- Called by: main, process_video, main, process_video

**`cleanup_temp_files`** *(in detect-text.py)*
- Called by: main

**`combine_segments`** *(in detect-text.py)*
- Called by: main

**`combine_videos`** *(in image-video-encoder.py)*
- Calls: get_file_size_mb
- Called by: process_mixed_media_folder

**`contrast_effect`** *(in brightness_filters.py)*
- Called by: apply_high_contrast

**`convert_image_to_video`** *(in image-video-encoder.py)*
- Called by: process_mixed_media_folder

**`create_consolidated_file`** *(in extract-code.py)*
- Calls: is_coding_file, should_ignore_path, scan_directory, read_file_content, should_ignore_path
- Called by: main

**`create_good_segments`** *(in detect-text.py)*
- Called by: main

**`create_parser`** *(in arg_parser.py)*
- Called by: parse_arguments

**`create_split_screen_video`** *(in split_screen_processor.py)*
- Calls: get_fit_mode, get_fit_mode, get_audio_preferences

**`curves_effect`** *(in brightness_filters.py)*
- Called by: apply_curves

**`decorator`** *(in filter_registry.py)*
- Calls: validate_filter_metadata, validate_filter_function

**`desaturate_effect`** *(in color_filters.py)*
- Called by: apply_desaturate

**`detect_high_contrast_text`** *(in detect-text.py)*
- Called by: detect_overlay_text

**`detect_overlay_text`** *(in detect-text.py)*
- Calls: detect_high_contrast_text, detect_stroke_text, detect_uniform_text_blocks
- Called by: main

**`detect_stroke_text`** *(in detect-text.py)*
- Called by: detect_overlay_text

**`detect_uniform_text_blocks`** *(in detect-text.py)*
- Called by: detect_overlay_text

**`detect_video_type`** *(in easy-text-detection.py)*
- Called by: build_ffmpeg_command, process_video

**`detect_vocal_changes`** *(in vocal_processor.py)*
- Calls: smooth_signal

**`download_pinterest_with_gallery_dl`** *(in pinterest-download.py)*
- Calls: extract_search_terms_from_url, check_executable
- Called by: main

**`download_reels_with_gallery_dl`** *(in insta-download.py)*
- Calls: extract_profile_name_from_url, check_executable
- Called by: main

**`edge_effect`** *(in artistic_filters.py)*
- Called by: apply_edge_detection

**`emboss_effect`** *(in artistic_filters.py)*
- Called by: apply_emboss

**`estimate_processing_time`** *(in multiple_image_processor.py)*
- Calls: get_image_count

**`exec_db`** *(in easy-text-detection.py)*
- Calls: print

**`expand_buffer`** *(in easy-text-detection.py)*
- Called by: process_video

**`exposure_effect`** *(in brightness_filters.py)*
- Called by: apply_exposure

**`extract_audio_ffmpeg`** *(in file-processor.py)*
- Calls: check_executable
- Called by: main

**`extract_audio_from_video`** *(in video-transcribe.py)*
- Called by: transcribe_video

**`extract_profile_name_from_url`** *(in insta-download.py)*
- Called by: download_reels_with_gallery_dl

**`extract_search_terms_from_url`** *(in pinterest-download.py)*
- Called by: download_pinterest_with_gallery_dl

**`extract_segments`** *(in detect-text.py)*
- Called by: main

**`find_all_media_files`** *(in batch_video_normalizer.py)*
- Called by: process_media_files

**`find_media_files`** *(in image-video-encoder.py)*
- Called by: process_mixed_media_folder

**`format_time`** *(in easy-text-detection.py)*
- Called by: process_video, process_video, process_video

**`frames_to_intervals`** *(in easy-text-detection.py)*
- Called by: process_video

**`gamma_effect`** *(in brightness_filters.py)*
- Called by: apply_gamma_correction

**`get_additional_media_configuration`** *(in main.py)*
- Called by: get_video_generation_inputs

**`get_audio_preferences`** *(in split_screen_processor.py)*
- Called by: create_split_screen_video

**`get_custom_filters`** *(in main.py)*
- Called by: get_filter_configuration

**`get_file_size_mb`** *(in image-video-encoder.py)*
- Called by: combine_videos, process_mixed_media_folder, process_mixed_media_folder, process_mixed_media_folder, process_mixed_media_folder

**`get_file_status`** *(in batch_video_normalizer.py)*
- Called by: process_media_files

**`get_filter_by_id`** *(in filter_registry.py)*
- Called by: apply_filter

**`get_filter_configuration`** *(in main.py)*
- Calls: get_preset_filters, get_custom_filters
- Called by: get_video_generation_inputs

**`get_filters_by_category`** *(in filter_registry.py)*
- Called by: list_available_filters, get_registry_stats

**`get_fit_mode`** *(in split_screen_processor.py)*
- Called by: create_split_screen_video, create_split_screen_video

**`get_format_presets`** *(in image-video-encoder.py)*
- Called by: main

**`get_image_count`** *(in multiple_image_processor.py)*
- Called by: estimate_processing_time

**`get_memory_usage`** *(in easy-text-detection.py)*
- Called by: process_video, process_video, main, main, process_video

**`get_preset_filters`** *(in main.py)*
- Called by: get_filter_configuration

**`get_processing_statistics`** *(in batch_video_normalizer.py)*
- Called by: process_media_files, process_media_files, main

**`get_record_from_db`** *(in file-processor.py)*
- Called by: main

**`get_registry_stats`** *(in filter_registry.py)*
- Calls: get_filters_by_category

**`get_user_inputs`** *(in main.py)*
- Calls: get_video_generation_inputs, handle_subtitles, handle_canvas, handle_formatting, handle_split_screen, handle_combine_videos, get_user_inputs
- Called by: main, get_user_inputs

**`get_video_generation_inputs`** *(in main.py)*
- Calls: get_filter_configuration, get_additional_media_configuration
- Called by: get_user_inputs

**`get_video_info`** *(in easy-text-detection.py)*
- Calls: print
- Called by: main

**`glow_effect`** *(in artistic_filters.py)*
- Called by: apply_glow

**`grain_effect`** *(in artistic_filters.py)*
- Called by: apply_film_grain

**`group_consecutive_frames`** *(in detect-text.py)*
- Called by: main

**`handle_canvas`** *(in main.py)*
- Called by: get_user_inputs

**`handle_combine_videos`** *(in main.py)*
- Called by: get_user_inputs

**`handle_formatting`** *(in main.py)*
- Called by: get_user_inputs

**`handle_split_screen`** *(in main.py)*
- Called by: get_user_inputs

**`handle_subtitles`** *(in main.py)*
- Called by: get_user_inputs

**`init_database`** *(in batch_video_normalizer.py)*
- Called by: process_media_files

**`init_processing_db`** *(in file-processor.py)*
- Called by: main

**`init_sqlite_db`** *(in insta-download.py)*
- Called by: main

**`insert_pinterest_metadata_sqlite`** *(in pinterest-download.py)*
- Called by: process_pinterest_metadata

**`insert_reel_metadata_sqlite`** *(in insta-download.py)*
- Called by: process_downloaded_metadata

**`invert_effect`** *(in color_filters.py)*
- Called by: apply_invert

**`is_coding_file`** *(in extract-code.py)*
- Called by: scan_directory, create_consolidated_file

**`list_available_filters`** *(in filter_registry.py)*
- Calls: get_filters_by_category

**`load_centralized_json`** *(in insta-download.py)*
- Called by: add_to_centralized_json

**`load_json_file`** *(in file-processor.py)*
- Called by: main, main, main

**`log_processing_message`** *(in batch_video_normalizer.py)*
- Called by: process_media_files, process_media_files, process_media_files

**`low_contrast_effect`** *(in brightness_filters.py)*
- Called by: apply_low_contrast

**`main`** *(in detect-text.py)*
- Calls: detect_overlay_text, group_consecutive_frames, create_good_segments, extract_segments, combine_segments, cleanup_temp_files

**`merge_intervals`** *(in easy-text-detection.py)*
- Called by: process_video

**`mosaic_effect`** *(in artistic_filters.py)*
- Called by: apply_mosaic

**`normalize_video`** *(in image-video-encoder.py)*
- Called by: process_mixed_media_folder

**`parse_arguments`** *(in arg_parser.py)*
- Calls: create_parser, validate_args

**`posterize_effect`** *(in artistic_filters.py)*
- Called by: apply_posterize

**`preprocess_frame`** *(in easy-text-detection.py)*
- Called by: process_video

**`print`** *(in easy-text-detection.py)*
- Calls: print
- Called by: main, main, main, main, main, main, main, print, test_ffmpeg_command, test_ffmpeg_command, process_video, process_video, process_video, process_video, process_video, process_video, process_video, process_video, process_video, process_video, process_video, process_video, main, main, main, get_video_info, test_ffmpeg_command, test_ffmpeg_command, test_ffmpeg_command, process_video, process_video, process_video, process_video, process_video, process_video, process_video, process_video, main, exec_db, process_video, process_video, process_video, process_video, process_video, process_video

**`process_downloaded_metadata`** *(in insta-download.py)*
- Calls: insert_reel_metadata_sqlite, add_to_centralized_json
- Called by: main

**`process_media_files`** *(in batch_video_normalizer.py)*
- Calls: find_all_media_files, get_processing_statistics, get_processing_statistics, init_database, get_file_size_mb, add_file_to_database, get_file_status, update_file_status, log_processing_message, get_file_size_mb, get_video_info, analyze_video_changes, normalize_video, get_file_size_mb, update_file_status, log_processing_message, update_file_status, update_file_status, log_processing_message, update_file_status, convert_image_to_video
- Called by: main

**`process_mixed_media_folder`** *(in image-video-encoder.py)*
- Calls: find_media_files, check_executable, check_executable, get_file_size_mb, get_video_info, analyze_video_changes, get_file_size_mb, normalize_video, convert_image_to_video, combine_videos, get_file_size_mb, get_file_size_mb
- Called by: main

**`process_pinterest_metadata`** *(in pinterest-download.py)*
- Calls: insert_pinterest_metadata_sqlite, add_to_centralized_json
- Called by: main

**`process_video`** *(in easy-text-detection.py)*
- Calls: get_memory_usage, print, print, print, detect_video_type, print, print, print, print, print, print, build_ffmpeg_command, test_ffmpeg_command, print, print, cleanup_memory, get_memory_usage, print, print, expand_buffer, print, print, print, frames_to_intervals, merge_intervals, print, print, print, print, cleanup_memory, print, print, print, print, format_time, get_memory_usage, preprocess_frame, print, print, format_time, format_time
- Called by: main

**`read_file_content`** *(in extract-code.py)*
- Called by: create_consolidated_file

**`reencode_all_videos`** *(in insta-download.py)*
- Calls: reencode_video_with_ffmpeg, update_reencoded_status
- Called by: main

**`reencode_video_ffmpeg`** *(in file-processor.py)*
- Calls: check_executable
- Called by: main

**`reencode_video_with_ffmpeg`** *(in insta-download.py)*
- Calls: check_executable
- Called by: reencode_all_videos

**`register_filter`** *(in filter_registry.py)*
- Calls: validate_filter_metadata, validate_filter_function

**`saturate_effect`** *(in color_filters.py)*
- Called by: apply_saturate

**`save_centralized_json`** *(in insta-download.py)*
- Called by: add_to_centralized_json

**`save_json_file`** *(in file-processor.py)*
- Called by: main, main, main

**`scan_directory`** *(in extract-code.py)*
- Calls: should_ignore_path, is_coding_file, scan_directory
- Called by: create_consolidated_file, scan_directory

**`sepia_effect`** *(in color_filters.py)*
- Called by: apply_sepia

**`shadow_highlight_effect`** *(in brightness_filters.py)*
- Called by: apply_shadow_highlight

**`sharpen_effect`** *(in artistic_filters.py)*
- Called by: apply_sharpen

**`should_ignore_path`** *(in extract-code.py)*
- Called by: scan_directory, create_consolidated_file, create_consolidated_file

**`smooth_signal`** *(in vocal_processor.py)*
- Called by: detect_vocal_changes

**`temperature_effect`** *(in color_filters.py)*
- Called by: apply_color_temperature

**`test_ffmpeg_command`** *(in easy-text-detection.py)*
- Calls: print, print, print, print, print
- Called by: process_video

**`tint_effect`** *(in color_filters.py)*
- Called by: apply_tint

**`transcribe_video`** *(in video-transcribe.py)*
- Calls: extract_audio_from_video
- Called by: main

**`update_file_status`** *(in batch_video_normalizer.py)*
- Called by: process_media_files, process_media_files, process_media_files, process_media_files, process_media_files

**`update_or_insert_processed_reel_sqlite`** *(in file-processor.py)*
- Called by: main, main

**`update_reencoded_status`** *(in insta-download.py)*
- Called by: reencode_all_videos

**`validate_args`** *(in arg_parser.py)*
- Called by: parse_arguments

**`validate_filter_function`** *(in filter_registry.py)*
- Called by: register_filter, decorator

**`validate_filter_metadata`** *(in filter_registry.py)*
- Called by: register_filter, decorator

**`vignette_effect`** *(in artistic_filters.py)*
- Called by: apply_vignette

**`vintage_effect`** *(in color_filters.py)*
- Called by: apply_vintage_colors

**`wrap_text`** *(in subtitle_video_processor.py)*
- Called by: calculate_text_size, calculate_text_size

### Class Dependencies

**`AnalysisType`** *(in audio_processor.py)*
- Inherits from: Enum

**`AnimationType`** *(in multiple_image_processor.py)*
- Inherits from: Enum

**`CachePolicy`** *(in cache_manager.py)*
- Inherits from: Enum

**`CacheStatus`** *(in cache_manager.py)*
- Inherits from: Enum

**`CompressionLevel`** *(in io_operations.py)*
- Inherits from: Enum

**`ContentType`** *(in video_generator.py)*
- Inherits from: Enum

**`FileOperation`** *(in io_operations.py)*
- Inherits from: Enum

**`FilterRegistrationError`** *(in filter_registry.py)*
- Inherits from: Exception

**`FilterValidationError`** *(in filter_registry.py)*
- Inherits from: Exception

**`MediaType`** *(in mixed_media_processor.py)*
- Inherits from: Enum

**`ProcessingPhase`** *(in mixed_media_processor.py)*
- Inherits from: Enum

**`QueueType`** *(in queue_manager.py)*
- Inherits from: Enum

**`SoundCategory`** *(in sound_effects_processor.py)*
- Inherits from: Enum

**`SpeedPatternType`** *(in video_processor.py)*
- Inherits from: Enum

**`TaskPriority`** *(in queue_manager.py)*
- Inherits from: Enum

**`TaskStatus`** *(in queue_manager.py)*
- Inherits from: Enum

**`TaskType`** *(in temp_file_manager.py)*
- Inherits from: Enum

**`TransitionType`** *(in multiple_image_processor.py)*
- Inherits from: Enum

## 🔐 Hash Reference

*Use these hashes to track changes between analyses*

| Entity | Type | File | Hash |
|--------|------|------|------|
| `ACCELERATING` | variable | video_processor.py | `84b2d61aff6c` |
| `ACTIVE` | variable | cache_manager.py | `04dff8e01e02` |
| `ADAPTIVE` | variable | cache_manager.py | `913d88ad68ad` |
| `AMBIENT` | variable | sound_effects_processor.py | `2b936c245e25` |
| `ANALYSIS` | variable | mixed_media_processor.py | `9c3000e8445d` |
| `ANALYSIS` | variable | video_processor.py | `e2ef37819366` |
| `APPEND` | variable | io_operations.py | `fd6d35e902b2` |
| `APPLY_FILTER` | variable | temp_file_manager.py | `2f02bf5f1595` |
| `AUDIO_ANALYSIS` | variable | video_generator.py | `943a4b5d8687` |
| `AnalysisType` | class | audio_processor.py | `c5a3609bd9f4` |
| `AnimationType` | class | multiple_image_processor.py | `968774c2fe6c` |
| `AudioAnalysisResult` | class | audio_processor.py | `5f3fb8e7d5b1` |
| `AudioExtractor` | class | extract-audio.py | `8d57b4021d80` |
| `AudioProcessor` | class | audio_processor.py | `56ff200b2ce8` |
| `BALANCED` | variable | io_operations.py | `34444cbc5dc2` |
| `BATCH` | variable | queue_manager.py | `1d00181cbe3e` |
| `BATCH_PROCESSING` | variable | video_processor.py | `6f6d1d4bda08` |
| `BEATS` | variable | audio_processor.py | `c3dc41917084` |
| `BEAT_SYNC` | variable | video_processor.py | `0c3f34889291` |
| `BEST` | variable | io_operations.py | `88be1058b8b0` |
| `BOUNCE_IN` | variable | multiple_image_processor.py | `6c2bde931ad7` |
| `BUFFER_FRAMES` | variable | easy-text-detection.py | `33c56ebbea2f` |
| `CANCELLED` | variable | queue_manager.py | `26b6eee180eb` |
| `CLEANUP` | variable | mixed_media_processor.py | `88776fcfb331` |
| `CLEANUP` | variable | temp_file_manager.py | `1ef9cb8b0ee6` |
| `COMBINATION` | variable | mixed_media_processor.py | `7545c8791223` |
| `COMPLETED` | variable | queue_manager.py | `fa44ba66e80a` |
| `COMPOSITE_VIDEO` | variable | temp_file_manager.py | `4e1905624e89` |
| `COMPRESS` | variable | io_operations.py | `ee68ea14efe4` |
| `COMPRESS` | variable | temp_file_manager.py | `bb418cdd61f8` |
| `CONCATENATION` | variable | video_processor.py | `cd6477697f3f` |
| `CONSTANT` | variable | video_processor.py | `9ff6cee41e80` |
| `CONTENT_ANALYSIS` | variable | video_generator.py | `96b34ac94fc0` |
| `CRITICAL` | variable | queue_manager.py | `cefa4a73d42a` |
| `CROSSFADE` | variable | multiple_image_processor.py | `1bea9800bc06` |
| `CUT` | variable | multiple_image_processor.py | `62a0f15e7b49` |
| `CacheEntry` | class | cache_manager.py | `9d5bf1336a2b` |
| `CacheEntry` | class | temp_file_manager.py | `f73d1ade580f` |
| `CacheManager` | class | cache_manager.py | `799ffed91731` |
| `CachePolicy` | class | cache_manager.py | `f812b2940b19` |
| `CacheStats` | class | cache_manager.py | `fb8b81654cfd` |
| `CacheStatus` | class | cache_manager.py | `5f348f630b30` |
| `CanvasProcessor` | class | canvas_processor.py | `2816ec93f784` |
| `CanvasResult` | class | canvas_processor.py | `7d95e41ab320` |
| `CompressionLevel` | class | io_operations.py | `58b5ae23c45b` |
| `ContentInfo` | class | video_generator.py | `f466ecc7f18f` |
| `ContentType` | class | video_generator.py | `bafe748f2ebd` |
| `DB_FILE` | variable | easy-text-detection.py | `3f6e61de6485` |
| `DECELERATING` | variable | video_processor.py | `293453cdd680` |
| `DECOMPRESS` | variable | io_operations.py | `a18d6d39c3d0` |
| `DECOMPRESS` | variable | temp_file_manager.py | `71fd35b3f499` |
| `DELETE` | variable | io_operations.py | `1ca886f327ac` |
| `DELETION_THRESHOLD` | variable | easy-text-detection.py | `fa36b412663b` |
| `DETECTION_SCALE` | variable | easy-text-detection.py | `909570e9d5d3` |
| `DISSOLVE` | variable | multiple_image_processor.py | `bedd6bc977a0` |
| `DROP_DOWN` | variable | multiple_image_processor.py | `29c62d6ddbf6` |
| `DiskSpaceInfo` | class | io_operations.py | `6da5df51e38d` |
| `ERROR` | variable | cache_manager.py | `05914a124845` |
| `EVICTED` | variable | cache_manager.py | `55f84ecfb933` |
| `EXPIRED` | variable | cache_manager.py | `632d10bee4f0` |
| `FADE` | variable | multiple_image_processor.py | `895be3f3b3d5` |
| `FADE_IN` | variable | multiple_image_processor.py | `280fb9afecf4` |
| `FAILED` | variable | queue_manager.py | `12f27b207c6f` |
| `FAST` | variable | io_operations.py | `4fdc6a9bcc95` |
| `FFMPEG_CONCAT` | variable | temp_file_manager.py | `5ddbbf8199e6` |
| `FFMPEG_EXTRACT` | variable | temp_file_manager.py | `1071a01b9869` |
| `FFMPEG_FILTER` | variable | temp_file_manager.py | `577327651f20` |
| `FFMPEG_SETTINGS` | variable | easy-text-detection.py | `5b7006bf5172` |
| `FFmpegCanvasProcessor` | class | canvas_processor.py | `4d41ef508c5a` |
| `FFmpegImageProcessor` | class | image_processor.py | `b6e89b4497cc` |
| `FFmpegMultiImageProcessor` | class | multiple_image_processor.py | `dca98e93b247` |
| `FFmpegProcessor` | class | temp_file_manager.py | `a14437d63795` |
| `FFmpegProcessor` | class | video_processor.py | `86c63f90f06d` |
| `FFmpegResult` | class | temp_file_manager.py | `a3ae7c412cb4` |
| `FFmpegUtils` | class | main.py | `1efab01fbaa4` |
| `FFmpegVideoAnalyzer` | class | video_generator.py | `14f645cd08a1` |
| `FINALIZATION` | variable | video_generator.py | `a7186d114c4c` |
| `FINALIZATION` | variable | video_processor.py | `a8640892647f` |
| `FRAME_SKIP` | variable | easy-text-detection.py | `9bddee1fd166` |
| `FileMetadata` | class | io_operations.py | `c14406ff661d` |
| `FileOperation` | class | io_operations.py | `da99b2037590` |
| `FilterRegistrationError` | class | filter_registry.py | `1aae40f9588a` |
| `FilterValidationError` | class | filter_registry.py | `3e2a7073afc4` |
| `GenerationSession` | class | video_generator.py | `89bc72c95a52` |
| `HARMONIC_PERCUSSIVE` | variable | audio_processor.py | `538bc0a0d095` |
| `HIGH` | variable | queue_manager.py | `f55b9cfbfd3a` |
| `HIGH` | variable | temp_file_manager.py | `2887e9782c01` |
| `IMAGE` | variable | mixed_media_processor.py | `02cc141ebf8d` |
| `IMAGE` | variable | video_generator.py | `4f6475f87c05` |
| `IMAGE_CONVERSION` | variable | mixed_media_processor.py | `7a292874a574` |
| `IMAGE_FOLDER` | variable | video_generator.py | `6c688411b6d0` |
| `IMPACTS` | variable | sound_effects_processor.py | `9694f205eddf` |
| `INITIALIZATION` | variable | video_generator.py | `344277ac1785` |
| `INITIALIZATION` | variable | video_processor.py | `894a6fbb220c` |
| `IOOperations` | class | io_operations.py | `71fff7b173ac` |
| `ImageProcessingResult` | class | image_processor.py | `e36b0b076428` |
| `ImageProcessingResult` | class | multiple_image_processor.py | `b7a76784c5dc` |
| `ImageSegment` | class | image_processor.py | `65969d134f9f` |
| `ImageSegmentInfo` | class | multiple_image_processor.py | `1ac388063d84` |
| `ImageVideoProcessor` | class | image-to-video.py | `d9bce994a3df` |
| `KEN_BURNS` | variable | multiple_image_processor.py | `bd81b1dbdba6` |
| `LFU` | variable | cache_manager.py | `842162293d8d` |
| `LOADING` | variable | cache_manager.py | `d251a0cbba37` |
| `LOAD_CLIP` | variable | temp_file_manager.py | `0f5fd8bcc173` |
| `LOW` | variable | queue_manager.py | `0a6ecbfe23a8` |
| `LOW` | variable | temp_file_manager.py | `344a2f620a57` |
| `LRU` | variable | cache_manager.py | `181e12ecd236` |
| `Logger` | class | easy-text-detection.py | `424559d9706a` |
| `MAGIC` | variable | sound_effects_processor.py | `5a218a8ac8d1` |
| `MAIN_PROCESSING` | variable | video_generator.py | `a4cd8edbcc37` |
| `MEDIA_ADDITION` | variable | video_generator.py | `f35f5f25b8fe` |
| `MIXED_MEDIA` | variable | video_generator.py | `0b422d440faa` |
| `MarkdownToAudioConverter` | class | convert-audio-file.py | `f3782973ee35` |
| `MediaFile` | class | mixed_media_processor.py | `763933450c6e` |
| `MediaType` | class | mixed_media_processor.py | `ad0616436c13` |
| `MixedMediaProcessor` | class | mixed_media_processor.py | `90cda6391495` |
| `MultipleImageProcessor` | class | multiple_image_processor.py | `2d2f8c81bdee` |
| `NORMAL` | variable | queue_manager.py | `46c9225c5d43` |
| `NORMAL` | variable | temp_file_manager.py | `4bcd58c71a42` |
| `ONSET_STRENGTH` | variable | audio_processor.py | `8b3e44d264dc` |
| `PENDING` | variable | queue_manager.py | `e2c2ba685dba` |
| `PIL.Image` | import | canvas_processor.py | `4f84112b888e` |
| `PIL.Image` | import | image-to-video.py | `4f84112b888e` |
| `PIL.Image` | import | image_processor.py | `4f84112b888e` |
| `PIL.Image` | import | multiple_image_processor.py | `4f84112b888e` |
| `PIL.ImageDraw` | import | canvas_processor.py | `c28315682ac5` |
| `PIL.ImageEnhance` | import | image_processor.py | `6d408e85d5bd` |
| `PIL.ImageEnhance` | import | multiple_image_processor.py | `6d408e85d5bd` |
| `PIL.ImageFont` | import | canvas_processor.py | `0b3f967150c4` |
| `PIL.ImageOps` | import | image_processor.py | `960ee6fea7ae` |
| `PIL.ImageOps` | import | multiple_image_processor.py | `960ee6fea7ae` |
| `POPS` | variable | sound_effects_processor.py | `bd43278bc0ed` |
| `PROCESS_ANIMATION` | variable | temp_file_manager.py | `3c712067821c` |
| `PROCESS_POOL` | variable | queue_manager.py | `8a3d61eb35e0` |
| `ProcessingPhase` | class | mixed_media_processor.py | `fb2f16310fed` |
| `ProcessingPhase` | class | video_generator.py | `d11ffdf0a562` |
| `ProcessingPhase` | class | video_processor.py | `d24f7b883bad` |
| `ProcessingSession` | class | mixed_media_processor.py | `3f0752959ca9` |
| `ProcessingSession` | class | multiple_image_processor.py | `41e05dab32b6` |
| `ProcessingSession` | class | video_processor.py | `fc005e6d865a` |
| `QueueManager` | class | queue_manager.py | `525f744976e0` |
| `QueueStats` | class | queue_manager.py | `24b8dc48945a` |
| `QueueType` | class | queue_manager.py | `e06625c4a679` |
| `RANDOM` | variable | cache_manager.py | `6ea5d18af11e` |
| `RANDOM` | variable | video_processor.py | `8e918286e30e` |
| `READ` | variable | io_operations.py | `0e838014986a` |
| `RETRYING` | variable | queue_manager.py | `f1109f964275` |
| `RUNNING` | variable | queue_manager.py | `56c38af7fcd5` |
| `SAVE_CLIP` | variable | temp_file_manager.py | `5a489a75369f` |
| `SCALE_IN` | variable | multiple_image_processor.py | `9c12e70017c4` |
| `SEGMENTATION` | variable | video_processor.py | `27c63edf820d` |
| `SEQUENTIAL` | variable | queue_manager.py | `2e1de3464195` |
| `SLIDE` | variable | multiple_image_processor.py | `6ed0319ec664` |
| `SLIDE_IN_BOTTOM` | variable | multiple_image_processor.py | `fadada9db425` |
| `SLIDE_IN_LEFT` | variable | multiple_image_processor.py | `c98654d2a756` |
| `SLIDE_IN_RIGHT` | variable | multiple_image_processor.py | `605937e5e6d0` |
| `SLIDE_IN_TOP` | variable | multiple_image_processor.py | `345659769c73` |
| `SOCIAL_RATIOS` | variable | easy-text-detection.py | `f5c6a49e678c` |
| `SPECTRAL_FEATURES` | variable | audio_processor.py | `a5d9c13c1d10` |
| `SequentialTimingCalculator` | class | sequential_timing.py | `c7819977c07e` |
| `SingleImageProcessor` | class | image_processor.py | `69d2ec8afb5c` |
| `SoundCategory` | class | sound_effects_processor.py | `3bf9a6c5042f` |
| `SoundEffectsProcessor` | class | sound_effects_processor.py | `5cdd906dd19f` |
| `SpeedPatternType` | class | video_processor.py | `8b67b571c3f8` |
| `SplitScreenProcessor` | class | split_screen_processor.py | `bd060cbc06b5` |
| `SubtitleDesignManager` | class | subtitle_design_manager.py | `9f9abf180f1b` |
| `SubtitleProcessor` | class | subtitle_processor.py | `179c3d737072` |
| `SubtitleVideoProcessor` | class | subtitle_video_processor.py | `bfd0fb812dd7` |
| `TEMPO` | variable | audio_processor.py | `aee4463bafc1` |
| `THREAD_POOL` | variable | queue_manager.py | `27c9233373ca` |
| `TIMEOUT` | variable | queue_manager.py | `8fbfe778ab48` |
| `TTL` | variable | cache_manager.py | `de0ed83a1a0b` |
| `Task` | class | queue_manager.py | `702b2a8af5bf` |
| `Task` | class | temp_file_manager.py | `953ad5542b55` |
| `TaskPriority` | class | queue_manager.py | `de33205c3fb2` |
| `TaskPriority` | class | temp_file_manager.py | `58a3c1672de0` |
| `TaskQueue` | class | queue_manager.py | `11d5503b76f2` |
| `TaskResult` | class | queue_manager.py | `2a14ae412bf9` |
| `TaskStatus` | class | queue_manager.py | `33d7f58a92d8` |
| `TaskType` | class | temp_file_manager.py | `f32404f27e29` |
| `TempFileManager` | class | temp_file_manager.py | `965a352bba95` |
| `TextOverlay` | class | canvas_processor.py | `8018fc3e64e6` |
| `TransitionType` | class | multiple_image_processor.py | `49941a217c20` |
| `UNKNOWN` | variable | mixed_media_processor.py | `2317ba356f88` |
| `UNKNOWN` | variable | video_generator.py | `e6f7d5fc8ef4` |
| `URGENT` | variable | queue_manager.py | `2c4547e97a6f` |
| `URGENT` | variable | temp_file_manager.py | `80b6ea9c0cd7` |
| `VIDEO` | variable | mixed_media_processor.py | `35edef0feda3` |
| `VIDEO` | variable | video_generator.py | `2ffb98785d3c` |
| `VIDEO_EXTENSIONS` | variable | easy-text-detection.py | `eadc9b0c6db1` |
| `VIDEO_FOLDER` | variable | video_generator.py | `127734d4ebd3` |
| `VIDEO_NORMALIZATION` | variable | mixed_media_processor.py | `245e0628322c` |
| `VOCAL_CHANGES` | variable | audio_processor.py | `68bb4ef1ecd7` |
| `VideoFilterProcessor` | class | video_filter_processor.py | `0ccd5a89f944` |
| `VideoFormatter` | class | video_formatter.py | `00290f0d0ca5` |
| `VideoGenerator` | class | video_generator.py | `386c12e9b2de` |
| `VideoGroupCombiner` | class | combine-video.py | `54314f52aefc` |
| `VideoInfo` | class | video_processor.py | `1b3a3e9f226b` |
| `VideoProcessingManager` | class | main.py | `d2014dccda5a` |
| `VideoProcessor` | class | combine_video.py | `908521036a4c` |
| `VideoProcessor` | class | video_processor.py | `a5ff046d08eb` |
| `VideoSegment` | class | video_processor.py | `78383098b37b` |
| `WHOOSHES` | variable | sound_effects_processor.py | `ce0290836100` |
| `WIPE` | variable | multiple_image_processor.py | `12d391e7174b` |
| `WIPE_LEFT` | variable | multiple_image_processor.py | `a9fa06a82900` |
| `WIPE_RIGHT` | variable | multiple_image_processor.py | `5313343498c6` |
| `WRITE` | variable | io_operations.py | `0f490dfb1046` |
| `ZOOM` | variable | multiple_image_processor.py | `70c792efe8c2` |
| `ZOOM_IN` | variable | multiple_image_processor.py | `f056f57e422e` |
| `__all__` | variable | __init__.py | `12d0ea8e8d94` |
| `__all__` | variable | __init__.py | `df8bea70a14f` |
| `__all__` | variable | __init__.py | `fbbedf7dcb0e` |
| `__all__` | variable | file_handler.py | `0a49ab725c85` |
| `__author__` | variable | __init__.py | `d1e41172bff6` |
| `__description__` | variable | __init__.py | `284c7ac6f645` |
| `__init__` | function | audio_processor.py | `d23bce897790` |
| `__init__` | function | cache_manager.py | `8e7dd0b1281f` |
| `__init__` | function | canvas_processor.py | `f17e3012af0d` |
| `__init__` | function | combine-video.py | `48cbc42ba31e` |
| `__init__` | function | combine_video.py | `9d766d73aa0f` |
| `__init__` | function | convert-audio-file.py | `7bf516d79a0f` |
| `__init__` | function | easy-text-detection.py | `2b4e2e27d2c1` |
| `__init__` | function | extract-audio.py | `ec3f0f1eaf03` |
| `__init__` | function | image-to-video.py | `449613914c07` |
| `__init__` | function | image_processor.py | `0ff98b3f981d` |
| `__init__` | function | io_operations.py | `b9809cf75dbb` |
| `__init__` | function | main.py | `6fce9d336176` |
| `__init__` | function | mixed_media_processor.py | `559a3c9fce9f` |
| `__init__` | function | multiple_image_processor.py | `5fdebe768f1b` |
| `__init__` | function | queue_manager.py | `c47b89697aca` |
| `__init__` | function | sequential_timing.py | `8b2be876c7ef` |
| `__init__` | function | sound_effects_processor.py | `7a6fdfe5efa0` |
| `__init__` | function | split_screen_processor.py | `5cea7d4c2ef8` |
| `__init__` | function | subtitle_design_manager.py | `7dffc1e61fd3` |
| `__init__` | function | subtitle_processor.py | `ce7d64fb6b3c` |
| `__init__` | function | subtitle_video_processor.py | `43c9b7155513` |
| `__init__` | function | temp_file_manager.py | `fc49315f1f65` |
| `__init__` | function | video_filter_processor.py | `f1eca0cd2cde` |
| `__init__` | function | video_formatter.py | `70acae9f5323` |
| `__init__` | function | video_generator.py | `bfe2328a9510` |
| `__init__` | function | video_processor.py | `1541f3197725` |
| `__lt__` | function | queue_manager.py | `88699b394fcc` |
| `__post_init__` | function | cache_manager.py | `5e0b5896144a` |
| `__post_init__` | function | queue_manager.py | `054e5a3ca496` |
| `__post_init__` | function | temp_file_manager.py | `bea45d1654f6` |
| `__version__` | variable | __init__.py | `e4e3db4d21af` |
| `_add_to_policy_structures` | function | cache_manager.py | `4f8b1dcda39e` |
| `_cache_cleanup_worker` | function | temp_file_manager.py | `30f29f49e8b1` |
| `_cache_segment_path` | function | video_processor.py | `8bf9dc84d8cf` |
| `_calculate_checksum` | function | io_operations.py | `7aada5058eea` |
| `_can_execute_now` | function | queue_manager.py | `ed5c08fecddb` |
| `_check_dependent_tasks` | function | queue_manager.py | `522bad87f2d0` |
| `_check_ffmpeg` | function | mixed_media_processor.py | `1e126c9d13a2` |
| `_cleanup_cache` | function | temp_file_manager.py | `a4e350952a75` |
| `_cleanup_old_tasks` | function | queue_manager.py | `be388604d382` |
| `_cleanup_temp_segments` | function | video_processor.py | `456558d7dde7` |
| `_convert_color_to_ffmpeg` | function | canvas_processor.py | `1fbfe4ae30d6` |
| `_convert_color_to_hex` | function | canvas_processor.py | `6fc48e593eeb` |
| `_create_default_queues` | function | queue_manager.py | `142b9f03b3ed` |
| `_create_text_overlays` | function | canvas_processor.py | `1e14298db1f5` |
| `_crop_video` | function | split_screen_processor.py | `cc8bf217a715` |
| `_crop_video` | function | video_formatter.py | `111ad8700218` |
| `_ensure_space` | function | cache_manager.py | `7d9e5b4a0be2` |
| `_estimate_size` | function | cache_manager.py | `6ac8b7e0b102` |
| `_evict_adaptive` | function | cache_manager.py | `0bbfbb0d375f` |
| `_evict_entries` | function | cache_manager.py | `3ea2979eee30` |
| `_evict_lfu` | function | cache_manager.py | `3dd80fa79385` |
| `_evict_lru` | function | cache_manager.py | `4b847d87756c` |
| `_evict_random` | function | cache_manager.py | `9fd687687572` |
| `_evict_ttl` | function | cache_manager.py | `5e68f28743d9` |
| `_expire_entries` | function | cache_manager.py | `10206addc0ee` |
| `_file_lock` | function | io_operations.py | `17325618bf70` |
| `_fit_video` | function | split_screen_processor.py | `0d2cd1906800` |
| `_fit_video` | function | video_formatter.py | `7cebb096c73d` |
| `_get_box_color_preference` | function | subtitle_design_manager.py | `27bb0bdb7c7a` |
| `_get_box_opacity_preference` | function | subtitle_design_manager.py | `f49bc83929e8` |
| `_get_box_preference` | function | subtitle_design_manager.py | `392f2feeddd1` |
| `_get_cached_segment_path` | function | video_processor.py | `3fe3dcd8455e` |
| `_get_color_scheme_preference` | function | subtitle_design_manager.py | `62c5dd5c7d89` |
| `_get_file_lock` | function | io_operations.py | `1a1dfc9b39b8` |
| `_get_position_preference` | function | subtitle_design_manager.py | `013eb48e3e7e` |
| `_get_queue_for_task` | function | queue_manager.py | `13213dabec80` |
| `_get_size_preference` | function | subtitle_design_manager.py | `d4d766d2052d` |
| `_get_sound_preferences` | function | sound_effects_processor.py | `fc9fd65ea27b` |
| `_get_static_color_preferences` | function | subtitle_design_manager.py | `0e763c008e9b` |
| `_handle_task_completion` | function | queue_manager.py | `adc8a1386836` |
| `_init_policy_structures` | function | cache_manager.py | `8d816b5c0fbe` |
| `_initialize_filters` | function | __init__.py | `191d1af5230e` |
| `_initialize_presets` | function | video_filter_processor.py | `71f0ef672407` |
| `_initialize_session` | function | main.py | `179c6068e21e` |
| `_is_image_file` | function | main.py | `342bf839b47d` |
| `_load_cache_index` | function | temp_file_manager.py | `a966e39e4969` |
| `_load_persistent_cache` | function | cache_manager.py | `bc652786aa1c` |
| `_load_persistent_data` | function | queue_manager.py | `07c22113f934` |
| `_log_statistics` | function | queue_manager.py | `21acec71371d` |
| `_maintenance_worker` | function | cache_manager.py | `62c87934b3d0` |
| `_monitoring_worker` | function | queue_manager.py | `de9bd756ace9` |
| `_optimize_cache` | function | cache_manager.py | `d99332ce1a58` |
| `_parse_selection` | function | video_filter_processor.py | `044fe2d960ae` |
| `_persistence_worker` | function | queue_manager.py | `c985357f1010` |
| `_process_audio_duration` | function | sound_effects_processor.py | `75df4353fc29` |
| `_process_canvas_task` | function | canvas_processor.py | `726987d63e46` |
| `_process_cleanup_task` | function | temp_file_manager.py | `8a08ef496bbf` |
| `_process_compress_task` | function | temp_file_manager.py | `88df21bf7e95` |
| `_process_decompress_task` | function | temp_file_manager.py | `9a8acaff88be` |
| `_process_ffmpeg_concat_task` | function | temp_file_manager.py | `690841e57581` |
| `_process_ffmpeg_extract_task` | function | temp_file_manager.py | `6a41234d6b37` |
| `_process_ffmpeg_filter_task` | function | temp_file_manager.py | `c0d2411d7001` |
| `_process_load_clip_task` | function | temp_file_manager.py | `2d6db89d5437` |
| `_process_random_with_beat_timing` | function | video_processor.py | `0960f5971e24` |
| `_process_save_clip_task` | function | temp_file_manager.py | `2c3aa8579d5d` |
| `_process_segment_batch` | function | video_processor.py | `129e6f661c95` |
| `_process_segments_in_batches` | function | video_processor.py | `73f3698260bd` |
| `_process_sequential_with_beat_timing` | function | video_processor.py | `56d4106cf65f` |
| `_process_single_segment` | function | video_processor.py | `0d51887e2505` |
| `_process_task` | function | temp_file_manager.py | `7ad8d6c2b61c` |
| `_queue_worker` | function | queue_manager.py | `72c03fee6b2f` |
| `_rebuild_frequency_buckets` | function | cache_manager.py | `e91e7ccb4e83` |
| `_remove_entry` | function | cache_manager.py | `75acd1fe631d` |
| `_remove_from_policy_structures` | function | cache_manager.py | `6c21cf078eeb` |
| `_resize_with_padding` | function | video_formatter.py | `965e2195c21e` |
| `_retry_task` | function | queue_manager.py | `d6f9dd8b3cb5` |
| `_save_cache_index` | function | temp_file_manager.py | `6844bc7d5b56` |
| `_save_persistent_cache` | function | cache_manager.py | `2860d374bdb9` |
| `_save_persistent_data` | function | queue_manager.py | `633897044d2a` |
| `_setup_directories` | function | temp_file_manager.py | `84d3161f1af1` |
| `_setup_logging` | function | temp_file_manager.py | `2993986643e2` |
| `_signal_handler` | function | main.py | `0434c6af6b7c` |
| `_start_background_workers` | function | queue_manager.py | `473b78e53f71` |
| `_start_background_workers` | function | temp_file_manager.py | `754226529415` |
| `_start_maintenance` | function | cache_manager.py | `756814998213` |
| `_statistics_worker` | function | temp_file_manager.py | `d6ab628ecad4` |
| `_stretch_video` | function | split_screen_processor.py | `c0ff33fa5f78` |
| `_task_processor_worker` | function | temp_file_manager.py | `6fa1538147c5` |
| `_update_policy_structures` | function | cache_manager.py | `1e71601dab38` |
| `_update_statistics` | function | cache_manager.py | `59f987b7d892` |
| `_update_statistics` | function | temp_file_manager.py | `057fef22e735` |
| `access_time` | variable | cache_manager.py | `f585ac88a2a4` |
| `actual_checksum` | variable | io_operations.py | `c9fc7b521004` |
| `actual_download_path` | variable | insta-download.py | `948e86f7f534` |
| `add_access_callback` | function | cache_manager.py | `9e32100125da` |
| `add_border` | variable | canvas_processor.py | `6cc54dbd31d4` |
| `add_canvas` | variable | video_formatter.py | `e73e18ec6860` |
| `add_effects` | variable | canvas_processor.py | `308240ec446a` |
| `add_eviction_callback` | function | cache_manager.py | `0ca4501ab0fa` |
| `add_file_to_database` | function | batch_video_normalizer.py | `db7c5fb47579` |
| `add_media_to_video_ffmpeg` | function | video_generator.py | `5e40c6ba7685` |
| `add_rounded` | variable | canvas_processor.py | `5d560c0b9ff4` |
| `add_subtitles` | variable | video_formatter.py | `6e705e7dc66a` |
| `add_subtitles_to_video` | function | subtitle_video_processor.py | `d233b7fe5674` |
| `add_text` | variable | canvas_processor.py | `fbbbd6705ef7` |
| `add_text_overlay` | function | canvas_processor.py | `2255f86185a4` |
| `add_to_centralized_json` | function | insta-download.py | `41ea861c74c8` |
| `add_to_centralized_json` | function | pinterest-download.py | `3fb9876c1858` |
| `age` | function | cache_manager.py | `79af89dc1317` |
| `age` | function | queue_manager.py | `a59b161f6c12` |
| `age_threshold` | variable | io_operations.py | `bd999fe67272` |
| `all_files` | variable | extract-code.py | `10a5be7ce563` |
| `all_indices` | variable | video_formatter.py | `fce5cda8a502` |
| `all_records` | variable | file-processor.py | `8a7d5be1edb2` |
| `all_records` | variable | insta-download.py | `28fe3eb24fb3` |
| `all_records` | variable | pinterest-download.py | `ca995a4941f9` |
| `all_text_frames` | variable | easy-text-detection.py | `e6ca4053fee4` |
| `allowed_executions` | variable | queue_manager.py | `23ad6095051c` |
| `analysis` | variable | mixed_media_processor.py | `c6eae05bcc3c` |
| `analysis_params` | variable | audio_processor.py | `d716cc48ce4d` |
| `analyze_and_group_videos` | function | combine-video.py | `f84dee895ccd` |
| `analyze_beats` | function | audio_processor.py | `ed802181cad4` |
| `analyze_beats_with_caching` | function | audio_processor.py | `6e42bd076419` |
| `analyze_content_info` | function | video_generator.py | `a3fb6d91d8f2` |
| `analyze_folder` | function | mixed_media_processor.py | `97093c8e2053` |
| `analyze_video_changes` | function | batch_video_normalizer.py | `3d99095cd8dd` |
| `analyze_video_changes` | function | image-video-encoder.py | `f767b81cd4d1` |
| `analyze_vocal_changes_with_caching` | function | audio_processor.py | `80cf769f1060` |
| `animation` | variable | multiple_image_processor.py | `87a40accc786` |
| `animation_filters` | variable | image_processor.py | `712a9819e856` |
| `animation_filters` | variable | multiple_image_processor.py | `1b3f7837e8cb` |
| `animation_type` | variable | image_processor.py | `87aac5d629e9` |
| `animation_type` | variable | multiple_image_processor.py | `5a2594519999` |
| `animation_types` | variable | image_processor.py | `eb170569d5b1` |
| `animation_types` | variable | multiple_image_processor.py | `2d4e7a59807c` |
| `another` | variable | extract-audio.py | `326a5b0fe105` |
| `applied_filters` | variable | video_filter_processor.py | `6bd84786c91f` |
| `apply_anime_style` | function | preset_filters.py | `801a433ad59a` |
| `apply_auto_levels` | function | brightness_filters.py | `658700a15dbb` |
| `apply_blur` | function | artistic_filters.py | `fddf8c1622df` |
| `apply_brighten` | function | brightness_filters.py | `91e4dca428ee` |
| `apply_canvas_effects` | function | canvas_processor.py | `91689735715d` |
| `apply_canvas_to_video` | function | canvas_processor.py | `4d80ff42b643` |
| `apply_canvas_with_caching` | function | canvas_processor.py | `9e19faad65f9` |
| `apply_cinematic_look` | function | preset_filters.py | `c7900d3fcfe7` |
| `apply_cold_winter` | function | preset_filters.py | `0ae4b8fcd185` |
| `apply_color_grading` | function | multiple_image_processor.py | `9a06b461e7ca` |
| `apply_color_temperature` | function | color_filters.py | `023990012a60` |
| `apply_curves` | function | brightness_filters.py | `32beca7b711a` |
| `apply_cyberpunk` | function | preset_filters.py | `b15d1895c6da` |
| `apply_darken` | function | brightness_filters.py | `a62cc584e9c0` |
| `apply_desaturate` | function | color_filters.py | `e76af9dcf3a5` |
| `apply_documentary` | function | preset_filters.py | `27a04c90fb26` |
| `apply_dream_sequence` | function | preset_filters.py | `834c00730489` |
| `apply_edge_detection` | function | artistic_filters.py | `6eb13f091c26` |
| `apply_emboss` | function | artistic_filters.py | `a82723a25611` |
| `apply_exposure` | function | brightness_filters.py | `d013cc6212cd` |
| `apply_film_grain` | function | artistic_filters.py | `ca87f191f707` |
| `apply_filter` | function | filter_registry.py | `42d0306d78ff` |
| `apply_filter_chain` | function | video_filter_processor.py | `5a0d37ed39dc` |
| `apply_filter_chain_cached` | function | video_filter_processor.py | `5fc5ed820780` |
| `apply_filters` | function | temp_file_manager.py | `9b03468eea7c` |
| `apply_filters` | function | video_filter_processor.py | `e4451d71d87e` |
| `apply_filters_async` | function | video_filter_processor.py | `cf9ae6637ee8` |
| `apply_gamma_correction` | function | brightness_filters.py | `e09b479083c5` |
| `apply_glow` | function | artistic_filters.py | `b16f4713f591` |
| `apply_grayscale` | function | color_filters.py | `33e1bd2df7c4` |
| `apply_high_contrast` | function | brightness_filters.py | `4b07103bd9e3` |
| `apply_high_energy` | function | preset_filters.py | `96f22a1bd46d` |
| `apply_horror_atmosphere` | function | preset_filters.py | `25ae3034cd60` |
| `apply_image_effects` | function | image_processor.py | `f05142829fb2` |
| `apply_image_filters` | function | image_processor.py | `1f2726524faf` |
| `apply_instagram_style` | function | preset_filters.py | `8501b3fc27cd` |
| `apply_invert` | function | color_filters.py | `29b93346e3e9` |
| `apply_low_contrast` | function | brightness_filters.py | `2a2bc207bef5` |
| `apply_mosaic` | function | artistic_filters.py | `366b8573569b` |
| `apply_music_video` | function | preset_filters.py | `d962f587dc84` |
| `apply_noir_style` | function | preset_filters.py | `d5823853eb5a` |
| `apply_posterize` | function | artistic_filters.py | `d6b1a09f6947` |
| `apply_preset_filters` | function | video_filter_processor.py | `1a6ca9742068` |
| `apply_retro_80s` | function | preset_filters.py | `ba05ae57cfd7` |
| `apply_saturate` | function | color_filters.py | `bcbb9808f947` |
| `apply_sepia` | function | color_filters.py | `2f495094cdfa` |
| `apply_shadow_highlight` | function | brightness_filters.py | `8aad27097862` |
| `apply_sharpen` | function | artistic_filters.py | `6017dae90f53` |
| `apply_single_filter_cached` | function | video_filter_processor.py | `63c664587e44` |
| `apply_tint` | function | color_filters.py | `2cd33586c032` |
| `apply_video_filters` | function | temp_file_manager.py | `a65966b91b5d` |
| `apply_vignette` | function | artistic_filters.py | `0c27e17d5530` |
| `apply_vintage_colors` | function | color_filters.py | `ea4b56ec99ea` |
| `apply_vintage_film` | function | preset_filters.py | `68745a9899db` |
| `apply_warm_sunset` | function | preset_filters.py | `0618cd65c4c8` |
| `approx_char_width` | variable | subtitle_video_processor.py | `60ab010c2e76` |
| `area` | variable | detect-text.py | `692083b636aa` |
| `argparse` | import | arg_parser.py | `f534a72c58d1` |
| `args` | variable | arg_parser.py | `859f202cad35` |
| `args` | variable | filter_registry.py | `9c71a64852c3` |
| `args` | variable | main.py | `958a2e0ca18a` |
| `artistic_filters.apply_blur` | import | preset_filters.py | `bfcad2bbdc30` |
| `artistic_filters.apply_edge_detection` | import | preset_filters.py | `f1e711c81275` |
| `artistic_filters.apply_film_grain` | import | preset_filters.py | `96589ec984c3` |
| `artistic_filters.apply_glow` | import | preset_filters.py | `50ff42b6410d` |
| `artistic_filters.apply_posterize` | import | preset_filters.py | `697299be39fe` |
| `artistic_filters.apply_sharpen` | import | preset_filters.py | `e7d42bd22d51` |
| `artistic_filters.apply_vignette` | import | preset_filters.py | `d9eeb413a251` |
| `aspect_ratio` | variable | detect-text.py | `e5740c15ba3b` |
| `asyncio` | import | convert-audio-file.py | `9a98a75d0ce4` |
| `atomic_read` | function | io_operations.py | `4620d2d9088b` |
| `atomic_write` | function | io_operations.py | `254be2acd734` |
| `audio_bitrate` | variable | download-insta.py | `0b2e1e4d3e9d` |
| `audio_clip` | variable | sound_effects_processor.py | `b1dbac107f29` |
| `audio_clips` | variable | split_screen_processor.py | `56846daa3624` |
| `audio_codec` | variable | download-insta.py | `6aee5d72396a` |
| `audio_config` | variable | split_screen_processor.py | `30c33bc89db9` |
| `audio_duration` | variable | main.py | `64b2dfcac0b3` |
| `audio_extensions` | variable | main.py | `7293dca30fe7` |
| `audio_extract_error_msg` | variable | file-processor.py | `d595fd41a66f` |
| `audio_filename` | variable | download-insta.py | `093a2c042c9a` |
| `audio_files` | variable | convert-audio-file.py | `9a32ad77c06d` |
| `audio_format` | variable | extract-audio.py | `b086c484ab6f` |
| `audio_output_directory` | variable | download-insta.py | `e9dbe5a78285` |
| `audio_output_path` | variable | download-insta.py | `f7f3f474b54f` |
| `audio_path` | variable | main.py | `10d89ec11214` |
| `audio_path` | variable | split_screen_processor.py | `d32f36e96de5` |
| `audio_prefs` | variable | main.py | `12015412e287` |
| `audio_processor` | variable | audio_processor.py | `eec148d817b8` |
| `audio_processor.analyze_beats` | import | __init__.py | `04b1385ec74c` |
| `audio_segment` | variable | convert-audio-file.py | `9ea36f55aa88` |
| `audio_stream` | variable | batch_video_normalizer.py | `75d235ae234a` |
| `audio_stream` | variable | image-video-encoder.py | `fc4ed56a5a9c` |
| `auto_levels_effect` | function | brightness_filters.py | `d73e57c6aef6` |
| `available_categories` | variable | sound_effects_processor.py | `f47882056ff6` |
| `available_choices` | variable | subtitle_video_processor.py | `6a5eab72d857` |
| `available_duration` | variable | sound_effects_processor.py | `a988d8eb7fa9` |
| `available_gb` | variable | main.py | `ba3f320caf1a` |
| `available_gb` | variable | video_generator.py | `758fb33334e8` |
| `available_modes` | variable | subtitle_video_processor.py | `1c7734ef5409` |
| `avg_color` | variable | artistic_filters.py | `3daf62a838e8` |
| `background` | variable | image-to-video.py | `141237c11940` |
| `background` | variable | split_screen_processor.py | `805decf745f6` |
| `backup_path` | variable | io_operations.py | `cf0cbc2860ad` |
| `base_duration` | variable | sequential_timing.py | `cb58cedb72ef` |
| `base_filename` | variable | file-processor.py | `7682b1821496` |
| `base_font_size` | variable | subtitle_video_processor.py | `4dafc4a94fe4` |
| `base_info` | variable | video_generator.py | `c4e540fc7389` |
| `base_intensity` | variable | video_filter_processor.py | `3cbc948c5953` |
| `base_name` | variable | image-to-video.py | `29853d0b8310` |
| `base_name` | variable | image-video-encoder.py | `ce7b9ef258e3` |
| `base_name` | variable | pinterest-download.py | `9b256149a3bc` |
| `base_name` | variable | video-transcribe.py | `e9d901579efd` |
| `base_name_no_ext` | variable | insta-download.py | `dd43f03c9027` |
| `base_output_dir` | variable | pinterest-download.py | `6a97dc7caca2` |
| `base_path` | variable | canvas_processor.py | `17129eeebac4` |
| `base_path` | variable | subtitle_video_processor.py | `942101aa6e9b` |
| `base_presets` | variable | batch_video_normalizer.py | `bae87484ea01` |
| `base_time` | variable | canvas_processor.py | `7dc9457679ed` |
| `base_time` | variable | main.py | `6b01a2b4b71f` |
| `base_time` | variable | multiple_image_processor.py | `73f645f262ff` |
| `batch_apply_filters` | function | video_filter_processor.py | `fb93bdfaa418` |
| `batch_create_canvases` | function | canvas_processor.py | `349a55f8bf2b` |
| `batch_end` | variable | multiple_image_processor.py | `b939591fca94` |
| `batch_end` | variable | video_processor.py | `3b2a76bd0397` |
| `batch_paths` | variable | video_processor.py | `42829c058267` |
| `batch_segments` | variable | multiple_image_processor.py | `e709833b969a` |
| `batch_segments` | variable | video_processor.py | `f3688b936872` |
| `batch_size` | variable | easy-text-detection.py | `91837a0f979b` |
| `beat_times` | variable | audio_processor.py | `9f166f4bffab` |
| `beat_times` | variable | main.py | `525a85a6ae0f` |
| `beat_times` | variable | video_generator.py | `0a18a5953c39` |
| `beat_times` | variable | video_processor.py | `c9f8536d2273` |
| `beats` | variable | audio_processor.py | `05ec1cc80795` |
| `bg` | variable | video_formatter.py | `3f3bd85819fb` |
| `bg_audio` | variable | split_screen_processor.py | `24e96e5e5e19` |
| `bitrate` | variable | extract-audio.py | `de383b20c024` |
| `blend_frames` | function | color_filters.py | `68965d5e184e` |
| `blended` | variable | color_filters.py | `a1d8e5933315` |
| `block` | variable | artistic_filters.py | `effbd3bdd79d` |
| `block_size` | variable | artistic_filters.py | `2fd79664fe74` |
| `blur` | variable | canvas_processor.py | `d0da8736e866` |
| `blur_radius` | variable | artistic_filters.py | `8b99ef1d17bb` |
| `blur_strength` | variable | canvas_processor.py | `30405090ac50` |
| `blurred` | variable | artistic_filters.py | `31899a9199cf` |
| `blurred` | variable | detect-text.py | `730f808076a7` |
| `blurred_glow` | variable | artistic_filters.py | `7ff26d8b7220` |
| `border_color` | variable | canvas_processor.py | `b8e79d31b972` |
| `border_params` | variable | canvas_processor.py | `84710550b001` |
| `border_width` | variable | canvas_processor.py | `c437fd26d77a` |
| `bottom_text` | variable | canvas_processor.py | `2ea14799ff1a` |
| `box` | variable | subtitle_video_processor.py | `486be08e5ac0` |
| `box_color_rgb` | variable | subtitle_video_processor.py | `bddfa85a6533` |
| `box_height` | variable | subtitle_video_processor.py | `9704fa9075d9` |
| `box_width` | variable | subtitle_video_processor.py | `26ddab13909e` |
| `bright_mask` | variable | artistic_filters.py | `bed5c91c50dd` |
| `bright_mask_3d` | variable | artistic_filters.py | `c110a02bdb8e` |
| `brightness` | variable | artistic_filters.py | `13d4c4740769` |
| `brightness_factor` | variable | brightness_filters.py | `facd7e60b059` |
| `brightness_filters.apply_auto_levels` | import | preset_filters.py | `8f4c9000ed96` |
| `brightness_filters.apply_brighten` | import | preset_filters.py | `fbb2015f239e` |
| `brightness_filters.apply_darken` | import | preset_filters.py | `b22b6cfa9b04` |
| `brightness_filters.apply_high_contrast` | import | preset_filters.py | `3ced8cf7a412` |
| `brightness_filters.apply_low_contrast` | import | preset_filters.py | `e7dec35bc17e` |
| `brightness_filters.apply_shadow_highlight` | import | preset_filters.py | `8a14035d975b` |
| `build_ffmpeg_command` | function | easy-text-detection.py | `1c190e84f258` |
| `bytes_freed` | variable | io_operations.py | `5a6a631e4bfa` |
| `bytes_saved` | variable | io_operations.py | `b9046d457248` |
| `cache_data` | variable | cache_manager.py | `92b17c24bb08` |
| `cache_dir` | variable | temp_file_manager.py | `b75dc85e5826` |
| `cache_entries` | variable | main.py | `2c8e42ba5a2d` |
| `cache_entry` | variable | temp_file_manager.py | `4a13261ab2e9` |
| `cache_file_path` | variable | temp_file_manager.py | `6f9f76e5c914` |
| `cache_hit_rate` | variable | main.py | `edf046761ebc` |
| `cache_key` | variable | audio_processor.py | `262662e37ca2` |
| `cache_key` | variable | canvas_processor.py | `819986064350` |
| `cache_key` | variable | image_processor.py | `42640db3be4e` |
| `cache_key` | variable | mixed_media_processor.py | `e63d1ecc9e38` |
| `cache_key` | variable | multiple_image_processor.py | `1411595b2058` |
| `cache_key` | variable | video_filter_processor.py | `ae6d629c07b0` |
| `cache_key` | variable | video_processor.py | `9ce15f56b000` |
| `cache_path` | variable | io_operations.py | `e9a5283dda1f` |
| `cache_size_mb` | variable | main.py | `d0a6152b9b96` |
| `cache_stats` | variable | canvas_processor.py | `098c8e2321f1` |
| `cache_stats` | variable | main.py | `36df3dfbb58c` |
| `cache_stats` | variable | temp_file_manager.py | `9d769647bfbf` |
| `cache_stats` | variable | video_filter_processor.py | `4ac4c4ad0cc1` |
| `cache_string` | variable | temp_file_manager.py | `4f73bbcbfabc` |
| `cached_clip` | variable | video_filter_processor.py | `46749666aabe` |
| `cached_path` | variable | canvas_processor.py | `de06619fbbb7` |
| `cached_path` | variable | image_processor.py | `ef694e5c5868` |
| `cached_path` | variable | multiple_image_processor.py | `f650a4a0dea0` |
| `cached_path` | variable | temp_file_manager.py | `dcb1f50b5367` |
| `cached_path` | variable | video_processor.py | `38b905dd3a08` |
| `cached_result` | variable | audio_processor.py | `5704785c3d94` |
| `calculate_beat_based_segments` | function | video_processor.py | `bf4472549588` |
| `calculate_change_points` | function | sequential_timing.py | `0ef904f9aa42` |
| `calculate_image_timing` | function | multiple_image_processor.py | `1c5b5b2d9f55` |
| `calculate_text_size` | function | subtitle_video_processor.py | `b7f62cbf62d1` |
| `calculator` | variable | sequential_timing.py | `0729651dccc4` |
| `can_execute` | function | queue_manager.py | `7f17dd4bd937` |
| `cancel_batch` | function | video_filter_processor.py | `30dd3e7de2ac` |
| `cancel_task` | function | queue_manager.py | `d489afb3793b` |
| `cancelled` | variable | video_filter_processor.py | `3684f2e45663` |
| `canvas` | variable | image_processor.py | `a925a8012460` |
| `canvas` | variable | multiple_image_processor.py | `e8a25aca20f2` |
| `canvas_height` | variable | canvas_processor.py | `81613a035cee` |
| `canvas_params` | variable | canvas_processor.py | `e31c665be9a4` |
| `canvas_temp` | variable | canvas_processor.py | `4d70f333d5e1` |
| `canvas_width` | variable | canvas_processor.py | `cc2baec6dfa0` |
| `cap` | variable | detect-text.py | `895757ea8366` |
| `cap` | variable | easy-text-detection.py | `6d8fe9e7e6a8` |
| `categories` | variable | filter_registry.py | `a1ae97a54841` |
| `categorize_video_format` | function | combine-video.py | `26a001b781c4` |
| `category` | variable | combine-video.py | `e605212e5720` |
| `category` | variable | sound_effects_processor.py | `26d2e93f0607` |
| `category_path` | variable | sound_effects_processor.py | `0b429ca1fd01` |
| `cell_height` | variable | multiple_image_processor.py | `6e94c416aa94` |
| `cell_width` | variable | multiple_image_processor.py | `847e396af557` |
| `centralized_json_path` | variable | insta-download.py | `2d627565694d` |
| `centralized_json_path` | variable | pinterest-download.py | `1a22a5d8a758` |
| `chain_cache_key` | variable | video_filter_processor.py | `67b19a148d9a` |
| `chain_repr` | variable | video_filter_processor.py | `2ab649810073` |
| `change_interval` | variable | main.py | `c76a6e65e91c` |
| `change_points` | variable | sequential_timing.py | `f7faaa6a9eaa` |
| `changes_needed` | variable | batch_video_normalizer.py | `3b695b3d9fe1` |
| `changes_needed` | variable | image-video-encoder.py | `535e8bff92a2` |
| `check_executable` | function | batch_video_normalizer.py | `f3557bda850c` |
| `check_executable` | function | file-processor.py | `f3557bda850c` |
| `check_executable` | function | image-video-encoder.py | `f3557bda850c` |
| `check_executable` | function | insta-download.py | `f3557bda850c` |
| `check_executable` | function | pinterest-download.py | `f3557bda850c` |
| `check_ffmpeg` | function | image-to-video.py | `5080ba2f432d` |
| `check_ffmpeg_installation` | function | main.py | `f3c171e500fc` |
| `check_ffmpeg_installed` | function | combine-video.py | `8617a79ac5bd` |
| `check_ffmpeg_installed` | function | extract-audio.py | `f9abf4fa2d37` |
| `check_ffprobe_installation` | function | main.py | `d15da511b961` |
| `check_gpu_support` | function | batch_video_normalizer.py | `1d18c549d4f9` |
| `check_large_project_warning` | function | main.py | `b1275eaaa00d` |
| `check_video_validity` | function | combine_video.py | `959f94115baf` |
| `checksum` | variable | io_operations.py | `5e2318d7351d` |
| `choice` | variable | batch_video_normalizer.py | `25016d431b38` |
| `choice` | variable | extract-audio.py | `6ce0dde26a2b` |
| `choice` | variable | image-to-video.py | `49c4e300ae02` |
| `choice` | variable | image-video-encoder.py | `4c4e6dc6d508` |
| `choice` | variable | main.py | `3447591abc8d` |
| `choice` | variable | mixed_media_processor.py | `68b9b4076f7c` |
| `choice` | variable | sound_effects_processor.py | `5313c274f4e6` |
| `choice` | variable | split_screen_processor.py | `2a925a5b0946` |
| `choice` | variable | subtitle_design_manager.py | `8bb97af1a6ca` |
| `choice` | variable | subtitle_processor.py | `2923a44636e2` |
| `choice` | variable | subtitle_video_processor.py | `ab8aa35c46d5` |
| `choice` | variable | video_filter_processor.py | `a0a86e9f61ea` |
| `choice_num` | variable | extract-audio.py | `89ce27350344` |
| `choice_num` | variable | video_filter_processor.py | `4c2f37facde5` |
| `choose_audio_format` | function | extract-audio.py | `d7dfc502d319` |
| `chunk_duration` | variable | subtitle_processor.py | `edddd9ecf2fe` |
| `chunk_end` | variable | subtitle_processor.py | `6f3d895d4724` |
| `chunk_start` | variable | subtitle_processor.py | `009bc1bbb1e5` |
| `chunk_text` | variable | subtitle_processor.py | `b07cbc72d60f` |
| `chunk_words` | variable | subtitle_processor.py | `ccf40b1dca7f` |
| `clean_duration` | variable | easy-text-detection.py | `bf608cede360` |
| `clean_segments` | variable | easy-text-detection.py | `440824249fbb` |
| `clean_text_for_speech` | function | convert-audio-file.py | `903a7962afe3` |
| `cleaned` | variable | detect-text.py | `08c62fb50b72` |
| `cleaned_count` | variable | video_processor.py | `d3584793988b` |
| `cleaned_text` | variable | convert-audio-file.py | `f0b159900de1` |
| `cleanup_audio_cache` | function | audio_processor.py | `ab2403b90dbc` |
| `cleanup_cache` | function | audio_processor.py | `8ed89ae684d7` |
| `cleanup_effects` | function | sound_effects_processor.py | `7878db762274` |
| `cleanup_memory` | function | easy-text-detection.py | `d86052065b4e` |
| `cleanup_session` | function | canvas_processor.py | `f28d0ce80c8e` |
| `cleanup_session` | function | image_processor.py | `0f62a6b1337c` |
| `cleanup_session` | function | main.py | `1cede1303f6f` |
| `cleanup_session` | function | mixed_media_processor.py | `d42f61f9cc13` |
| `cleanup_session` | function | multiple_image_processor.py | `25eb6b812f42` |
| `cleanup_session` | function | temp_file_manager.py | `d273daa02d06` |
| `cleanup_session` | function | video_filter_processor.py | `9fdf871ee0c0` |
| `cleanup_session` | function | video_generator.py | `8e860b74caa3` |
| `cleanup_session` | function | video_processor.py | `a3195357a899` |
| `cleanup_temp_files` | function | convert-audio-file.py | `3547b59b10a6` |
| `cleanup_temp_files` | function | detect-text.py | `4f606f5d2c5a` |
| `cleanup_temp_files` | function | io_operations.py | `bd51d9186c48` |
| `cleanup_temp_manager` | function | temp_file_manager.py | `d140c8d0b839` |
| `cleanup_worker` | variable | temp_file_manager.py | `72ba8443a33c` |
| `clear` | function | cache_manager.py | `e28a634ef7b1` |
| `clear_cache` | function | canvas_processor.py | `01fb9c6fdd84` |
| `clear_cache` | function | temp_file_manager.py | `84d66bb3c20a` |
| `clear_cache` | function | video_filter_processor.py | `9af27aaf690d` |
| `clear_dead_letter_queue` | function | queue_manager.py | `31b14bdbf9b8` |
| `clear_registry` | function | filter_registry.py | `7e83dd19ec84` |
| `clip_id` | variable | video_filter_processor.py | `2ed8f5da8531` |
| `clip_ratio` | variable | split_screen_processor.py | `db1576836957` |
| `clip_ratio` | variable | video_formatter.py | `a67ea3b8adaf` |
| `clips` | variable | split_screen_processor.py | `96a548dc0224` |
| `clips_to_close` | variable | subtitle_video_processor.py | `7ea9524bd7e4` |
| `closed` | variable | detect-text.py | `e0dfc8e1b311` |
| `cmd` | variable | canvas_processor.py | `86d7fd7597ea` |
| `cmd` | variable | combine-video.py | `9f46d305226d` |
| `cmd` | variable | combine_video.py | `d66ef4e90c4b` |
| `cmd` | variable | detect-text.py | `339f1f229bb4` |
| `cmd` | variable | easy-text-detection.py | `d6921f971eb4` |
| `cmd` | variable | extract-audio.py | `9b5ab85e04f7` |
| `cmd` | variable | image_processor.py | `394b75bce927` |
| `cmd` | variable | main.py | `7bdbb5ee6a57` |
| `cmd` | variable | mixed_media_processor.py | `502fe6d722c0` |
| `cmd` | variable | multiple_image_processor.py | `c4e4f3a28624` |
| `cmd` | variable | temp_file_manager.py | `64b9508ec51c` |
| `cmd` | variable | video_generator.py | `e817dba318a3` |
| `cmd` | variable | video_processor.py | `817c8c275dee` |
| `cmd_concat` | variable | video_generator.py | `5a9031c71bf4` |
| `cmd_image_to_video` | variable | video_generator.py | `345a6befaa96` |
| `codec` | variable | combine-video.py | `e471396ad5f9` |
| `codec` | variable | extract-audio.py | `9d8d895aa43f` |
| `codec_name` | variable | batch_video_normalizer.py | `28b6d6610c41` |
| `coding_extensions` | variable | extract-code.py | `40f9283fbe1c` |
| `coding_files` | variable | extract-code.py | `3be0b9fd9a70` |
| `col` | variable | multiple_image_processor.py | `9a798c7b91c4` |
| `collect_python_code` | function | file-test.py | `90fda8670523` |
| `collections.OrderedDict` | import | cache_manager.py | `c95cd684505b` |
| `collections.defaultdict` | import | cache_manager.py | `4152f3fdb997` |
| `collections.defaultdict` | import | queue_manager.py | `4152f3fdb997` |
| `collections.deque` | import | multiple_image_processor.py | `f4b9d6458b8d` |
| `collections.deque` | import | queue_manager.py | `f4b9d6458b8d` |
| `collections.deque` | import | video_processor.py | `f4b9d6458b8d` |
| `color` | variable | canvas_processor.py | `b3a7f58b8174` |
| `color_choice` | variable | canvas_processor.py | `bce7e67067dd` |
| `color_filters.apply_color_temperature` | import | preset_filters.py | `290b1021864c` |
| `color_filters.apply_desaturate` | import | preset_filters.py | `8ad8a2ffd1c8` |
| `color_filters.apply_grayscale` | import | preset_filters.py | `050bbf51e463` |
| `color_filters.apply_saturate` | import | preset_filters.py | `bae87b5ea855` |
| `color_filters.apply_sepia` | import | preset_filters.py | `e499eb01e7c9` |
| `color_filters.apply_tint` | import | preset_filters.py | `bea7a51d7374` |
| `color_filters.apply_vintage_colors` | import | preset_filters.py | `dbbcc3b69324` |
| `color_hex` | variable | canvas_processor.py | `f0e002ebc406` |
| `color_map` | variable | canvas_processor.py | `d01639d78d41` |
| `color_name` | variable | subtitle_design_manager.py | `58ad3388d4ba` |
| `color_usage` | variable | canvas_processor.py | `2105797cb147` |
| `combine_audio_files` | function | convert-audio-file.py | `a78c36730c52` |
| `combine_choice` | variable | image-video-encoder.py | `dc9de7f3b5eb` |
| `combine_group_videos` | function | combine-video.py | `13cf19ebd9f6` |
| `combine_segments` | function | detect-text.py | `681814f88b9f` |
| `combine_videos` | function | combine_video.py | `b81fc01b111a` |
| `combine_videos` | function | image-video-encoder.py | `4ea09debbb37` |
| `combine_videos_with_caching` | function | mixed_media_processor.py | `1508f1a16896` |
| `combined` | variable | convert-audio-file.py | `b80c5a3db3db` |
| `combined_filename` | variable | image-video-encoder.py | `b8a8a8ad465f` |
| `combined_output_path` | variable | image-video-encoder.py | `5dbde94e1c92` |
| `combined_path` | variable | mixed_media_processor.py | `bf5f9615eb53` |
| `combined_video_path` | variable | mixed_media_processor.py | `c0ce772ef93d` |
| `combiner` | variable | combine-video.py | `34ae8b737649` |
| `command` | variable | batch_video_normalizer.py | `424758fdf33a` |
| `command` | variable | file-processor.py | `6dab7486de45` |
| `command` | variable | image-to-video.py | `6919184962d1` |
| `command` | variable | image-video-encoder.py | `22c1a8273371` |
| `command` | variable | insta-download.py | `05cfdcf420a6` |
| `command` | variable | pinterest-download.py | `c61c0f208def` |
| `communicate` | variable | convert-audio-file.py | `fd8f4aaed41f` |
| `complete_processing` | function | easy-text-detection.py | `22e65f02095f` |
| `completed_callback` | variable | canvas_processor.py | `291c8669dda0` |
| `completed_callback` | variable | video_filter_processor.py | `0d5c6ee88224` |
| `completed_count` | variable | easy-text-detection.py | `3bc65ebc6959` |
| `composite` | variable | multiple_image_processor.py | `ce70f5e3418b` |
| `compress_file` | function | io_operations.py | `316c4d24d20f` |
| `compressed_count` | variable | io_operations.py | `afcb5b602213` |
| `compressed_path` | variable | io_operations.py | `468e15e4b651` |
| `compressed_size` | variable | io_operations.py | `194213d6a524` |
| `compression_time` | variable | io_operations.py | `db6bcd03b9b4` |
| `concat_file` | variable | combine-video.py | `d492e99411d5` |
| `concat_file` | variable | detect-text.py | `4dfcf6e0530b` |
| `concat_file` | variable | main.py | `4a290dcd6bd8` |
| `concat_file` | variable | mixed_media_processor.py | `0d0754d98c95` |
| `concat_file` | variable | temp_file_manager.py | `45457d534ae3` |
| `concat_file` | variable | video_generator.py | `8bd181629313` |
| `concat_file` | variable | video_processor.py | `d230a790cac2` |
| `concatenate_video_segments` | function | temp_file_manager.py | `1107e3597b93` |
| `concatenate_videos` | function | temp_file_manager.py | `16f869348c87` |
| `concatenate_videos` | function | video_processor.py | `9076c447781e` |
| `concurrent.futures.Future` | import | queue_manager.py | `ef9743bf0695` |
| `concurrent.futures.ProcessPoolExecutor` | import | queue_manager.py | `4c633bc0d39e` |
| `concurrent.futures.ProcessPoolExecutor` | import | temp_file_manager.py | `4c633bc0d39e` |
| `concurrent.futures.ThreadPoolExecutor` | import | queue_manager.py | `107d7d8e1fd2` |
| `concurrent.futures.ThreadPoolExecutor` | import | temp_file_manager.py | `107d7d8e1fd2` |
| `concurrent.futures.as_completed` | import | queue_manager.py | `04389600475a` |
| `concurrent.futures.as_completed` | import | temp_file_manager.py | `04389600475a` |
| `config` | variable | arg_parser.py | `e606c9cb5e96` |
| `config` | variable | main.py | `59b71955aa1b` |
| `confirm` | variable | batch_video_normalizer.py | `42a570217cf6` |
| `confirm` | variable | detect-text.py | `4bfd64a7c5b8` |
| `confirm` | variable | image-video-encoder.py | `bfaaf37f45ac` |
| `conn` | variable | batch_video_normalizer.py | `e7c72e538dae` |
| `conn` | variable | easy-text-detection.py | `350ef74be576` |
| `conn` | variable | file-processor.py | `350ef74be576` |
| `conn` | variable | image-to-video.py | `371e525113db` |
| `conn` | variable | insta-download.py | `45929e6ab2c7` |
| `conn` | variable | pinterest-download.py | `34ee1e548cc1` |
| `content` | variable | convert-audio-file.py | `9c602263214c` |
| `content` | variable | extract-code.py | `ff43267d76f8` |
| `content` | variable | file-test.py | `3b53b1190c86` |
| `content_files` | variable | pinterest-download.py | `ad4fc4e60ce0` |
| `content_info` | variable | video_generator.py | `47e2f0b1ce63` |
| `content_path` | variable | main.py | `c461b736dfb2` |
| `content_type` | variable | video_generator.py | `ecb17e69e135` |
| `contextlib.contextmanager` | import | io_operations.py | `d4651b4ca1d3` |
| `contrast` | variable | audio_processor.py | `b38140ec70ec` |
| `contrast` | variable | vocal_processor.py | `f1a27cadc650` |
| `contrast_effect` | function | brightness_filters.py | `dabc7fa8332d` |
| `contrast_factor` | variable | brightness_filters.py | `0106b5f29829` |
| `convert_image_to_video` | function | batch_video_normalizer.py | `74f455d891bb` |
| `convert_image_to_video` | function | image-video-encoder.py | `0cf9960923a8` |
| `convert_image_to_video_with_caching` | function | mixed_media_processor.py | `656d1589da2d` |
| `converter` | variable | convert-audio-file.py | `7b63595f0a04` |
| `cookies_path` | variable | insta-download.py | `ddc5fc286b1c` |
| `copied_count` | variable | image-to-video.py | `bd59d09261ad` |
| `copy_file` | function | io_operations.py | `497742d6c5f1` |
| `copy_path` | variable | image-to-video.py | `87972d0bc811` |
| `corner_radius` | variable | canvas_processor.py | `49abf5d36fa9` |
| `corrected` | variable | brightness_filters.py | `d00e65c099bb` |
| `count` | variable | combine-video.py | `6344d6da962d` |
| `count` | variable | queue_manager.py | `2cbc7ec33ec9` |
| `create_animated_image_segment` | function | multiple_image_processor.py | `1d890a18f516` |
| `create_audio_effects_track` | function | sound_effects_processor.py | `402094eba345` |
| `create_canvas_batch` | function | canvas_processor.py | `ff07497eea23` |
| `create_canvas_preset` | function | canvas_processor.py | `2dbcbb09606b` |
| `create_canvas_preset_video` | function | canvas_processor.py | `2e82bb3d8ef3` |
| `create_canvas_with_video` | function | canvas_processor.py | `8df3b9406980` |
| `create_concat_file` | function | combine-video.py | `3f24050fec3e` |
| `create_consolidated_file` | function | extract-code.py | `ae57a038a4db` |
| `create_directory` | function | io_operations.py | `708eb1f638d6` |
| `create_filter_batch` | function | video_filter_processor.py | `e13d326d3520` |
| `create_filter_processor` | function | video_filter_processor.py | `b48a8c87d9f2` |
| `create_good_segments` | function | detect-text.py | `ccfa70fa5007` |
| `create_image_montage` | function | multiple_image_processor.py | `4905eb4455f5` |
| `create_image_segments` | function | image_processor.py | `bbae224ea012` |
| `create_image_segments_batch` | function | multiple_image_processor.py | `da2f82f6f3bc` |
| `create_image_slideshow` | function | multiple_image_processor.py | `d6d67b1d035f` |
| `create_image_with_animation` | function | image_processor.py | `164e814f31c0` |
| `create_parser` | function | arg_parser.py | `c1315c549f0a` |
| `create_queue` | function | queue_manager.py | `874dff827d2f` |
| `create_rounded_canvas` | function | canvas_processor.py | `1e02605233da` |
| `create_split_screen_video` | function | split_screen_processor.py | `32e4d0e91af1` |
| `create_task_chain` | function | queue_manager.py | `d8b772051f9b` |
| `create_task_group` | function | queue_manager.py | `ef500b69df15` |
| `create_text_clip` | function | subtitle_video_processor.py | `3bb09f5fbf1c` |
| `create_transition_between_images` | function | multiple_image_processor.py | `2f3276c4c4a5` |
| `create_video_from_image` | function | image-to-video.py | `6331b2860a9d` |
| `create_youtube_sized_image` | function | image-to-video.py | `870f5feb226c` |
| `current_audio_codec` | variable | batch_video_normalizer.py | `94a057375ef3` |
| `current_audio_codec` | variable | image-video-encoder.py | `d06b259d2591` |
| `current_channels` | variable | batch_video_normalizer.py | `edda29f4f505` |
| `current_channels` | variable | image-video-encoder.py | `d11fd7c2db87` |
| `current_error` | variable | file-processor.py | `74abf6c76f23` |
| `current_format` | variable | batch_video_normalizer.py | `b4ac341ded66` |
| `current_format` | variable | image-video-encoder.py | `4786ffc7bb56` |
| `current_height` | variable | batch_video_normalizer.py | `0f6c09a3f0c7` |
| `current_height` | variable | image-video-encoder.py | `b3ce9d69c9b9` |
| `current_length` | variable | subtitle_video_processor.py | `057053306ce9` |
| `current_line` | variable | subtitle_video_processor.py | `87ef11e3d0aa` |
| `current_memory` | variable | easy-text-detection.py | `06e465b522b7` |
| `current_paragraph` | variable | convert-audio-file.py | `88a74036d81b` |
| `current_path` | variable | video_formatter.py | `9f867244e2f0` |
| `current_record_had_audio_error` | variable | file-processor.py | `d6c017039a59` |
| `current_record_had_reencode_error` | variable | file-processor.py | `4c2b546098dd` |
| `current_resolution` | variable | batch_video_normalizer.py | `a967c07a1551` |
| `current_resolution` | variable | image-video-encoder.py | `3b589a9a80f2` |
| `current_sample_rate` | variable | batch_video_normalizer.py | `ef33787f5eb3` |
| `current_sample_rate` | variable | image-video-encoder.py | `9c56a96799ee` |
| `current_specs` | variable | batch_video_normalizer.py | `e7f4d98e09d0` |
| `current_specs` | variable | image-video-encoder.py | `6286f9513891` |
| `current_time` | variable | cache_manager.py | `7a1b0d18c627` |
| `current_time` | variable | detect-text.py | `12d26a30582c` |
| `current_time` | variable | image_processor.py | `6632645b5872` |
| `current_time` | variable | io_operations.py | `03c4178c37be` |
| `current_time` | variable | multiple_image_processor.py | `a511753e3c56` |
| `current_time` | variable | queue_manager.py | `28362b277ee9` |
| `current_time` | variable | sequential_timing.py | `f54eec5484f2` |
| `current_video` | variable | canvas_processor.py | `a84bb191f246` |
| `current_video` | variable | video_processor.py | `b269399216cb` |
| `current_video_time` | variable | video_processor.py | `5d6ebb8089ed` |
| `current_width` | variable | batch_video_normalizer.py | `c7fab2fd1624` |
| `current_width` | variable | image-video-encoder.py | `753487ff261b` |
| `cursor` | variable | batch_video_normalizer.py | `4b534c63210a` |
| `cursor` | variable | easy-text-detection.py | `049059f242e1` |
| `cursor` | variable | file-processor.py | `049059f242e1` |
| `cursor` | variable | image-to-video.py | `857e25d0d8f6` |
| `cursor` | variable | insta-download.py | `20d6a776c67c` |
| `cursor` | variable | pinterest-download.py | `c9fe404a4553` |
| `curve_strength` | variable | brightness_filters.py | `b394baacc651` |
| `curves_effect` | function | brightness_filters.py | `6aa8b035f750` |
| `custom_color` | variable | canvas_processor.py | `63736304c307` |
| `cut_mode_choice` | variable | video_formatter.py | `d8baf07d3470` |
| `cutoff_time` | variable | queue_manager.py | `f34139ef9798` |
| `cutting_choice` | variable | main.py | `6d2398fb784d` |
| `cutting_mode` | variable | main.py | `dacbe9c5d9d5` |
| `cv2` | import | detect-text.py | `7e8fceb2005a` |
| `cv2` | import | easy-text-detection.py | `7e8fceb2005a` |
| `data` | variable | batch_video_normalizer.py | `a67a001d45fd` |
| `data` | variable | canvas_processor.py | `d97ec66433fd` |
| `data` | variable | image-video-encoder.py | `556fa1116e5f` |
| `data` | variable | io_operations.py | `585eb135c505` |
| `data` | variable | main.py | `4657329311c3` |
| `data` | variable | queue_manager.py | `398fa170ef9b` |
| `data` | variable | subtitle_video_processor.py | `0c8b51d63694` |
| `data` | variable | temp_file_manager.py | `e60ed9465fe8` |
| `data` | variable | video_generator.py | `5599370632b5` |
| `data` | variable | video_processor.py | `86dc4d7d7588` |
| `dataclasses.dataclass` | import | audio_processor.py | `0010e60c88a0` |
| `dataclasses.dataclass` | import | cache_manager.py | `0010e60c88a0` |
| `dataclasses.dataclass` | import | canvas_processor.py | `0010e60c88a0` |
| `dataclasses.dataclass` | import | image_processor.py | `0010e60c88a0` |
| `dataclasses.dataclass` | import | io_operations.py | `0010e60c88a0` |
| `dataclasses.dataclass` | import | mixed_media_processor.py | `0010e60c88a0` |
| `dataclasses.dataclass` | import | multiple_image_processor.py | `0010e60c88a0` |
| `dataclasses.dataclass` | import | queue_manager.py | `0010e60c88a0` |
| `dataclasses.dataclass` | import | temp_file_manager.py | `0010e60c88a0` |
| `dataclasses.dataclass` | import | video_generator.py | `0010e60c88a0` |
| `dataclasses.dataclass` | import | video_processor.py | `0010e60c88a0` |
| `dataclasses.field` | import | cache_manager.py | `7cfc6d2d4075` |
| `dataclasses.field` | import | queue_manager.py | `7cfc6d2d4075` |
| `datetime` | import | easy-text-detection.py | `ab28f7340ed8` |
| `datetime` | import | file-processor.py | `ab28f7340ed8` |
| `datetime.datetime` | import | batch_video_normalizer.py | `605c90667b36` |
| `datetime.datetime` | import | cache_manager.py | `605c90667b36` |
| `datetime.datetime` | import | combine-video.py | `605c90667b36` |
| `datetime.datetime` | import | image-to-video.py | `605c90667b36` |
| `datetime.datetime` | import | queue_manager.py | `605c90667b36` |
| `datetime.datetime` | import | temp_file_manager.py | `605c90667b36` |
| `datetime.timedelta` | import | cache_manager.py | `fa21c1b1533d` |
| `datetime.timedelta` | import | queue_manager.py | `fa21c1b1533d` |
| `datetime.timedelta` | import | temp_file_manager.py | `fa21c1b1533d` |
| `db_entry` | variable | file-processor.py | `dc647343834e` |
| `db_path` | variable | batch_video_normalizer.py | `11b56eb3d9c8` |
| `decompress_file` | function | io_operations.py | `8d9df5d0de37` |
| `decompression_time` | variable | io_operations.py | `03c198367059` |
| `decorator` | function | filter_registry.py | `2a55674ae13c` |
| `default` | variable | filter_registry.py | `1957ebc5a727` |
| `default` | variable | video_filter_processor.py | `e33aae66d1db` |
| `deleted_count` | variable | easy-text-detection.py | `c4ab4d00d587` |
| `dependent_tasks` | variable | queue_manager.py | `4c9c3f5e4191` |
| `desaturate_effect` | function | color_filters.py | `e4b3e5401135` |
| `description` | variable | insta-download.py | `c8d81e1ea4e2` |
| `descriptions` | variable | canvas_processor.py | `9bc81ef16959` |
| `descriptions` | variable | multiple_image_processor.py | `8b0080a4f072` |
| `descriptions` | variable | preset_filters.py | `b660b3f3e428` |
| `design_settings` | variable | subtitle_video_processor.py | `0f40e56e99e7` |
| `detect_high_contrast_text` | function | detect-text.py | `5fb4d5730914` |
| `detect_language` | function | subtitle_processor.py | `634a4a623b69` |
| `detect_overlay_text` | function | detect-text.py | `97d57b2e018a` |
| `detect_stroke_text` | function | detect-text.py | `f503d0c104e6` |
| `detect_uniform_text_blocks` | function | detect-text.py | `05ae9716b1b6` |
| `detect_video_type` | function | easy-text-detection.py | `7efa2bfffb33` |
| `detect_vocal_changes` | function | audio_processor.py | `4a4d6a32fb50` |
| `detect_vocal_changes` | function | vocal_processor.py | `14f1b38b2556` |
| `detected_language` | variable | subtitle_video_processor.py | `178377d0e42f` |
| `directory` | variable | file_handler.py | `f4041e5a786a` |
| `discover_filters` | function | filter_registry.py | `1dde406f5c14` |
| `discover_images` | function | image-to-video.py | `580c8f56b2f1` |
| `discovered_count` | variable | __init__.py | `d53b5593bbd4` |
| `discovered_count` | variable | filter_registry.py | `e99f975f2e71` |
| `disk_info` | variable | io_operations.py | `e72405f2694c` |
| `disk_info` | variable | main.py | `e011744a142f` |
| `disk_info` | variable | video_generator.py | `bdb93dc101a0` |
| `display_group_statistics` | function | combine-video.py | `0f5475d4ca66` |
| `distance` | variable | artistic_filters.py | `c124d8f65970` |
| `download_pinterest_with_gallery_dl` | function | pinterest-download.py | `8be1a2faeca5` |
| `download_reels_with_gallery_dl` | function | insta-download.py | `b07a1a97ecd3` |
| `drawtext_filter` | variable | canvas_processor.py | `d292be0df3c4` |
| `duplicate_found` | variable | combine-video.py | `2a6fd0a5900a` |
| `duration` | variable | detect-text.py | `f4f2334d0a68` |
| `duration` | variable | easy-text-detection.py | `d98522274163` |
| `duration` | variable | extract-audio.py | `af126163c734` |
| `duration` | variable | main.py | `a5790598c2ba` |
| `duration` | variable | mixed_media_processor.py | `e61b2a29e6ff` |
| `duration` | variable | multiple_image_processor.py | `dd44a2a02acf` |
| `duration` | variable | sequential_timing.py | `87dbfd469980` |
| `duration` | variable | sound_effects_processor.py | `dfdc36ecbc31` |
| `duration` | variable | subtitle_video_processor.py | `7e36da8a9049` |
| `duration` | variable | video_generator.py | `0673f357d125` |
| `duration` | variable | video_processor.py | `0c34891daee0` |
| `duration_choice` | variable | main.py | `b1d6eeeb6932` |
| `duration_input` | variable | batch_video_normalizer.py | `b6d44b582050` |
| `duration_input` | variable | image-video-encoder.py | `d47babc963be` |
| `duration_input` | variable | mixed_media_processor.py | `4f1fd08705a4` |
| `duration_per_image` | variable | multiple_image_processor.py | `f03c07d054b4` |
| `easyocr` | import | easy-text-detection.py | `cc5b9a00a803` |
| `edge_effect` | function | artistic_filters.py | `b750042391aa` |
| `edge_tts` | import | convert-audio-file.py | `ad958d773348` |
| `edges` | variable | artistic_filters.py | `8f9e2e33ab1f` |
| `effect_clip` | variable | sound_effects_processor.py | `e0974e36c3fe` |
| `effects` | variable | canvas_processor.py | `7f0e284e7489` |
| `effects_audio` | variable | sound_effects_processor.py | `14a402bff6af` |
| `effects_temp` | variable | canvas_processor.py | `e29ae0b53322` |
| `effects_time` | variable | canvas_processor.py | `ef739f87c62b` |
| `elapsed_time` | function | video_generator.py | `b4b29514e0bc` |
| `emboss_effect` | function | artistic_filters.py | `a097eeacd7f9` |
| `emboss_kernel` | variable | artistic_filters.py | `a21a9e2dafd5` |
| `embossed` | variable | artistic_filters.py | `dfe54377e250` |
| `empty_buckets` | variable | cache_manager.py | `baa61864a90a` |
| `encodings` | variable | extract-code.py | `41ce7df45deb` |
| `end` | variable | detect-text.py | `3a3a59e28aaf` |
| `end` | variable | easy-text-detection.py | `ced1a54d655d` |
| `end_processing_session` | function | canvas_processor.py | `a4a880fcb0ab` |
| `end_processing_session` | function | video_filter_processor.py | `23506968e6bf` |
| `end_time` | variable | batch_video_normalizer.py | `634f20285797` |
| `end_time` | variable | detect-text.py | `ae663765a667` |
| `end_time` | variable | image-video-encoder.py | `f16f1b8ba795` |
| `end_time` | variable | sound_effects_processor.py | `f887781a54dd` |
| `end_time` | variable | subtitle_processor.py | `d3545fe4c13b` |
| `end_time` | variable | subtitle_video_processor.py | `0b62848e5858` |
| `end_time` | variable | video-transcribe.py | `93a57be30a35` |
| `end_time` | variable | video_formatter.py | `9bfe640fa621` |
| `end_time` | variable | video_processor.py | `c945b5ff6cd7` |
| `ensure_disk_space` | function | io_operations.py | `5e1dd67de5d7` |
| `ensure_output_dir` | function | file_handler.py | `9fa49a63506e` |
| `entries_info` | variable | cache_manager.py | `0d2fae9cc344` |
| `entry` | variable | cache_manager.py | `0405939f9d54` |
| `enum.Enum` | import | audio_processor.py | `3b3f4ac945d2` |
| `enum.Enum` | import | cache_manager.py | `3b3f4ac945d2` |
| `enum.Enum` | import | io_operations.py | `3b3f4ac945d2` |
| `enum.Enum` | import | mixed_media_processor.py | `3b3f4ac945d2` |
| `enum.Enum` | import | multiple_image_processor.py | `3b3f4ac945d2` |
| `enum.Enum` | import | queue_manager.py | `3b3f4ac945d2` |
| `enum.Enum` | import | sound_effects_processor.py | `3b3f4ac945d2` |
| `enum.Enum` | import | temp_file_manager.py | `3b3f4ac945d2` |
| `enum.Enum` | import | video_generator.py | `3b3f4ac945d2` |
| `enum.Enum` | import | video_processor.py | `3b3f4ac945d2` |
| `error_count` | variable | batch_video_normalizer.py | `b5acbdb5f8d5` |
| `error_count` | variable | image-video-encoder.py | `59b1d80b36af` |
| `error_in_this_run_count` | variable | file-processor.py | `ad9937eb985b` |
| `error_message` | variable | file-processor.py | `35b01192feb6` |
| `error_message` | variable | image-to-video.py | `4c7cba3f90de` |
| `error_msg` | variable | batch_video_normalizer.py | `fa45bbe40256` |
| `error_msg` | variable | easy-text-detection.py | `48c8fd3f1117` |
| `error_msg` | variable | image-video-encoder.py | `e652aa745c19` |
| `error_processing` | function | easy-text-detection.py | `62af42c2de92` |
| `errors` | variable | arg_parser.py | `c696a4519ad2` |
| `errors` | variable | easy-text-detection.py | `bf42daf6d0c5` |
| `errors` | variable | main.py | `8c5494650adf` |
| `escaped_path` | variable | combine-video.py | `bb75ee2f4dca` |
| `escaped_path` | variable | image-video-encoder.py | `bc73e2448c6d` |
| `escaped_text` | variable | canvas_processor.py | `54b4162a1ae1` |
| `estimate_processing_time` | function | canvas_processor.py | `9242a780d4ab` |
| `estimate_processing_time` | function | main.py | `e171959e9266` |
| `estimate_processing_time` | function | multiple_image_processor.py | `cdde705b5aa4` |
| `estimated_segments` | variable | main.py | `6563483e0c19` |
| `estimated_space_gb` | variable | main.py | `10599aeb1db6` |
| `estimated_space_gb` | variable | video_generator.py | `dc11ea4e3634` |
| `estimated_time` | variable | main.py | `c65dbebb3264` |
| `evicted` | variable | cache_manager.py | `a55507ed8f8c` |
| `exec_db` | function | easy-text-detection.py | `3d8248d586d1` |
| `execute_task` | function | queue_manager.py | `ff4c5379f568` |
| `execution_time` | function | queue_manager.py | `e9855ba6932b` |
| `execution_time` | variable | queue_manager.py | `3d83ca291dc6` |
| `existing` | variable | easy-text-detection.py | `767838bcc3c3` |
| `existing_images` | variable | image-to-video.py | `d9127d65c013` |
| `existing_normalized` | variable | combine-video.py | `07134e9a90bb` |
| `existing_record_index` | variable | insta-download.py | `4891c5f1bb81` |
| `existing_record_index` | variable | pinterest-download.py | `a0b43ec65a30` |
| `expand_buffer` | function | easy-text-detection.py | `20cc842cf6b6` |
| `expanded` | variable | easy-text-detection.py | `9eca506218ec` |
| `expired_keys` | variable | cache_manager.py | `490bfab32f91` |
| `expiry_time` | variable | cache_manager.py | `3c58c5b3bd38` |
| `exposed` | variable | brightness_filters.py | `65c42a239fb6` |
| `exposure_effect` | function | brightness_filters.py | `446aeb2c9a41` |
| `exposure_multiplier` | variable | brightness_filters.py | `130b000780cc` |
| `ext` | variable | extract-code.py | `01d6f2d2772f` |
| `ext_lower` | variable | batch_video_normalizer.py | `e0a81142f5b4` |
| `ext_lower` | variable | image-video-encoder.py | `acfa03a838f9` |
| `extract_audio` | function | extract-audio.py | `93f0817ec46c` |
| `extract_audio_and_repair_videos` | function | download-insta.py | `b846e8bc0a60` |
| `extract_audio_ffmpeg` | function | file-processor.py | `395a67eae642` |
| `extract_audio_from_video` | function | subtitle_processor.py | `99c6a2165c3b` |
| `extract_audio_from_video` | function | video-transcribe.py | `d39c606291aa` |
| `extract_command` | variable | download-insta.py | `a2e342c7a97a` |
| `extract_profile_name_from_url` | function | insta-download.py | `d615a33d1fe7` |
| `extract_search_terms_from_url` | function | pinterest-download.py | `83b7a4a0b5c3` |
| `extract_segment` | function | temp_file_manager.py | `9de22d5f3af2` |
| `extract_segment` | function | video_processor.py | `aec882b07023` |
| `extract_segments` | function | detect-text.py | `8f4ddc849df1` |
| `extract_video_segment` | function | temp_file_manager.py | `db851fdf91fe` |
| `extracted_audio_dir` | variable | file-processor.py | `9e898732fe18` |
| `extracted_audio_filename` | variable | file-processor.py | `cdb917524585` |
| `extracted_audio_path` | variable | file-processor.py | `c63483b34234` |
| `extractor` | variable | extract-audio.py | `9077cf9b5598` |
| `failed_count` | variable | easy-text-detection.py | `ddc59d5dee7a` |
| `failed_groups` | variable | combine-video.py | `5c265ca4169b` |
| `failed_reencodes` | variable | insta-download.py | `80ac239f582b` |
| `fcntl` | import | io_operations.py | `b55442722e8c` |
| `feature_smooth` | variable | audio_processor.py | `c260e6e6ac8c` |
| `feature_smooth` | variable | vocal_processor.py | `03edbc7e5965` |
| `feature_sum` | variable | audio_processor.py | `38e6c3e7782a` |
| `feature_sum` | variable | vocal_processor.py | `547c42b9189b` |
| `ffmpeg_temp_dir` | variable | temp_file_manager.py | `c9234a330119` |
| `file_age` | variable | io_operations.py | `c41d0bc2f4a9` |
| `file_count` | variable | file-test.py | `e28c94d62537` |
| `file_ext` | variable | mixed_media_processor.py | `9e25d429965f` |
| `file_ext` | variable | video_generator.py | `0499e4bc856c` |
| `file_extension` | variable | extract-audio.py | `497e83cf50cc` |
| `file_extension` | variable | image-to-video.py | `6076dfb79778` |
| `file_handler.ensure_output_dir` | import | __init__.py | `434e68b050c3` |
| `file_handler.validate_file_path` | import | __init__.py | `9ec1177e5cea` |
| `file_hash` | variable | image-to-video.py | `e79069a2f57b` |
| `file_id` | variable | batch_video_normalizer.py | `9ede0eeb0a13` |
| `file_name` | variable | batch_video_normalizer.py | `2b3029b86756` |
| `file_path` | variable | batch_video_normalizer.py | `2bc718d8bf27` |
| `file_path` | variable | combine-video.py | `096d8ebc605d` |
| `file_path` | variable | file-test.py | `5ddaf4477beb` |
| `file_path` | variable | image-to-video.py | `f71a4862b933` |
| `file_path` | variable | image-video-encoder.py | `dd41d0f22b1d` |
| `file_path` | variable | multiple_image_processor.py | `0b4b2b7e7272` |
| `file_path` | variable | sound_effects_processor.py | `910dec6ce56a` |
| `file_path` | variable | temp_file_manager.py | `e87b6b632aef` |
| `file_path` | variable | video_generator.py | `5a2316e5023e` |
| `file_size` | variable | combine-video.py | `31599bccd386` |
| `file_size` | variable | image-to-video.py | `b91f5d1d04a5` |
| `file_size` | variable | io_operations.py | `299699c43132` |
| `file_size` | variable | mixed_media_processor.py | `410f1db2c2e7` |
| `file_size` | variable | temp_file_manager.py | `a6a86b1d715c` |
| `file_size` | variable | video_generator.py | `48f6263e113c` |
| `file_status` | variable | batch_video_normalizer.py | `7b3548f57272` |
| `filelist_path` | variable | image-video-encoder.py | `7a45e8d6e998` |
| `filename` | variable | extract-code.py | `8a77f25fbc52` |
| `files` | variable | io_operations.py | `d3c69805b9d5` |
| `files_removed` | variable | io_operations.py | `5f1405db34dd` |
| `files_to_randomize` | variable | image-to-video.py | `b31c54a73e1d` |
| `filter_category` | variable | filter_registry.py | `cbaae2bfefdb` |
| `filter_chain` | variable | image_processor.py | `20b3e79f602f` |
| `filter_chain` | variable | multiple_image_processor.py | `d885e9939c7d` |
| `filter_choice` | variable | main.py | `66f2cec7ca7e` |
| `filter_complex` | variable | canvas_processor.py | `0f9888d5a095` |
| `filter_complex` | variable | easy-text-detection.py | `94fd3e8db305` |
| `filter_complex` | variable | multiple_image_processor.py | `b86ac796619d` |
| `filter_config` | variable | main.py | `94af7b1cf933` |
| `filter_config` | variable | video_filter_processor.py | `cf744860a632` |
| `filter_count` | variable | video_filter_processor.py | `91410f72197f` |
| `filter_effects` | variable | image_processor.py | `9d9aa3559792` |
| `filter_effects` | variable | multiple_image_processor.py | `b51320116f72` |
| `filter_files` | variable | filter_registry.py | `6a89ef8de23e` |
| `filter_func` | variable | filter_registry.py | `41707ff63aa6` |
| `filter_id` | variable | filter_registry.py | `a396be76e51e` |
| `filter_id` | variable | video_filter_processor.py | `44e229b22b2d` |
| `filter_info` | variable | filter_registry.py | `de2856cf3e90` |
| `filter_info` | variable | video_filter_processor.py | `efbc1cc69e57` |
| `filter_options` | variable | video_filter_processor.py | `7356f38c4086` |
| `filter_parts` | variable | canvas_processor.py | `12801e00b8da` |
| `filter_registry.FILTER_REGISTRY` | import | __init__.py | `a78214efb6fc` |
| `filter_registry.discover_filters` | import | __init__.py | `ee0f37c3fe52` |
| `filter_registry.get_all_filters` | import | __init__.py | `bd613e0ecb9e` |
| `filter_registry.get_filters_by_category` | import | __init__.py | `cfddc25ccd0b` |
| `filter_registry.register_filter` | import | __init__.py | `6bdc28233d9d` |
| `filter_registry.register_filter` | import | artistic_filters.py | `6bdc28233d9d` |
| `filter_registry.register_filter` | import | brightness_filters.py | `6bdc28233d9d` |
| `filter_registry.register_filter` | import | color_filters.py | `6bdc28233d9d` |
| `filter_registry.register_filter` | import | preset_filters.py | `6bdc28233d9d` |
| `filter_usage` | variable | video_filter_processor.py | `a65c9cc1cb68` |
| `filter_with_id` | variable | filter_registry.py | `2029a511aa9f` |
| `filtered_clip` | variable | video_filter_processor.py | `af46787a6758` |
| `filters.filter_registry.apply_filter` | import | video_filter_processor.py | `376d639f6a69` |
| `filters.filter_registry.get_all_filters` | import | video_filter_processor.py | `71fe9c985d25` |
| `filters.filter_registry.get_filter_by_id` | import | video_filter_processor.py | `3adaa3ffabc7` |
| `filters.filter_registry.get_filters_by_category` | import | video_filter_processor.py | `4aa8f553b224` |
| `filters.filter_registry.get_registry_stats` | import | video_filter_processor.py | `4d67a36029e4` |
| `filters.filter_registry.list_available_filters` | import | video_filter_processor.py | `d907386937f2` |
| `filters_after` | variable | filter_registry.py | `db851b98b2be` |
| `filters_before` | variable | filter_registry.py | `07816f7fe69c` |
| `filters_dir` | variable | filter_registry.py | `57e8ea181f1c` |
| `final_audio` | variable | split_screen_processor.py | `6b87cab937b5` |
| `final_audio_path` | variable | file-processor.py | `33a1d2d3fba4` |
| `final_cache_key` | variable | audio_processor.py | `e86135a31e60` |
| `final_cache_key` | variable | mixed_media_processor.py | `60da354d52d6` |
| `final_duration` | variable | detect-text.py | `f8e7cdeb0f5d` |
| `final_duration` | variable | video_formatter.py | `9c419267262b` |
| `final_frames` | variable | detect-text.py | `3da0c59455d6` |
| `final_intensity` | variable | video_filter_processor.py | `de60cdf5bd36` |
| `final_memory` | variable | easy-text-detection.py | `3e21a1276e3a` |
| `final_output` | variable | batch_video_normalizer.py | `5d6ff1fffaa2` |
| `final_output` | variable | combine_video.py | `6a12d5da3a3b` |
| `final_output` | variable | image-video-encoder.py | `acedb05f2a68` |
| `final_path` | variable | easy-text-detection.py | `fa2e7165bc5c` |
| `final_reencoded_path` | variable | file-processor.py | `24cb6c586e0e` |
| `final_size` | variable | batch_video_normalizer.py | `09abc85a51a4` |
| `final_size` | variable | detect-text.py | `5fb089be43a8` |
| `final_stats` | variable | batch_video_normalizer.py | `a781bc0c6119` |
| `final_stats` | variable | image-to-video.py | `8222d12ed8d0` |
| `final_status` | variable | file-processor.py | `2c2ae7c83895` |
| `final_video` | variable | split_screen_processor.py | `aeecb84d762e` |
| `final_video` | variable | subtitle_video_processor.py | `a77f025ff293` |
| `final_video_count` | variable | insta-download.py | `ff8194eec095` |
| `find_all_media_files` | function | batch_video_normalizer.py | `224fc6a6d8cd` |
| `find_all_videos` | function | combine-video.py | `daf43a5595f5` |
| `find_media_files` | function | image-video-encoder.py | `d532f157273f` |
| `first_video_info` | variable | mixed_media_processor.py | `1fd52c76faa8` |
| `fit_mode` | variable | main.py | `030a78b1b0de` |
| `fit_mode` | variable | video_formatter.py | `effecd370396` |
| `fit_modes` | variable | video_formatter.py | `2e57e6caa622` |
| `folder_id` | variable | easy-text-detection.py | `65cbdf329b9b` |
| `folder_info` | variable | video_generator.py | `369b9279ae2f` |
| `folder_name` | variable | image-video-encoder.py | `75f61c35a747` |
| `folder_path` | variable | easy-text-detection.py | `aaff6ff03fb3` |
| `folder_path` | variable | image-video-encoder.py | `b0e3650e4b34` |
| `folders` | variable | combine-video.py | `c10f912ac17b` |
| `font_path` | variable | subtitle_video_processor.py | `531c6ada4294` |
| `format_choice` | variable | main.py | `9c9498759122` |
| `format_choice` | variable | split_screen_processor.py | `a56c2ff8225e` |
| `format_choice` | variable | video_formatter.py | `bc0539874b97` |
| `format_menu` | function | video_formatter.py | `9af638e286b4` |
| `format_time` | function | easy-text-detection.py | `d8e7f9b28cf7` |
| `format_video` | function | video_formatter.py | `6962017faf19` |
| `formats` | variable | extract-audio.py | `442239b2b000` |
| `formatted_video` | variable | video_formatter.py | `9db046b2f09a` |
| `formatter` | variable | video_formatter.py | `6b5389a4c3d7` |
| `found_files` | variable | extract-code.py | `2b19e9742898` |
| `fps` | variable | combine-video.py | `e7b081875d99` |
| `fps` | variable | detect-text.py | `45f6d22c4fd3` |
| `fps` | variable | easy-text-detection.py | `11bb6c32de31` |
| `frame` | variable | artistic_filters.py | `e6cb1541ee30` |
| `frame` | variable | brightness_filters.py | `a7769e92e429` |
| `frame` | variable | color_filters.py | `5228a2ef3291` |
| `frame_count` | variable | detect-text.py | `93679459e6a0` |
| `frame_count` | variable | easy-text-detection.py | `f8db4705c8be` |
| `frame_list` | variable | easy-text-detection.py | `29a33dad5d6d` |
| `frames` | variable | easy-text-detection.py | `0c627886fab7` |
| `frames_processed` | variable | easy-text-detection.py | `5ac762f4dc03` |
| `frames_to_check` | variable | easy-text-detection.py | `accc28488f9c` |
| `frames_to_intervals` | function | easy-text-detection.py | `7a3f3bc8c72c` |
| `frames_with_text` | variable | detect-text.py | `150454d360f7` |
| `freed_bytes` | variable | temp_file_manager.py | `80cdbffdcd07` |
| `freq` | variable | cache_manager.py | `aa54cc3caef9` |
| `freq_choice` | variable | main.py | `2e4430a2054b` |
| `frequency` | variable | main.py | `7308fd1605a3` |
| `frequency` | variable | sequential_timing.py | `e060e898ca8c` |
| `frequency_map` | variable | main.py | `27ca8a64e6d4` |
| `full_module_name` | variable | filter_registry.py | `515d0ef8c070` |
| `functools.wraps` | import | filter_registry.py | `cdad882aa468` |
| `future` | variable | queue_manager.py | `5c7cf63958ca` |
| `gamma` | variable | brightness_filters.py | `1609f6b2d153` |
| `gamma_effect` | function | brightness_filters.py | `fb93ec308550` |
| `gap_percentage` | variable | image-to-video.py | `613772953e9c` |
| `gc` | import | easy-text-detection.py | `28a6b0b61821` |
| `generate_subtitles` | function | subtitle_processor.py | `aa51c8423fc0` |
| `generate_video` | function | video_generator.py | `dbbfb7bfa2ca` |
| `generate_video_with_temp_management` | function | video_generator.py | `43dd0f21ad2b` |
| `generation_time` | variable | video_generator.py | `443f7d90ce4b` |
| `generator` | variable | video_generator.py | `0bed01294de1` |
| `get` | function | cache_manager.py | `96cb9631b3aa` |
| `get_additional_media_configuration` | function | main.py | `f8a32b58c44c` |
| `get_all_filters` | function | filter_registry.py | `11db2de737ff` |
| `get_all_presets` | function | preset_filters.py | `d79e3f833ab2` |
| `get_animation_description` | function | multiple_image_processor.py | `695e0187f94c` |
| `get_audio_duration` | function | main.py | `847f7e15e80d` |
| `get_audio_info` | function | extract-audio.py | `c827b34968f7` |
| `get_audio_preferences` | function | split_screen_processor.py | `91a7236a435d` |
| `get_audio_processing_stats` | function | audio_processor.py | `5dd7061c719e` |
| `get_available_animations` | function | multiple_image_processor.py | `5bba5acc97e5` |
| `get_available_presets` | function | canvas_processor.py | `bbf5519d18ac` |
| `get_available_transitions` | function | multiple_image_processor.py | `ebed294f5c3e` |
| `get_cache_key` | function | audio_processor.py | `425bcbd238ef` |
| `get_cache_key` | function | canvas_processor.py | `6f4d9e949713` |
| `get_cache_key` | function | image_processor.py | `489ce55a30a5` |
| `get_cache_key` | function | mixed_media_processor.py | `2b6526433c1b` |
| `get_cache_key` | function | multiple_image_processor.py | `c9ebed7e5a87` |
| `get_cache_key` | function | temp_file_manager.py | `ab2437e38428` |
| `get_cache_key` | function | video_processor.py | `7d6f485c6a7c` |
| `get_cache_statistics` | function | canvas_processor.py | `6590fd053885` |
| `get_cache_statistics` | function | video_filter_processor.py | `7938fafdad9b` |
| `get_canvas_usage_stats` | function | canvas_processor.py | `70bc0beb80f8` |
| `get_content_type` | function | video_generator.py | `bf11cfc7933f` |
| `get_custom_filters` | function | main.py | `379a20205815` |
| `get_custom_filters` | function | video_filter_processor.py | `43954c89f220` |
| `get_dependent_tasks` | function | queue_manager.py | `58ce31523bb9` |
| `get_disk_space_info` | function | io_operations.py | `5425e418fb16` |
| `get_entries_info` | function | cache_manager.py | `6baa7800a884` |
| `get_error_details` | function | easy-text-detection.py | `396bab08bbcc` |
| `get_file_hash` | function | image-to-video.py | `857c189ee0a1` |
| `get_file_metadata` | function | io_operations.py | `37af5014406f` |
| `get_file_path` | function | extract-audio.py | `0f719c700c0e` |
| `get_file_size` | function | io_operations.py | `63413ae0edad` |
| `get_file_size_mb` | function | batch_video_normalizer.py | `daad57cc9c2d` |
| `get_file_size_mb` | function | image-video-encoder.py | `daad57cc9c2d` |
| `get_file_status` | function | batch_video_normalizer.py | `39695f7589ea` |
| `get_filter_by_id` | function | filter_registry.py | `e325d76ae73a` |
| `get_filter_cache_key` | function | video_filter_processor.py | `b39013c26df2` |
| `get_filter_chain_cache_key` | function | video_filter_processor.py | `74b8951af602` |
| `get_filter_configuration` | function | main.py | `6f5b5959e76c` |
| `get_filter_info` | function | video_filter_processor.py | `a295e205c701` |
| `get_filter_usage_stats` | function | video_filter_processor.py | `69b675249434` |
| `get_filters_by_category` | function | filter_registry.py | `ca3b8e383194` |
| `get_fit_mode` | function | split_screen_processor.py | `d04377193a6f` |
| `get_folder_info` | function | video_generator.py | `d0209536d4f4` |
| `get_folder_paths` | function | combine-video.py | `f7cac7601559` |
| `get_font_for_language` | function | subtitle_video_processor.py | `dbfb5c6781e4` |
| `get_format_presets` | function | batch_video_normalizer.py | `dc027248e306` |
| `get_format_presets` | function | image-video-encoder.py | `93ce95aeb4d6` |
| `get_generation_stats` | function | video_generator.py | `8517b032182a` |
| `get_global_statistics` | function | queue_manager.py | `59c66ec6a6cc` |
| `get_image_count` | function | multiple_image_processor.py | `5fd4d57e69ab` |
| `get_image_info` | function | image_processor.py | `5ca58f937e34` |
| `get_image_info` | function | mixed_media_processor.py | `ee52c57a0a75` |
| `get_memory_usage` | function | canvas_processor.py | `2c66078e8ef0` |
| `get_memory_usage` | function | easy-text-detection.py | `c11dbe96741a` |
| `get_memory_usage` | function | video_filter_processor.py | `d0b2fffc00bb` |
| `get_next_task` | function | queue_manager.py | `4de2d5ae7238` |
| `get_operation_stats` | function | io_operations.py | `081f91ad5436` |
| `get_or_create_session` | function | image-to-video.py | `36a5bcd77590` |
| `get_pending` | function | easy-text-detection.py | `0f268a87cf20` |
| `get_pending_images` | function | image-to-video.py | `f3c5c04375cd` |
| `get_performance_stats` | function | canvas_processor.py | `5d8b921e847e` |
| `get_performance_stats` | function | video_filter_processor.py | `36c49302c3c6` |
| `get_preset_description` | function | canvas_processor.py | `609160df7652` |
| `get_preset_description` | function | preset_filters.py | `921a7a774401` |
| `get_preset_filters` | function | main.py | `3397a7054539` |
| `get_preset_filters` | function | video_filter_processor.py | `e5ef15da78ec` |
| `get_processing_statistics` | function | batch_video_normalizer.py | `f9e0961458de` |
| `get_processing_statistics` | function | image-to-video.py | `54f80c9e90dd` |
| `get_processing_stats` | function | audio_processor.py | `c85b7fdd4e02` |
| `get_processing_stats` | function | image_processor.py | `830d845d7e46` |
| `get_processing_stats` | function | mixed_media_processor.py | `98144cb735af` |
| `get_processing_stats` | function | multiple_image_processor.py | `c5c7c0d84c9a` |
| `get_processing_stats` | function | video_processor.py | `84cc0c8b274a` |
| `get_queue_statistics` | function | queue_manager.py | `b22f4adb984f` |
| `get_record_from_db` | function | file-processor.py | `24ef0a62c422` |
| `get_registry_stats` | function | filter_registry.py | `184687df1137` |
| `get_sequential_timing` | function | sequential_timing.py | `db876947a192` |
| `get_sound_for_animation` | function | sound_effects_processor.py | `96b3e43c42c1` |
| `get_statistics` | function | cache_manager.py | `58bbe181bd05` |
| `get_statistics` | function | queue_manager.py | `22c0f8e4fdbe` |
| `get_statistics` | function | temp_file_manager.py | `82d5225d711b` |
| `get_stats` | function | video_filter_processor.py | `97fac94be7e4` |
| `get_subtitle_mode` | function | subtitle_processor.py | `759122a7e1c4` |
| `get_subtitle_mode` | function | subtitle_video_processor.py | `af9001567e65` |
| `get_summary` | function | easy-text-detection.py | `d4f3f57767e8` |
| `get_task_dependencies` | function | queue_manager.py | `d9b7f7c6fc01` |
| `get_task_result` | function | queue_manager.py | `dccc46cc4772` |
| `get_task_status` | function | queue_manager.py | `f032d9dd720b` |
| `get_temp_manager_stats` | function | temp_file_manager.py | `94192d0c3921` |
| `get_text_color` | function | subtitle_design_manager.py | `d52c74865c48` |
| `get_user_inputs` | function | main.py | `63544f15d8ae` |
| `get_user_preferences` | function | canvas_processor.py | `fd8a9b27ae30` |
| `get_user_preferences` | function | mixed_media_processor.py | `ab9011ee761f` |
| `get_user_preferences` | function | sound_effects_processor.py | `087e82c0199a` |
| `get_user_preferences` | function | subtitle_design_manager.py | `b245ddf7b771` |
| `get_video_duration` | function | main.py | `d22f217f6140` |
| `get_video_generation_inputs` | function | main.py | `915adb12f61a` |
| `get_video_info` | function | batch_video_normalizer.py | `82d849cb2877` |
| `get_video_info` | function | canvas_processor.py | `ab780b5b13cf` |
| `get_video_info` | function | combine-video.py | `d35bad3ca883` |
| `get_video_info` | function | combine_video.py | `1a80ff87d6d8` |
| `get_video_info` | function | easy-text-detection.py | `37c8710adedf` |
| `get_video_info` | function | image-video-encoder.py | `82d849cb2877` |
| `get_video_info` | function | mixed_media_processor.py | `56c911505d91` |
| `get_video_info` | function | temp_file_manager.py | `a0bb1ab52e10` |
| `get_video_info` | function | video_generator.py | `f393839fdf97` |
| `get_video_info` | function | video_processor.py | `b270c6744841` |
| `get_video_info_simple` | function | main.py | `64d5ab363f66` |
| `get_video_properties` | function | combine-video.py | `e2b33168c28d` |
| `glob` | import | easy-text-detection.py | `8dcc5586a68c` |
| `glow_effect` | function | artistic_filters.py | `44758ed6b275` |
| `glow_layer` | variable | artistic_filters.py | `01d470763670` |
| `glowing` | variable | artistic_filters.py | `b8b9108a8c0d` |
| `good_segments` | variable | detect-text.py | `bca01378f5d9` |
| `gradient` | variable | detect-text.py | `cde1cb537a1a` |
| `grain_effect` | function | artistic_filters.py | `3969a0d1f9a3` |
| `grainy` | variable | artistic_filters.py | `a7c857b1f664` |
| `gray` | variable | artistic_filters.py | `b85e993a50d5` |
| `gray` | variable | color_filters.py | `4c1912226ebb` |
| `gray` | variable | detect-text.py | `07e4912dca66` |
| `gray` | variable | easy-text-detection.py | `ea289b81612d` |
| `gray_frame` | variable | color_filters.py | `8001ec89d611` |
| `gray_rgb` | variable | color_filters.py | `db1795258f19` |
| `grayscale_clip` | variable | color_filters.py | `b79f48fd19b4` |
| `group_consecutive_frames` | function | detect-text.py | `7136d793b6be` |
| `group_output_dir` | variable | combine-video.py | `4190ef08801d` |
| `gx` | variable | artistic_filters.py | `381e19b1241b` |
| `gy` | variable | artistic_filters.py | `fcbc8a49ded3` |
| `gzip` | import | io_operations.py | `f667174a8019` |
| `half_height` | variable | split_screen_processor.py | `7dbf9534b87b` |
| `handle_canvas` | function | main.py | `c8cc14675be7` |
| `handle_combine_videos` | function | main.py | `058baf9e3d68` |
| `handle_formatting` | function | main.py | `eec644e8b1c4` |
| `handle_split_screen` | function | main.py | `eb57bd48b3f9` |
| `handle_subtitles` | function | main.py | `c1f847e4125d` |
| `has_videotoolbox` | variable | batch_video_normalizer.py | `6a219679a3a7` |
| `hash_func` | variable | io_operations.py | `714c3946d336` |
| `hash_md5` | variable | image-to-video.py | `82fe74d13b33` |
| `hashlib` | import | audio_processor.py | `ada1d9e0a360` |
| `hashlib` | import | image-to-video.py | `ada1d9e0a360` |
| `hashlib` | import | io_operations.py | `ada1d9e0a360` |
| `hashlib` | import | temp_file_manager.py | `ada1d9e0a360` |
| `heapq` | import | cache_manager.py | `dcaa9b42ef60` |
| `heapq` | import | queue_manager.py | `dcaa9b42ef60` |
| `height` | variable | combine-video.py | `ee3a5b876726` |
| `height` | variable | easy-text-detection.py | `06569fa7d186` |
| `height_ratio` | variable | video_formatter.py | `b79585d44964` |
| `hex_color` | variable | subtitle_video_processor.py | `ef9963af9a9a` |
| `hex_to_rgb` | function | subtitle_video_processor.py | `97f86d9860d8` |
| `highlight_mask` | variable | brightness_filters.py | `30a990fe7675` |
| `highlight_pull` | variable | brightness_filters.py | `b3eb856ff8aa` |
| `highlights` | variable | brightness_filters.py | `528f67264085` |
| `i_end` | variable | artistic_filters.py | `fc5a5f7909df` |
| `image_count` | variable | multiple_image_processor.py | `85cc6db72c87` |
| `image_duration` | variable | batch_video_normalizer.py | `0c777b9eaced` |
| `image_duration` | variable | image-video-encoder.py | `7ff6f0c1335b` |
| `image_extensions` | variable | batch_video_normalizer.py | `535f7c504786` |
| `image_extensions` | variable | image-to-video.py | `f454a6e7dd33` |
| `image_extensions` | variable | image-video-encoder.py | `b43f09da049c` |
| `image_extensions` | variable | main.py | `ebc26ea56997` |
| `image_extensions` | variable | multiple_image_processor.py | `690e270624fe` |
| `image_extensions` | variable | video_generator.py | `8c0767c90f24` |
| `image_file_id` | variable | image-to-video.py | `f7fb466fb563` |
| `image_filename` | variable | image-video-encoder.py | `668de11d74c0` |
| `image_files` | variable | image-video-encoder.py | `0e0ddb63c59a` |
| `image_files` | variable | mixed_media_processor.py | `b7fe3d7025b0` |
| `image_files` | variable | multiple_image_processor.py | `7077489397d4` |
| `image_files` | variable | video_generator.py | `a410de3e7b4b` |
| `image_index` | variable | multiple_image_processor.py | `1a3eedb4257a` |
| `image_info` | variable | mixed_media_processor.py | `c605787c39f9` |
| `image_path` | variable | multiple_image_processor.py | `d98ad760fb4d` |
| `image_paths` | variable | multiple_image_processor.py | `3912fb5146d9` |
| `image_time` | variable | multiple_image_processor.py | `f3f9722bf33e` |
| `image_time` | variable | video_generator.py | `4860921c6ed9` |
| `image_timings` | variable | multiple_image_processor.py | `d1aff92d7a37` |
| `image_to_video` | function | image_processor.py | `e27288729b07` |
| `img` | variable | image_processor.py | `e7362c1e7e5c` |
| `img` | variable | multiple_image_processor.py | `545edbe65eeb` |
| `img_ratio` | variable | image_processor.py | `d4d50d96940d` |
| `img_ratio` | variable | multiple_image_processor.py | `6e4d88d638f2` |
| `importlib` | import | filter_registry.py | `856a29a936ce` |
| `indent` | variable | combine-video.py | `04ad9d4aee19` |
| `index_file` | variable | temp_file_manager.py | `e720aa716f8f` |
| `indices` | variable | video_filter_processor.py | `d6349a748aa0` |
| `info` | variable | batch_video_normalizer.py | `95811a25b6dd` |
| `info` | variable | combine-video.py | `694555d4a347` |
| `info` | variable | combine_video.py | `1e627adc41bb` |
| `info` | variable | easy-text-detection.py | `e3756012279e` |
| `info` | variable | extract-audio.py | `ce160e8a69a9` |
| `info` | variable | image-video-encoder.py | `51b1770f1925` |
| `info` | variable | mixed_media_processor.py | `7d084a01aa8f` |
| `init_database` | function | batch_video_normalizer.py | `51f17fcc246d` |
| `init_database` | function | image-to-video.py | `d51834f99ae4` |
| `init_db` | function | easy-text-detection.py | `47b5617b8e78` |
| `init_processing_db` | function | file-processor.py | `3a4c19cb68b5` |
| `init_sqlite_db` | function | insta-download.py | `cc66d8c86803` |
| `init_sqlite_db` | function | pinterest-download.py | `fb76e5c710b0` |
| `initial_memory` | variable | easy-text-detection.py | `4b65823537fa` |
| `initial_result` | variable | subtitle_processor.py | `e29e76050fce` |
| `initialize_model` | function | subtitle_processor.py | `b8a29b5be397` |
| `input_dir` | variable | extract-audio.py | `972cca5be21d` |
| `input_directory` | variable | download-insta.py | `28e144455c6c` |
| `input_file` | variable | extract-audio.py | `8bd0ea46c58d` |
| `input_name` | variable | extract-audio.py | `555e439fdc87` |
| `input_path` | variable | download-insta.py | `e0ea7576230e` |
| `input_path` | variable | insta-download.py | `bde223e9b3d9` |
| `input_path` | variable | video_formatter.py | `c137978599d7` |
| `input_paths` | variable | extract-code.py | `9da44060b938` |
| `insert_pinterest_metadata_sqlite` | function | pinterest-download.py | `64c73356a436` |
| `insert_reel_metadata_sqlite` | function | insta-download.py | `f8c0726ed934` |
| `inspect` | import | filter_registry.py | `c3a743e6d24c` |
| `intensity` | variable | filter_registry.py | `8fbcceff2a74` |
| `intensity` | variable | video_filter_processor.py | `aaef30f8221d` |
| `intensity_choice` | variable | video_filter_processor.py | `7cd90a62c1bc` |
| `intensity_info` | variable | filter_registry.py | `55c07d9da1ca` |
| `intensity_info` | variable | video_filter_processor.py | `25755910994f` |
| `intensity_input` | variable | video_filter_processor.py | `912755f1ded7` |
| `intermediate_clip_id` | variable | video_filter_processor.py | `886cf6f490fc` |
| `interval_choice` | variable | main.py | `bca43b9f9655` |
| `interval_map` | variable | main.py | `f37ee61339f2` |
| `intervals` | variable | easy-text-detection.py | `81fd3e5ff2b2` |
| `invalid_files` | variable | multiple_image_processor.py | `e25d2529ecb3` |
| `invert_effect` | function | color_filters.py | `5559e517351d` |
| `inverted` | variable | color_filters.py | `b5ec53a7415f` |
| `io_operations.CompressionLevel` | import | temp_file_manager.py | `37cdd93356c8` |
| `io_operations.FileMetadata` | import | temp_file_manager.py | `2a197bed5fb9` |
| `io_operations.IOOperations` | import | temp_file_manager.py | `f38d6f18767a` |
| `is_audio_file` | function | main.py | `259f924082bf` |
| `is_coding_file` | function | extract-code.py | `c8d62ddd5e46` |
| `is_compressed` | variable | io_operations.py | `46917f1fc1e7` |
| `is_expired` | function | cache_manager.py | `8a340086d679` |
| `is_image_file` | function | video_generator.py | `e295c92fb4ff` |
| `is_video_file` | function | main.py | `02d6018f5715` |
| `is_video_file` | function | video_generator.py | `d56a3c47a3c9` |
| `j_end` | variable | artistic_filters.py | `41e353a158e9` |
| `json` | import | audio_processor.py | `ff3e4d4dcf72` |
| `json` | import | batch_video_normalizer.py | `ff3e4d4dcf72` |
| `json` | import | cache_manager.py | `ff3e4d4dcf72` |
| `json` | import | canvas_processor.py | `ff3e4d4dcf72` |
| `json` | import | combine-video.py | `ff3e4d4dcf72` |
| `json` | import | combine_video.py | `ff3e4d4dcf72` |
| `json` | import | extract-audio.py | `ff3e4d4dcf72` |
| `json` | import | file-processor.py | `ff3e4d4dcf72` |
| `json` | import | image-video-encoder.py | `ff3e4d4dcf72` |
| `json` | import | image_processor.py | `ff3e4d4dcf72` |
| `json` | import | insta-download.py | `ff3e4d4dcf72` |
| `json` | import | main.py | `ff3e4d4dcf72` |
| `json` | import | mixed_media_processor.py | `ff3e4d4dcf72` |
| `json` | import | multiple_image_processor.py | `ff3e4d4dcf72` |
| `json` | import | pinterest-download.py | `ff3e4d4dcf72` |
| `json` | import | queue_manager.py | `ff3e4d4dcf72` |
| `json` | import | subtitle_processor.py | `ff3e4d4dcf72` |
| `json` | import | subtitle_video_processor.py | `ff3e4d4dcf72` |
| `json` | import | temp_file_manager.py | `ff3e4d4dcf72` |
| `json` | import | video-transcribe.py | `ff3e4d4dcf72` |
| `json` | import | video_generator.py | `ff3e4d4dcf72` |
| `json` | import | video_processor.py | `ff3e4d4dcf72` |
| `json_filename` | variable | pinterest-download.py | `e64f4e8eae4d` |
| `json_filepath` | variable | pinterest-download.py | `f5171b84536f` |
| `kernel` | variable | detect-text.py | `65222afc46fe` |
| `kernel_size` | variable | artistic_filters.py | `a89b711ad6dc` |
| `key` | variable | cache_manager.py | `7b4c8ad45720` |
| `key` | variable | combine-video.py | `4309169e33f6` |
| `keys` | variable | cache_manager.py | `1563e5e9d577` |
| `large_files` | variable | io_operations.py | `bd3a47b8a186` |
| `large_regions` | variable | detect-text.py | `84d929e3c36c` |
| `last_end` | variable | easy-text-detection.py | `cd8ed717e434` |
| `level` | variable | combine-video.py | `ba50e70df051` |
| `levels` | variable | artistic_filters.py | `747a5f6dcd31` |
| `librosa` | import | audio_processor.py | `c4b231211c35` |
| `librosa` | import | vocal_processor.py | `c4b231211c35` |
| `line` | variable | convert-audio-file.py | `35ca2df9bd05` |
| `lines` | variable | convert-audio-file.py | `ec9f76180ae5` |
| `lines` | variable | subtitle_video_processor.py | `1b4101480ee2` |
| `list_all_filters` | function | video_filter_processor.py | `9b906327312b` |
| `list_available_filters` | function | filter_registry.py | `8ad475fc57a7` |
| `list_files` | function | io_operations.py | `dbc58be921db` |
| `load_centralized_json` | function | insta-download.py | `9a2f1da59db2` |
| `load_centralized_json` | function | pinterest-download.py | `2bc47439875a` |
| `load_file_sync` | function | temp_file_manager.py | `a2401fcfe000` |
| `load_json_file` | function | file-processor.py | `7cb83bc07d62` |
| `load_sound_library` | function | sound_effects_processor.py | `da123f51690d` |
| `local_processing_json_path` | variable | file-processor.py | `8f6c577d60bc` |
| `lock` | variable | io_operations.py | `3ee2c829ee7f` |
| `log_dir` | variable | temp_file_manager.py | `bd7691a2945b` |
| `log_folder` | function | easy-text-detection.py | `1b45560dfe4b` |
| `log_performance_summary` | function | canvas_processor.py | `05b45ac044f8` |
| `log_performance_summary` | function | video_filter_processor.py | `4f81edcd6d7c` |
| `log_processing_message` | function | batch_video_normalizer.py | `f9584ca72ece` |
| `log_video` | function | easy-text-detection.py | `341668f1e0c7` |
| `logger` | variable | easy-text-detection.py | `6eebf14d2fe4` |
| `logging` | import | audio_processor.py | `27dced094c95` |
| `logging` | import | cache_manager.py | `27dced094c95` |
| `logging` | import | canvas_processor.py | `27dced094c95` |
| `logging` | import | image_processor.py | `27dced094c95` |
| `logging` | import | io_operations.py | `27dced094c95` |
| `logging` | import | mixed_media_processor.py | `27dced094c95` |
| `logging` | import | multiple_image_processor.py | `27dced094c95` |
| `logging` | import | queue_manager.py | `27dced094c95` |
| `logging` | import | subtitle_processor.py | `27dced094c95` |
| `logging` | import | subtitle_video_processor.py | `27dced094c95` |
| `logging` | import | temp_file_manager.py | `27dced094c95` |
| `logging` | import | video_filter_processor.py | `27dced094c95` |
| `logging` | import | video_generator.py | `27dced094c95` |
| `logging` | import | video_processor.py | `27dced094c95` |
| `low_contrast_effect` | function | brightness_filters.py | `548570dff3e0` |
| `main` | function | batch_video_normalizer.py | `e64a716155d6` |
| `main` | function | combine-video.py | `dbce2fb96e1d` |
| `main` | function | detect-text.py | `4cb95cbaac49` |
| `main` | function | easy-text-detection.py | `3e52fd80c310` |
| `main` | function | extract-audio.py | `3c5d95e21ae5` |
| `main` | function | extract-code.py | `24c414130e25` |
| `main` | function | file-processor.py | `32ddd0a69987` |
| `main` | function | image-to-video.py | `60fd2ef85b9e` |
| `main` | function | image-video-encoder.py | `fb0ca258acb8` |
| `main` | function | insta-download.py | `3c944971653d` |
| `main` | function | main.py | `89c5c0615c1e` |
| `main` | function | pinterest-download.py | `ec68330e4c5e` |
| `main` | function | video-transcribe.py | `1e11937b035b` |
| `main_audio` | variable | split_screen_processor.py | `c55746ea60fd` |
| `main_output_dir` | variable | file-processor.py | `cec81c075967` |
| `manager` | variable | main.py | `e2c9e1bc5b5d` |
| `map_change_preference` | function | sequential_timing.py | `bf4266f4916d` |
| `margin` | variable | canvas_processor.py | `e9d8aa78b84e` |
| `margin_range` | variable | canvas_processor.py | `005dfd6ca910` |
| `margin_usage` | variable | canvas_processor.py | `4c3e005ad069` |
| `margin_x` | variable | subtitle_video_processor.py | `776a3c57eeff` |
| `margin_y` | variable | subtitle_video_processor.py | `b3efc16427de` |
| `markdown_path` | variable | convert-audio-file.py | `ed39baed45e9` |
| `match` | variable | insta-download.py | `cac37590dd0f` |
| `max_chars` | variable | subtitle_video_processor.py | `c0daaf3cd491` |
| `max_clip_duration` | variable | sound_effects_processor.py | `0a9245835521` |
| `max_distance` | variable | artistic_filters.py | `ae986948c6c6` |
| `max_downloads` | variable | pinterest-download.py | `c8ee42de329e` |
| `max_duration` | variable | split_screen_processor.py | `8461ca07cf3f` |
| `max_segments` | variable | video_formatter.py | `ab99479a92d2` |
| `max_start` | variable | video_processor.py | `e27fef85130f` |
| `max_val` | variable | brightness_filters.py | `1eb89fa66f73` |
| `max_val` | variable | filter_registry.py | `28448fe7aa22` |
| `max_val` | variable | video_filter_processor.py | `70aa4a269686` |
| `max_width` | variable | subtitle_video_processor.py | `929e1dce073c` |
| `media_choice` | variable | main.py | `de3aefa418c1` |
| `media_config` | variable | main.py | `9ceb6934d01f` |
| `media_files` | variable | batch_video_normalizer.py | `9b65afb10aa1` |
| `media_path` | variable | main.py | `38506980c76a` |
| `media_to_concat` | variable | video_generator.py | `ab85cfb9f3cf` |
| `media_type` | variable | arg_parser.py | `8a1ea5bc8823` |
| `media_type` | variable | main.py | `568141f56b47` |
| `mel_spect` | variable | audio_processor.py | `3756370fdb64` |
| `mel_spect` | variable | vocal_processor.py | `154fbbde499d` |
| `mel_spect_db` | variable | audio_processor.py | `c502f43358a3` |
| `mel_spect_db` | variable | vocal_processor.py | `811521d380fa` |
| `memory_freed` | variable | easy-text-detection.py | `58ce7074e67c` |
| `memory_info` | variable | canvas_processor.py | `4f1b47fcc21b` |
| `memory_info` | variable | video_filter_processor.py | `82a61a6fc1c8` |
| `memory_stats` | variable | canvas_processor.py | `a71b971ef78d` |
| `memory_stats` | variable | video_filter_processor.py | `3e30c163c1d2` |
| `merge_intervals` | function | easy-text-detection.py | `7d786bd7d03e` |
| `merged` | variable | easy-text-detection.py | `a00465c12a5e` |
| `merged_intervals` | variable | easy-text-detection.py | `44b18885c14f` |
| `message` | variable | batch_video_normalizer.py | `c3ccd1a978aa` |
| `metadata` | variable | filter_registry.py | `5418933e3ec8` |
| `metadata` | variable | insta-download.py | `ac567a2d92ec` |
| `metadata` | variable | pinterest-download.py | `8de4d5488e37` |
| `metadata` | variable | queue_manager.py | `ffb5f1592464` |
| `metadata_filename` | variable | insta-download.py | `b725b46f44ee` |
| `metadata_filename_alt` | variable | insta-download.py | `9e63ce637291` |
| `metadata_filepath` | variable | insta-download.py | `56ac3a7b468c` |
| `metadata_filepath_alt` | variable | insta-download.py | `099c59663f36` |
| `midpoint` | variable | brightness_filters.py | `d2bf18bf3419` |
| `min_val` | variable | brightness_filters.py | `3d9adfec4d6d` |
| `min_val` | variable | filter_registry.py | `878e3cc23d8e` |
| `min_val` | variable | video_filter_processor.py | `125bfabe1275` |
| `mixed_processor` | variable | mixed_media_processor.py | `117e14ce133f` |
| `mmap` | import | io_operations.py | `1e63722bfc8d` |
| `mode_choice` | variable | video_formatter.py | `bc627bc443f6` |
| `model` | variable | video-transcribe.py | `196a3efece23` |
| `modes` | variable | subtitle_video_processor.py | `e5d73a5d6a4d` |
| `monitor_thread` | variable | queue_manager.py | `cc7f77d9cb2b` |
| `mosaic` | variable | artistic_filters.py | `6c8e6e773e6d` |
| `mosaic_effect` | function | artistic_filters.py | `5f5490965257` |
| `move_file` | function | io_operations.py | `9d352ce45082` |
| `moviepy.editor.AudioFileClip` | import | sound_effects_processor.py | `75416f1085ae` |
| `moviepy.editor.AudioFileClip` | import | split_screen_processor.py | `75416f1085ae` |
| `moviepy.editor.ColorClip` | import | split_screen_processor.py | `071a5536fb22` |
| `moviepy.editor.ColorClip` | import | subtitle_video_processor.py | `071a5536fb22` |
| `moviepy.editor.ColorClip` | import | video_formatter.py | `071a5536fb22` |
| `moviepy.editor.CompositeAudioClip` | import | sound_effects_processor.py | `0146c8002669` |
| `moviepy.editor.CompositeAudioClip` | import | split_screen_processor.py | `0146c8002669` |
| `moviepy.editor.CompositeVideoClip` | import | split_screen_processor.py | `66154cf9d138` |
| `moviepy.editor.CompositeVideoClip` | import | subtitle_video_processor.py | `66154cf9d138` |
| `moviepy.editor.CompositeVideoClip` | import | video_formatter.py | `66154cf9d138` |
| `moviepy.editor.ImageClip` | import | artistic_filters.py | `87414a4771ba` |
| `moviepy.editor.ImageClip` | import | brightness_filters.py | `87414a4771ba` |
| `moviepy.editor.ImageClip` | import | color_filters.py | `87414a4771ba` |
| `moviepy.editor.ImageClip` | import | preset_filters.py | `87414a4771ba` |
| `moviepy.editor.ImageClip` | import | video_filter_processor.py | `87414a4771ba` |
| `moviepy.editor.TextClip` | import | subtitle_video_processor.py | `d5613d5bab2a` |
| `moviepy.editor.VideoFileClip` | import | artistic_filters.py | `3951e41b0ab1` |
| `moviepy.editor.VideoFileClip` | import | brightness_filters.py | `3951e41b0ab1` |
| `moviepy.editor.VideoFileClip` | import | color_filters.py | `3951e41b0ab1` |
| `moviepy.editor.VideoFileClip` | import | preset_filters.py | `3951e41b0ab1` |
| `moviepy.editor.VideoFileClip` | import | split_screen_processor.py | `3951e41b0ab1` |
| `moviepy.editor.VideoFileClip` | import | subtitle_processor.py | `3951e41b0ab1` |
| `moviepy.editor.VideoFileClip` | import | subtitle_video_processor.py | `3951e41b0ab1` |
| `moviepy.editor.VideoFileClip` | import | video-transcribe.py | `3951e41b0ab1` |
| `moviepy.editor.VideoFileClip` | import | video_filter_processor.py | `3951e41b0ab1` |
| `moviepy.editor.VideoFileClip` | import | video_formatter.py | `3951e41b0ab1` |
| `moviepy.video.fx.all` | import | artistic_filters.py | `9ae2cd698897` |
| `moviepy.video.fx.all` | import | brightness_filters.py | `9ae2cd698897` |
| `moviepy.video.fx.all` | import | color_filters.py | `9ae2cd698897` |
| `multi_choice` | variable | video_formatter.py | `ce402427f1c2` |
| `multiprocessing` | import | queue_manager.py | `23faa645f361` |
| `multiprocessing` | import | temp_file_manager.py | `23faa645f361` |
| `name` | variable | easy-text-detection.py | `d3697383624b` |
| `name_without_ext` | variable | insta-download.py | `34d9e9689aa2` |
| `new_buckets` | variable | cache_manager.py | `ed06f78ed679` |
| `new_error` | variable | file-processor.py | `20eb9b8649ca` |
| `new_filename` | variable | image-to-video.py | `452eddf1ca31` |
| `new_filters` | variable | filter_registry.py | `67cb12a42bd4` |
| `new_freq` | variable | cache_manager.py | `7bc140e9a778` |
| `new_height` | variable | image-to-video.py | `84538c0b0244` |
| `new_height` | variable | image_processor.py | `9cf518d78ca3` |
| `new_height` | variable | multiple_image_processor.py | `b93b7b6149ac` |
| `new_height` | variable | split_screen_processor.py | `33923acdde06` |
| `new_height` | variable | video_formatter.py | `8f257696854b` |
| `new_image_name` | variable | image-to-video.py | `527d8c59dc20` |
| `new_image_path` | variable | image-to-video.py | `7ef241b4ce72` |
| `new_images` | variable | image-to-video.py | `21fcd1225ea2` |
| `new_video_name` | variable | image-to-video.py | `1405687e0ec4` |
| `new_video_path` | variable | image-to-video.py | `fccca454208f` |
| `new_width` | variable | combine_video.py | `1f869007b625` |
| `new_width` | variable | image-to-video.py | `7c7a92f52e9e` |
| `new_width` | variable | image_processor.py | `4af8f2a5bd62` |
| `new_width` | variable | multiple_image_processor.py | `1e621748cb2d` |
| `new_width` | variable | split_screen_processor.py | `d17c5f1e88e4` |
| `new_width` | variable | video_formatter.py | `90923085d26d` |
| `next_beat_time` | variable | multiple_image_processor.py | `a553a2698c98` |
| `noise` | variable | artistic_filters.py | `d9317423b4ab` |
| `normalize_video` | function | batch_video_normalizer.py | `537ff48f2553` |
| `normalize_video` | function | image-video-encoder.py | `a0e692d096ce` |
| `normalize_video_with_caching` | function | mixed_media_processor.py | `edbccc0ed939` |
| `normalized` | variable | brightness_filters.py | `35389a06ac0c` |
| `normalized` | variable | color_filters.py | `7a4405a628b3` |
| `normalized_frame` | variable | color_filters.py | `23ba1aa6297b` |
| `normalized_path` | variable | combine-video.py | `a233bf810b90` |
| `normalized_tint` | variable | color_filters.py | `4831db2bb57b` |
| `num` | variable | video_filter_processor.py | `f2273362db25` |
| `num_segments` | variable | multiple_image_processor.py | `a33c5326028b` |
| `num_segments` | variable | sequential_timing.py | `6360dd3d2b89` |
| `num_segments` | variable | video_processor.py | `d91ef77600fd` |
| `numpy` | import | artistic_filters.py | `d8fca9deea52` |
| `numpy` | import | audio_processor.py | `d8fca9deea52` |
| `numpy` | import | brightness_filters.py | `d8fca9deea52` |
| `numpy` | import | canvas_processor.py | `d8fca9deea52` |
| `numpy` | import | color_filters.py | `d8fca9deea52` |
| `numpy` | import | detect-text.py | `d8fca9deea52` |
| `numpy` | import | image_processor.py | `d8fca9deea52` |
| `numpy` | import | multiple_image_processor.py | `d8fca9deea52` |
| `numpy` | import | vocal_processor.py | `d8fca9deea52` |
| `offset_x` | variable | canvas_processor.py | `d07447349861` |
| `offset_y` | variable | canvas_processor.py | `86a959670ddf` |
| `old_freq` | variable | cache_manager.py | `5f48003533d6` |
| `old_results` | variable | queue_manager.py | `b2ef0e8de7b8` |
| `old_task_ids` | variable | queue_manager.py | `1b280753c46d` |
| `oldest_entries` | variable | cache_manager.py | `38cbdea661be` |
| `onset_env` | variable | audio_processor.py | `5c7706883c19` |
| `onset_env` | variable | vocal_processor.py | `a26bd7ad8267` |
| `opacity_map` | variable | subtitle_design_manager.py | `1bb0bd40e760` |
| `optimize_cache` | function | video_filter_processor.py | `dcbbe8443762` |
| `optimize_canvas_cache` | function | canvas_processor.py | `4a79d540a8ba` |
| `optimize_for_content_type` | function | video_generator.py | `bd0332b6813c` |
| `optimize_storage` | function | io_operations.py | `059d432ff67d` |
| `optimized_config` | variable | video_generator.py | `b9f6f868e9c1` |
| `option_num` | variable | video_filter_processor.py | `3a2c2138efe5` |
| `ordered_files` | variable | mixed_media_processor.py | `e495487e2b72` |
| `ordering` | variable | mixed_media_processor.py | `c0bf9d13aeca` |
| `original_duration` | variable | sound_effects_processor.py | `929c9aae9905` |
| `original_frame` | variable | color_filters.py | `9859cd863ffe` |
| `original_height` | variable | canvas_processor.py | `94a2c57efda7` |
| `original_height` | variable | combine_video.py | `eceb4e88aeb5` |
| `original_image` | variable | image-to-video.py | `3ac1fc2b8d52` |
| `original_input_json_path` | variable | file-processor.py | `186e383792d8` |
| `original_records` | variable | file-processor.py | `f932850902ac` |
| `original_size` | variable | batch_video_normalizer.py | `d26c2d61adda` |
| `original_size` | variable | detect-text.py | `32b5d2be20c6` |
| `original_size` | variable | image-video-encoder.py | `b31f65c560a7` |
| `original_size` | variable | io_operations.py | `6b5e7d24572a` |
| `original_video_filepath` | variable | file-processor.py | `77d1b1c5b828` |
| `original_width` | variable | canvas_processor.py | `a1c35951eb58` |
| `original_width` | variable | combine_video.py | `4a394e0feacb` |
| `os` | import | arg_parser.py | `de2abade832c` |
| `os` | import | audio_processor.py | `de2abade832c` |
| `os` | import | batch_video_normalizer.py | `de2abade832c` |
| `os` | import | cache_manager.py | `de2abade832c` |
| `os` | import | canvas_processor.py | `de2abade832c` |
| `os` | import | combine-video.py | `de2abade832c` |
| `os` | import | combine_video.py | `de2abade832c` |
| `os` | import | convert-audio-file.py | `de2abade832c` |
| `os` | import | detect-text.py | `de2abade832c` |
| `os` | import | download-insta.py | `de2abade832c` |
| `os` | import | easy-text-detection.py | `de2abade832c` |
| `os` | import | extract-audio.py | `de2abade832c` |
| `os` | import | extract-code.py | `de2abade832c` |
| `os` | import | file-processor.py | `de2abade832c` |
| `os` | import | file-test.py | `de2abade832c` |
| `os` | import | file_handler.py | `de2abade832c` |
| `os` | import | filter_registry.py | `de2abade832c` |
| `os` | import | image-to-video.py | `de2abade832c` |
| `os` | import | image-video-encoder.py | `de2abade832c` |
| `os` | import | image_processor.py | `de2abade832c` |
| `os` | import | insta-download.py | `de2abade832c` |
| `os` | import | io_operations.py | `de2abade832c` |
| `os` | import | main.py | `de2abade832c` |
| `os` | import | mixed_media_processor.py | `de2abade832c` |
| `os` | import | multiple_image_processor.py | `de2abade832c` |
| `os` | import | pinterest-download.py | `de2abade832c` |
| `os` | import | queue_manager.py | `de2abade832c` |
| `os` | import | sound_effects_processor.py | `de2abade832c` |
| `os` | import | split_screen_processor.py | `de2abade832c` |
| `os` | import | subtitle_processor.py | `de2abade832c` |
| `os` | import | subtitle_video_processor.py | `de2abade832c` |
| `os` | import | temp_file_manager.py | `de2abade832c` |
| `os` | import | video-transcribe.py | `de2abade832c` |
| `os` | import | video_filter_processor.py | `de2abade832c` |
| `os` | import | video_formatter.py | `de2abade832c` |
| `os` | import | video_generator.py | `de2abade832c` |
| `os` | import | video_processor.py | `de2abade832c` |
| `output_data` | variable | subtitle_processor.py | `f1f181d76643` |
| `output_ext` | variable | extract-audio.py | `c5a114b8468b` |
| `output_file` | variable | convert-audio-file.py | `41e82a9374c4` |
| `output_file` | variable | extract-audio.py | `16497a41d4e4` |
| `output_file` | variable | extract-code.py | `f21f31ec95e3` |
| `output_filename` | variable | combine-video.py | `17da0bf389de` |
| `output_filename` | variable | file-test.py | `dd772948bdc8` |
| `output_filename` | variable | image_processor.py | `d4b8e57f0e9b` |
| `output_filename` | variable | insta-download.py | `51def83499c0` |
| `output_filename` | variable | multiple_image_processor.py | `f49274e3a06b` |
| `output_filename` | variable | temp_file_manager.py | `e2227d5f9210` |
| `output_folder` | variable | image-to-video.py | `87e16457fdc3` |
| `output_name` | variable | main.py | `7f97cdae0ef7` |
| `output_name` | variable | split_screen_processor.py | `4e8826b4fa40` |
| `output_name` | variable | video_formatter.py | `11da8b735460` |
| `output_path` | variable | canvas_processor.py | `4290ab88e994` |
| `output_path` | variable | combine-video.py | `c63185a77576` |
| `output_path` | variable | combine_video.py | `67779b5a6b97` |
| `output_path` | variable | convert-audio-file.py | `2b8653950aac` |
| `output_path` | variable | detect-text.py | `fd219accb1e2` |
| `output_path` | variable | easy-text-detection.py | `9190fcc9d898` |
| `output_path` | variable | extract-audio.py | `a915862af5b1` |
| `output_path` | variable | image_processor.py | `9d04328d556a` |
| `output_path` | variable | insta-download.py | `5c1d560f71c3` |
| `output_path` | variable | main.py | `bb9fa0a53020` |
| `output_path` | variable | multiple_image_processor.py | `84ad9456cffa` |
| `output_path` | variable | split_screen_processor.py | `72caf89ba419` |
| `output_path` | variable | subtitle_video_processor.py | `8edd223d941c` |
| `output_path` | variable | temp_file_manager.py | `2d77ddc1b1d5` |
| `output_path` | variable | video-transcribe.py | `9142dc849abe` |
| `output_path` | variable | video_formatter.py | `71b189bf5fa0` |
| `output_size` | variable | image-video-encoder.py | `f4ca191b903c` |
| `overall_intensity` | variable | video_filter_processor.py | `92d96601352f` |
| `overlays` | variable | canvas_processor.py | `044ce63ff717` |
| `overwrite` | variable | extract-audio.py | `c9c904d8e054` |
| `padding` | variable | subtitle_video_processor.py | `b62c9b0170c7` |
| `paragraph_text` | variable | convert-audio-file.py | `8f8c3fb6aec4` |
| `paragraphs` | variable | convert-audio-file.py | `bcab9ca9c435` |
| `param_str` | variable | temp_file_manager.py | `645d2f5eb468` |
| `params` | variable | audio_processor.py | `dc23dacb5aa8` |
| `params` | variable | filter_registry.py | `d81568f53419` |
| `params` | variable | mixed_media_processor.py | `1f80f0964518` |
| `params` | variable | multiple_image_processor.py | `47dfdd09af76` |
| `params` | variable | video_filter_processor.py | `2a1338577554` |
| `parse_arguments` | function | arg_parser.py | `ab4740945b1c` |
| `parse_arguments` | variable | main.py | `c1760bc19cf4` |
| `parsed_url` | variable | pinterest-download.py | `2a1a69333ea4` |
| `parser` | variable | arg_parser.py | `fb30be7adb7b` |
| `part` | variable | video_filter_processor.py | `f5384c01f96a` |
| `patch` | variable | artistic_filters.py | `622c8e78797b` |
| `path` | variable | combine-video.py | `3ef34672f881` |
| `path` | variable | extract-audio.py | `c36586a1d677` |
| `path` | variable | extract-code.py | `9a2682d06c2d` |
| `path` | variable | io_operations.py | `65db3ade9ec7` |
| `pathlib.Path` | import | audio_processor.py | `fa6ee8aff4ab` |
| `pathlib.Path` | import | batch_video_normalizer.py | `fa6ee8aff4ab` |
| `pathlib.Path` | import | cache_manager.py | `fa6ee8aff4ab` |
| `pathlib.Path` | import | canvas_processor.py | `fa6ee8aff4ab` |
| `pathlib.Path` | import | combine-video.py | `fa6ee8aff4ab` |
| `pathlib.Path` | import | combine_video.py | `fa6ee8aff4ab` |
| `pathlib.Path` | import | convert-audio-file.py | `fa6ee8aff4ab` |
| `pathlib.Path` | import | detect-text.py | `fa6ee8aff4ab` |
| `pathlib.Path` | import | easy-text-detection.py | `fa6ee8aff4ab` |
| `pathlib.Path` | import | extract-audio.py | `fa6ee8aff4ab` |
| `pathlib.Path` | import | extract-code.py | `fa6ee8aff4ab` |
| `pathlib.Path` | import | image-to-video.py | `fa6ee8aff4ab` |
| `pathlib.Path` | import | image-video-encoder.py | `fa6ee8aff4ab` |
| `pathlib.Path` | import | image_processor.py | `fa6ee8aff4ab` |
| `pathlib.Path` | import | io_operations.py | `fa6ee8aff4ab` |
| `pathlib.Path` | import | main.py | `fa6ee8aff4ab` |
| `pathlib.Path` | import | mixed_media_processor.py | `fa6ee8aff4ab` |
| `pathlib.Path` | import | multiple_image_processor.py | `fa6ee8aff4ab` |
| `pathlib.Path` | import | queue_manager.py | `fa6ee8aff4ab` |
| `pathlib.Path` | import | temp_file_manager.py | `fa6ee8aff4ab` |
| `pathlib.Path` | import | video_generator.py | `fa6ee8aff4ab` |
| `pathlib.Path` | import | video_processor.py | `fa6ee8aff4ab` |
| `pause` | variable | easy-text-detection.py | `24c7dbc67ec4` |
| `pause_queue` | function | queue_manager.py | `19d3311ecf99` |
| `peaks` | variable | audio_processor.py | `a6012b11fe60` |
| `peaks` | variable | vocal_processor.py | `d69e57768be6` |
| `pending` | variable | easy-text-detection.py | `a4fa3dd14b2d` |
| `pending_images` | variable | image-to-video.py | `6b76c6ae285c` |
| `percentage` | variable | combine-video.py | `a49ff1b5bc61` |
| `persist_thread` | variable | queue_manager.py | `390b962ad2bd` |
| `persistence_file` | variable | queue_manager.py | `6358a9891a45` |
| `phrase_count` | variable | subtitle_processor.py | `f02a6b67191e` |
| `phrase_subtitles` | variable | subtitle_processor.py | `7cf36276cf10` |
| `phrases` | variable | subtitle_processor.py | `43978841ed1c` |
| `pickle` | import | cache_manager.py | `888eeaa6fc98` |
| `pickle` | import | queue_manager.py | `888eeaa6fc98` |
| `pickle` | import | temp_file_manager.py | `888eeaa6fc98` |
| `pinterest_dir` | variable | pinterest-download.py | `2fca9b2942b6` |
| `pinterest_url` | variable | pinterest-download.py | `33b9be81e2b6` |
| `placement` | variable | main.py | `cd87ca8bfab9` |
| `platform` | import | file-processor.py | `817f6e305a60` |
| `position` | variable | split_screen_processor.py | `c6a755999857` |
| `positioned_clip` | variable | sound_effects_processor.py | `bd9bccd23fa6` |
| `positioned_clips` | variable | sound_effects_processor.py | `1c18cd2afa4f` |
| `posterize_effect` | function | artistic_filters.py | `7264a98156e8` |
| `posterized` | variable | artistic_filters.py | `26181db2a65a` |
| `preference_map` | variable | sequential_timing.py | `d74bdf8a7739` |
| `preferences` | variable | canvas_processor.py | `f203ebfaa53f` |
| `prefs` | variable | mixed_media_processor.py | `1dbfbcbf7a1d` |
| `preprocess_frame` | function | easy-text-detection.py | `0ac5723935f8` |
| `preprocess_image` | function | image_processor.py | `236393096854` |
| `preprocess_image` | function | multiple_image_processor.py | `4924957a69f4` |
| `preprocess_params` | variable | image_processor.py | `18d08b0b965f` |
| `preset_choice` | variable | main.py | `b44fdc257a38` |
| `preset_config` | variable | canvas_processor.py | `22f9c712f3ad` |
| `preset_id` | variable | video_filter_processor.py | `36e47ae5ff64` |
| `preset_info` | variable | video_filter_processor.py | `475e439a9f36` |
| `preset_list` | variable | video_filter_processor.py | `c25d6a57b93d` |
| `presets` | variable | batch_video_normalizer.py | `95598399c2ec` |
| `presets` | variable | canvas_processor.py | `b4024be54db6` |
| `presets` | variable | image-video-encoder.py | `b276c39afcd7` |
| `presets` | variable | main.py | `c340fe896c7d` |
| `preview_filter` | function | video_filter_processor.py | `54197496cb0c` |
| `print` | function | easy-text-detection.py | `7623fda3b701` |
| `print_summary` | function | subtitle_processor.py | `614c3f3d8eb9` |
| `priority_score` | variable | queue_manager.py | `7b7090973058` |
| `proceed` | variable | combine-video.py | `1c9726aee8cf` |
| `proceed` | variable | extract-audio.py | `33aa19c0bd70` |
| `process` | variable | canvas_processor.py | `d49e1ea1abc1` |
| `process` | variable | easy-text-detection.py | `421520048387` |
| `process` | variable | insta-download.py | `d517a9e4b418` |
| `process` | variable | pinterest-download.py | `52eccc0a3a98` |
| `process` | variable | video_filter_processor.py | `45eb98750de4` |
| `process_downloaded_metadata` | function | insta-download.py | `6b83c19c71db` |
| `process_filters` | function | video_filter_processor.py | `66c16607eefb` |
| `process_image` | function | image_processor.py | `94517fa2bb35` |
| `process_images` | function | image-to-video.py | `6d00c1d02992` |
| `process_media_files` | function | batch_video_normalizer.py | `06011d8e10c0` |
| `process_mixed_folder_with_temp_management` | function | mixed_media_processor.py | `ce79822067c0` |
| `process_mixed_media_folder` | function | image-video-encoder.py | `240d2f73f358` |
| `process_mixed_media_folder` | function | mixed_media_processor.py | `cb7b1381aa37` |
| `process_multiple_images` | function | multiple_image_processor.py | `fac8ab42caa9` |
| `process_pinterest_metadata` | function | pinterest-download.py | `7fea087d0967` |
| `process_segments_to_phrases` | function | subtitle_processor.py | `3bf37965823f` |
| `process_segments_to_words` | function | subtitle_processor.py | `bc24b513ced0` |
| `process_single_image` | function | image_processor.py | `761aa4c98896` |
| `process_subtitles` | function | subtitle_video_processor.py | `6de67d35f9ee` |
| `process_transcription` | function | subtitle_processor.py | `0329a90c2128` |
| `process_video` | function | easy-text-detection.py | `c2ce1b1824c5` |
| `process_video` | function | video_processor.py | `22dfc4fdc124` |
| `process_video_with_canvas` | function | canvas_processor.py | `afde2e6c54f3` |
| `process_videos` | function | combine_video.py | `ded3929af560` |
| `process_videos` | function | split_screen_processor.py | `50e614235def` |
| `process_videos` | function | video_processor.py | `f7837f8616b2` |
| `processed` | variable | easy-text-detection.py | `43fa73ea4317` |
| `processed` | variable | preset_filters.py | `48c6c85a2876` |
| `processed_audio` | variable | sound_effects_processor.py | `57ccc08cf6fc` |
| `processed_cache_keys` | variable | mixed_media_processor.py | `4348ebfcf035` |
| `processed_clip` | variable | video_filter_processor.py | `bf45bee0ef02` |
| `processed_count` | variable | batch_video_normalizer.py | `7dbf28f327c9` |
| `processed_count` | variable | pinterest-download.py | `100e9e1daa95` |
| `processed_image` | variable | multiple_image_processor.py | `c86e65b006dc` |
| `processed_image_path` | variable | image-to-video.py | `2df16181c2c3` |
| `processed_image_path` | variable | image_processor.py | `1bb00a8b99c4` |
| `processed_in_this_run_count` | variable | file-processor.py | `c7824b4e3775` |
| `processed_metadata_count` | variable | insta-download.py | `3e241ba5f563` |
| `processed_path` | variable | multiple_image_processor.py | `3fc2c054dc5c` |
| `processed_segment_paths` | variable | video_processor.py | `5d0c2e168c7c` |
| `processed_size` | variable | image-video-encoder.py | `89d5bc6053b9` |
| `processing_db_path` | variable | file-processor.py | `b2c97db3e5cb` |
| `processing_mode` | variable | image-to-video.py | `ce598bf443e0` |
| `processing_time` | variable | audio_processor.py | `42b3c50134f6` |
| `processing_time` | variable | batch_video_normalizer.py | `4e5fb106e8e0` |
| `processing_time` | variable | canvas_processor.py | `6fab5fbcc900` |
| `processing_time` | variable | easy-text-detection.py | `e8ecf863e6ef` |
| `processing_time` | variable | image-video-encoder.py | `aa2064e08b54` |
| `processing_time` | variable | image_processor.py | `ced0e9b99dcd` |
| `processing_time` | variable | multiple_image_processor.py | `9223b4739142` |
| `processing_time` | variable | temp_file_manager.py | `ad77d75ba938` |
| `processing_time` | variable | video_filter_processor.py | `42434713c63f` |
| `processor` | variable | canvas_processor.py | `de48e46011a2` |
| `processor` | variable | image-to-video.py | `c7bda6fc0b96` |
| `processor` | variable | image_processor.py | `f97396c64b5d` |
| `processor` | variable | multiple_image_processor.py | `8299ad7a3b71` |
| `processor` | variable | split_screen_processor.py | `49f0cd902dcf` |
| `processor` | variable | subtitle_processor.py | `22947dc8ce41` |
| `processor` | variable | subtitle_video_processor.py | `ffe82bd6f173` |
| `processor` | variable | video_filter_processor.py | `1c5504d304f9` |
| `processor` | variable | video_processor.py | `b862168ed82c` |
| `profile_name` | variable | insta-download.py | `6e1ca4959145` |
| `profile_reels_url` | variable | insta-download.py | `6a5b98480091` |
| `progress` | variable | easy-text-detection.py | `45804204addf` |
| `progress` | variable | multiple_image_processor.py | `4ea1dfed932e` |
| `progress` | variable | subtitle_video_processor.py | `c86371c0636c` |
| `progress` | variable | video_processor.py | `a8f27300d464` |
| `progress_interval` | variable | easy-text-detection.py | `7f317f1f71e6` |
| `progress_percent` | function | mixed_media_processor.py | `f81fa30827e4` |
| `progress_percent` | function | multiple_image_processor.py | `5f98a5d856e1` |
| `psutil` | import | canvas_processor.py | `f6b32ab9229e` |
| `psutil` | import | easy-text-detection.py | `f6b32ab9229e` |
| `psutil` | import | io_operations.py | `f6b32ab9229e` |
| `psutil` | import | video_filter_processor.py | `f6b32ab9229e` |
| `put` | function | cache_manager.py | `9a144c52066a` |
| `put` | function | queue_manager.py | `3ad01460dbc5` |
| `pydub.AudioSegment` | import | convert-audio-file.py | `a8a62585b41e` |
| `query` | variable | batch_video_normalizer.py | `a3add5f1d8ff` |
| `query_params` | variable | pinterest-download.py | `ed4ca36991ae` |
| `queue` | import | queue_manager.py | `90665960003f` |
| `queue` | import | temp_file_manager.py | `90665960003f` |
| `queue` | variable | queue_manager.py | `ef72e129faec` |
| `queue_manager` | variable | queue_manager.py | `f0dd26478022` |
| `queue_name` | variable | queue_manager.py | `0b15243e0d4a` |
| `queue_stats` | variable | main.py | `a0db8da8da3d` |
| `queue_stats` | variable | queue_manager.py | `6c59aa89fecd` |
| `queue_type` | variable | queue_manager.py | `170a9580dce9` |
| `random` | import | artistic_filters.py | `7e18ed429647` |
| `random` | import | cache_manager.py | `7e18ed429647` |
| `random` | import | combine-video.py | `7e18ed429647` |
| `random` | import | image-to-video.py | `7e18ed429647` |
| `random` | import | image_processor.py | `7e18ed429647` |
| `random` | import | main.py | `7e18ed429647` |
| `random` | import | multiple_image_processor.py | `7e18ed429647` |
| `random` | import | sequential_timing.py | `7e18ed429647` |
| `random` | import | sound_effects_processor.py | `7e18ed429647` |
| `random` | import | video_formatter.py | `7e18ed429647` |
| `random` | import | video_generator.py | `7e18ed429647` |
| `random` | import | video_processor.py | `7e18ed429647` |
| `randomize_and_rename_files` | function | image-to-video.py | `87dc666ae9af` |
| `randomized_count` | variable | image-to-video.py | `87af059ec3d7` |
| `rate` | variable | combine_video.py | `f09719c2d600` |
| `ratio` | variable | easy-text-detection.py | `bb0f0cd995ea` |
| `ratio` | variable | io_operations.py | `6e6eeeed69be` |
| `re` | import | convert-audio-file.py | `66ec018201fb` |
| `re` | import | insta-download.py | `66ec018201fb` |
| `read_file_content` | function | extract-code.py | `06e4e9703104` |
| `reader` | variable | easy-text-detection.py | `a6692798fda8` |
| `record` | variable | file-processor.py | `4c5c2bc82435` |
| `record` | variable | insta-download.py | `bd6634a0540c` |
| `record` | variable | pinterest-download.py | `d6cbc37df1a6` |
| `reencode_all_videos` | function | insta-download.py | `a40c8461cf0e` |
| `reencode_error_msg` | variable | file-processor.py | `39e6849cf872` |
| `reencode_video_ffmpeg` | function | file-processor.py | `6776bc27394f` |
| `reencode_video_with_ffmpeg` | function | insta-download.py | `6b305f2ab402` |
| `reencode_videos` | variable | insta-download.py | `d5048635da6f` |
| `reencoded_video_filename` | variable | file-processor.py | `a8fa184be6fb` |
| `reencoded_video_path` | variable | file-processor.py | `1adfacf1ef4b` |
| `reencoded_videos_dir` | variable | file-processor.py | `1fa912eb9fdc` |
| `region` | variable | artistic_filters.py | `4c1032f94963` |
| `register_filter` | function | filter_registry.py | `ca83131aa344` |
| `relative_path` | variable | batch_video_normalizer.py | `f2b71a9ef1b3` |
| `relative_path` | variable | extract-code.py | `cb70530e4bba` |
| `remaining` | variable | easy-text-detection.py | `357cf213d533` |
| `remove` | function | cache_manager.py | `3bf91ce824d9` |
| `remove_directory` | function | io_operations.py | `44cd7d94669f` |
| `removed_count` | variable | temp_file_manager.py | `5a0d8775e4db` |
| `repair_command` | variable | download-insta.py | `25ac4aa1f9df` |
| `repair_path` | variable | combine_video.py | `cf2e36186050` |
| `repair_video` | function | combine_video.py | `5d222e09e853` |
| `replace` | variable | easy-text-detection.py | `876e60483e19` |
| `reprocess_choice` | variable | batch_video_normalizer.py | `261e63433466` |
| `required_fields` | variable | filter_registry.py | `6b7694ac784c` |
| `required_fields` | variable | video_generator.py | `8031466f3638` |
| `reset_stats` | function | io_operations.py | `64e096d5dc97` |
| `resized` | variable | easy-text-detection.py | `2c8de748f133` |
| `resized` | variable | split_screen_processor.py | `84c95fa57ed7` |
| `resized` | variable | video_formatter.py | `80b95d9cb3e9` |
| `resized_image` | variable | image-to-video.py | `0213a68972a1` |
| `resolution` | variable | combine-video.py | `302f6cc5f80f` |
| `response` | variable | main.py | `dd448cac3c92` |
| `response` | variable | video_generator.py | `6b53210c36f5` |
| `result` | variable | artistic_filters.py | `4ecf625e7a38` |
| `result` | variable | audio_processor.py | `04e77438378a` |
| `result` | variable | batch_video_normalizer.py | `ee8c2a4ce42a` |
| `result` | variable | brightness_filters.py | `7d338e1e59df` |
| `result` | variable | canvas_processor.py | `1732d6fb1f98` |
| `result` | variable | color_filters.py | `a31cb2592ab2` |
| `result` | variable | combine-video.py | `46c2387ddc7e` |
| `result` | variable | combine_video.py | `d07c092787a5` |
| `result` | variable | easy-text-detection.py | `f7a9d91f2c9b` |
| `result` | variable | extract-audio.py | `45218fd2db94` |
| `result` | variable | file-processor.py | `39ac97d5d935` |
| `result` | variable | image-to-video.py | `240b0681c42b` |
| `result` | variable | image-video-encoder.py | `042c1550bd50` |
| `result` | variable | image_processor.py | `5f31ec935f39` |
| `result` | variable | insta-download.py | `a60e85a552ff` |
| `result` | variable | main.py | `a19e01cddc00` |
| `result` | variable | mixed_media_processor.py | `171710c20fe0` |
| `result` | variable | multiple_image_processor.py | `c84c34db28ec` |
| `result` | variable | queue_manager.py | `0c31335072a5` |
| `result` | variable | sound_effects_processor.py | `fadfd47d087c` |
| `result` | variable | subtitle_processor.py | `79bc8f051c14` |
| `result` | variable | temp_file_manager.py | `eb892fef225a` |
| `result` | variable | video-transcribe.py | `e11c79afbace` |
| `result` | variable | video_filter_processor.py | `2acc3459390e` |
| `result` | variable | video_generator.py | `9f039ecaa0e8` |
| `result` | variable | video_processor.py | `b796194bfe14` |
| `result_data` | variable | audio_processor.py | `b84675def6d9` |
| `result_path` | variable | canvas_processor.py | `d74832bbb6b2` |
| `result_path` | variable | video_formatter.py | `0a78244b55f4` |
| `results` | variable | canvas_processor.py | `74eb2a303fa2` |
| `results` | variable | easy-text-detection.py | `a3715572d2aa` |
| `results` | variable | image-to-video.py | `bf850b9526b1` |
| `results` | variable | queue_manager.py | `965a76fe7fd1` |
| `results` | variable | video_filter_processor.py | `f42c237cbaa6` |
| `resume_choice` | variable | batch_video_normalizer.py | `9d4bea3f3379` |
| `resume_queue` | function | queue_manager.py | `332bcadd4fb7` |
| `retried` | variable | queue_manager.py | `d73c9f657baa` |
| `retry_dead_letter_tasks` | function | queue_manager.py | `2af6f5439bf7` |
| `retry_delay` | variable | queue_manager.py | `508b3385a780` |
| `retry_func` | function | queue_manager.py | `ce15d42e1922` |
| `retry_thread` | variable | queue_manager.py | `7ad669602262` |
| `root_folder` | variable | image-to-video.py | `82eb116fa4e2` |
| `root_path` | variable | batch_video_normalizer.py | `df6dcfa3d850` |
| `row` | variable | multiple_image_processor.py | `b1626aa2859f` |
| `run` | function | combine-video.py | `39c4011219de` |
| `run` | function | extract-audio.py | `a83e91f693b1` |
| `s_curve` | variable | brightness_filters.py | `9206e9a56638` |
| `safe_delete` | function | io_operations.py | `8c7cdc699a69` |
| `saturate_effect` | function | color_filters.py | `a6f89830e44c` |
| `saturation_factor` | variable | color_filters.py | `c43ddfaed583` |
| `save_centralized_json` | function | insta-download.py | `dc340d8084a4` |
| `save_centralized_json` | function | pinterest-download.py | `dc340d8084a4` |
| `save_file_sync` | function | temp_file_manager.py | `56ed4d82ca56` |
| `save_json_file` | function | file-processor.py | `20dae4fd9369` |
| `saved_cache_key` | variable | video_filter_processor.py | `e5bd4ce5a94d` |
| `scale` | variable | easy-text-detection.py | `d89dc4d9b97b` |
| `scale` | variable | image-to-video.py | `3201300d457d` |
| `scale_factor` | variable | video_formatter.py | `b5c911e61ee7` |
| `scale_filter` | variable | video_processor.py | `0eb475efef87` |
| `scale_height` | variable | image-to-video.py | `d7de1b0f7765` |
| `scale_width` | variable | image-to-video.py | `2443e5b85805` |
| `scan_directory` | function | extract-code.py | `567786d5348c` |
| `scipy.ndimage.gaussian_filter1d` | import | audio_processor.py | `1b5d27bc9a0a` |
| `scipy.ndimage.gaussian_filter1d` | import | vocal_processor.py | `1b5d27bc9a0a` |
| `script_base_output_dir` | variable | insta-download.py | `ea07eca07b04` |
| `search_term` | variable | pinterest-download.py | `2effa5c9bbca` |
| `segment` | variable | video_processor.py | `b47736ed206d` |
| `segment_duration` | variable | image_processor.py | `1d2b771c87aa` |
| `segment_duration` | variable | video_processor.py | `fa7a3f5bc061` |
| `segment_durations` | variable | sequential_timing.py | `3f1d16e25d16` |
| `segment_file` | variable | detect-text.py | `f06fa1ab9e76` |
| `segment_filename` | variable | video_processor.py | `6a18f04afb4b` |
| `segment_files` | variable | detect-text.py | `a210c7ba8bb5` |
| `segment_indices` | variable | video_formatter.py | `ed1cb1869890` |
| `segment_params` | variable | image_processor.py | `4df4d22b27be` |
| `segment_params` | variable | video_processor.py | `6ff475bbae61` |
| `segment_path` | variable | multiple_image_processor.py | `c58d5fdf5f83` |
| `segment_path` | variable | video_processor.py | `6075a562dc19` |
| `segment_paths` | variable | image_processor.py | `d37e29e273bc` |
| `segment_paths` | variable | multiple_image_processor.py | `ed8dfe93d4a8` |
| `segment_timings` | variable | image_processor.py | `21cc947d35e2` |
| `segment_timings` | variable | video_processor.py | `ab9ea4e75e51` |
| `segment_words` | variable | subtitle_processor.py | `652f5270474d` |
| `segments` | variable | detect-text.py | `56e395e3c3cd` |
| `segments` | variable | main.py | `dbf05c5ae9ac` |
| `segments` | variable | video_processor.py | `6df304711bb8` |
| `selected_filters` | variable | video_filter_processor.py | `47cee96ddd7b` |
| `selected_images` | variable | multiple_image_processor.py | `14d1519227ab` |
| `selected_indices` | variable | video_filter_processor.py | `13a61a92a4f7` |
| `selected_preset` | variable | video_filter_processor.py | `726a3ed9db30` |
| `selected_sound` | variable | sound_effects_processor.py | `0654ada38a89` |
| `selected_timings` | variable | multiple_image_processor.py | `9ff6607163c3` |
| `selected_video` | variable | video_processor.py | `dd7805a5595c` |
| `selection` | variable | video_filter_processor.py | `63b54362eb49` |
| `sensitivity_map` | variable | arg_parser.py | `42a77e70113c` |
| `sepia_effect` | function | color_filters.py | `9bf32e9a843e` |
| `sepia_frame` | variable | color_filters.py | `1250cda7bcac` |
| `sepia_matrix` | variable | color_filters.py | `708321348ac0` |
| `sequential_timing.get_sequential_timing` | import | video_processor.py | `de951b91b0e4` |
| `session_id` | variable | canvas_processor.py | `6f831080f4a2` |
| `session_id` | variable | image-to-video.py | `3617828edf3a` |
| `session_id` | variable | mixed_media_processor.py | `048e47530286` |
| `session_id` | variable | multiple_image_processor.py | `c9d6277ca74b` |
| `session_id` | variable | video_filter_processor.py | `3bcaabb6b000` |
| `session_id` | variable | video_generator.py | `84837fd14a22` |
| `session_id` | variable | video_processor.py | `ac8172737c65` |
| `setup_output_directory` | function | combine-video.py | `7fddc828b165` |
| `shadow_highlight_effect` | function | brightness_filters.py | `ba99b7007482` |
| `shadow_lift` | variable | brightness_filters.py | `f606af0da2f5` |
| `shadow_mask` | variable | brightness_filters.py | `e0ee260b83b2` |
| `shadow_mask` | variable | color_filters.py | `5b06e34f53e0` |
| `shadow_params` | variable | canvas_processor.py | `65d1e98f7c52` |
| `shadows` | variable | brightness_filters.py | `6efedde029c1` |
| `sharpen_effect` | function | artistic_filters.py | `fc19e4c04ff6` |
| `sharpened` | variable | artistic_filters.py | `8f07290488d1` |
| `short_phrase_count` | variable | subtitle_processor.py | `302defc8bc50` |
| `short_phrase_subtitles` | variable | subtitle_processor.py | `0339a2341cf2` |
| `should_ignore_path` | function | extract-code.py | `2ef2404608c8` |
| `should_use_gpu` | variable | file-processor.py | `fcb9916325be` |
| `shutdown` | function | cache_manager.py | `9accba4345a0` |
| `shutdown` | function | queue_manager.py | `d07fcbaefaab` |
| `shutil` | import | batch_video_normalizer.py | `582f9ff727d7` |
| `shutil` | import | canvas_processor.py | `582f9ff727d7` |
| `shutil` | import | combine-video.py | `582f9ff727d7` |
| `shutil` | import | download-insta.py | `582f9ff727d7` |
| `shutil` | import | easy-text-detection.py | `582f9ff727d7` |
| `shutil` | import | file-processor.py | `582f9ff727d7` |
| `shutil` | import | image-to-video.py | `582f9ff727d7` |
| `shutil` | import | image-video-encoder.py | `582f9ff727d7` |
| `shutil` | import | image_processor.py | `582f9ff727d7` |
| `shutil` | import | insta-download.py | `582f9ff727d7` |
| `shutil` | import | io_operations.py | `582f9ff727d7` |
| `shutil` | import | mixed_media_processor.py | `582f9ff727d7` |
| `shutil` | import | multiple_image_processor.py | `582f9ff727d7` |
| `shutil` | import | pinterest-download.py | `582f9ff727d7` |
| `shutil` | import | temp_file_manager.py | `582f9ff727d7` |
| `sig` | variable | filter_registry.py | `5ef214fa1cc1` |
| `signal` | import | main.py | `10f4eea8db43` |
| `simple_copy_images` | function | image-to-video.py | `1a79c9dc62da` |
| `size` | variable | cache_manager.py | `2ea81236d9f6` |
| `size` | variable | canvas_processor.py | `b45e7c8c0171` |
| `size_bytes` | variable | batch_video_normalizer.py | `333111067195` |
| `size_bytes` | variable | image-video-encoder.py | `8204c936b99b` |
| `size_change` | variable | batch_video_normalizer.py | `2524faf0270a` |
| `size_change` | variable | image-video-encoder.py | `800ad69098d9` |
| `size_change_percent` | variable | batch_video_normalizer.py | `0cf6f97a7985` |
| `size_change_percent` | variable | image-video-encoder.py | `b5cb5b38415c` |
| `size_factor` | variable | canvas_processor.py | `5854174e166e` |
| `size_mb` | variable | batch_video_normalizer.py | `d414f715347f` |
| `size_mb` | variable | combine-video.py | `a3ea355b0270` |
| `size_mb` | variable | extract-audio.py | `b33a5d43faa2` |
| `size_mb` | variable | image-video-encoder.py | `a07cc8cd8d1a` |
| `sizes` | variable | subtitle_design_manager.py | `dd2acb35c53f` |
| `skipped_count` | variable | file-processor.py | `0d0ad3a7536c` |
| `smooth_signal` | function | audio_processor.py | `0eca3f4f9249` |
| `smooth_signal` | function | vocal_processor.py | `33a029b3fea3` |
| `sobel_x` | variable | artistic_filters.py | `5218e17799b6` |
| `sobel_y` | variable | artistic_filters.py | `d069390734e9` |
| `sorted_entries` | variable | temp_file_manager.py | `88c1c68bf3a1` |
| `sorted_groups` | variable | combine-video.py | `423ddd6624b8` |
| `sound_mode` | variable | sound_effects_processor.py | `de2de405978e` |
| `sounds` | variable | sound_effects_processor.py | `1f133157197b` |
| `source` | variable | io_operations.py | `288f8131e78a` |
| `special_files` | variable | extract-code.py | `9a8211877e72` |
| `split_into_paragraphs` | function | convert-audio-file.py | `03d3e7ae5c97` |
| `sqlite3` | import | batch_video_normalizer.py | `cc7487a33558` |
| `sqlite3` | import | easy-text-detection.py | `cc7487a33558` |
| `sqlite3` | import | file-processor.py | `cc7487a33558` |
| `sqlite3` | import | image-to-video.py | `cc7487a33558` |
| `sqlite3` | import | insta-download.py | `cc7487a33558` |
| `sqlite3` | import | pinterest-download.py | `cc7487a33558` |
| `sqlite_db_path` | variable | insta-download.py | `8fb0101fd86f` |
| `sqlite_db_path` | variable | pinterest-download.py | `70e097f7fee3` |
| `src.processors.audio_processor.analyze_beats` | import | main.py | `a94d8f54c915` |
| `src.processors.audio_processor.analyze_beats` | import | video_generator.py | `a94d8f54c915` |
| `src.processors.canvas_processor.process_video_with_canvas` | import | main.py | `f3ec9c5b1d4d` |
| `src.processors.canvas_processor.process_video_with_canvas` | import | video_formatter.py | `f3ec9c5b1d4d` |
| `src.processors.image_processor.process_image` | import | video_generator.py | `0860c9576eed` |
| `src.processors.multiple_image_processor.process_multiple_images` | import | video_generator.py | `d6bc2eb50761` |
| `src.processors.split_screen_processor.SplitScreenProcessor` | import | main.py | `eaa9cdd6380c` |
| `src.processors.split_screen_processor.create_split_screen_video` | import | main.py | `9bae604ce472` |
| `src.processors.split_screen_processor.get_audio_preferences` | import | main.py | `025847556ed2` |
| `src.processors.split_screen_processor.get_fit_mode` | import | main.py | `a1e7657b2895` |
| `src.processors.subtitle_processor.generate_subtitles` | import | main.py | `21a187d2b25c` |
| `src.processors.subtitle_processor.generate_subtitles` | import | video_formatter.py | `21a187d2b25c` |
| `src.processors.subtitle_video_processor.add_subtitles_to_video` | import | main.py | `896ebeb516fb` |
| `src.processors.subtitle_video_processor.add_subtitles_to_video` | import | video_formatter.py | `896ebeb516fb` |
| `src.processors.video_formatter.format_menu` | import | main.py | `e194616c05be` |
| `src.processors.video_generator.generate_video` | import | main.py | `0259e9863e68` |
| `src.processors.video_processor.process_video` | import | video_generator.py | `9f11718c3699` |
| `src.processors.vocal_processor.detect_vocal_changes` | import | video_generator.py | `84d7e9d1e54b` |
| `src.utils.arg_parser.parse_arguments` | import | main.py | `5a61eea164fe` |
| `src.utils.cache_manager.CacheManager` | import | audio_processor.py | `45d99fb5400b` |
| `src.utils.cache_manager.CacheManager` | import | canvas_processor.py | `45d99fb5400b` |
| `src.utils.cache_manager.CacheManager` | import | image_processor.py | `45d99fb5400b` |
| `src.utils.cache_manager.CacheManager` | import | main.py | `45d99fb5400b` |
| `src.utils.cache_manager.CacheManager` | import | mixed_media_processor.py | `45d99fb5400b` |
| `src.utils.cache_manager.CacheManager` | import | multiple_image_processor.py | `45d99fb5400b` |
| `src.utils.cache_manager.CacheManager` | import | video_filter_processor.py | `45d99fb5400b` |
| `src.utils.cache_manager.CacheManager` | import | video_generator.py | `45d99fb5400b` |
| `src.utils.cache_manager.CacheManager` | import | video_processor.py | `45d99fb5400b` |
| `src.utils.io_operations.IOOperations` | import | main.py | `5958acd8bacb` |
| `src.utils.queue_manager.QueueManager` | import | main.py | `e30079541bab` |
| `src.utils.queue_manager.TaskStatus` | import | audio_processor.py | `d7680471f6db` |
| `src.utils.queue_manager.TaskStatus` | import | canvas_processor.py | `d7680471f6db` |
| `src.utils.queue_manager.TaskStatus` | import | image_processor.py | `d7680471f6db` |
| `src.utils.queue_manager.TaskStatus` | import | mixed_media_processor.py | `d7680471f6db` |
| `src.utils.queue_manager.TaskStatus` | import | multiple_image_processor.py | `d7680471f6db` |
| `src.utils.queue_manager.TaskStatus` | import | video_filter_processor.py | `d7680471f6db` |
| `src.utils.queue_manager.TaskStatus` | import | video_generator.py | `d7680471f6db` |
| `src.utils.queue_manager.TaskStatus` | import | video_processor.py | `d7680471f6db` |
| `src.utils.queue_manager.queue_manager` | import | audio_processor.py | `0323b6ccd7c3` |
| `src.utils.queue_manager.queue_manager` | import | canvas_processor.py | `0323b6ccd7c3` |
| `src.utils.queue_manager.queue_manager` | import | image_processor.py | `0323b6ccd7c3` |
| `src.utils.queue_manager.queue_manager` | import | main.py | `0323b6ccd7c3` |
| `src.utils.queue_manager.queue_manager` | import | mixed_media_processor.py | `0323b6ccd7c3` |
| `src.utils.queue_manager.queue_manager` | import | multiple_image_processor.py | `0323b6ccd7c3` |
| `src.utils.queue_manager.queue_manager` | import | video_filter_processor.py | `0323b6ccd7c3` |
| `src.utils.queue_manager.queue_manager` | import | video_generator.py | `0323b6ccd7c3` |
| `src.utils.queue_manager.queue_manager` | import | video_processor.py | `0323b6ccd7c3` |
| `src.utils.temp_file_manager.TaskPriority` | import | audio_processor.py | `0b5c99e92ed8` |
| `src.utils.temp_file_manager.TaskPriority` | import | canvas_processor.py | `0b5c99e92ed8` |
| `src.utils.temp_file_manager.TaskPriority` | import | image_processor.py | `0b5c99e92ed8` |
| `src.utils.temp_file_manager.TaskPriority` | import | mixed_media_processor.py | `0b5c99e92ed8` |
| `src.utils.temp_file_manager.TaskPriority` | import | multiple_image_processor.py | `0b5c99e92ed8` |
| `src.utils.temp_file_manager.TaskPriority` | import | video_filter_processor.py | `0b5c99e92ed8` |
| `src.utils.temp_file_manager.TaskPriority` | import | video_generator.py | `0b5c99e92ed8` |
| `src.utils.temp_file_manager.TaskPriority` | import | video_processor.py | `0b5c99e92ed8` |
| `src.utils.temp_file_manager.TaskType` | import | audio_processor.py | `41fc328bd601` |
| `src.utils.temp_file_manager.TaskType` | import | canvas_processor.py | `41fc328bd601` |
| `src.utils.temp_file_manager.TaskType` | import | image_processor.py | `41fc328bd601` |
| `src.utils.temp_file_manager.TaskType` | import | mixed_media_processor.py | `41fc328bd601` |
| `src.utils.temp_file_manager.TaskType` | import | multiple_image_processor.py | `41fc328bd601` |
| `src.utils.temp_file_manager.TaskType` | import | video_filter_processor.py | `41fc328bd601` |
| `src.utils.temp_file_manager.TaskType` | import | video_generator.py | `41fc328bd601` |
| `src.utils.temp_file_manager.TaskType` | import | video_processor.py | `41fc328bd601` |
| `src.utils.temp_file_manager.TempFileManager` | import | main.py | `ca937778ff5b` |
| `src.utils.temp_file_manager.temp_manager` | import | audio_processor.py | `71efb9f12f50` |
| `src.utils.temp_file_manager.temp_manager` | import | canvas_processor.py | `71efb9f12f50` |
| `src.utils.temp_file_manager.temp_manager` | import | image_processor.py | `71efb9f12f50` |
| `src.utils.temp_file_manager.temp_manager` | import | main.py | `71efb9f12f50` |
| `src.utils.temp_file_manager.temp_manager` | import | mixed_media_processor.py | `71efb9f12f50` |
| `src.utils.temp_file_manager.temp_manager` | import | multiple_image_processor.py | `71efb9f12f50` |
| `src.utils.temp_file_manager.temp_manager` | import | video_filter_processor.py | `71efb9f12f50` |
| `src.utils.temp_file_manager.temp_manager` | import | video_generator.py | `71efb9f12f50` |
| `src.utils.temp_file_manager.temp_manager` | import | video_processor.py | `71efb9f12f50` |
| `standardize_video` | function | combine_video.py | `200583949c64` |
| `start` | variable | detect-text.py | `5cc7db0fcad5` |
| `start` | variable | easy-text-detection.py | `d925c69f9a62` |
| `start_dt` | variable | easy-text-detection.py | `9f94a27fbfdf` |
| `start_generation_session` | function | video_generator.py | `ebd8c7f0c887` |
| `start_offset` | variable | sound_effects_processor.py | `05d71c9abe2c` |
| `start_processing` | function | easy-text-detection.py | `41411443ef97` |
| `start_processing_session` | function | canvas_processor.py | `8848bdb31499` |
| `start_processing_session` | function | mixed_media_processor.py | `a463f9b0f45a` |
| `start_processing_session` | function | multiple_image_processor.py | `995d4beb3fc8` |
| `start_processing_session` | function | video_filter_processor.py | `f9961fa0510e` |
| `start_processing_session` | function | video_processor.py | `d317eb88ddf2` |
| `start_time` | variable | audio_processor.py | `6dfdf41d2d6b` |
| `start_time` | variable | batch_video_normalizer.py | `0a626f091ffa` |
| `start_time` | variable | cache_manager.py | `27b78009ddf6` |
| `start_time` | variable | canvas_processor.py | `0851d5ccc380` |
| `start_time` | variable | detect-text.py | `268926a76c3f` |
| `start_time` | variable | easy-text-detection.py | `8c31ce5f9360` |
| `start_time` | variable | image-video-encoder.py | `db6edfb22b13` |
| `start_time` | variable | image_processor.py | `293e34e70ab6` |
| `start_time` | variable | io_operations.py | `593a3624a4b0` |
| `start_time` | variable | multiple_image_processor.py | `445ad5a45c92` |
| `start_time` | variable | queue_manager.py | `7656f7de27d2` |
| `start_time` | variable | subtitle_processor.py | `edfbc98362ae` |
| `start_time` | variable | subtitle_video_processor.py | `cc9676b99604` |
| `start_time` | variable | video-transcribe.py | `e8829afb284f` |
| `start_time` | variable | video_filter_processor.py | `b59cddd0c56c` |
| `start_time` | variable | video_formatter.py | `48416534f1f8` |
| `start_time` | variable | video_processor.py | `77588e07a11c` |
| `start_time_op` | variable | temp_file_manager.py | `236c07916b3c` |
| `stat` | import | io_operations.py | `f9e42ccd54cc` |
| `stat_info` | variable | io_operations.py | `18c47cb38b5b` |
| `stats` | variable | batch_video_normalizer.py | `c361262905fb` |
| `stats` | variable | cache_manager.py | `455fba7c3abb` |
| `stats` | variable | canvas_processor.py | `63aeeb2dd366` |
| `stats` | variable | filter_registry.py | `d8b9f3478ad3` |
| `stats` | variable | image-to-video.py | `7032ab3a2324` |
| `stats` | variable | multiple_image_processor.py | `e41d0251dfdc` |
| `stats` | variable | queue_manager.py | `1ed4b94c76ae` |
| `stats` | variable | video_filter_processor.py | `26d6065f0cf9` |
| `stats` | variable | video_processor.py | `558c6c9b12ef` |
| `stats_worker` | variable | temp_file_manager.py | `f51b343af5ec` |
| `status` | variable | combine-video.py | `149c728fcf4c` |
| `status` | variable | easy-text-detection.py | `172e28da8508` |
| `status` | variable | queue_manager.py | `58691f38fc19` |
| `step` | variable | artistic_filters.py | `d2c6b84dfa40` |
| `strategies` | variable | cache_manager.py | `316b3980eb16` |
| `stream` | variable | combine_video.py | `8c4ad3db0b90` |
| `stream` | variable | mixed_media_processor.py | `ac8be68f39c0` |
| `stretched` | variable | brightness_filters.py | `fb898b6d34fe` |
| `sub_count` | variable | video_formatter.py | `f7187e5c156b` |
| `sub_length` | variable | video_formatter.py | `2d1a0f48dcdb` |
| `sub_output_path` | variable | video_formatter.py | `700df5dcdd98` |
| `subclip` | variable | video_formatter.py | `2fd60acc216c` |
| `subindent` | variable | combine-video.py | `9fe606a96631` |
| `submit_concat_task` | function | temp_file_manager.py | `e7d508495011` |
| `submit_extract_task` | function | temp_file_manager.py | `468d6359d5d3` |
| `submit_filter_task` | function | temp_file_manager.py | `49abdfd8df88` |
| `submit_task` | function | queue_manager.py | `b872a3c915e4` |
| `subprocess` | import | batch_video_normalizer.py | `7d8752c4c7ea` |
| `subprocess` | import | canvas_processor.py | `7d8752c4c7ea` |
| `subprocess` | import | combine-video.py | `7d8752c4c7ea` |
| `subprocess` | import | combine_video.py | `7d8752c4c7ea` |
| `subprocess` | import | detect-text.py | `7d8752c4c7ea` |
| `subprocess` | import | download-insta.py | `7d8752c4c7ea` |
| `subprocess` | import | easy-text-detection.py | `7d8752c4c7ea` |
| `subprocess` | import | extract-audio.py | `7d8752c4c7ea` |
| `subprocess` | import | file-processor.py | `7d8752c4c7ea` |
| `subprocess` | import | image-to-video.py | `7d8752c4c7ea` |
| `subprocess` | import | image-video-encoder.py | `7d8752c4c7ea` |
| `subprocess` | import | image_processor.py | `7d8752c4c7ea` |
| `subprocess` | import | insta-download.py | `7d8752c4c7ea` |
| `subprocess` | import | main.py | `7d8752c4c7ea` |
| `subprocess` | import | mixed_media_processor.py | `7d8752c4c7ea` |
| `subprocess` | import | multiple_image_processor.py | `7d8752c4c7ea` |
| `subprocess` | import | pinterest-download.py | `7d8752c4c7ea` |
| `subprocess` | import | temp_file_manager.py | `7d8752c4c7ea` |
| `subprocess` | import | video_generator.py | `7d8752c4c7ea` |
| `subprocess` | import | video_processor.py | `7d8752c4c7ea` |
| `subtitle` | variable | canvas_processor.py | `d28ebcf51dc6` |
| `subtitle_clips` | variable | subtitle_video_processor.py | `fdce5a7a412b` |
| `subtitle_design_manager.SubtitleDesignManager` | import | subtitle_video_processor.py | `6ffc9fda5e73` |
| `subtitle_json` | variable | main.py | `16a74d350c21` |
| `subtitle_json` | variable | video_formatter.py | `0ab8708f0e0a` |
| `subtitle_mode` | variable | subtitle_video_processor.py | `e660216b5662` |
| `subtitle_modes` | variable | subtitle_processor.py | `620e69c19f12` |
| `subtitles` | variable | subtitle_video_processor.py | `20acd2e8c7aa` |
| `success` | variable | batch_video_normalizer.py | `ea54af86ee7f` |
| `success` | variable | canvas_processor.py | `76a3d105486d` |
| `success` | variable | convert-audio-file.py | `aa45e96d9d14` |
| `success` | variable | detect-text.py | `f1728cf6dc43` |
| `success` | variable | easy-text-detection.py | `52c2f6f6c60f` |
| `success` | variable | extract-audio.py | `604d23a56f44` |
| `success` | variable | image_processor.py | `ca643d38e33d` |
| `success` | variable | main.py | `26e61900ccd8` |
| `success` | variable | multiple_image_processor.py | `cd755aaa5fed` |
| `success` | variable | temp_file_manager.py | `4a30ddb9f7fb` |
| `success` | variable | video_processor.py | `664991c5f8e7` |
| `successful_count` | variable | image-video-encoder.py | `6b2e4f6f3e00` |
| `successful_groups` | variable | combine-video.py | `83faede38418` |
| `successful_reencodes` | variable | insta-download.py | `56c4c16fe640` |
| `successful_videos` | variable | combine_video.py | `ecb830f39cdd` |
| `successfully_processed_files` | variable | image-video-encoder.py | `baf96741be55` |
| `summary` | variable | easy-text-detection.py | `b368c8261b3c` |
| `supported_extensions` | variable | download-insta.py | `1d31eb71cfeb` |
| `sync_choice` | variable | main.py | `75e583975caf` |
| `sync_mode` | variable | main.py | `db5017d3bd59` |
| `sys` | import | arg_parser.py | `9e77b3746ea0` |
| `sys` | import | easy-text-detection.py | `9e77b3746ea0` |
| `sys` | import | extract-audio.py | `9e77b3746ea0` |
| `sys` | import | extract-code.py | `9e77b3746ea0` |
| `sys` | import | file-test.py | `9e77b3746ea0` |
| `sys` | import | image-to-video.py | `9e77b3746ea0` |
| `sys` | import | main.py | `9e77b3746ea0` |
| `target` | variable | io_operations.py | `c94efe4ca640` |
| `target_aspect` | variable | easy-text-detection.py | `f47b87482f4c` |
| `target_codec` | variable | batch_video_normalizer.py | `47e20e33d955` |
| `target_format` | variable | batch_video_normalizer.py | `fd24c83e64c6` |
| `target_format` | variable | image-video-encoder.py | `5f54f54d2b67` |
| `target_format` | variable | video_formatter.py | `b3d62ad8a355` |
| `target_path` | variable | file-test.py | `332393a19e52` |
| `target_ratio` | variable | image_processor.py | `6954d724dfa5` |
| `target_ratio` | variable | multiple_image_processor.py | `e3c576ea2b5e` |
| `target_ratio` | variable | split_screen_processor.py | `56bd7ece6e38` |
| `target_ratio` | variable | video_formatter.py | `6ca16a359148` |
| `target_size` | variable | main.py | `407c7b88a6dc` |
| `target_size` | variable | mixed_media_processor.py | `043eb551232b` |
| `target_size` | variable | split_screen_processor.py | `2c0ae224ddf8` |
| `target_size` | variable | video_formatter.py | `a7f58bf197c8` |
| `task` | variable | queue_manager.py | `ecf52c8fb943` |
| `task` | variable | temp_file_manager.py | `5bf8cb4b3665` |
| `task_data` | variable | canvas_processor.py | `b4edd44ec839` |
| `task_id` | variable | canvas_processor.py | `142e4012fce5` |
| `task_id` | variable | queue_manager.py | `4db07d51d007` |
| `task_id` | variable | temp_file_manager.py | `68167057bbee` |
| `task_id` | variable | video_filter_processor.py | `23365c1f121e` |
| `task_ids` | variable | canvas_processor.py | `bdd67c3da93a` |
| `task_ids` | variable | queue_manager.py | `454b904f71ed` |
| `task_ids` | variable | video_filter_processor.py | `da2077b3b14e` |
| `task_result` | variable | queue_manager.py | `7f38ab26c92b` |
| `task_worker` | variable | temp_file_manager.py | `547b2d25ea38` |
| `tasks_to_queue` | variable | queue_manager.py | `eb776b425a39` |
| `tasks_to_retry` | variable | queue_manager.py | `67b7d938e3be` |
| `temp` | variable | multiple_image_processor.py | `85791b74f26c` |
| `temp_audio_path` | variable | subtitle_processor.py | `47ea9d5dde0b` |
| `temp_audio_path` | variable | video-transcribe.py | `027d0d702bba` |
| `temp_composite_path` | variable | multiple_image_processor.py | `50ee8fdbaa65` |
| `temp_dir` | variable | detect-text.py | `d03dd914a328` |
| `temp_dir` | variable | mixed_media_processor.py | `e805d88452b6` |
| `temp_dir` | variable | temp_file_manager.py | `72a93f81d71c` |
| `temp_dirs` | variable | io_operations.py | `b9d4a2b080f7` |
| `temp_file` | variable | audio_processor.py | `6377d60d6c35` |
| `temp_files` | variable | canvas_processor.py | `2888c6e43dab` |
| `temp_manager` | variable | temp_file_manager.py | `7deb8f74ba18` |
| `temp_output` | variable | batch_video_normalizer.py | `51815e48f037` |
| `temp_output` | variable | image-video-encoder.py | `f56539d7bb44` |
| `temp_output` | variable | mixed_media_processor.py | `598127a6186c` |
| `temp_output` | variable | video_generator.py | `7186a9c2acb2` |
| `temp_path` | variable | io_operations.py | `eeeb2ef9d981` |
| `temp_path` | variable | video_formatter.py | `f1d6c1affe5d` |
| `temp_video` | variable | video_generator.py | `6e30cdcbbb61` |
| `temp_video_path` | variable | download-insta.py | `51cc37f06404` |
| `temp_video_path` | variable | mixed_media_processor.py | `7fea8ed0886b` |
| `temperature_effect` | function | color_filters.py | `de160ff8a2c7` |
| `tempfile` | import | canvas_processor.py | `09d25239ae3d` |
| `tempfile` | import | image_processor.py | `09d25239ae3d` |
| `tempfile` | import | io_operations.py | `09d25239ae3d` |
| `tempfile` | import | mixed_media_processor.py | `09d25239ae3d` |
| `tempfile` | import | subtitle_processor.py | `09d25239ae3d` |
| `tempfile` | import | temp_file_manager.py | `09d25239ae3d` |
| `tempfile` | import | video-transcribe.py | `09d25239ae3d` |
| `tempfile` | import | video_processor.py | `09d25239ae3d` |
| `test_clip` | variable | subtitle_video_processor.py | `d8d02624e0a8` |
| `test_ffmpeg_command` | function | easy-text-detection.py | `b69b632b2ed6` |
| `test_single` | variable | easy-text-detection.py | `04197181eafc` |
| `text` | variable | convert-audio-file.py | `a288078cb6cf` |
| `text` | variable | subtitle_processor.py | `5fda7e2252f5` |
| `text` | variable | subtitle_video_processor.py | `7a7302c9f371` |
| `text` | variable | video-transcribe.py | `866b636015cb` |
| `text_color` | variable | canvas_processor.py | `3b816736912e` |
| `text_color` | variable | subtitle_video_processor.py | `4f4afd55d1cf` |
| `text_contours` | variable | detect-text.py | `0c85ceabfb43` |
| `text_detected` | variable | detect-text.py | `33f64a64680f` |
| `text_frames` | variable | easy-text-detection.py | `dd180655a73c` |
| `text_intervals` | variable | easy-text-detection.py | `a9b16d6d0a58` |
| `text_overlays` | variable | canvas_processor.py | `41fb9747ca78` |
| `text_percentage` | variable | easy-text-detection.py | `a8b205458ab5` |
| `text_prefs` | variable | canvas_processor.py | `9ecda0dc7aa8` |
| `text_regions` | variable | detect-text.py | `681236a08b31` |
| `text_segments` | variable | detect-text.py | `0917bd26ad24` |
| `text_temp` | variable | canvas_processor.py | `aef1ce9261b3` |
| `text_time` | variable | canvas_processor.py | `a96b9c0175a9` |
| `text_usage` | variable | canvas_processor.py | `e4cf9ec38f0f` |
| `threading` | import | audio_processor.py | `90781f3efdcb` |
| `threading` | import | cache_manager.py | `90781f3efdcb` |
| `threading` | import | canvas_processor.py | `90781f3efdcb` |
| `threading` | import | image_processor.py | `90781f3efdcb` |
| `threading` | import | io_operations.py | `90781f3efdcb` |
| `threading` | import | mixed_media_processor.py | `90781f3efdcb` |
| `threading` | import | multiple_image_processor.py | `90781f3efdcb` |
| `threading` | import | queue_manager.py | `90781f3efdcb` |
| `threading` | import | temp_file_manager.py | `90781f3efdcb` |
| `threading` | import | video_filter_processor.py | `90781f3efdcb` |
| `threading` | import | video_processor.py | `90781f3efdcb` |
| `thresh` | variable | detect-text.py | `64979af448c6` |
| `time` | import | audio_processor.py | `4f9b8491ba4d` |
| `time` | import | batch_video_normalizer.py | `4f9b8491ba4d` |
| `time` | import | cache_manager.py | `4f9b8491ba4d` |
| `time` | import | canvas_processor.py | `4f9b8491ba4d` |
| `time` | import | convert-audio-file.py | `4f9b8491ba4d` |
| `time` | import | image-video-encoder.py | `4f9b8491ba4d` |
| `time` | import | image_processor.py | `4f9b8491ba4d` |
| `time` | import | io_operations.py | `4f9b8491ba4d` |
| `time` | import | main.py | `4f9b8491ba4d` |
| `time` | import | mixed_media_processor.py | `4f9b8491ba4d` |
| `time` | import | multiple_image_processor.py | `4f9b8491ba4d` |
| `time` | import | queue_manager.py | `4f9b8491ba4d` |
| `time` | import | temp_file_manager.py | `4f9b8491ba4d` |
| `time` | import | video_filter_processor.py | `4f9b8491ba4d` |
| `time` | import | video_generator.py | `4f9b8491ba4d` |
| `time` | import | video_processor.py | `4f9b8491ba4d` |
| `time_per_word` | variable | subtitle_processor.py | `fc49f13f50ac` |
| `time_per_word` | variable | video-transcribe.py | `7ae9b7ed1dc2` |
| `time_since_access` | function | cache_manager.py | `9b2c35fc301d` |
| `time_window` | variable | queue_manager.py | `1e3d370ad442` |
| `timestamp` | variable | combine-video.py | `389892b153ac` |
| `timing_points` | variable | video_generator.py | `78753b5ba797` |
| `tint_effect` | function | color_filters.py | `12ba0acd56b1` |
| `tint_overlay` | variable | color_filters.py | `cbb3f76aebbe` |
| `title` | variable | canvas_processor.py | `298219b0d284` |
| `torch` | import | easy-text-detection.py | `cf1070d3a16f` |
| `total_duration` | variable | detect-text.py | `7e16eb5be2bd` |
| `total_files` | variable | file-test.py | `25061eb53013` |
| `total_frames` | variable | detect-text.py | `94af16af922d` |
| `total_frames` | variable | easy-text-detection.py | `35fe551dbac3` |
| `total_images` | variable | multiple_image_processor.py | `9f6997c33465` |
| `total_original_size` | variable | image-video-encoder.py | `e9f3c05826f7` |
| `total_processed_size` | variable | image-video-encoder.py | `6c3071bf5513` |
| `total_requests` | variable | cache_manager.py | `6953b4627b8b` |
| `total_requests` | variable | canvas_processor.py | `47fd64219805` |
| `total_segments` | variable | video_processor.py | `3dfc379424fd` |
| `total_size` | variable | video_generator.py | `bd4843f4ee7d` |
| `total_sounds` | variable | sound_effects_processor.py | `96d5ee1b29c6` |
| `total_stats` | variable | queue_manager.py | `6c6ac06c316c` |
| `total_subtitles` | variable | subtitle_video_processor.py | `fb87b6e914e3` |
| `total_text_duration` | variable | detect-text.py | `3bcb7543b548` |
| `total_time` | variable | canvas_processor.py | `e519aad4e899` |
| `total_videos` | variable | combine-video.py | `fa00a207e3c4` |
| `total_videos` | variable | easy-text-detection.py | `960626a0caf0` |
| `touch` | function | cache_manager.py | `6d18979c82d3` |
| `traceback` | import | easy-text-detection.py | `6a6eacd0dfa2` |
| `traceback` | import | main.py | `6a6eacd0dfa2` |
| `traceback` | import | split_screen_processor.py | `6a6eacd0dfa2` |
| `transcribe_audio` | function | subtitle_processor.py | `42677ba7f25c` |
| `transcribe_video` | function | subtitle_processor.py | `64d40b5419b3` |
| `transcribe_video` | function | video-transcribe.py | `9a7df6d2c5e5` |
| `transcription` | variable | video-transcribe.py | `fd2d61bab7bf` |
| `transition_filters` | variable | multiple_image_processor.py | `c52f683c47f0` |
| `transition_types` | variable | multiple_image_processor.py | `88b18b022d72` |
| `ttl` | variable | cache_manager.py | `a64d3649ed8c` |
| `txt_clip` | variable | subtitle_video_processor.py | `4ba1aca03d60` |
| `typing.Any` | import | arg_parser.py | `4ec2ae0495c2` |
| `typing.Any` | import | audio_processor.py | `4ec2ae0495c2` |
| `typing.Any` | import | cache_manager.py | `4ec2ae0495c2` |
| `typing.Any` | import | canvas_processor.py | `4ec2ae0495c2` |
| `typing.Any` | import | filter_registry.py | `4ec2ae0495c2` |
| `typing.Any` | import | io_operations.py | `4ec2ae0495c2` |
| `typing.Any` | import | mixed_media_processor.py | `4ec2ae0495c2` |
| `typing.Any` | import | queue_manager.py | `4ec2ae0495c2` |
| `typing.Any` | import | temp_file_manager.py | `4ec2ae0495c2` |
| `typing.Any` | import | video_filter_processor.py | `4ec2ae0495c2` |
| `typing.Callable` | import | cache_manager.py | `60ed66b7a141` |
| `typing.Callable` | import | filter_registry.py | `60ed66b7a141` |
| `typing.Callable` | import | queue_manager.py | `60ed66b7a141` |
| `typing.Callable` | import | temp_file_manager.py | `60ed66b7a141` |
| `typing.Dict` | import | arg_parser.py | `db5e932b3c49` |
| `typing.Dict` | import | audio_processor.py | `db5e932b3c49` |
| `typing.Dict` | import | cache_manager.py | `db5e932b3c49` |
| `typing.Dict` | import | canvas_processor.py | `db5e932b3c49` |
| `typing.Dict` | import | combine-video.py | `db5e932b3c49` |
| `typing.Dict` | import | combine_video.py | `db5e932b3c49` |
| `typing.Dict` | import | filter_registry.py | `db5e932b3c49` |
| `typing.Dict` | import | image_processor.py | `db5e932b3c49` |
| `typing.Dict` | import | io_operations.py | `db5e932b3c49` |
| `typing.Dict` | import | mixed_media_processor.py | `db5e932b3c49` |
| `typing.Dict` | import | multiple_image_processor.py | `db5e932b3c49` |
| `typing.Dict` | import | queue_manager.py | `db5e932b3c49` |
| `typing.Dict` | import | sound_effects_processor.py | `db5e932b3c49` |
| `typing.Dict` | import | split_screen_processor.py | `db5e932b3c49` |
| `typing.Dict` | import | subtitle_processor.py | `db5e932b3c49` |
| `typing.Dict` | import | subtitle_video_processor.py | `db5e932b3c49` |
| `typing.Dict` | import | temp_file_manager.py | `db5e932b3c49` |
| `typing.Dict` | import | video_filter_processor.py | `db5e932b3c49` |
| `typing.Dict` | import | video_generator.py | `db5e932b3c49` |
| `typing.Dict` | import | video_processor.py | `db5e932b3c49` |
| `typing.List` | import | audio_processor.py | `eada0f80bf58` |
| `typing.List` | import | cache_manager.py | `eada0f80bf58` |
| `typing.List` | import | canvas_processor.py | `eada0f80bf58` |
| `typing.List` | import | combine-video.py | `eada0f80bf58` |
| `typing.List` | import | filter_registry.py | `eada0f80bf58` |
| `typing.List` | import | image_processor.py | `eada0f80bf58` |
| `typing.List` | import | io_operations.py | `eada0f80bf58` |
| `typing.List` | import | mixed_media_processor.py | `eada0f80bf58` |
| `typing.List` | import | multiple_image_processor.py | `eada0f80bf58` |
| `typing.List` | import | queue_manager.py | `eada0f80bf58` |
| `typing.List` | import | sequential_timing.py | `eada0f80bf58` |
| `typing.List` | import | sound_effects_processor.py | `eada0f80bf58` |
| `typing.List` | import | subtitle_processor.py | `eada0f80bf58` |
| `typing.List` | import | subtitle_video_processor.py | `eada0f80bf58` |
| `typing.List` | import | temp_file_manager.py | `eada0f80bf58` |
| `typing.List` | import | video_filter_processor.py | `eada0f80bf58` |
| `typing.List` | import | video_generator.py | `eada0f80bf58` |
| `typing.List` | import | video_processor.py | `eada0f80bf58` |
| `typing.Optional` | import | arg_parser.py | `abdbaea6ab57` |
| `typing.Optional` | import | audio_processor.py | `abdbaea6ab57` |
| `typing.Optional` | import | cache_manager.py | `abdbaea6ab57` |
| `typing.Optional` | import | canvas_processor.py | `abdbaea6ab57` |
| `typing.Optional` | import | combine_video.py | `abdbaea6ab57` |
| `typing.Optional` | import | filter_registry.py | `abdbaea6ab57` |
| `typing.Optional` | import | image_processor.py | `abdbaea6ab57` |
| `typing.Optional` | import | io_operations.py | `abdbaea6ab57` |
| `typing.Optional` | import | mixed_media_processor.py | `abdbaea6ab57` |
| `typing.Optional` | import | multiple_image_processor.py | `abdbaea6ab57` |
| `typing.Optional` | import | queue_manager.py | `abdbaea6ab57` |
| `typing.Optional` | import | sound_effects_processor.py | `abdbaea6ab57` |
| `typing.Optional` | import | subtitle_processor.py | `abdbaea6ab57` |
| `typing.Optional` | import | subtitle_video_processor.py | `abdbaea6ab57` |
| `typing.Optional` | import | temp_file_manager.py | `abdbaea6ab57` |
| `typing.Optional` | import | video_filter_processor.py | `abdbaea6ab57` |
| `typing.Optional` | import | video_formatter.py | `abdbaea6ab57` |
| `typing.Optional` | import | video_generator.py | `abdbaea6ab57` |
| `typing.Optional` | import | video_processor.py | `abdbaea6ab57` |
| `typing.Tuple` | import | audio_processor.py | `23996b744beb` |
| `typing.Tuple` | import | cache_manager.py | `23996b744beb` |
| `typing.Tuple` | import | canvas_processor.py | `23996b744beb` |
| `typing.Tuple` | import | combine-video.py | `23996b744beb` |
| `typing.Tuple` | import | combine_video.py | `23996b744beb` |
| `typing.Tuple` | import | image_processor.py | `23996b744beb` |
| `typing.Tuple` | import | io_operations.py | `23996b744beb` |
| `typing.Tuple` | import | mixed_media_processor.py | `23996b744beb` |
| `typing.Tuple` | import | multiple_image_processor.py | `23996b744beb` |
| `typing.Tuple` | import | queue_manager.py | `23996b744beb` |
| `typing.Tuple` | import | sequential_timing.py | `23996b744beb` |
| `typing.Tuple` | import | sound_effects_processor.py | `23996b744beb` |
| `typing.Tuple` | import | split_screen_processor.py | `23996b744beb` |
| `typing.Tuple` | import | subtitle_design_manager.py | `23996b744beb` |
| `typing.Tuple` | import | subtitle_video_processor.py | `23996b744beb` |
| `typing.Tuple` | import | temp_file_manager.py | `23996b744beb` |
| `typing.Tuple` | import | video_formatter.py | `23996b744beb` |
| `typing.Tuple` | import | video_generator.py | `23996b744beb` |
| `typing.Tuple` | import | video_processor.py | `23996b744beb` |
| `typing.Union` | import | artistic_filters.py | `26723ff1b972` |
| `typing.Union` | import | brightness_filters.py | `26723ff1b972` |
| `typing.Union` | import | cache_manager.py | `26723ff1b972` |
| `typing.Union` | import | color_filters.py | `26723ff1b972` |
| `typing.Union` | import | image_processor.py | `26723ff1b972` |
| `typing.Union` | import | io_operations.py | `26723ff1b972` |
| `typing.Union` | import | multiple_image_processor.py | `26723ff1b972` |
| `typing.Union` | import | preset_filters.py | `26723ff1b972` |
| `typing.Union` | import | queue_manager.py | `26723ff1b972` |
| `typing.Union` | import | subtitle_processor.py | `26723ff1b972` |
| `typing.Union` | import | temp_file_manager.py | `26723ff1b972` |
| `typing.Union` | import | video_filter_processor.py | `26723ff1b972` |
| `typing.Union` | import | video_generator.py | `26723ff1b972` |
| `typing.Union` | import | video_processor.py | `26723ff1b972` |
| `unique_uuid` | variable | image-to-video.py | `006d8ba141b7` |
| `update_avg_access_time` | function | cache_manager.py | `d9ae8c8e4d2a` |
| `update_completion` | function | queue_manager.py | `5b034800e7fa` |
| `update_fields` | variable | batch_video_normalizer.py | `912950ba8372` |
| `update_file_status` | function | batch_video_normalizer.py | `9d311a3a309e` |
| `update_hit_rate` | function | cache_manager.py | `e77306a3cffe` |
| `update_image_processing_status` | function | image-to-video.py | `91c77d0f921b` |
| `update_or_insert_processed_reel_sqlite` | function | file-processor.py | `ba21a6880fd8` |
| `update_reencoded_status` | function | insta-download.py | `d8142ab869b6` |
| `update_session_phase` | function | mixed_media_processor.py | `412031d5fc0b` |
| `update_session_phase` | function | video_generator.py | `d18454d46fe2` |
| `update_session_phase` | function | video_processor.py | `d18454d46fe2` |
| `update_session_progress` | function | mixed_media_processor.py | `4a67034aaa3a` |
| `update_simple_copy_status` | function | image-to-video.py | `eacdac2bd606` |
| `update_values` | variable | batch_video_normalizer.py | `5b0d54e933f6` |
| `update_video_creation_status` | function | image-to-video.py | `bab3a92728bf` |
| `urllib.parse.parse_qs` | import | pinterest-download.py | `4f8180effeba` |
| `urllib.parse.urlparse` | import | pinterest-download.py | `355246b66170` |
| `usable_height` | variable | image-to-video.py | `1f0158578dfb` |
| `usable_width` | variable | image-to-video.py | `ba565e161040` |
| `usage` | variable | io_operations.py | `fb51f2e4c2d3` |
| `usage_stats` | variable | canvas_processor.py | `31da9c23d5b1` |
| `use_canvas` | variable | canvas_processor.py | `e43e90e327b9` |
| `use_gpu` | variable | batch_video_normalizer.py | `d8dee632e0f5` |
| `use_gpu` | variable | easy-text-detection.py | `8de22c0fe96c` |
| `use_gpu_input` | variable | file-processor.py | `de24ff46e9cc` |
| `user_preferences` | variable | mixed_media_processor.py | `f5af8e5fc47f` |
| `uuid` | import | image-to-video.py | `8b76fbd04977` |
| `uuid` | import | queue_manager.py | `8b76fbd04977` |
| `uuid` | import | video_filter_processor.py | `8b76fbd04977` |
| `uuids` | variable | image-to-video.py | `8be5f2642448` |
| `valid_extensions` | variable | file_handler.py | `8bd587dd0a8c` |
| `valid_extensions` | variable | image_processor.py | `ceb95c4038f9` |
| `validate_args` | function | arg_parser.py | `61c6c674108c` |
| `validate_audio_path` | function | split_screen_processor.py | `81f6721c1778` |
| `validate_canvas_config` | function | canvas_processor.py | `b118696a98c5` |
| `validate_config` | function | video_generator.py | `69bf1e5f4ee6` |
| `validate_file_path` | function | file_handler.py | `961398577160` |
| `validate_filter_config` | function | video_filter_processor.py | `13561d3ac79a` |
| `validate_filter_function` | function | filter_registry.py | `76a91e55da10` |
| `validate_filter_metadata` | function | filter_registry.py | `13df60b3690e` |
| `validate_image_file` | function | image_processor.py | `2b0511d4de2f` |
| `validate_image_folder` | function | multiple_image_processor.py | `ba002ec7402a` |
| `validate_images_folder` | function | multiple_image_processor.py | `e7545299ebbe` |
| `validate_input_files` | function | main.py | `5967b269db45` |
| `validate_video_path` | function | split_screen_processor.py | `d345e91d5bcc` |
| `value` | variable | cache_manager.py | `a434615e2fa1` |
| `variation` | variable | sequential_timing.py | `b65addc30a36` |
| `verify_file_integrity` | function | io_operations.py | `e2ec6dbf5953` |
| `vid_id` | variable | easy-text-detection.py | `939fb50d7106` |
| `video` | variable | subtitle_processor.py | `5aadf0c8f63c` |
| `video` | variable | subtitle_video_processor.py | `3b99b31dbdac` |
| `video` | variable | video-transcribe.py | `389ee52fd03f` |
| `video` | variable | video_formatter.py | `57947adccf1c` |
| `video1` | variable | split_screen_processor.py | `b85586a86e3f` |
| `video1_fit_mode` | variable | split_screen_processor.py | `33b9698e7d74` |
| `video1_path` | variable | main.py | `2b250fffef5f` |
| `video1_path` | variable | split_screen_processor.py | `705b2b24d324` |
| `video1_pos` | variable | split_screen_processor.py | `8a65ffed1b71` |
| `video1_processed` | variable | split_screen_processor.py | `a92b20b4a188` |
| `video2` | variable | split_screen_processor.py | `f29e19515461` |
| `video2_fit_mode` | variable | split_screen_processor.py | `2cc2de02b9ec` |
| `video2_path` | variable | main.py | `97303a1e6bd1` |
| `video2_path` | variable | split_screen_processor.py | `f5f5401a27a5` |
| `video2_pos` | variable | split_screen_processor.py | `33b02c6a7780` |
| `video2_processed` | variable | split_screen_processor.py | `e4bf70c4c33a` |
| `video_clip` | variable | mixed_media_processor.py | `6ec64de839a5` |
| `video_extensions` | variable | batch_video_normalizer.py | `87d3854deda2` |
| `video_extensions` | variable | image-video-encoder.py | `239ee235d3ee` |
| `video_extensions` | variable | video_generator.py | `8b8a8ac87b46` |
| `video_filename` | variable | image-video-encoder.py | `150a3c19c9b3` |
| `video_filepath` | variable | insta-download.py | `ddfcb65741bf` |
| `video_filepath` | variable | pinterest-download.py | `03553227d355` |
| `video_files` | variable | combine-video.py | `de18c8aed8ba` |
| `video_files` | variable | combine_video.py | `024c6294535f` |
| `video_files` | variable | image-video-encoder.py | `af17d8c207f3` |
| `video_files` | variable | insta-download.py | `673703bab9be` |
| `video_files` | variable | mixed_media_processor.py | `92f0cedc13eb` |
| `video_files` | variable | pinterest-download.py | `5c7dd6cdce63` |
| `video_files` | variable | video_generator.py | `8c848499ef44` |
| `video_files` | variable | video_processor.py | `359d91a126ee` |
| `video_files_downloaded` | variable | insta-download.py | `b3e31b5cc755` |
| `video_filter` | variable | canvas_processor.py | `31b7bb56e383` |
| `video_format` | variable | main.py | `4a71952f55c1` |
| `video_format` | variable | split_screen_processor.py | `fcb859a362dc` |
| `video_generator.generate_video` | import | __init__.py | `6bcd760bfb3e` |
| `video_groups` | variable | combine-video.py | `912b197bf4d7` |
| `video_index` | variable | video_processor.py | `b30aa5328ca9` |
| `video_info` | variable | canvas_processor.py | `bc593e48e1ea` |
| `video_info` | variable | easy-text-detection.py | `fb09bb004f50` |
| `video_info` | variable | main.py | `48ed35bb8eb2` |
| `video_info` | variable | mixed_media_processor.py | `d02f15b1cfc2` |
| `video_info` | variable | video_generator.py | `72723032eeec` |
| `video_info` | variable | video_processor.py | `2131c30f39f0` |
| `video_output_filename` | variable | image-video-encoder.py | `6b4009c20bc1` |
| `video_output_path` | variable | image-video-encoder.py | `93bc5a88778e` |
| `video_path` | variable | combine-video.py | `adc4a95ec415` |
| `video_path` | variable | combine_video.py | `11e1229ad6f8` |
| `video_path` | variable | detect-text.py | `5a38ad04c44b` |
| `video_path` | variable | extract-audio.py | `c98d3042ca92` |
| `video_path` | variable | image-to-video.py | `27db99c28f20` |
| `video_path` | variable | main.py | `b7642f4f1476` |
| `video_path` | variable | video-transcribe.py | `554c0d6dec83` |
| `video_path_obj` | variable | detect-text.py | `8c609e72f9cd` |
| `video_paths` | variable | main.py | `5641b22e09b6` |
| `video_processor.process_video` | import | __init__.py | `c74b770fc47a` |
| `video_processor.process_video` | import | mixed_media_processor.py | `c74b770fc47a` |
| `video_size` | variable | subtitle_video_processor.py | `181a74fe403a` |
| `video_start_time` | variable | video_processor.py | `89968f63027a` |
| `video_stream` | variable | batch_video_normalizer.py | `974e189fc94b` |
| `video_stream` | variable | canvas_processor.py | `2a8b4724b633` |
| `video_stream` | variable | combine-video.py | `9b1de7ee1791` |
| `video_stream` | variable | image-video-encoder.py | `6cb140ea9898` |
| `video_stream` | variable | main.py | `b2682d4d2fdb` |
| `video_stream` | variable | mixed_media_processor.py | `5e102357f417` |
| `video_stream` | variable | temp_file_manager.py | `51107f11cf3d` |
| `video_stream` | variable | video_generator.py | `b2682d4d2fdb` |
| `video_stream` | variable | video_processor.py | `5591eca46755` |
| `video_target_size` | variable | split_screen_processor.py | `d54c87e07fe2` |
| `video_time` | variable | video_generator.py | `a04fdd006ee1` |
| `video_to_extract_from` | variable | file-processor.py | `0409dbc14804` |
| `video_url` | variable | insta-download.py | `abd14b183c9c` |
| `video_x` | variable | canvas_processor.py | `f1ca2f7722dc` |
| `video_y` | variable | canvas_processor.py | `9adaf7a2c8cd` |
| `videos` | variable | combine-video.py | `5e591ffc0118` |
| `videos` | variable | easy-text-detection.py | `9d5db9e4679f` |
| `vignette_effect` | function | artistic_filters.py | `d8e79fb5c65c` |
| `vignette_mask` | variable | artistic_filters.py | `549392af0417` |
| `vignetted` | variable | artistic_filters.py | `44f9432fbfc2` |
| `vintage_effect` | function | color_filters.py | `434ff39118f4` |
| `vocal_times` | variable | audio_processor.py | `f9bda5c9f463` |
| `vocal_times` | variable | video_generator.py | `3aacaf331e2a` |
| `vocal_times` | variable | vocal_processor.py | `72978528d5b5` |
| `vocal_times_list` | variable | vocal_processor.py | `d5c197057eb8` |
| `volume` | variable | sound_effects_processor.py | `f4b34c11e6aa` |
| `volume` | variable | split_screen_processor.py | `31ed2aff49e6` |
| `volume_choice` | variable | sound_effects_processor.py | `96557af3b11f` |
| `wait_for_batch` | function | canvas_processor.py | `25aa1e4e679b` |
| `wait_for_batch` | function | video_filter_processor.py | `e4c49aa5e679` |
| `wait_for_task` | function | queue_manager.py | `4f02e3ed2c84` |
| `wait_for_tasks` | function | queue_manager.py | `7a2897b1dfe6` |
| `warm_cache` | function | cache_manager.py | `e641a276a0d4` |
| `warm_cache` | function | video_filter_processor.py | `faf1c93d16bc` |
| `weakref` | import | cache_manager.py | `2b00e696942a` |
| `weakref` | import | queue_manager.py | `2b00e696942a` |
| `whisper` | import | subtitle_processor.py | `c35eef0ba470` |
| `whisper` | import | video-transcribe.py | `c35eef0ba470` |
| `width` | variable | canvas_processor.py | `de3a4b877207` |
| `width` | variable | combine-video.py | `7ad532702a23` |
| `width` | variable | easy-text-detection.py | `70b140d9e554` |
| `width_ratio` | variable | video_formatter.py | `70e40848ae12` |
| `word` | variable | subtitle_processor.py | `d002ea222e0a` |
| `word` | variable | video-transcribe.py | `0607ff211092` |
| `word_count` | variable | subtitle_processor.py | `26702618f830` |
| `word_end` | variable | subtitle_processor.py | `73e1b821fe8c` |
| `word_end` | variable | video-transcribe.py | `71afa7692404` |
| `word_start` | variable | subtitle_processor.py | `af72df96509d` |
| `word_start` | variable | video-transcribe.py | `e25b74889356` |
| `word_subtitles` | variable | subtitle_processor.py | `d1db8b01ef8e` |
| `words` | variable | subtitle_processor.py | `4f44e3cfec29` |
| `words` | variable | subtitle_video_processor.py | `9a4a3e2d8e47` |
| `words` | variable | video-transcribe.py | `ced09822322d` |
| `worker_thread` | variable | queue_manager.py | `8ad17ab192b5` |
| `wrap_text` | function | subtitle_video_processor.py | `87cd041bfddf` |
| `wrapper` | function | filter_registry.py | `63785b32fa63` |
| `x` | variable | artistic_filters.py | `7dee8bc84c3b` |
| `x` | variable | multiple_image_processor.py | `6ef1242c8039` |
| `x_offset` | variable | image-to-video.py | `7cbea9b26148` |
| `x_offset` | variable | image_processor.py | `ec3c89c9b78b` |
| `x_offset` | variable | multiple_image_processor.py | `93cbfe61316b` |
| `x_offset` | variable | split_screen_processor.py | `382ad06ba308` |
| `x_offset` | variable | video_formatter.py | `79be9bb0c4bc` |
| `x_pos` | variable | subtitle_video_processor.py | `b0d3279be462` |
| `x_pos` | variable | video_formatter.py | `9496b860b997` |
| `y` | variable | artistic_filters.py | `7e4dc3428435` |
| `y` | variable | multiple_image_processor.py | `ae2cfd9fdcf3` |
| `y_offset` | variable | image-to-video.py | `922285c34743` |
| `y_offset` | variable | image_processor.py | `72b5f7f2d022` |
| `y_offset` | variable | multiple_image_processor.py | `98cc5e85caac` |
| `y_offset` | variable | split_screen_processor.py | `fdb96bb86e76` |
| `y_offset` | variable | video_formatter.py | `3d20d36e20bd` |
| `y_pos` | variable | subtitle_video_processor.py | `fd39ac8ad7e3` |
| `y_pos` | variable | video_formatter.py | `a13d83ab7ab8` |
| `youtube_height` | variable | image-to-video.py | `01e445eafd8e` |
| `youtube_width` | variable | image-to-video.py | `fec5c5e40a22` |

## 📝 Usage Notes

- Each entity has a unique hash based on its content
- When code changes, the hash changes, enabling precise change detection
- Dependencies show how functions and classes connect to each other
- Use this report to understand code structure and track modifications
- Upload this markdown file to AI assistants for code analysis and questions

