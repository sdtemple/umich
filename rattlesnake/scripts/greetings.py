import sys
filein,fileout,player_number,player_character=sys.argv[1:]
f=open(filein,'r')
greeting=f.readline().strip()
f.close()
greeting += ' '
greeting += str(player_character) 
greeting += ' '
greeting += player_number
g=open(fileout,'w')
g.write(greeting)
g.write('\n')
g.close()
