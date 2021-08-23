import os
import re
import json
from gclient import GClient
from options import Options
from logger import Logger

DOC_ID_FIELD = "doc_id"


class Worker:
    def __init__(self, logger: Logger, options: Options):
        self.opts = options
        self.logger = logger
        self.gclient = GClient()

    def save_blob(self, bytes, name):
        with open(name, "wb") as f:
            f.write(bytes)

    def new_filename(self, dir, name, ext):
        filename = f"{dir}/{name}.{ext}"

        i = 0
        while os.path.isfile(filename):
            filename = f"{dir}/{name}{str(i)}.{ext}"
            i += 1

        return filename

    def meta(self, filename):
        base = os.path.basename(filename)
        name, ext = os.path.splitext(base)
        dir = os.path.dirname(filename)

        with open(filename, "r") as f:
            # Apparently .gdoc/.gsheet files sometimes contain comments!
            content = re.sub(r"\n\s*//.*\n", "", f.read())
            doc_id = json.loads(content)[DOC_ID_FIELD]

        return dir, name, ext[1:], doc_id

    def move(self, source, destination):
        if not os.path.exists(destination):
            os.mkdir(destination)

        base = os.path.basename(source)
        os.rename(source, os.path.join(destination, base))

    def delete(self, source):
        os.remove(source)

    def work(self):
        for filename in self.opts.files:
            try:
                dir, name, ext, id = self.meta(filename)
            except Exception as e:
                self.logger.errorf('Error processing "%0": %1', filename, e)
                continue

            to_ext = self.opts.export_map[ext]

            metadata, err = self.gclient.get(id, to_ext)

            if err:
                self.logger.errorf('Error processing "%0": %1', filename, err)
                continue

            bytes = metadata['content']
            if not self.opts.inplace:
                dir = self.opts.output_dir

            new_filename = self.new_filename(dir, name, to_ext)
            self.save_blob(bytes, new_filename)
            self.logger.infof('Saved "%0" as "%1" %2', filename,
                              new_filename, f'(inplace)' if self.opts.inplace else "")

            if self.opts.delete_remote:
                err = self.gclient.delete(id)
                if err:
                    self.logger.errorf(err)
                else:
                    self.logger.infof(
                        "Deleted remote document with id %0 (%1)", id, name + "." + ext)

            if self.opts.delete_local:
                self.delete(filename)
                self.logger.infof('Deleted "%0"', filename)

            elif self.opts.move_local_path:
                self.move(filename, self.opts.move_local_path)
                self.logger.infof('Moved "%0" to "%1"', filename,
                                  self.opts.move_local_path)
