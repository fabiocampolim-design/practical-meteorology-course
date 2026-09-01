import pymupdf
import os, sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = os.path.join(root, "book", "Practical_Meteorology-v1.02b-WholeBookColor.pdf")
first, last, name = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
doc = pymupdf.open(src)
out = pymupdf.open()
out.insert_pdf(doc, from_page=first - 1, to_page=last - 1)
here = os.path.dirname(os.path.abspath(__file__))
dest = os.path.join(here, name + ".pdf")
out.save(dest)
print("saved", dest, out.page_count, "pages")
