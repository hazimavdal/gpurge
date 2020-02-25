import os
import glob


class Options:
    def __init__(self, logger, parser):
        self.logger = logger
        args = parser.parse_args()

        if args.list:
            self.files = self.read_file(args.list)
        elif args.folder:
            self.files = self.find_files(
                args.folder, args.extensions, args.recursive)
        else:
            raise Exception("Unexpected error")

        self.delete_remote = args.trash
        self.delete_local = args.delete
        self.move_local_path = args.move

        self.inplace = args.inplace
        self.output_dir = args.output

        self.report_filename = args.report
        self.verbose_level = args.verbosity
        self.export_map = {"gdoc": args.gdoc, "gsheet": args.gsheet}

        self.make(self.output_dir, self.move_local_path)

    def read_file(self, filename):
        self.logger.infof('Reading "%0"', filename)

        def verify(filenames):
            for f in filenames:
                assert os.path.exists(f)

        with open(filename, "r") as f:
            lines = f.read().split('\n')
            nonblank = [l for l in lines if len(l) > 0]
            verify(nonblank)
            return nonblank

    def find_files(self, path, exts, r):
        self.logger.infof('Searching for files in "%0"', path)

        files = []
        for ext in exts:
            ext_count = 0
            if r:
                pattern = os.path.join(path, f"**/*.{ext}")
            else:
                pattern = os.path.join(path, f"*.{ext}")

            for filename in glob.glob(pattern, recursive=r):
                ext_count += 1
                files.append(filename)

            self.logger.infof("Found %0 %1 files", ext_count, ext)

        return files

    def make(self, *args):
        for arg in args:
            if arg is None:
                continue

            if not os.path.exists(arg):
                os.mkdir(arg)
