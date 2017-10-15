# http://www.smbaker.com//
#
# Generates mapping of keyboard scancodes to midi notes and channels 

from scancode_list import *
from midipercuss import *

lowcodes={}
hicodes={}
for entry in codes:
    lowcodes[entry[0]] = entry[1]
    hicodes[entry[0]] = entry[2]

extcodes={}
for entry in extended_codes:
    extcodes[entry[0]] = entry[1]

# List of keyboard lines. Each one of these lines will be mapped to a set
# of notes starting with middle C for a particular instrument.

lines = ["1234567890-=",
         "qwertyuiop[]\\",
         "asdfghjkl;'",
         "zxcvbnm,./",
         F1 + F2 + F3 + F4 + F5 + F6 + F7 + F8 + F9 + F10 + F11 + F12]

# The percussion line is special, as it isn't really notes, but rather a
# set of instruments.

percuss_line = {" ": HIGHTOM1,
                "`": MUTHIGHCONGA,
                BS: LOWCONGA,
                TAB: HIGHTIMBALE,
                ENTER: OPENHIGHCONGA,
                BACKQUOTE: LOWAPOGO,
                ESC: SHORTWHISTLE,
                LCTRL: CLAVES,
                LALT: LONGGUIRO,
                SCROLL: HIGHWOODBLOCK,
                NUM: LOWWOODBLOCK,
                LARR: OPENCUICA,
                DARR: OPENTRIANGLE,
                UARR: EIGHTTHREE,
                RARR: BASSDRUM1,
                INS: SNAREDRUM1,
                DEL: SNAREDRUM2,
                HOME: LOWTOM2,
                PGUP: LOWTOM1,
                PGDN: MIDTOM2,
                END: MIDTOM1,
                LGUI: HIGHTOM2,
                RGUI: 50,
                LSHIFT: CHINESECYMBAL,
                RSHIFT: VIBRASLAP,
                CAPSLOCK: HANDCLAP,
                RCTRL: CRASHCYMBAL2,
                RALT: MIDTOM2,
                "*": COWBELL,
                "+": MIDTOM2,
                APPS: CRASHCYMBAL1}

# List of notes. 60 is middle C, 62 is D, ...

notes = [60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81, 83, 
         36, 38, 40, 41, 43, 45, 47, 48, 50, 52, 53, 55, 57, 59,
         24, 26]

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

        if ch in percuss_line:
            return (percuss_line[ch], 7)

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
