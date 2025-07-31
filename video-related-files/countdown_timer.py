import os
import subprocess
from PIL import Image, ImageDraw, ImageFont
import tempfile
import random
import colorsys
import asyncio
import edge_tts

def get_color_choice():
    """Get color preference from user"""
    print("\nChoose color option:")
    print("1. White (default)")
    print("2. Single color (specify RGB values)")
    print("3. RGB rainbow (continuously changing colors)")
    
    while True:
        try:
            choice = input("Enter your choice (1, 2, or 3): ").strip()
            if choice in ['1', '2', '3']:
                return choice
            else:
                print("Please enter 1, 2, or 3.")
        except KeyboardInterrupt:
            print("\nExiting...")
            exit(0)

def get_single_color():
    """Get RGB values for single color"""
    print("Enter RGB values (0-255):")
    while True:
        try:
            r = int(input("Red (0-255): "))
            g = int(input("Green (0-255): "))
            b = int(input("Blue (0-255): "))
            
            if all(0 <= val <= 255 for val in [r, g, b]):
                return (r, g, b)
            else:
                print("All values must be between 0 and 255.")
        except ValueError:
            print("Please enter valid numbers.")
        except KeyboardInterrupt:
            print("\nExiting...")
            exit(0)

def get_voice_choice():
    """Get voice preference from user"""
    print("\nAdd voice countdown?")
    print("1. No voice (silent)")
    print("2. Yes, add voice countdown")
    
    while True:
        try:
            choice = input("Enter your choice (1 or 2): ").strip()
            if choice in ['1', '2']:
                return choice == '2'
            else:
                print("Please enter 1 or 2.")
        except KeyboardInterrupt:
            print("\nExiting...")
            exit(0)

def get_voice_selection():
    """Let user select voice from available options"""
    voices = [
        "en-US-AriaNeural",
        "en-US-JennyNeural", 
        "en-US-GuyNeural",
        "en-US-AndrewNeural",
        "en-US-EmmaNeural",
        "en-US-BrianNeural",
        "en-GB-SoniaNeural",
        "en-GB-RyanNeural"
    ]
    
    print("\nAvailable voice options:")
    for i, voice in enumerate(voices, 1):
        print(f"{i}. {voice}")
    print(f"{len(voices) + 1}. Random voices (different voice for each number)")
    
    while True:
        try:
            choice = int(input(f"Select voice option (1-{len(voices) + 1}): "))
            if 1 <= choice <= len(voices):
                return voices[choice - 1]
            elif choice == len(voices) + 1:
                return "random"
            else:
                print(f"Please enter a number between 1 and {len(voices) + 1}.")
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nExiting...")
            exit(0)

def get_rainbow_color(frame_num, total_frames):
    """Generate rainbow color based on frame number"""
    # Create a smooth color transition over the duration
    hue = (frame_num / total_frames) % 1.0
    saturation = 1.0
    value = 1.0
    
    # Convert HSV to RGB
    rgb = colorsys.hsv_to_rgb(hue, saturation, value)
    return tuple(int(c * 255) for c in rgb)

async def generate_audio_files(duration, voice_choice, temp_dir):
    """Generate audio files for countdown numbers"""
    print("Generating audio files...")
    
    voices = [
        "en-US-AriaNeural",
        "en-US-JennyNeural", 
        "en-US-GuyNeural",
        "en-US-AndrewNeural",
        "en-US-EmmaNeural",
        "en-US-BrianNeural",
        "en-GB-SoniaNeural",
        "en-GB-RyanNeural"
    ]
    
    audio_files = {}
    
    # Generate audio for each number from duration down to 0 (including 0)
    for num in range(duration, -1, -1):
        text = str(num)
        audio_file = os.path.join(temp_dir, f"audio_{num}.wav")
        
        # Choose voice for this number
        if voice_choice == "random":
            selected_voice = random.choice(voices)
            print(f"Generating audio for {num} with voice: {selected_voice}")
        else:
            selected_voice = voice_choice
            print(f"Generated audio for: {num}")
        
        try:
            # Create TTS
            communicate = edge_tts.Communicate(text, selected_voice)
            await communicate.save(audio_file)
            
            audio_files[num] = audio_file
        except Exception as e:
            print(f"Error generating audio for {num}: {e}")
            continue
    
    return audio_files

