# fastaReader.py
class fastaReader():

    def __init__(self):
        self.path = "multifasta.fasta"
        self.seqs = []
        self.names = []
        self.read()

    def read(self):
        with open(self.path, "r") as f:
            lines = f.readlines()
        seq = ""
        for line in lines:
            if line.startswith(">"):
                self.names.append(line[1:].strip())
                if seq:
                    self.seqs.append(seq)
                seq = ""
            else:
                seq += line.strip()
        self.seqs.append(seq)
