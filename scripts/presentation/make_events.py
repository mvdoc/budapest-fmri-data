"""Parse the log file outputted by show_movie.py and make the events.tsv
automatically"""
import argparse


def parse_log(fn):
    """Take only lines containing BIDS"""
    bids_log = []
    with open(fn, 'r') as f:
        for line in f.readlines():
            if 'BIDS' in line:
                bids_log.append('\t'.join(line.strip('\n').split()[2:]))
    return bids_log


def fill_duration(bids_log):
    """Fill the duration -- assumes {duration} present in the string"""
    header = bids_log[0]
    rows = bids_log[1:]
    bids_log_duration = [header]
    for i in range(len(rows) - 1):
        duration = float(rows[i + 1].split()[0]) - float(rows[i].split()[0])
        bids_log_duration.append(rows[i].format(duration=duration))
    return bids_log_duration


def write_events(bids_log, events_fn):
    with open(events_fn, 'wb') as f:
        f.write('\n'.join(bids_log))


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--input', '-i', type=str,
                        help='input file',
                        required=True)
    parser.add_argument('--output', '-o', type=str,
                        help='output file',
                        required=True)

    return parser.parse_args()


def main():
    parsed = parse_args()
    fnin = parsed.input
    fnout = parsed.output

    events_file = fill_duration(parse_log(fnin))
    write_events(events_file, fnout)


if __name__ == '__main__':
    main()