def create_video_silent(temp_dir, fps, output_filename):
    """Create silent video (original method)"""
    ffmpeg_cmd = [
        'ffmpeg', '-y',
        '-framerate', str(fps),
        '-i', os.path.join(temp_dir, 'frame_%06d.png'),
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-crf', '18',
        '-preset', 'medium',
        output_filename
    ]
    
    try:
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Silent video created successfully: {output_filename}")
            print(f"Video resolution: 1920x1080")
            print(f"Frame rate: {fps} fps")
        else:
            print("Error creating video:")
            print(result.stderr)
            
    except FileNotFoundError:
        print("Error: FFmpeg not found. Please install FFmpeg and make sure it's in your PATH.")
        print("Download from: https://ffmpeg.org/download.html")
    except Exception as e:
        print(f"Error running FFmpeg: {e}")

async def create_video_with_audio(temp_dir, fps, output_filename, duration, audio_files):
    """Create video with synchronized audio"""
    print("Creating video with audio...")
    
    try:
        # First create silent video
        silent_video = os.path.join(temp_dir, "silent_video.mp4")
        ffmpeg_cmd = [
            'ffmpeg', '-y',
            '-framerate', str(fps),
            '-i', os.path.join(temp_dir, 'frame_%06d.png'),
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-crf', '18',
            '-preset', 'medium',
            silent_video
        ]
        
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print("Error creating silent video:")
            print(result.stderr)
            return
        
        # Create audio track with properly timed audio files
        audio_inputs = []
        filter_complex_parts = []
        
        for i, (num, audio_file) in enumerate(sorted(audio_files.items(), reverse=True)):
            # Calculate when this number should play (at the start of that second)
            delay_time = duration - num
            
            audio_inputs.extend(['-i', audio_file])
            # Add delay and volume boost (increase volume by 10dB)
            filter_complex_parts.append(f"[{i+1}:a]adelay={delay_time * 1000}|{delay_time * 1000},volume=10dB[a{i}]")
        
        # Mix all audio streams
        if len(audio_files) > 1:
            mix_inputs = ''.join([f'[a{i}]' for i in range(len(audio_files))])
            filter_complex_parts.append(f"{mix_inputs}amix=inputs={len(audio_files)}:duration=longest[audio]")
            audio_map = '[audio]'
        else:
            audio_map = '[a0]'
        
        # Combine video with audio
        final_cmd = [
            'ffmpeg', '-y',
            '-i', silent_video
        ] + audio_inputs + [
            '-filter_complex', ';'.join(filter_complex_parts),
            '-map', '0:v',
            '-map', audio_map,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-shortest',
            output_filename
        ]
        
        result = subprocess.run(final_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Video with audio created successfully: {output_filename}")
            print(f"Video duration: {duration} seconds")
            print(f"Audio: Voice countdown included")
        else:
            print("Error creating video with audio:")
            print(result.stderr)
            
    except Exception as e:
        print(f"Error in video creation with audio: {e}")

async def create_countdown_video():
    """Main function to create countdown video"""
    # Get countdown duration from user
    while True:
        try:
            duration = int(input("Enter countdown duration in seconds: "))
            if duration > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nExiting...")
            exit(0)
    
    # Get color choice
    color_choice = get_color_choice()
    single_color = None
    
    if color_choice == '2':
        single_color = get_single_color()
        print(f"Using color: RGB{single_color}")
    elif color_choice == '3':
        print("Using rainbow colors")
    else:
        print("Using white color")
    
    # Get voice choice
    add_voice = get_voice_choice()
    voice = None
    audio_files = {}
    
    if add_voice:
        voice = get_voice_selection()
        if voice == "random":
            print("Selected: Random voices for each number")
        else:
            print(f"Selected voice: {voice}")
    
    # Video settings
    width, height = 1920, 1080  # YouTube standard HD resolution
    fps = 30
    total_frames = duration * fps
    
    # Create temporary directory for frames
    temp_dir = tempfile.mkdtemp()
    print(f"Creating frames in: {temp_dir}")
    
    try:
        # Generate audio files if voice is enabled
        if add_voice:
            audio_files = await generate_audio_files(duration, voice, temp_dir)
        
        # Try to load a font (much bigger size now)
        font = None
        try:
            # Windows
            font = ImageFont.truetype("arial.ttf", 350)
        except (OSError, IOError):
            try:
                # macOS
                font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 350)
            except (OSError, IOError):
                try:
                    # Linux
                    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 350)
                except (OSError, IOError):
                    # Fallback to default font
                    font = ImageFont.load_default()
                    print("Warning: Using default font. Text may appear small.")
        
        print("Generating frames...")
        
        # Generate frames
        for frame_num in range(total_frames):
            # Calculate current time remaining
            time_remaining = duration - (frame_num / fps)
            
            # Round to nearest tenth for smooth countdown
            if time_remaining <= 0:
                display_time = "0"
            else:
                display_time = f"{time_remaining:.1f}"
            
            # Create image
            img = Image.new('RGB', (width, height), color='black')
            draw = ImageDraw.Draw(img)
            
            # Determine text color based on user choice
            if color_choice == '1':  # White
                text_color = 'white'
            elif color_choice == '2':  # Single color
                text_color = single_color
            else:  # RGB rainbow
                text_color = get_rainbow_color(frame_num, total_frames)
            
            # Get text dimensions for centering
            bbox = draw.textbbox((0, 0), display_time, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Calculate position to center text
            x = (width - text_width) // 2
            y = (height - text_height) // 2
            
            # Draw countdown text
            draw.text((x, y), display_time, fill=text_color, font=font)
            
            # Save frame
            frame_path = os.path.join(temp_dir, f"frame_{frame_num:06d}.png")
            img.save(frame_path)
            
            # Progress indicator
            if frame_num % 30 == 0:  # Every second
                print(f"Progress: {frame_num}/{total_frames} frames ({frame_num/total_frames*100:.1f}%)")
        
        print("Frames generated. Creating video...")
        
        # Output video filename
        output_filename = f"countdown_{duration}s{'_voiced' if add_voice else ''}.mp4"
        
        if add_voice and audio_files:
            # Create video with audio
            await create_video_with_audio(temp_dir, fps, output_filename, duration, audio_files)
        else:
            # Create video without audio (original method)
            create_video_silent(temp_dir, fps, output_filename)
            
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        # Clean up temporary files
        print("Cleaning up temporary files...")
        try:
            for file in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, file))
            os.rmdir(temp_dir)
        except Exception as e:
            print(f"Error cleaning up: {e}")

