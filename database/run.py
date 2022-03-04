import argparse
from csv import writer
from loganalyzer import Game, Parser, Analyzer

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rcg", help="RCG file path", metavar='<RCG log file>',
                        required=True, dest='rcg')
    parser.add_argument(
        "--output", help="Output saving path.", metavar='<Output file path>', dest='output')
    args = parser.parse_args()
    if args.output is None:
        args.output = args.rcg.split('.rcg')[0] + ".csv"
    return args

def write_to_file(save_path, analyzer):
    with open(save_path, 'a') as outfile:
        csv_writer = writer(outfile, lineterminator='\n')
        for row in analyzer.shot_data:
            csv_writer.writerow(row)

def run_analysis(rcg_path, output_path):
    parser = Parser(rcg_path)
    game = Game(parser)
    analyzer = Analyzer(game)
    analyzer.analyze()
    write_to_file(output_path, analyzer)

def main():
    args = parse_args()
    run_analysis(args.rcg, args.output)

if __name__ == '__main__':
    main()
