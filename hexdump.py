def printDumpList(file,coding = None,biteSign = '',decodeSign = "X",posisions = [],color = 'turn',printRange = [0,-1]):
    import re
    pos = printRange[0]
    end = printRange[1]
    file.seek(pos)
    blank = re.compile(r'\s')
    mb = 0
    mbBin = bytearray()
    modeChange = False
    modes = {'ascii':b'\x1b(B','roma':b'\x1b(J','JIS78':b'\x1b$@','JIS83':b'\x1b$B','JIS90':b'\x1b$(D','JIS2004-1':b'\x1b$(Q','JIS2004-2':b'\x1b$(P'}
    mode = modes['ascii']
    colors = {'turn':'\033[7m','clear': '\033[0m','black': '\033[30m','red': '\033[31m','green': '\033[32m','yellow': '\033[33m','blue': '\033[34m','purple': '\033[35m','cyan': '\033[36m','white': '\033[37m'}
    if coding in {'ascii', 'ASCII', 'Ascii'}: coding = None
    while True:
        temp = file.read(16)
        tempHeader, tempBody, tempFooter = '','',''
        if len(temp) == 0 :
            file.seek(0)
            break
        tempHeader = '%09x: ' % pos
        for b in temp:
            if pos in posisions:
                tempBody += " " + colors[color] + "%02x\033[0m" % b
                tempFooter += colors[color]
            else:
                tempBody += " %02x" % b
            mbBin.append(b)
            if coding in {"shift-JIS","shitf-jis","sj"}:
                try:
                    if mb == 0:
                        if (32 <= b and b <= 126) or (160 <= b and b <= 223):
                            tempFooter += mbBin.decode("shift-JIS")
                            mbBin = bytearray()
                        elif (128 <= b and b <= 159) or (224 <= b and b <= 253):
                            mb = 1
                            tempFooter += biteSign
                        else:
                            tempFooter += '.'
                            mbBin = bytearray()
                    elif mb == 1:
                        tempFooter += mbBin.decode('shift-JIS')
                        mb = 0
                        mbBin = bytearray()
                except UnicodeDecodeError:
                    mbBin = bytearray()
                    mb = 0
                    tempFooter += decodeSign
            elif coding in {"utf-8",'utf8'}:
                try:
                    if mb == 0:
                        if (32 <= b and b <= 126) or (160 <= b and b <= 223):
                            tempFooter += mbBin.decode("utf-8")
                            mbBin = bytearray()
                        elif 192 <= b and b <= 223:
                            mb = 1
                            tempFooter += biteSign
                        elif 224 <= b and b <= 239:
                            mb = 2
                            tempFooter += biteSign
                        elif 240 <= b and b <= 247:
                            mb = 3
                            tempFooter += biteSign
                        elif 248 <= b and b <= 251:
                            mb = 4
                            tempFooter += biteSign
                        elif 252 <= b and b <= 255:
                            mb = 5
                            tempFooter += biteSign
                        else:
                            tempFooter += '.'
                            mbBin = bytearray()
                    elif mb > 1:
                        mb -= 1
                        tempFooter += biteSign
                    elif mb == 1:
                        tempFooter += mbBin.decode('utf-8')
                        mb = 0
                        mbBin = bytearray()
                except UnicodeDecodeError:
                    mbBin = bytearray()
                    mb = 0
                    tempFooter += decodeSign
            elif coding in {'JIS','jis','Jis'}:
                try:
                    if modeChange == True:
                        if bytes(mbBin) in modes.values():
                            mode = bytes(mbBin)
                            mbBin = bytearray()
                            modeChange = False
                            if mode in [modes['ascii'],modes['roma']]: mb = 0
                            elif mode in [modes['JIS78'],modes['JIS83'],modes['JIS90'],modes['JIS2004-1'],modes['JIS2004-2']]: mb = 1
                    else:
                        if mb == 0:
                            if b == 27:#modeChange
                                modeChange = True
                                tempFooter += '[MC]'
                                mode = None
                            elif b <= 32:#Control character
                                tempFooter += ' '
                                mbBin = bytearray()
                            elif mode in [modes['ascii'],modes['roma']]:
                                tempFooter += bytearray(mode + bytes(mbBin)).decode("iso2022jp")
                                mbBin = bytearray()
                            elif mode in [modes['JIS78'],modes['JIS83'],modes['JIS90']]:
                                tempFooter += bytearray(mode + bytes(mbBin)).decode("iso2022jp")
                                mbBin = bytearray()
                                mb = 1
                                tempFooter += biteSign
                            elif mode in [modes['JIS2004-1'],modes['JIS2004-2']]:
                                tempFooter += bytearray(mode + bytes(mbBin)).decode("iso-2022-jp-2004")
                                mbBin = bytearray()
                                mb = 1
                                tempFooter += biteSign
                            else:
                                tempFooter += '.'
                                mbBin = bytearray()
                        else:
                            if b == 27:
                                modeChange = True
                                tempFooter += '[MC]'
                                mode = None
                            elif (b < 21) or (126 < b):
                                tempFooter += '.'
                                mbBin = bytearray()
                            mb -= 1
                except UnicodeDecodeError:
                    mbBin = bytearray()
                    mb = 0
                    tempFooter += decodeSign
            elif coding in {'EUC','euc','euc-jp','euc_jp','eucjp'}:
                try:
                    if mb == 0:
                        if 32 <= b and b <= 126:
                            tempFooter += mbBin.decode("euc_jp")
                            mbBin = bytearray()
                        elif 160 <= b and b <= 255:
                            mb = 1
                            tempFooter += biteSign
                        elif b == 142:
                            mb = 2
                            tempFooter += biteSign
                        elif b == 143:
                            mb = 3
                            tempFooter += biteSign
                        else:
                            tempFooter += '.'
                            mbBin = bytearray()
                    elif mb > 1:
                        mb -= 1
                        tempFooter += biteSign
                    elif mb == 1:
                        tempFooter += mbBin.decode('euc_jp')
                        mb = 0
                        mbBin = bytearray()
                except UnicodeDecodeError:
                    mbBin = bytearray()
                    mb = 0
                    tempFooter += decodeSign
            else:
                if 32 <= b and b <= 126:
                    tempFooter += chr(b)
                else:
                    tempFooter += '.'
            if pos in posisions:
                tempFooter += colors["clear"]
            if pos == end:
                file.read()
                break
            pos += 1
        print(tempHeader + tempBody.ljust(50 +(4 + len(colors[color]))*tempFooter.count(colors["clear"])) + blank.sub(' ',tempFooter))
    print("%09x:" % pos)
