import argparse
from workflow.test_generation_workflow import export_workflow_png


def main():
    parser = argparse.ArgumentParser(
        description="Export the test generation workflow graph as a PNG image."
    )
    parser.add_argument(
        "-o", "--output", default="src/services/workflow_graph.png",
        help="Output path for the PNG file (default: src/services/workflow_graph.png)"
    )
    args = parser.parse_args()
    export_workflow_png(args.output)


if __name__ == "__main__":
    main()