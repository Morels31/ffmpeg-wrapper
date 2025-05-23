# ffmpeg-wrapper

Simple python3 ffmpeg wrapper intended for personal use.


## TODO
- [x] Think
- [x] Base script
- [x] Ask user the codec, preset and crf
- [ ] Check input files existance and read permission.
- [ ] Ask user output directory.
- [ ] Create if it does not exists the directory (and error if cannot write).
- [ ] Check if output files already exists, and ask the user to overwrite or not (check write permission).
- [ ] Call ffmpeg and check execution code, if failed save failed files names and logs and report it later.
- [ ] Optional: add --use-defaults argument
- [ ] Optional: time how much time each file has taken.
- [ ] Optional: check if output file is smaller, and if it is by how much.
- [ ] Optional: Makefile to install the script
