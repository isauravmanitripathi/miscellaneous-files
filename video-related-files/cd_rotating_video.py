from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import os
import subprocess
import math
import random
import shutil
from concurrent.futures import ThreadPoolExecutor
import traceback
import sys
import re
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn
from rich.panel import Panel
from rich.traceback import install
from rich.table import Table
import time
import mimetypes

# Install rich traceback handler
install(show_locals=True)

# Initialize rich console
console = Console()

# Constants
OUTPUT_DIR = "/Volumes/hard-drive/miscellaneous-files/video-related-files/Results"
FRAMES_DIR = os.path.join(OUTPUT_DIR, "frames")

def is_valid_audio_file(file_path):
    """Check if the file is a valid audio file using ffprobe"""
    try:
        if not file_path.lower().endswith('.mp3'):
            return False
        cmd = [
            'ffprobe',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_streams',
            file_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False

def is_valid_image_file(file_path):
    """Check if the file is a valid image file using PIL"""
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except Exception:
        return False

def get_valid_audio_files(directory):
    """Get all valid MP3 files from a directory"""
    valid_files = []
    with console.status("[bold yellow]Scanning directory for audio files..."):
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path) and is_valid_audio_file(file_path):
                valid_files.append(file_path)
    return valid_files

def format_time(seconds):
    """Convert seconds to human readable time"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    if hours > 0:
        return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
    elif minutes > 0:
        return f"{int(minutes)}m {int(seconds)}s"
    else:
        return f"{seconds:.1f}s"

class Star:
    def __init__(self, count):
        self.positions = np.random.uniform(-1000, 1000, (count, 3))  # x, y, z
        self.speeds = np.random.uniform(3, 20, count)
        self.trail_lengths = np.random.randint(0, 8, count)
        self.brightness = np.random.uniform(0.3, 1.0, count)
        self.twinkle = np.random.random(count) < 0.3
        self.size = np.random.uniform(0.8, 1.5, count)
    
    def update(self, frame_number):
        # Update z positions
        self.positions[:, 2] -= self.speeds
        
        # Reset stars that went too far
        reset_mask = self.positions[:, 2] <= 0
        count_reset = np.sum(reset_mask)
        
        if count_reset > 0:
            self.positions[reset_mask] = np.column_stack((
                np.random.uniform(-1000, 1000, count_reset),
                np.random.uniform(-1000, 1000, count_reset),
                np.full(count_reset, 1000)
            ))
            self.brightness[reset_mask] = np.random.uniform(0.3, 1.0, count_reset)
    
    def draw(self, image, width, height, frame_number):
        draw = ImageDraw.Draw(image)
        
        # Calculate projected positions
        visible_mask = self.positions[:, 2] > 0
        visible_positions = self.positions[visible_mask]
        
        if len(visible_positions) > 0:
            factors = 200.0 / visible_positions[:, 2]
            screen_x = visible_positions[:, 0] * factors + width / 2
            screen_y = visible_positions[:, 1] * factors + height / 2
            
            sizes = self.size[visible_mask] * np.maximum(0.5, np.minimum(2, 200.0 / visible_positions[:, 2]))
            brightness = self.brightness[visible_mask] * (1 - visible_positions[:, 2] / 1000)
            
            # Draw each star
            for i in range(len(screen_x)):
                color_val = int(255 * brightness[i])
                color = (color_val, color_val, color_val)
                size = sizes[i]
                
                x, y = screen_x[i], screen_y[i]
                draw.ellipse([x-size/2, y-size/2, x+size/2, y+size/2], fill=color)

def create_galaxy_effect(width, height, frame_number):
    """Create galaxy effect using PIL"""
    galaxy = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(galaxy)
    
    angles = np.linspace(0, 360 * 3, 216)  # 216 points for efficiency
    for angle_deg in angles:
        angle = math.radians(angle_deg)
        r = (angle_deg / 30) * math.exp(angle * 0.1)
        x = width/2 + r * math.cos(angle + frame_number * 0.01)
        y = height/2 + r * math.sin(angle + frame_number * 0.01)
        
        hue = (angle_deg + frame_number) % 360
        if hue < 120:
            color = (int(255 * (120-hue)/120), 0, int(255 * hue/120), 50)
        else:
            color = (0, 0, int(255 * (360-hue)/240), 50)
            
        size = max(1, 10 - r/100)
        draw.ellipse([x-size, y-size, x+size, y+size], fill=color)
    
    return galaxy.filter(ImageFilter.GaussianBlur(3))

def get_audio_duration(audio_path):
    """Get audio duration using ffprobe"""
    try:
        with console.status("[bold yellow]Analyzing audio file..."):
            cmd = [
                'ffprobe', 
                '-i', audio_path,
                '-show_format',
                '-v', 'quiet',
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            duration_match = re.search(r'duration=(\d+\.\d+)', result.stdout)
            if duration_match:
                return float(duration_match.group(1))
                
            duration_match = re.search(r"Duration: (\d{2}):(\d{2}):(\d{2})\.(\d{2})", result.stderr)
            if duration_match:
                hours = int(duration_match.group(1))
                minutes = int(duration_match.group(2))
                seconds = int(duration_match.group(3))
                ms = int(duration_match.group(4))
                
                total_seconds = hours * 3600 + minutes * 60 + seconds + ms/100.0
                return total_seconds
                
            cmd = ['ffmpeg', '-i', audio_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            duration_match = re.search(r"Duration: (\d{2}):(\d{2}):(\d{2})\.(\d{2})", result.stderr)
            if duration_match:
                hours = int(duration_match.group(1))
                minutes = int(duration_match.group(2))
                seconds = int(duration_match.group(3))
                ms = int(duration_match.group(4))
                
                total_seconds = hours * 3600 + minutes * 60 + seconds + ms/100.0
                return total_seconds
            
            raise ValueError("Could not determine audio duration")
            
    except Exception as e:
        console.print("[red]Error getting audio duration:[/red]", str(e))
        raise

def generate_cd_frame(stars, frame_number, total_frames, image_path, width=1920, height=1080):
    """Generate a single frame of the CD video"""
    try:
        # Create base image and update stars
        image = Image.new('RGBA', (width, height), (0, 0, 0, 255))
        stars.update(frame_number)
        stars.draw(image, width, height, frame_number)
        
        # Add galaxy effect
        galaxy = create_galaxy_effect(width, height, frame_number)
        image = Image.alpha_composite(image.convert('RGBA'), galaxy)
        
        # Load and process CD image
        cd_image = Image.open(image_path).convert('RGBA')
        cd_image = cd_image.resize((1000, 1000))
        
        # Rotate CD
        angle = (frame_number * 360) / 30  # Complete rotation every second
        rotated_cd = cd_image.rotate(angle, resample=Image.BICUBIC)
        
        # Create CD mask
        cd_mask = Image.new("L", (1000, 1000), 0)
        cd_draw = ImageDraw.Draw(cd_mask)
        cd_draw.ellipse([(0, 0), (1000, 1000)], fill=255)
        cd_draw.ellipse([(450, 450), (550, 550)], fill=0)
        
        # Add reflection effect
        reflection = Image.new("RGBA", (1000, 1000), (0, 0, 0, 0))
        reflection_draw = ImageDraw.Draw(reflection)
        progress = frame_number / total_frames
        
        for i in range(0, 1000, 4):
            opacity = int(128 + 64 * math.sin(i * 0.01 + angle * 0.1 + progress * math.pi * 2))
            reflection_draw.arc([0, 0, 1000, 1000], i, i + 2, fill=(255, 255, 255, opacity))
        
        rotated_cd = Image.alpha_composite(rotated_cd, reflection)
        
        # Composite CD onto background
        image.paste(rotated_cd, (width//2 - 500, height//2 - 500), cd_mask)
        
        return image
        
    except Exception as e:
        console.print(f"[red]Error generating frame {frame_number}:[/red]")
        console.print_exception()
        raise

def run_ffmpeg_command(cmd, description):
    """Run FFmpeg command with suppressed output unless there's an error"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"\n[red]Error in {description}:[/red]")
        console.print(Panel(e.stderr, title="FFmpeg Error"))
        raise

