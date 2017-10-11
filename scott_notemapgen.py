import scancode_list

lowcodes={}
hicodes={}
for entry in scancode_list.codes:
    lowcodes[entry[0]] = entry[1]
    hicodes[entry[0]] = entry[2]

lines = ["1234567890-=",
         "qwertyuiop[]",
         "asdfghjkl;'",
         "zxcvbnm,./"]

notes = [60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81]
instruments = [1, # acoustic grand piano
       14, # xylophone
       27, # electric guitar
       74, # flute
      ]

notecodelist = []
chancodelist = []
for i in range(128):
    note = None
    ins = None
    if i in lowcodes:
        ch = lowcodes[i]
        line_index = 0
        for line in lines:
            char_index = 0
            for lch in line:
                if (lch == ch):
                    note = notes[char_index]
                    chan = line_index + 2
                char_index += 1
            line_index += 1

    if note:
        notecodelist.append( note )
        chancodelist.append( chan )
    else:
        notecodelist.append(0)
        chancodelist.append(0)
 
print "const char notemap[128] PROGMEM = {%s};" % ",".join([str(x) for x in notecodelist])
print "const char chanmap[128] PROGMEM = {%s};" % ",".join([str(x) for x in chancodelist]) 
