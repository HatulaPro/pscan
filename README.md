# pscan 1.0.1v

- pscan is a python tool used for finding directories and files in websites

## Usage

```bash 
python scanner.py [-h] -u URL [-d depth] [-o file-name]
```

- `-u`, `--url` (required): the url to scan. Schema must be specified.
- `-d`, `--depth`: The depth of the scan. Default is 5.
- `-o`, `--output-file`: Path to log file to write to. **WARNING**: All of the contents of the file will be deleted.
- `-r`, `--robots`: When this flag is set, the program looks for links in `/robots.txt` as well.
- `-f`, `--follow-redirects`: Add this flag to make the program follow redirects (recommended).
- `-s`, `--static`: Add this flag to find static files (such as css files or images).