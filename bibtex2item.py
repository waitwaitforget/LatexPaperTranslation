import sys

class BibItem(object):
    def __init__(self, code):
        self.code = code
        self.title = None
        self.venue = None
        self.volume = None
        self.number = None
        self.pages = None
        self.year = None
        self.journal = None
        self.booktitle = None
        self.publisher = None
        self.authors = None

    def non_empty_publisher(self):
        for a in [self.booktitle, self.journal]:
            if a: return a
        return ""

    def write_tofile(self):

        if not self.title:
            raise ValueError('Attempting to write an empty item!')
        else:
            res = '\\bibitem{' + self.code + '}\n'
            res += self.authors + '. ' + self.title + '. '
            publisher = self.non_empty_publisher()
            if publisher:
                res += publisher + ', '
            if self.venue:
                res += self.venue +', '
            if self.publisher:
                res += self.publisher + ', '
            if self.year:
                res += self.year + ', '
            if self.volume:
                if self.number:
                    res += self.volume +'(%s)'%self.number+':'
                else:
                    res += self.volume + ':'
            if self.pages:
                self.pages = self.pages.replace('--','-')
                res += "{}".format(self.pages) if self.volume else "pp. {}".format(self.pages)
            
            if res.endswith(', '):
                res = res[:-2] + '.\n'
            else:
                res += '.\n'

            res += '\n\n'
            return res

def parse_singleline(line):
    if line.endswith(','):
        res = line.split('{')[-1][:-2]
    else:
        res = line.split('{')[-1][:-1]
    return res

def phase_tex2item(bibfile, itemfile):
    item_file = open(itemfile, 'w')
    with open(bibfile, 'r') as f:
        bibtexlines = f.readlines()
        is_first = True
        item = None
        for line in bibtexlines:
            line = line.strip()
            if not line: continue
            if line.startswith('@'):
                if not is_first:
                    item_file.write(item.write_tofile())
                else:
                    is_first = False
                code = line.split('{')[-1][:-1] # remove the comma
                item = BibItem(code)
                item.authors = []
            else:
                if line.startswith('title'):
                    item.title = parse_singleline(line)
                elif line.startswith('journal'):
                    item.venue = parse_singleline(line)
                elif line.startswith('booktitle'):
                    item.booktitle = parse_singleline(line)
                elif line.startswith('volume'):
                    item.volume = parse_singleline(line)
                elif line.startswith('number'):
                    item.number = parse_singleline(line)
                elif line.startswith('pages'):
                    item.pages = parse_singleline(line)
                elif line.startswith('year'):
                    item.year = parse_singleline(line)
                elif line.startswith('publisher'):
                    item.publisher = parse_singleline(line)
                elif line.startswith('author'):
                    authors = line[line.find("{")+1:line.rfind("}")]

                    for LastFirst in authors.split('and'):
                        lf = LastFirst.replace(' ', '').split(',')
                        if len(lf) != 2: continue
                        last, first = lf[0], lf[1]
                        item.authors.append("{}, {}.".format(last.capitalize(), first.capitalize()[0]))
                    
                    # print(item.authors)
                    if len(item.authors) == 1:
                        item.authors = (item.authors[0] + " {}. ".format(item.title))
                    else:
                        try:
                            item.authors = (", ".join(_ for _ in item.authors[:-1]) + " \& " + item.authors[-1]) #+ " {}. ".format(item.title))
                        except:
                            print(item.code)
                            print(item.authors)
        item_file.write(item.write_tofile())


if __name__=='__main__':
    phase_tex2item('bib2.bib','bibitem2.tex')