def generate_base_video(image_path, duration=10):
    """Generate base video segment that will loop seamlessly"""
    width, height = 1920, 1080
    fps = 30
    total_frames = duration * fps
    
    # Initialize stars
    stars = Star(500)  # 500 stars
    
    # Create output directories
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(FRAMES_DIR, exist_ok=True)
    
    # Generate frames using thread pool for I/O operations
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Generating frames...", total=total_frames)
        
        def save_frame(frame_num):
            frame = generate_cd_frame(stars, frame_num, total_frames, image_path)
            frame.save(os.path.join(FRAMES_DIR, f"frame_{frame_num:05d}.png"))
            progress.update(task, advance=1)
        
        with ThreadPoolExecutor() as executor:
            list(executor.map(save_frame, range(total_frames)))
    
    # Create base video with hardware acceleration
    base_video = os.path.join(OUTPUT_DIR, "base_video.mp4")
    with console.status("[bold yellow]Encoding base video..."):
        run_ffmpeg_command([
            'ffmpeg', '-y',
            '-framerate', str(fps),
            '-i', os.path.join(FRAMES_DIR, 'frame_%05d.png'),
            '-c:v', 'h264_videotoolbox',  # Use Apple Silicon hardware encoder
            '-b:v', '5M',
            '-movflags', '+faststart',
            base_video
        ], "base video encoding")
    
    # Clean up frames
    shutil.rmtree(FRAMES_DIR)
    
    return base_video

def get_output_filename(audio_path):
    """Generate output filename based on audio filename"""
    audio_name = os.path.splitext(os.path.basename(audio_path))[0]
    return os.path.join(OUTPUT_DIR, f"{audio_name}.mp4")

