# ffmpeg-wrapper

python3 ffmpeg wrapper intended for personal use.


## TODO
- [x] Think
- [x] Base script
- [x] Ask user the codec, preset and crf.
- [x] Check input files existance and read permission.
- [x] Ask user output directory.
- [x] Create the output directory if it doesn't exists (error if cannot write).
- [x] Check if output files already exists, and ask the user to overwrite or not (check write permission).
- [x] Normalize input files and output directory path.
- [x] Mantain sub-directory tree of the output files.
- [x] Execute ffmpeg and check return code, if failed save failed filenames and logs and report it later.
- [x] Add --use-defaults argument.
- [ ] Check if ffmpeg is installed.
- [ ] Log everything.
- [ ] Comment everything.

## Optional TODO
- [ ] Time how much time each file has taken.
- [ ] Check if output file is smaller, and if it is by how much.
- [ ] Makefile to install the script.
- [ ] Telegram notification when rendering has been finished.
- [ ] Option to automatically delete files smaller than the original.
- [ ] Option to automatically replace original files.
