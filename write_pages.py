""" Write markdown pages in docs folder.

Generate an index page and algorithm pages, linking to the images.
"""
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from pathlib import Path
from textwrap import dedent

from libsortvis import algos


def parse_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--prefix',
                        '-e',
                        default='docs',
                        type=Path,
                        help='prefix path for docs folder')
    parser.add_argument('--stub',
                        '-s',
                        type=Path,
                        default='images/stub-',
                        help='prefix path for stub images, relative to docs')
    parser.add_argument('--weave',
                        '-w',
                        type=Path,
                        default='images/weave-',
                        help='prefix path for weave images, relative to docs')
    return parser.parse_args()


def main():
    args = parse_args()
    docs_path = args.prefix
    index_path = docs_path / 'index.md'
    stub_parent = args.stub.parent
    stub_prefix = args.stub.name
    weave_parent = args.weave.parent
    weave_prefix = args.weave.name
    algos_path = Path(__file__).parent / 'libsortvis' / 'algos'
    algorithm_names = sorted(algos.algorithms)
    with index_path.open('w') as f:
        f.write(dedent("""\
            ## All Algorithms
            Click on an image to see the algorithm's code, or read [about] the
            project.
            
            """))
        for algorithm_name in algorithm_names:
            f.write(f'### {algorithm_name}\n')
            f.write(f'[![{algorithm_name} stub]][{algorithm_name}]\n\n')

        f.write('[about]: about.md\n')
        for algorithm_name in algorithm_names:
            stub_path = stub_parent / f'{stub_prefix}{algorithm_name}.png'
            f.write(f'[{algorithm_name} stub]: {stub_path}\n')
            f.write(f'[{algorithm_name}]: {algorithm_name}.md\n')

    for algorithm_name in algorithm_names:
        detail_path = docs_path / f'{algorithm_name}.md'
        weave_path = weave_parent / f'{weave_prefix}{algorithm_name}.png'
        algorithm_path = algos_path / f'{algorithm_name}.py'
        code = algorithm_path.read_text().strip()
        with detail_path.open('w') as f:
            f.write(f'# {algorithm_name}\n')
            f.write(f'![detail]({weave_path})\n')
            f.write(f'## code\n')
            f.write('```python\n')
            f.write(code)
            f.write('\n```\n\n')
            f.write('List order is sampled for visualisation whenever '
                    '`lst.log()` is called.')


main()