def generate_long_video(image_path, audio_path, base_duration=10):
    """Generate full-length video with audio"""
    try:
        start_time = time.time()
        
        # Create input information table
        table = Table(show_header=False, box=None)
        table.add_row("[cyan]Image[/cyan]", image_path)
        table.add_row("[cyan]Audio[/cyan]", audio_path)
        
        console.print("\n[bold cyan]Starting Video Generation[/bold cyan]")
        console.print(Panel(table, title="Input Files"))
        
        # Ensure output directory exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        output_path = get_output_filename(audio_path)
        
        # Get audio duration
        audio_duration = get_audio_duration(audio_path)
        formatted_duration = format_time(audio_duration)
        console.print(f"[green]Audio Duration:[/green] {formatted_duration}")
        
        # Generate base video segment
        base_video = generate_base_video(image_path, base_duration)
        
        # Calculate loops needed
        loops = math.ceil(audio_duration / base_duration)
        console.print(f"\nCreating [cyan]{loops}[/cyan] loops of base video")
        
        # Create concat file
        concat_file = os.path.join(OUTPUT_DIR, "concat.txt")
        with open(concat_file, 'w') as f:
            for _ in range(loops):
                f.write(f"file '{os.path.basename(base_video)}'\n")
        
        # Change directory for concat operation
        original_dir = os.getcwd()
        os.chdir(OUTPUT_DIR)
        
        # Generate final video
        with console.status("[bold yellow]Creating final video..."):
            run_ffmpeg_command([
                'ffmpeg', '-y',
                '-f', 'concat',
                '-safe', '0',
                '-i', 'concat.txt',
                '-i', audio_path,
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-shortest',
                '-movflags', '+faststart',
                output_path
            ], "final video creation")
        
        # Change back to original directory
        os.chdir(original_dir)
        
        # Cleanup
        with console.status("[bold yellow]Cleaning up..."):
            os.remove(os.path.join(OUTPUT_DIR, "base_video.mp4"))
            os.remove(os.path.join(OUTPUT_DIR, "concat.txt"))
        
        # Show completion information
        end_time = time.time()
        total_time = end_time - start_time
        
        table = Table(show_header=False, box=None)
        table.add_row("[cyan]Total Time[/cyan]", format_time(total_time))
        table.add_row("[cyan]Output[/cyan]", output_path)
        
        console.print("\n[bold green]Video Generation Complete![/bold green]")
        console.print(Panel(table, title="Summary"))
        
        return output_path
        
    except Exception as e:
        console.print("\n[red bold]Error during video generation:[/red bold]")
        console.print_exception(show_locals=True)
        raise

def process_audio_files(image_path, audio_input, base_duration=10):
    """Process single audio file or directory of audio files"""
    try:
        if os.path.isfile(audio_input):
            # Single file processing
            if not is_valid_audio_file(audio_input):
                console.print("[red]Error:[/red] Not a valid audio file.")
                return
            return generate_long_video(image_path, audio_input, base_duration)
        
        elif os.path.isdir(audio_input):
            # Directory processing
            audio_files = get_valid_audio_files(audio_input)
            if not audio_files:
                console.print("[red]No valid audio files found in directory.[/red]")
                return
            
            # Show summary of files to process
            console.print(f"\nFound [green]{len(audio_files)}[/green] valid audio files")
            
            # Process each audio file
            for idx, audio_file in enumerate(audio_files, 1):
                console.print(f"\n[bold cyan]Processing file {idx}/{len(audio_files)}[/bold cyan]")
                console.print(f"[cyan]File:[/cyan] {os.path.basename(audio_file)}")
                try:
                    generate_long_video(image_path, audio_file, base_duration)
                except Exception as e:
                    console.print(f"[red]Error processing {os.path.basename(audio_file)}:[/red]")
                    console.print_exception()
                    continue
            
            console.print("\n[bold green]All files processed![/bold green]")
        
        else:
            console.print("[red]Error:[/red] Invalid audio input path")
            
    except Exception as e:
        console.print("[red bold]Error during processing:[/red bold]")
        console.print_exception()
        raise

if __name__ == "__main__":    
    console = Console()
    
    # Get image path interactively with validation
    while True:
        image_path = input("Enter the path to the CD cover image: ").strip()
        if not os.path.exists(image_path):
            console.print(f"[red]Error:[/red] Image file not found: {image_path}")
            continue
        if not is_valid_image_file(image_path):
            console.print(f"[red]Error:[/red] Not a valid image file: {image_path}")
            continue
        break
    
    # Get audio input path with validation
    while True:
        audio_input = input("Enter the path to the audio file or directory: ").strip()
        if not os.path.exists(audio_input):
            console.print(f"[red]Error:[/red] Path not found: {audio_input}")
            continue
        break
    
    # Get base duration with default value
    while True:
        duration_input = input("Enter base duration in seconds (default 10): ").strip()
        if duration_input == "":
            base_duration = 10
            break
        try:
            base_duration = int(duration_input)
            if base_duration > 0:
                break
            console.print("[red]Error:[/red] Duration must be positive")
        except ValueError:
            console.print("[red]Error:[/red] Please enter a valid number")
    
    try:
        process_audio_files(image_path, audio_input, base_duration)
        
    except Exception as e:
        console.print("[red bold]Processing failed![/red bold]")
        console.print_exception(show_locals=True)
        sys.exit(1)