def check_dependencies():
    """Check if required dependencies are available"""
    all_good = True
    
    try:
        import PIL
        print("✓ Pillow is installed")
    except ImportError:
        print("✗ Pillow not found. Install with: pip install Pillow")
        all_good = False
    
    try:
        import edge_tts
        print("✓ edge-tts is installed")
    except ImportError:
        print("✗ edge-tts not found. Install with: pip install edge-tts")
        all_good = False
    
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ FFmpeg is available")
        else:
            print("✗ FFmpeg not working properly")
            all_good = False
    except FileNotFoundError:
        print("✗ FFmpeg not found. Please install FFmpeg")
        print("Download from: https://ffmpeg.org/download.html")
        all_good = False
    except Exception as e:
        print(f"✗ Error checking FFmpeg: {e}")
        all_good = False
    
    return all_good

async def main():
    """Main entry point"""
    print("Countdown Timer Video Generator")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        print("\nPlease install missing dependencies before running this program.")
        print("Required packages:")
        print("- pip install Pillow")
        print("- pip install edge-tts")
        print("- FFmpeg (download from https://ffmpeg.org/download.html)")
        return
    
    print("\nDependencies check passed!")
    await create_countdown_video()
    print("\nDone!")

if __name__ == "__main__":
    asyncio.run(main())