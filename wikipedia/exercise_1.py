import json

from bs4 import BeautifulSoup
import mwparserfromhell as mwp
import lxml

def yield_pages(filename):
    """
    Reads the Wiki dump XML, and produces a sequence of "page" elements as string
    """
    with open(filename) as istr:
        lines = map(str.strip, istr)
        page = []
        for line in lines:
            if line == "<page>":
                page = []
            page.append(line)
            if line == "</page>":
                yield "\n".join(page)

def get_title_text(page_str):
    """
    Takes a "page" element string, and converts it into a sequence of triples
    containing title (ie. article subject), and text (ie. article content)
    """
    page = BeautifulSoup(page_str, "lxml")
    if page.find("redirect"):
        return None
    title = page.title.get_text()
    text = mwp.parse(page.revision.find('text').get_text())
    return title, text
    

    
def xml_to_jsons(xml_dump):
    """
    Converts XML dump into a sequence of simplified JSON page representations
    """
    instream = yield_pages(xml_dump)
    instream = map(get_title_text, instream)
    instream = filter(None, instream)
    for title, text in instream:
        links = list({str(lnk.title) for lnk in text.ifilter_wikilinks()})
        lead = next(str(t.strip_code()) for t in text.get_sections(include_lead=True))
        yield {
            "title": title,
            "lead_section" :lead,
            "links":links,
        }
        
def dump(xmldump_filename, output_jsonfile):
    """
    Produces a JSON dump out of the Wiki XML dump
    """
    with open(output_jsonfile, "w") as ostr:
        for json_page in xml_to_jsons(xmldump_filename):
            print(json.dumps(json_page), file=ostr)

def load_jsons(jsondump_filename):
    """
    Question 1. Load the JSON dump file
    """
    pass
    
def compute_graph(jsons):
    """
    Question 2. Compute a graph representation based on the links contained in each page
    """
    pass

def compute_average_local_clustering_coefficient(graph):
    """
    Question 3. Compute the average local clustering coefficient
    """
    pass
    
    
def compute_average_shortest_path_length(graph):
    """
    Question 4. Compute the average minimum path length
    """
    pass
    
