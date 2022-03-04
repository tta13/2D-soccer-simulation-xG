import glob, os
import run

def get_files_by_extension(ext: str) -> list[str]:
    result = []
    for file in glob.glob(f'*.{ext}'):
        result.append(file)
    return result

def main():
    script_directory = os.getcwd()
    data_dir = os.path.join(script_directory, 'data')
    if(os.getcwd() != data_dir):
        os.chdir(data_dir)
    rcg_files = get_files_by_extension('rcg')
    total_files = len(rcg_files)
    print(f'Found {len(rcg_files)} files: {rcg_files}')
    proceed = input('Proceed? [Y/n] ')
    if proceed == 'N' or proceed == 'n':
        exit(0)
    analyzed_files = 0
    for rcg in rcg_files:
        print(f'Running analysis: {rcg} ...')
        run.run_analysis(os.path.join(data_dir, rcg), os.path.join(data_dir, 'database_2019+2021.csv'))
        analyzed_files += 1
        print(f'Done! ({analyzed_files}/{total_files})')
    print('Finished.')


if __name__ == '__main__':
    main()
