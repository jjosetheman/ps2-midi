# http://www.smbaker.com/
#
# List of general midi percussion instruments

class percuss_list:
  BASSDRUM2 = 35
  BASSDRUM1 = 36
  SIDESTICK = 37
  SNAREDRUM1 = 38
  HANDCLAP = 39
  SNAREDRUM2 = 40
  LOWTOM2 = 41
  CLOSEDHIHAT= 42
  LOWTOM1 = 43
  PEDALHIHAT= 44
  MIDTOM2 = 45
  OPENHIHAT = 46
  MIDTOM1 = 47
  HIGHTOM2 = 48
  CRASHCYMBAL1 = 49
  HIGHTOM1 = 50
  RIDECYMBAL1 = 51
  CHINESECYMBAL= 52
  RIDEBELL = 53
  TAMBOURINE = 54
  SPLASHCYMBAL = 55
  COWBELL = 56
  CRASHCYMBAL2 = 57
  VIBRASLAP = 58
  RIDECYMBAL2 = 59
  HIGHBONGO= 60
  LOWBONGO = 61
  MUTHIGHCONGA = 62
  OPENHIGHCONGA = 63
  LOWCONGA = 64
  HIGHTIMBALE = 65
  LOWTIMBALE = 66
  HIGHAPOGO = 67
  LOWAPOGO = 68
  CABASA = 69
  MARACAS = 70
  SHORTWHISTLE = 71
  LONGWHISTLE=72
  SHORTGUIRO=73
  LONGGUIRO = 74
  CLAVES = 75
  HIGHWOODBLOCK = 76
  LOWWOODBLOCK = 77
  MUTECUICA = 78
  OPENCUICA = 79
  MUTETRIANGLE = 80
  OPENTRIANGLE = 81
  EIGHTTHREE = 83

percuss_to_note = {}
note_to_percuss = {}

for item_name in dir(percuss_list):
    item = getattr(percuss_list, item_name)
    if isinstance(item, int):
        globals()[item_name] = item

        percuss_to_note[item_name] = item
        note_to_percuss[item] = item_name
