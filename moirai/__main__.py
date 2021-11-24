from argparse import ArgumentParser
from subprocess import run
from pathlib import Path
from moirai.moirai import DocParser, DockerfileGenerator, LLVM_PLATFORMS 

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--platform", nargs="+", metavar="PLATFORM", choices=LLVM_PLATFORMS, required=True, help="The platform to generate the Dockerfile for.")
    parser.add_argument("--output", type=Path, default=Path("Dockerfile"), help="The output file to write the Dockerfile to.")
    parser.add_argument("--run", action="store_true", help="Run the Dockerfile.")
    parser.add_argument("--parse",  action="store_true", help="Whether to parse outputted files.")
    args = parser.parse_args()

    df = DockerfileGenerator.generate(args.platform)

    with args.output.open("w") as f:
        f.write(df)

    if args.run:
        # USE BUILDKIT IF YOU DONT HATE YOURSELF!
        spr = run(["docker", "build", "-t", "moirai", "."], cwd=args.output.parent, env={"DOCKER_BUILDKIT": "1"})
        spr.check_returncode()
        spr = run(["docker", "build", "-t", "moirai", "."], cwd=args.output.parent, capture_output=True, env={"DOCKER_BUILDKIT": "1"})
        spr.check_returncode()
        did = spr.stdout.decode("utf-8").strip()
        spr = run(["docker", "build", "-t", "moirai", "."], cwd=args.output.parent, env={"DOCKER_BUILDKIT": "1"})
        spr.check_returncode()
    
    if args.parse:
        dp = DocParser(args.output.parent / "output")
        dp.parse()



    
