from music21 import *

def make_sheet(title,data,destinationPath):
    stream1 = stream.Stream()

    #연속적으로 같은 코드인데 중간에 하나만 다른 것은 같은 것으로 취급할 수 있어야 함
    #data=['A','A',0,0,0,0,0,'B','E','E','E','E',0,0,0,0,0]

    last=data[0]
    s=0 
    si=list()

    for i in data:
        if last!=i:
            si.append([last, s])
            last=i
            s=0
        else: 
            s+=1
    si.append([i, s])
    m=0 
    for i in si:
        m+=i[1]
    avg=m/len(si)

    ral=0
    beat=2

    for i in si:
        if i[1]<0.5*avg:
            beat=0.5
        elif 0.5*avg<=i[1] and i[1]<1.5*avg:
            beat=1
        elif 1.5*avg<=i[1] and i[1]<2.5*avg:
            beat=2
        else:
            beat=4
        if i[0]==0:
            n=note.Rest()
            n.quarterLength=beat
            stream1.append(n)
        else:
            n=note.Note(i[0])
            n.quarterLength=beat
            stream1.append(n)
    md = metadata.Metadata()
    md.title=title
    md.composer='으악 기타'
    stream1.insert(0, md)
    #stream1.show('xml')
    stream1.write('xml',destinationPath)

#make_sheet('asdf',['A','A',0,0,0,0,0,'B','E','E','E','E',0,0,0,0,0],'processed/asdf.musicxml')
