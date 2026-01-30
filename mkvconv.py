import os
import sys
import subprocess
import argparse
from pathlib import Path

class MKVConverter:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.check_ffmpeg()
    
    def check_ffmpeg(self):
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        except:
            print("Error: FFmpeg not found. Install it first")
            sys.exit(1)
    
    def convert(self, input_file, fast=True, preset='medium', crf=23):
        input_path = Path(input_file)
        output_path = input_path.with_suffix('.mp4')
        
        if output_path.exists():
            res = input(f"File {output_path.name} exists. Overwrite? (y/n): ")
            if res.lower() != 'y': return False

        if fast:
            cmd = ['ffmpeg', '-i', str(input_path), '-c', 'copy', '-y', str(output_path)]
            print(f"Fast Remuxing: {input_file} -> {output_path.name}")
        else:
            cmd = [
                'ffmpeg', '-i', str(input_path),
                '-c:v', 'libx264', '-preset', preset, '-crf', str(crf),
                '-c:a', 'aac', '-b:a', '128k', '-y', str(output_path)
            ]
            print(f"Encoding Mode: {input_file} -> {output_path.name}")

        try:
            process = subprocess.Popen(
                cmd, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, 
                text=True, universal_newlines=True, bufsize=1
            )
            
            for line in process.stderr:
                if self.verbose: print(line.strip())
                if "frame=" in line and not fast:
                    print(f"\rProcessing: {line.strip().split('fps=')[0]}", end='', flush=True)

            process.wait()
            if process.returncode == 0:
                print(f"\nDone: {output_path.name}")
                return True
        except Exception as e:
            print(f"\nError: {e}")
            return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='+')
    parser.add_argument('--slow', action='store_true')
    parser.add_argument('-p', '--preset', default='medium')
    parser.add_argument('-c', '--crf', type=int, default=23)
    
    args = parser.parse_args()
    conv = MKVConverter()

    for f in args.input:
        conv.convert(f, fast=(not args.slow), preset=args.preset, crf=args.crf)

if __name__ == '__main__':
    main()