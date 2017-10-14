from scancode_list import *

lowcodes={}
hicodes={}
for entry in codes:
    lowcodes[entry[0]] = entry[1]
    hicodes[entry[0]] = entry[2]

extcodes={}
for entry in extended_codes:
    extcodes[entry[0]] = entry[1]

lines = ["1234567890-=",
         "qwertyuiop[]\\",
         "asdfghjkl;'",
         "zxcvbnm,./",
         F1 + F2 + F3 + F4 + F5 + F6 + F7 + F8 + F9 + F10 + F11 + F12,
         "",
         "",
         ""
         " `" + BS + TAB + ENTER + BACKQUOTE + ESC + LCTRL + LALT + SCROLL + NUM + LARR + DARR + UARR + RARR + INS + DEL + HOME + PGUP + PGDN + END]

notes = [60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81, 83, 36, 38, 40, 41, 43, 45, 47]

def map_code(ch):
        line_index = 0
        for line in lines:
            char_index = 0
            for lch in line:
                if (lch == ch):
                    note = notes[char_index]
                    chan = line_index
                    return (note, chan)
                char_index += 1
            line_index += 1

        return (None, None)

# The highest scancode is function key F7 which is 0x83. So we only need to 
# create arrays for 132 scan codes.

notecodelist = []
chancodelist = []
for i in range(132):
    note = None
    ins = None
    if i in lowcodes:
        (this_note, this_chan) = map_code(lowcodes[i])
        if this_note:
            note=this_note
            chan=this_chan

    if note:
        notecodelist.append( note )
        chancodelist.append( chan )
    else:
        notecodelist.append(0)
        chancodelist.append(0)

ext_notecodelist = []
ext_chancodelist = []
for i in range(132):
    note = None
    ins = None
    if i in extcodes:
        (this_note, this_chan) = map_code(extcodes[i])
        if this_note:
            note=this_note
            chan=this_chan

    if note:
        ext_notecodelist.append( note )
        ext_chancodelist.append( chan )
    else:
        ext_notecodelist.append(0)
        ext_chancodelist.append(0)
 
print "const char notemap[132] PROGMEM = {%s};" % ",".join([str(x) for x in notecodelist])
print "const char chanmap[132] PROGMEM = {%s};" % ",".join([str(x) for x in chancodelist]) 
print "const char ext_notemap[132] PROGMEM = {%s};" % ",".join([str(x) for x in ext_notecodelist])
print "const char ext_chanmap[132] PROGMEM = {%s};" % ",".join([str(x) for x in ext_chancodelist])
