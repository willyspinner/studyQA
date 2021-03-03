from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
from whoosh.fields import TEXT, Schema, ID
from os import path, mkdir, walk
from pathlib import Path
from preprocess import preprocess_text


schema = Schema(title=TEXT(stored=True), filepath=ID(stored=True), content=TEXT)

if not path.exists("./index"):
    mkdir("./index")
    index = create_in("./index", schema)
else:
    index = open_dir('./index')

queryparser = QueryParser("content", index.schema)

def search(querystring):
    """
    searches the 'content' for the query string

    """
    global index, queryparser
    query = queryparser.parse(querystring)
    with index.searcher() as searcher:
        results = [{
            'filepath': hit['filepath'],
            'title': hit['title'],
        } for hit in searcher.search(query, limit=10)
        ]

    return results


def index_files(dirpath):
    """
    traverses the filetree from dirpath and index all indexable
    files (so far, markdown)

    """
    global index
    writer = index.writer()
    abspath = str(Path(dirpath).expanduser())
    for rootdir, dirs, files in walk(abspath):
        print("indexing files in ", rootdir)
        for file in files:
            filepath = path.join(rootdir, file)
            index_file(filepath, writer, do_commit=False)
    writer.commit()




def index_file(filepath, ix_writer=None, do_commit=True):
    """
    main function to index an individual file. if do_commit is True,
    then it will commit the writer

    """
    global index
    if ix_writer is None:
        ix_writer = index.writer()

    if filepath.endswith('.md'):
        index_markdown(filepath, ix_writer)
    else:
        pass
    if do_commit:
        ix_writer.commit()


def index_markdown(markdown_filepath, ix_writer):
    file = path.basename(markdown_filepath)
    with open(markdown_filepath) as f:
        content = preprocess_text(f.read())
    # Do any preprocessing here, but the QA model may also read from the filepath.
    ix_writer.add_document(title=file, content=content, filepath=markdown_filepath)








