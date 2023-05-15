# SWAPER: Star Wars API Parser

SWAPER is a command line tool for searching Star Wars characters and retrieving their information, including homeworld details. It uses the [Star Wars API](https://swapi.dev/) to fetch the data.

For the persistence of caching, SWAPER uses the sqlite3 built-in module from Python to store the search queries, responses, and timestamps. If a search query is made without the --world option and is later called again with the --world option, SWAPER will execute only the homeworld request and will update the cache record on the database and the timestamp.

## 1. Installation

1. Clone this repository to your local machine

   ```bash
   git clone git@github.com:theopsall/SWAPER.git
   ```

2. Navigate to the project directory:

   ```bash
   cd swaper
   ```

3. Create a virtual environment:

   ```bash
   python3 -m virtualenv venv
   ```

4. Activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```

5. Install the project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## 2. Usage

SWAPER has three main tasks: search, cache and plot.

### 2.1. Search

The search task allows you to search for a Star Wars character by name and optionally retrieve their homeworld information. To use the search task, run the following command:

```bash
python main.py search [QUERY] [--world]
```

where [QUERY] is the name of the Star Wars character you want to search for, and --world is an optional flag to retrieve homeworld information.

Example
To search for a Star Wars character named "Luke", run the following command:

```bash
python main.py search "luke"
```

To search for a Star Wars character named "Anakin" and retrieve their homeworld information, run the following command:

```bash
python main.py search "anakin" --world
```

### 2.2. Cache

The cache task allows you to clear the cached Star Wars characters. To use the cache task, run the following command:

```bash
python main.py cache --clean
```

### 2.3. Plot

The plot task allows you To generate a plot of the cached Star Wars characters and save it to a png file, run the following command:

```bash
python main.py plot -o plot.png
```

The `-o` or `--output` flag specifies the name of the output file. If not specified, the default filename is swapi_plots.png. This command will generate a plot that visualizes the cached queries that have been made to the Star Wars API, including information on the most popular searched queries, the distribution of searches over time of day, and the most searched planets. The resulting plot file will be saved in the current directory with the specified filename.
