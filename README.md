### Kitebuilder
#### Using Kitebuilder
```bash
usage: kitebuilder.py [-h] {parse,convert} ...

Assetnote OpenAPI/Swagger API schema parser

optional arguments:
  -h, --help       show this help message and exit

action:
  {parse,convert}
    parse          Parse a directory of swagger JSON files into a single JSON file output for Kiterunner
    convert        Convert a file to a number of swagger JSON files in the provided output directory
```

Kitebuilder is capable of parsing a large dataset of swagger files into our iterim format, to be utilised by Kiterunner.
It also supplies a convert utility to parse other formats into a number of spec files.

```
usage: kitebuilder.py parse [-h] [--blacklist HOSTS] [--scrape-dir DIR] [--output-file FILE]

optional arguments:
  -h, --help          show this help message and exit
  --blacklist HOSTS   Exclude specs with host field matching any of these strings (default googleapis, azure, petstore, amazon)
  --scrape-dir DIR    Directory to read list of specs from (default ./scrape)
  --output-file FILE  File to output resulting schema to (default output.json)
```

```
usage: kitebuilder.py convert [-h] --file FILE [--format FORMAT] [--scrape-dir DIR]

optional arguments:
  -h, --help        show this help message and exit
  --file FILE       File to convert to a number of swagger spec files.
  --format FORMAT   File format to convert. Only CSV files supported. Must be in the format 'id,name,content'
  --scrape-dir DIR  File to output resulting schema files to (defaults to ./scrape)
```
### Examples
#### Parse specs in ./specs directory to output.json
```
python kitebuilder.py parse --scrape-dir ./specs --output-file output.json
```
Note that the `--output-file` here is not necessary, as output.json is the default. 


#### Convert BigQuery CSV export to a number of spec files in ./specs
```
python kitebuilder.py convert --file swagger-github.csv --format CSV --scrape-dir ./specs
```
Note: this requires the CSV file to be in the format 'id,name,file_content'.

Looking for [Kiterunner](https://github.com/assetnote/kiterunner)?