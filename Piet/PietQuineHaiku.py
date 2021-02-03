#
# piet quinelike haiku
# this is in public domain
# make war not poems
#

def P(s):
 h=v=0;l=len(s)+1;R=[[192,0,0]]
 C=[1,3,2,6,4,5];V=[0,192,192,255,0,255]
 for x in map("=|^+-*/%~>.,:@$?#!".find,s):
  C=C[x//3:]+C[:x//3];V=V[x%3*2:]+V[:x%3*2]
  R+=[[V[(C[0]//i)%2]for i in[1,2,4]]]
 return R

def addup(n):
    if n == 0:
        return '|~'

    b = bin(n)[3:]
    m = {'0':':+', '1':'::+'}
    s = '|'+''.join(m[i] for i in b[::-1])
    s+= '+'*b.count('1')
    
    return s

def printstring(s):
    p = ''
    o = 0
    for c in s:
        co = ord(c)
        if co > o:
            p+= addup(co-o) + '+'*(o!=0)+':!'
        elif co == o:
            p+= ':!'
        else:
            p+= addup(o-co) + '-'*(o!=0)+':!'
        o = co
    return p

alph = """\
      ooooo oooo  ooooo oooo  ooooo ooooo ooooo o   o ooooo    oo o   o o     ooooo o   o  ooo  ooooo  ooo  ooooo ooooo ooooo o   o o   o o o o o   o o   o ooooo 
      o   o o   o o     o   o o     o     o     o   o   o       o o  o  o     o o o oo  o o   o o   o o   o o   o o       o   o   o o   o o o o  o o   o o     o  
      ooooo oooo  o     o   o ooooo ooooo o ooo ooooo   o       o ooo   o     o o o o o o o   o ooooo o   o ooooo ooooo   o   o   o o   o o o o   o     o     o   
      o   o o   o o     o   o o     o     o   o o   o   o   o   o o  o  o     o o o o  oo o   o o     o  oo o  o      o   o   o   o  o o  o o o  o o    o    o    
      o   o oooo  ooooo oooo  ooooo o     ooooo o   o ooooo ooooo o   o ooooo o o o o   o  ooo  o      oooo o   o ooooo   o   ooooo   o   ooooo o   o   o   ooooo  
                                                                                                                                                                   """.split('\n')

pixwid = 6 
pixhgt = 6

lett = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ'
Alph = dict((a,[alph[i][pixwid*j:pixwid*(j+1)] for i in range(pixhgt)]) for j,a in enumerate(lett))


print "filename then haiku"
print "punctuation ruins poem"
print "you might as well yell"

filename = raw_input()
hku = [raw_input() for _ in range(3)]

hlen = max(map(len,hku))

msg = [''.join(Alph[c][i] for c in hku[0]+' '*(hlen-len(hku[0]))) for i in range(pixhgt)]
msg+= [''.join(Alph[c][i] for c in hku[1]+' '*(hlen-len(hku[1]))) for i in range(pixhgt)]
msg+= [''.join(Alph[c][i] for c in hku[2]+' '*(hlen-len(hku[2]))) for i in range(pixhgt)]

last = 0

outfile = open(filename,'w')
outfile.write( "P3 %d %d 255 "%(pixwid*hlen*2 + 5, pixhgt*3*2) )

left = [" 255 0 0  255 0   0    255 255 255 ",
        " 0   0 0  0   0   0    255 255 255 ",
        " 255 0 0  255 255 255  255 255 255 ",
        " 255 0 0  255 255 255  255 255 255 "]

right = [" 255 255 255  255 0 0 ",
         " 255 255 255  255 0 0 ",
         " 255 0   0    255 0 0 ",
         " 0   0   0      0 0 0 "]

lastleft = [" 0 0 0 0 0 0 255 255 255 ",
            " 255 0 0 255 0 0 255 255 255 "]
lastright = [" 255 0 0 255 0 0 ",
             " 0 0 0 0 0 0 "]

ins = printstring('\n'.join(hku))

for i in range(pixhgt*3):
    line = msg[i]
    outline = []
    progline = ''
    if i%2:
        line = line[::-1]    
    dotlen = 0
    for c in line:
        if dotlen and c == ' ':
            next=last+2*dotlen-1
            p = ins[last:next]
            p+= '='*(next-last-len(p))
            outline += P(p)
            progline += 's' + p
            last = next
            dotlen = 0
        if c == ' ':
            outline += [[255]*3]*2
            progline += '  '
        else:
            dotlen += 1
    if dotlen:
        next=last+2*dotlen-1
        p = ins[last:next]
        p+= '='*(next-last-len(p))
        outline += P(p)
        progline += 's' + p
        last = next

    if i%2:
        progline = progline[::-1]
        outline = outline[::-1]
        line = line[::-1]
    outfile.write(left[(2*i)%4])
    outfile.write(' '.join(map(str,sum(outline,[]))))
    outfile.write(right[(2*i)%4])
    if i == pixhgt*3-1:
        outfile.write(lastleft[i%2])
        outfile.write(''.join([' 0 0 0 ',' 255 255 255 '][c==' ']*2 for c in line))
        outfile.write(lastright[i%2])
    else:
        outfile.write(left[(2*i+1)%4])
        outfile.write(''.join([' 0 0 0 ',' 255 255 255 '][c==' ']*2 for c in line))
        outfile.write(right[(2*i+1)%4])
    print progline

if last == len(ins):
    print "congratulations,",
print "your haiku was %.2f%% zen"%(last*100./len(ins))