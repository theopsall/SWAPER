import argparse


def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments for SWAPER (Star Wars API Parser) program.

    Returns:
    argparse.Namespace: Namespace object containing the parsed arguments
    """

    epilog = """SWAPER: Star Wars API Parser.

    USAGE EXAMPLES:
        python main.py search "luke"
            Search for a Star Wars character named "luke".

        python main.py search "anakin" --world
            Search for a Star Wars character named "anakin" and retrieve homeworld information.

        python main.py cache --clean
            Clear the cache.
        
        python main.py plot (-o plot.png)
            Generate a plot of the cached Star Wars characters and save it to a png file, default file is swapi_plots.png.
    """
    parser = argparse.ArgumentParser(
        description="SWAPER, Star Wars APi parsER",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=epilog,
    )

    tasks = parser.add_subparsers(
        title="subcommands", description="Available tasks", dest="task", metavar=""
    )

    search_task = tasks.add_parser("search", help="Search for a Star Wars character")
    search_task.add_argument("query", help="Search query")
    search_task.add_argument(
        "--world", default=False, action="store_true", help="Retrieve homeworld info"
    )

    cache_task = tasks.add_parser("cache", help="Cache Star Wars characters")
    cache_task.add_argument("--clean", action="store_true", help="Clear cache")

    plot_task = tasks.add_parser("plot", help="Plot cache Star Wars characters")
    plot_task.add_argument(
        "-o",
        "--output",
        required=False,
        default="swapi_plots.png",
        help="Output plot file",
    )

    return parser.parse_args()