def main():
    import sys, argparse, readline ,io
    def expand(list):
        result = []
        for item in list:
            try: result.append(int(item,16))
            except ValueError:
                try:
                    if '~' in item:
                        expand = item.split('~')[:2]
                        if expand[0] == '': expand[0] = '0'
                        if expand[1] != '': result.extend([ i for i in range(int(expand[0],16),int(expand[1],16)+1)])
                    else:
                        raise Exception
                except Exception:
                    pass
        return result
    inputArgs = None
    AppDescription = 'This app show you input-file as hex-dump. And you can edit your file.'
    mainParser = argparse.ArgumentParser(prog='python3 ' + sys.argv[0],description = AppDescription, prefix_chars='-',)
    mainParser.add_argument('file', action = "store", help = 'file input.',)
    mainParser.add_argument('-c', action = "store", dest = 'coding', default = None, help = 'Set encoding type.(default:ascii)',)
    mainParser.add_argument('-color', action = "store", dest = 'color', default = 'turn', help = 'Set color.(default:red)',)
    mainParser.add_argument('-b', action = "store", dest = 'byteSign', default = '', help = 'Set byte sign. If you set this print byte sign, when read multi-bytes character. (default:"")',)
    mainParser.add_argument('-d', action = "store", dest = "undecodeSign", default = 'X', help = 'Set un-decode sign. If you set this print un-decode sign, when catch decode exception. (default:"X")',)
    mainParser.add_argument('-p', action = "store",dest="pos",default = "",nargs = "+")
    mainParser.add_argument('--range', action = "store",dest="range",default = ['0','-1'],nargs = 2)#--RANGE
    mainParser.add_argument('-e', action = "store_true", dest = 'edit', default = False,help='Turn Editor mode on',)
    inputParser = argparse.ArgumentParser(prog='', prefix_chars='-+',)
    inputParserSwitch = inputParser.add_mutually_exclusive_group()
    inputParserSwitch.add_argument('-q', action = "store_false",dest = 'edit', help="Don't save file and quit.",)
    editMode = inputParser.add_mutually_exclusive_group()
    editMode.add_argument('-i',action = "store",dest = 'insert',nargs = 2, help = 'Set input mode.')
    editMode.add_argument('-r',action = "store",dest = 'replace',nargs = 2, help = 'Set replave mode.')
    editMode.add_argument('-d',action = "store",dest = 'delete',nargs = 1, help = 'Set delete mode.')
    editMode.add_argument('-s', action = "store_true",dest = 'save', default = False, help='Save.',)
    editMode.add_argument('-a',action = "store",dest = 'append',nargs = 1, help = 'Set append mode.')
    editMode.add_argument('-0',action = "store",dest = 'zero',nargs = 2, help = 'Set zero mode.')
    inputParser.add_argument('--range', action = "store",dest="range",default = ['0','-1'],nargs = 2)#--RANGE
    inputParser.add_argument('-p', action = "store",dest="pos",default = "",nargs = "+")
    args = mainParser.parse_args()
    editor = args.edit
    try: printRange = [int(args.range[i],16) for i in range(2)]
    except ValueError:
        printRange = [0,-1]
        print('[ERROR] Input arguments as hex syntax.')
    posisions = expand(args.pos)
    try:
        with open(args.file,'rb') as f:
            tempFile = io.BytesIO(f.read())
            isNewFile = False
    except FileNotFoundError:
        print('[NEW FILE] : ' + args.file )
        tempFile = io.BytesIO()
        isNewFile = True
    while True:
        try:
            size = len(tempFile.read())
            tempFile.seek(0)
            if editor:
                printDumpList(tempFile,args.coding,args.byteSign,args.undecodeSign,posisions,args.color,printRange)
                inputArgs = inputParser.parse_args(input("[EDIT] >>> ").split())
                editor = inputArgs.edit
                posisions = expand(inputArgs.pos)
                try: printRange = [int(inputArgs.range[i],16) for i in range(2)]
                except ValueError:
                    printRange = [0,-1]
                    print('[ERROR] Input arguments as hex syntax.')
                if inputArgs.insert:
                    posisions.append(int(inputArgs.insert[0],16))
                    if int(inputArgs.insert[1],16) <= 255:
                        b = bytearray()
                        b.append(int(inputArgs.insert[1],16))
                        newFile = io.BytesIO()
                        newFile.write(tempFile.read(int(inputArgs.insert[0],16)))
                        newFile.write(b)
                        newFile.write(tempFile.read())
                        newFile.seek(0)
                        tempFile.seek(0)
                        tempFile = newFile
                elif inputArgs.replace:
                    if  int(inputArgs.replace[0],16) > size and int(inputArgs.replace[1],16) >= 255: print('[ERROR] First argument out of file size.\n[ERROR] Please input second argument in range from 00 to ff.')
                    elif int(inputArgs.replace[0],16) > size: print('[ERROR] First argument out of file size.')
                    else:
                        posisions.append(int(inputArgs.replace[0],16))
                        if int(inputArgs.replace[1],16) <= 255:
                            b = bytearray()
                            b.append(int(inputArgs.replace[1],16))
                            newFile = io.BytesIO()
                            newFile.write(tempFile.read(int(inputArgs.replace[0],16)))
                            newFile.write(b)
                            tempFile.read(1)
                            newFile.write(tempFile.read())
                            newFile.seek(0)
                            tempFile.seek(0)
                            tempFile = newFile
                        else: print('[ERROR] Please input second argument in range from 00 to ff.' )
                elif inputArgs.append:
                    if int(inputArgs.append[0],16) <= 255:
                        b = bytearray()
                        b.append(int(inputArgs.append[0],16))
                        newFile = io.BytesIO()
                        newFile.write(tempFile.read())
                        newFile.write(b)
                        newFile.seek(0)
                        tempFile.seek(0)
                        tempFile = newFile
                elif inputArgs.delete:
                    newFile = io.BytesIO()
                    newFile.write(tempFile.read(int(inputArgs.delete[0],16)))
                    tempFile.read(1)
                    newFile.write(tempFile.read())
                    newFile.seek(0)
                    tempFile.seek(0)
                    tempFile = newFile
                elif inputArgs.zero:
                    try:
                        st = int(inputArgs.zero[0],16)
                        end = st + int(inputArgs.zero[1],16)
                        if st <= size:
                            posisions.extend([i for i in range(st, end)])
                            newFile = io.BytesIO()
                            newFile.write(tempFile.read(st))
                            newFile.write(bytearray(int(inputArgs.zero[1],16)))
                            newFile.write(tempFile.read())
                            newFile.seek(0)
                            tempFile.seek(0)
                            tempFile = newFile
                    except Exception: pass
                elif inputArgs.save:
                    if isNewFile:
                        try:
                            outFile = open(args.file,'wb')
                            outFile.write(tempFile.read())
                        finally:
                            outFile.close()
                            print("Saveed successfully...")
                            break
                    else:
                        while True:
                            readline.insert_text(args.file)
                            saveAs = input("Save as ... > ")
                            if saveAs == '': saveAs = args.file
                            if saveAs == args.file:
                                overwrite = input('Are you sure to overwrite file? (yes:1, no:2) : ')
                                if overwrite in {'1','yes','YES','Yes','True','true','y'}: break
                                else: pass
                            else: break
                        try:
                            outFile = open(saveAs,'wb')
                            outFile.write(tempFile.read())
                        finally:
                            outFile.close()
                            print("Saveed successfully...")
                            break
            elif not editor and inputArgs is None:
                printDumpList(tempFile,args.coding,args.byteSign,args.undecodeSign,posisions,args.color,printRange)
                break
            else: break
        except Exception: print("[ERROR]")
if __name__ == '__main__':
    main()
