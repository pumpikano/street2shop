from tomorrow import threads
import imghdr
import requests
import os
from itertools import islice
import sys
import logging


def split(x):
    first = x.find(',')
    return (x[:first], x[first+1:])


def main(args):

    if args.fail_file is not None:
        logging.basicConfig(filename=args.fail_file, format='%(message)s', level=logging.ERROR)



    @threads(args.threads)
    def download(item_id, url, i, images_dir=''):

        try:
            r = requests.get(url)

            if r.status_code == 200:

                image_type = imghdr.what(None, r.content)

                if image_type is not None:
                    with open(os.path.join(images_dir, item_id + '.' + image_type), 'wb') as f:
                        f.write(r.content)
                        f.close()
                else:
                    logging.error('%s\t%s\tunknown_type' % (item_id, url))
            else:
                logging.error('%s\t%s\tstatus:%d' % (item_id, url, r.status_code))

        except KeyboardException:
            raise
        except:
            print "Unexpected error:", sys.exc_info()[0]
            logging.error(sys.exc_info()[0])

        if i % 200 == 0:
            print i




    f = open(args.urls)

    itr = enumerate(f)
    itr = islice(itr, args.start, None)

    for i, line in itr:
        [item_id, url] = split(line.strip())
        download(item_id, url, i, images_dir=args.images_dir)



if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()

    # Data handling parameters
    parser.add_argument('--urls', dest='urls', type=str, default=None, required=True, help='urls')
    parser.add_argument('--image_dir', dest='images_dir', type=str, default='images', help='image directory')
    parser.add_argument('--failures', dest='fail_file', type=str, default=None, help='failure records')
    parser.add_argument('--start', dest='start', type=int, default=0, help='start offset')
    parser.add_argument('--threads', dest='threads', type=int, default=10, help='threads')

    args = parser.parse_args()


    main(args)

    exit(0)