# encoding: utf-8
class autoCobol:
    def __init__(self, programname, tables, files):
        self.programname = programname
        self.files = files
        self.tables = tables
        self.cobolFile = open('COBOL.txt', 'a')
        self.varlist = []

    def createprogram(self):
        self.creatIDENTIFICATION()
        self.createnvironment()
        self.createdatadicision()
        self.createvardefine()
        self.createcursordefine()
        self.createprocedure()


    def creatIDENTIFICATION(self):
        temstr = ' '*7 + 'IDENTIFICATION DIVISION.\n'
        line = ' '*7 + 'PROGRAM-ID.   %s.\n' % self.programname
        temstr = temstr + line
        line = ' '*6 + '*'*65 + '\n'
        temstr = temstr + line
        self.cobolFile.writelines(temstr)

    def createnvironment(self):
        line = ' '*7 + 'ENVIRONMENT DIVISION.\n' + ' '*7 + 'CONFIGURATION SECTION.\n' \
               + ' '*7 + 'INPUT-OUTPUT SECTION.\n' \
               + ' '*7 + 'FILE-CONTROL.\n'
        templine = ' '*12 + 'SELECT OPTIONAL BATCHNO ASSIGN TO S-BATCHNO\n' \
                   + ' '*19 + 'FILE STATUS IS FILE-STATUS.\n'
        line = line + templine
        self.cobolFile.writelines(line)
        for filemap in self.files:
            line = templine.replace('BATCHNO', filemap)
            self.cobolFile.writelines(line)

    def createdatadicision(self):
        # FILE SECTION
        line = ' '* 7 + '*--------------------------------------------------------------*\n'
        line = line + ' '*7 + 'DATA  DIVISION.\n' + ' '*7 + 'FILE  SECTION.\n' \
            + ' '*7 + 'FD  BATCHNO.\n' + ' '*7 + '01  BATCHNO-RES.\n' + ' '*11 + '02  BATCHNO-BATCHNO    PIC X(80).\n'
        for file in self.files:
            line = line + ' '*7 + 'FD %s.\n' %file
            line = line + ' '*11 + 'COPY %s.\n' %file.replace('F', 'C', 1)
        self.cobolFile.writelines(line)
        # WORKING-STORAGE SECTION
        line = ' '* 7 + '*--------------------------------------------------------------*\n'
        line = line + ' '*7 + 'WORKING-STORAGE SECTION.\n' + ' '*7 + '77 DEBUG-VAR       PIC X(50) VALUE\n' \
               + ' '*13 + '\'<#NOVA+ V1.8.2#FF V1.0.0#F-ABDB V1.21.00.3#>.\'\n' \
               + ' '*7 + '77 DUBUG-PRG-VER   PIC X(50) VALUE\n' \
               + ' '*13 + '\'<#MAOLX#100608#Y#0000#>\'.\n'
        self.cobolFile.writelines(line)
        # 生成* CPY 注释
        line = ' '*6 + '*'*65 + '\n' + ' '*6 + '*       DB2 SQL TABLE\'S COPYBOOK' + ' '*(63-31) + '*\n' \
               + ' '*6 + '*'*65 + '\n'
        self.cobolFile.writelines(line)
        #生成表的CPY
        templine = ' '*11 + 'EXEC SQL INCLUDE ATHMODTL END-EXEC.\n'
        for tablemap in self.tables:
            line = templine.replace('ATHMODTL',tablemap)
            self.cobolFile.writelines(line)
        line = ' '*6 + '*'*65 + '\n' \
               + ' '*6 + '*    INCLUDE PUBLIC VARIABLE :                                  *\n' \
               + ' '*6 + '*       1.  PROGRAM-NAME                                        *\n' \
               + ' '*6 + '*       2.  MIN-ACCNO                                           *\n' \
               + ' '*6 + '*       3.  MAX-ACCNO                                           *\n' \
               + ' '*6 + '*       4.  NOT-FOUND       ( VALUE +100 )                      *\n' \
               + ' '*6 + '*       5.  WARNING-COUNT   ( VALUE  0  )                       *\n' \
               + ' '*6 + '*       6.  COMMIT-COUNT    ( VALUE SPACES )                    *\n' \
               + ' '*6 + '*       7.  M-ACTION        ( VALUE SPACES )                    *\n' \
               + ' '*6 + '*       8.  M-ACTION-KEY    ( VALUE SPACES )                    *\n' \
               + ' '*6 + '*****************************************************************\n' \
               + ' '*14 + 'EXEC SQL INCLUDE PUBVARCB END-EXEC.\n' \
               + ' '*14 + 'EXEC SQL INCLUDE PROVARCB END-EXEC.\n'
        self.cobolFile.writelines(line)

    # 生成变量定义 初始化默认值
    def createvardefine(self):
        line = '      *****************************************************************\n' \
             + '      *       PRIVATE VARIBLES                                        *\n' \
             + '      *****************************************************************\n'
        self.cobolFile.writelines(line)
        for tablemap in self.tables:
            rw = self.tables[tablemap][0]
            dealtyp = self.tables[tablemap][1]
            if rw.upper() == 'R':
                if dealtyp.upper() == 'CURSOR':
                    line = ''
                    # END-OF-TABLE PIC X VALUE 'F'
                    templine = ' '*7 + '77 END-OF-TABLE            PIC X(01) VALUE \'F\'.\n'
                    line = line + templine.replace('TABLE', tablemap)
                    varname = 'END-OF-%s' %tablemap
                    self.varlist.append(varname)
                    # 77 FETCH-TABLE-COUNT       PIC 9 VALUE 0.
                    templine = ' '*7 + '77 FETCH-TABLE-COUNT       PIC 9(17) VALUE 0.\n'
                    line = line + templine.replace('TABLE', tablemap)
                    varname = 'FETCH-%s-COUNT' %tablemap
                    self.varlist.append(varname)
                    self.cobolFile.writelines(line)

                if dealtyp.upper() == 'SELECT':
                    line = ''
                    # 77 SELECT-TABLE-COUNT      PIC 9 VALUE 0.
                    templine = ' '*7 + '77 SELECT-TABLE-COUNT      PIC 9(17) VALUE 0.\n'
                    line = line + templine.replace('TABLE', tablemap)
                    varname = 'SELECT-%s-COUNT' %tablemap
                    self.varlist.append(varname)
                    self.cobolFile.writelines(line)

            if rw.upper() == 'W':
                line = ''
                #77 INSERT-TABLE-COUNT      PIC 9(17) VALUE 0.
                templine = ' '*7 + '77 INSERT-TABLE-COUNT      PIC 9(17) VALUE 0.\n'
                line = line + templine.replace('TABLE', tablemap)
                varname = 'INSERT-%s-COUNT' %tablemap
                self.varlist.append(varname)
                self.cobolFile.writelines(line)
        for filemap in self.files:
            if rw.upper() == 'R':
               line = ''
               # END-OF-FILE PIC X VALUE 'F'
               templine = ' '*7 + '77 END-OF-FILE             PIC X(01) VALUE \'F\'.\n'
               line = line + templine.replace('FILE', filemap)
               varname = 'END-OF-%s' %filemap
               self.varlist.append(varname)
               # 77 READ-FILE-COUNT       PIC 9 VALUE 0.
               templine = ' '*7 + '77 READ-FILE-COUNT         PIC 9(17) VALUE 0.\n'
               line = line + templine.replace('FILE', filemap)
               varname = 'READ-%s-COUNT' %filemap
               self.varlist.append(varname)
               self.cobolFile.writelines(line)
            if rw.upper() == 'R':
               line = ''
               # 77 WRITE-FILE-COUNT       PIC 9 VALUE 0.
               templine = ' '*7 + '77 WRITE-FILE-COUNT        PIC 9(17) VALUE 0.\n'
               line = line + templine.replace('FILE', filemap)
               varname = 'WRITE-%s-COUNT' %filemap
               self.varlist.append(varname)
               self.cobolFile.writelines(line)

    def createcursordefine(self):
        line = ''
        templine = '      *****************************************************************\n' \
                 + '      *       DECLARE CURSOR                                          *\n' \
                 + '      *****************************************************************\n'
        line = '\n' + templine
        self.cobolFile.writelines(templine)
        for tablemap in self.tables:
            dealtyp = self.tables[tablemap][1]
            cpypath = self.tables[tablemap][2]
            if dealtyp.upper() == 'CURSOR':
               templine = '           EXEC SQL DECLARE CSR-TABLE CURSOR WITH HOLD FOR\n' \
                        + '                    SELECT\n'
               templine = templine.replace('TABLE', tablemap)
               cpyfile = open(cpypath,'r')
               for cpyline in cpyfile.readlines():
                    if 'NOT NULL' in cpyline and ',' in cpyline[cpyline.index('NOT NULL'):]:
                        cpyvar = cpyline[13:].split()[0]
                        l = ' '*27 + cpyvar + ' '*10
                        lenth = len(l)
                        l = l + ' '*(42-lenth) + ','
                        templine = templine + l + '\n'
                    elif 'NOT NULL' in cpyline and ',' not in cpyline[cpyline.index('NOT NULL'):]:
                        cpyvar = ' '*27 + cpyline[13:].split()[0]
                        templine = templine + cpyvar + '\n'
               l = ' '*22 + 'FROM %s' %tablemap + '\n'
               l = l + ' '*21 + 'WHERE \n'
               l = l + ' '*11 + 'END-EXEC' + '\n'
               templine = templine + l
               self.cobolFile.writelines(templine)
               cpyfile.close()

    def createprocedure(self):
        self.createmain()
        self.createmainend()
        self.createinitialize()
        self.createcurfetch()
        self.createselect()
        self.createinsert()
        self.createread()
        self.createwrite()
        self.createopncur()
        self.createclosecur()
        self.createopnfile()
        self.createdul()
        self.closefile()


    def createmain(self):
        templine = ' '*6 + '*' + '-'*63 + '*\n' \
                 + ' '*6 + '*       PROCEDURE DIVISION                                      *\n' \
                 + ' '*6 + '*' + '-'*63 + '*\n' \
                 + ' '*7 + 'PROCEDURE DIVISION.\n' \
                 + ' '*7 + '000-MAIN-BEGIN.\n' \
                 + ' '*11 + 'MOVE \'%s\'' %self.programname + ' '*4 + 'TO PROGRAM-NAME\n' \
                 + ' '*11 + 'MOVE \'T\'           TO PABPC-OPERFLAG-USE\n' \
                 + ' '*11 + 'MOVE \'F\'           TO PABPC-OPERFLAG-REPEAT\n' \
                 + ' '*11 + 'MOVE 3             TO ATHPABPC-PREBTHF\n' \
                 + ' '*11 + 'MOVE \'T\'           TO 910-AUTO-RERUN-FLAG\n' \
                 + ' '*11 + 'PERFORM PRE-PROCESS\n' \
                 + ' '*11 + 'PERFORM INITIALIZE-WORKING-STORAGE\n' \
                 + ' '*11 + 'MOVE ATHPABPC-PROCACTN TO RESTART-PROCACTN\n' \
                 + ' '*11 + 'DISPLAY \' ATHPABPC-WORKDATE = \' ATHPABPC-WORKDATE \n' \
                 + ' '*11 + 'DISPLAY \' ATHPASCT-WORKDATE = \' ATHPASCT-WORKDATE \n' \
                 + '\n' + '\n' + '\n' \
                 + ' '*11 + 'MOVE 3             TO ATHPABPC-PROCSTAT\n' \
                 + ' '*11 + 'MOVE SPACES        TO ATHPABPC-PROCACTN\n' \
                 + ' '*11 + 'MOVE SPACES        TO ATHPABPC-PROCPOS\n' \
                 + ' '*11 + 'MOVE SPACES        TO ATHPABPC-PROCPOS1\n' \
                 + ' '*11 + 'PERFORM END-PROCESS\n' \
                 + ' '*11 + 'CONTINUE.\n'
        self.cobolFile.writelines(templine)

    def createmainend(self):
        templine = ' '*6 + '*' + '-'*63 + '*\n' \
                 + ' '*6 + '*       THE END OF MAIN                                         *\n' \
                 + ' '*6 + '*' + '-'*63 + '*\n' \
                 + ' '*7 + '000-MAIN-END.\n'
        for file in self.files:
            templine = templine + ' '*11 + 'CLOSE %s\n' %file
        templine = templine +'\n\n'
        for varname in self.varlist:
            if 'COUNT' in varname:
                templine = templine + ' '*11 + 'DISPLAY \' %s = \'' %varname + ' %s' %varname + '\n'

        templine = templine + ' '*11 + 'IF WARNING-COUNT > 0\n' \
                 + ' '*14 + 'DISPLAY \' WARNING-COUNT = \' WARNING-COUNT\n' \
                 + ' '*14 + 'IF RETURN-COUND = 0\n' \
                 + ' '*17 + 'MOVE 1 TO RETURN-CODE\n' \
                 + ' '*14 + 'END-IF\n' \
                 + ' '*11 + 'END-IF\n' \
                 + ' '*11 + 'STOP RUN.\n'
        self.cobolFile.writelines(templine)

    def createinitialize(self):
        templine = ' '*6 + '*---------------------------------------------------------------*\n' \
                 + ' '*7 + 'INITIALIZ-WORKING-STORAGE.\n'
        for varname in self.varlist:
            if 'COUNT' in varname:
                templine = templine + ' '*11 + 'MOVE 0' +' '*17 + 'TO %s' %varname + '\n'
            elif 'END-OF' in varname:
                templine = templine + ' '*11 + 'MOVE \'F\'' + ' '*15 + 'TO %s' %varname + '\n'
        for file in self.files:
            templine = templine + ' '*11 + 'CLOSE %s' %file + '\n'
        templine = templine + ' '*11 + 'CONTINUE.\n'
        self.cobolFile.writelines(templine)

    def createcurfetch(self):
        for table in self.tables:
            if self.tables[table][1].upper() == 'CURSOR':
                templine = ' '*6 + '*---------------------------------------------------------------*\n'
                templine = templine + ' '*7 + 'MLX-FETCH-%s-PROCESS.' %table + '\n'
                lines = self.generatefetch(table)
                templine = templine + lines
                templine = templine + ' '*11 +'END-EXEC\n'
                sqlline = self.createsqlcodedeal(table,'FETCH-%s-COUNT' %table,'FETCH')
                templine = templine + sqlline
                templine = templine + ' '*11 + 'CONTINUE.\n'
                self.cobolFile.writelines(templine)

    def generatefetch(self,table):
        templine = ' '*11 + 'EXEC SQL FETCH CSR-%s' %table + '\n'
        templine = templine + ' '*21 + 'INTO\n'
        cpyfile = open(self.tables[table][2],'r')
        cpylines = cpyfile.readlines()
        for cpyline in cpylines:
            if 'NOT NULL' in cpyline and ',' in cpyline[cpyline.index('NOT NULL'):]:
                cpyvar = cpyline[13:].split()[0]
                l = ' '*27 + ':%s-' %table + cpyvar + ' '*10
                lenth = len(l)
                l = l + ' '*(53-lenth) + ','
                templine = templine + l + '\n'
            elif 'NOT NULL' in cpyline and ',' not in cpyline[cpyline.index('NOT NULL'):]:
                cpyvar = ' '*27 + ':%s-' %table  +cpyline[13:].split()[0]
                templine = templine + cpyvar + '\n'
        cpyfile.close()
        return templine

    def createselect(self):
        for table in self.tables:
            if self.tables[table][1].upper() == 'SELECT':
                templine = '      *---------------------------------------------------------------*\n' \
                         + ' '*7 + 'MLX-SELECT-%s' %table + '-PROCESS.\n'
                line = self.generateselect(table)
                templine = templine + line[:-2] + '\n'
                templine = templine + ' '*22 + 'FROM %s\n' %table
                templine = templine + ' '*21 + 'WHERE\n'
                templine = templine + ' '*11 + 'END-EXEC\n'
                sqlline = self.createsqlcodedeal(table,'SELECT-%s-COUNT' %table,'SELECT')
                templine = templine + sqlline
                templine = templine + ' '*11 + 'CONTINUE.\n'
                self.cobolFile.writelines(templine)



    def generateselect(self,table):
        templine = ' '*11 + 'EXEC SQL SELECT \n'
        cpyfile = open(self.tables[table][2],'r')
        cpylines = cpyfile.readlines()
        templist = []
        for cpyline in cpylines:
            if 'NOT NULL' in cpyline and ',' in cpyline[cpyline.index('NOT NULL'):]:
                cpyvar = cpyline[13:].split()[0]
                l = ' '*27 + cpyvar + ' '*10
                lenth = len(l)
                l = l + ' '*(53-lenth) + ','
                templine = templine + l + '\n'
                templist.append(cpyvar)
            elif 'NOT NULL' in cpyline and ',' not in cpyline[cpyline.index('NOT NULL'):]:
                cpyvar = ' '*27 + cpyline[13:].split()[0]
                templine = templine + cpyvar + '\n'
                templine = templine + ' '*22 + 'INTO\n'
                templist.append(cpyline[13:].split()[0])

        for varname in templist:
            l = ' '*27 + ':%s' %table + '-%s' %varname + ' '*10
            lenth = len(l)
            l = l + ' '*(53-lenth) + ',\n'
            templine = templine + l

        cpyfile.close()
        return templine

    def createinsert(self):
        for table in self.tables:
            if self.tables[table][0].upper() == 'W':
                templine = '      *---------------------------------------------------------------*\n' \
                         + ' '*7 + 'MLX-INSERT-%s' %table + '-PROCESS.\n'
                line = self.generateinsert(table)
                templine = templine + line[:-2] + ' )\n'
                templine = templine + ' '*11 +'END-EXEC\n'
                sqlline = self.createsqlcodedeal(table,'INSERT-%s-COUNT' %table,'INSERT')
                templine = templine + sqlline
                templine = templine + ' '*11 + 'CONTINUE.\n'
                self.cobolFile.writelines(templine)

    def generateinsert(self, table):
        templine = ' '*11 + 'EXEC SQL INSERT INTO %s ( \n' %table
        cpyfile = open(self.tables[table][2], 'r')
        cpylines = cpyfile.readlines()
        templist = []
        for cpyline in cpylines:
            if 'NOT NULL' in cpyline and ',' in cpyline[cpyline.index('NOT NULL'):]:
                cpyvar = cpyline[13:].split()[0]
                l = ' '*27 + cpyvar + ' '*10
                lenth = len(l)
                l = l + ' '*(53-lenth) + ','
                templine = templine + l + '\n'
                templist.append(cpyvar)
            elif 'NOT NULL' in cpyline and ',' not in cpyline[cpyline.index('NOT NULL'):]:
                cpyvar = ' '*27 + cpyline[13:].split()[0]
                templine = templine + cpyvar + '\n'
                templine = templine + ' '*22 + 'VALUES (\n'
                templist.append(cpyline[13:].split()[0])

        for varname in templist:
            l = ' '*27 + ':%s' %table + '-%s' %varname + ' '*10
            lenth = len(l)
            l = l + ' '*(53-lenth) + ',\n'
            templine = templine + l

        cpyfile.close()
        return templine

    def createread(self):
        for file in self.files:
            if self.files[file][0].upper() == 'R':
                templine = '      *---------------------------------------------------------------*\n' \
                         + ' '*7 + 'MLX-READ-%s' %file + '-PROCESS.\n'
                line = self.generateread(file)
                if line != '':
                   templine = templine + line
                   self.cobolFile.writelines(templine)

    def generateread(self, file):
        templine = ''
        cpyfile = open(self.files[file][2], 'r')
        cpylines = cpyfile.readlines()
        templist = []
        for cpyline in cpylines:
            if '01 ' in cpyline and 'PIC' not in cpyline and '*' not in cpyline:
                tempvar  = cpyline.split()[1][:-1]
                templine = ' '*11 + 'MOVE \'READ %s\'             TO M-ACTION\n' %file
                templine = templine + ' '*11 + 'READ %s' %file  + ' NEXT RECORD\n'
                templine = templine + ' '*11 + 'AT END\n'
                templine = templine + ' '*14 + 'MOVE \'T\'                TO END-OF-%s\n\n' %file
                templine = templine + ' '*11 + 'NOT AT END\n\n'
                templine = templine + ' '*14 + 'PERFORM FIEL-ERRCHK\n'
                templine = templine + ' '*14 + 'ADD 1              TO READ-%s-COUNT\n' %file
                templine = templine + ' '*11 + 'END-READ\n'
                templine = templine + ' '*11 + 'CONTINUE.\n'
                break
        return templine

    def createwrite(self):
        for file in self.files:
            if self.files[file][0].upper() == 'W':
                templine = '      *---------------------------------------------------------------*\n' \
                         + ' '*7 + 'MLX-WRITE-%s' %file + '-PROCESS.\n'
                line = self.generatewrite(file)
                if line != '':
                   templine = templine + line
                   self.cobolFile.writelines(templine)

    def generatewrite(self, file):
        templine = ''
        cpyfile = open(self.files[file][2], 'r')
        cpylines = cpyfile.readlines()
        templist = []
        tempfilerec = ''
        for cpyline in cpylines:
            if 'PIC' in cpyline and '*' not in cpyline:
                tempvar  = cpyline[6:].split()[1]
                templine =  templine + ' '*11 + 'MOVE      TO %s\n' %tempvar

            if '01 ' in cpyline and 'PIC' not in cpyline and '*' not in cpyline:
                tempfilerec = cpyline.split()[1][:-1]
        if templine != '' and tempfilerec != '':
            templine = templine + ' '*11 + 'WRITE %s' %tempfilerec + '\n'
            templine = templine + ' '*11 + 'PERFORM FILE-ERRCHK\n'
            templine = templine + ' '*11 + 'ADD 1              TO WRITE-%s-COUNT\n' %file
            templine = templine + ' '*11 + 'CONTINUE.\n'

        return templine

    def createopncur(self):
        for table in self.tables:
            if self.tables[table][1].upper() == 'CURSOR':
                templine = '      *---------------------------------------------------------------*\n' \
                         + ' '*7 + 'OPEN-CURSOR-%s.\n' %table \
                         + ' '*11 + 'MOVE \'OPEN CSR-%s\'         TO M-ACTION\n' %table \
                         + ' '*11 + 'MOVE SPACES TO M-ACTION-KEY\n' \
                         + ' '*11 + 'EXEC SQL OPEN CSR-%s' %table + ' END-EXEC\n' \
                         + ' '*11 + 'IF SQLCODE NOT = 0\n' \
                         + ' '*14 + 'DISPLAY \' FAILD TO OPEN CSR-%s\'\n' %table \
                         + ' '*14 + 'PERFORM SQL-ERRCHK\n' \
                         + ' '*11 + 'END-IF\n' \
                         + ' '*11 + 'CONTINUE.\n'
                self.cobolFile.writelines(templine)

    def createclosecur(self):
        for table in self.tables:
            if self.tables[table][1].upper() == 'CURSOR':
                templine = '      *---------------------------------------------------------------*\n' \
                         + ' '*7 + 'CLOSE-CURSOR-%s.\n' %table \
                         + ' '*11 + 'MOVE \'CLOSE CSR-%s\'         TO M-ACTION\n' %table \
                         + ' '*11 + 'MOVE SPACES TO M-ACTION-KEY\n' \
                         + ' '*11 + 'EXEC SQL CLOSE CSR-%s' %table + ' END-EXEC\n' \
                         + ' '*11 + 'IF SQLCODE NOT = 0\n' \
                         + ' '*14 + 'DISPLAY \' FAILD TO CLOSE CURSOR %s\'\n' %table \
                         + ' '*14 + 'PERFORM SQL-ERRCHK\n' \
                         + ' '*11 + 'END-IF\n' \
                         + ' '*11 + 'CONTINUE.\n'
                self.cobolFile.writelines(templine)

    def createopnfile(self):
        i = 0
        line = ''
        templine = ''
        line = '      *---------------------------------------------------------------*\n' \
                         + ' '*7 + 'OPEN-FILE-PROCESS.\n'
        for file in self.files:

            if self.files[file][0].upper() == 'W':
               templine = templine + ' '*11 + 'MOVE \'OPEN %s ERROR\'           TO M-ACTION\n' %file \
                         + ' '*11 + 'MOVE SPACES               TO M-ACTION-KEY\n' \
                         + ' '*11 + 'OPEN OUTPUT %s\n' %file  \
                         + ' '*11 + 'PERFORM FILE-ERRCHK\n\n' \

            if self.files[file][0].upper() == 'R':
               templine = templine + ' '*11 + 'MOVE \'OPEN %s ERROR\'           TO M-ACTION\n' %file \
                         + ' '*11 + 'MOVE SPACES               TO M-ACTION-KEY\n' \
                         + ' '*11 + 'OPEN INPUT %s\n' %file \
                         + ' '*11 + 'PERFORM FILE-ERRCHK\n\n'
        if templine != '':
           templine = line + templine + ' '*11 + 'CONTINUE.\n'
        self.cobolFile.writelines(templine)

    def createsqlcodedeal(self,table,varcount,dealname):
        templine = ' '*11 + 'IF SQLCODE = 0\n' \
                 + ' '*14 + 'ADD 1                TO %s\n' %varcount \
                 + ' '*11 + 'ELSE\n' \
                 + ' '*14 + 'IF SQLCODE = 100\n' \
                 + ' '*17 + 'DISPLAY \'%s %s NOT FOUND \'\n\n' %(dealname, table) \
                 + ' '*14 + 'ELSE\n' \
                 + ' '*17 + 'DISPLAY \'%s %s ERROR\'\n' %(dealname, table) \
                 + ' '*17 + 'MOVE \'%s %s\'          TO M-ACTION\n' %(dealname, table) \
                 + ' '*17 + 'MOVE SPACES                     TO M-ACTION\n' \
                 + ' '*14 + 'END-IF\n' \
                 + ' '*11 + 'END-IF\n'
        return templine

    def createdul(self):
        templine = '      *---------------------------------------------------------------*\n' \
                 + '      *    INLUDE PUBLIC MODULE  :                                    *\n' \
                 + '      *      1.  PRO-PROCESS                                          *\n' \
                 + '      *      2.  END-PROCESS                                          *\n' \
                 + '      *      3.  ABEND-PROCESS                                        *\n' \
                 + '      *      4.  COMMIT-PROCESS                                       *\n' \
                 + '      *      5.  SIMPLE-COMMIT-PROCESS                                *\n' \
                 + '      *      6.  PROCSTAT-COMMIT-PROCESS                              *\n' \
                 + '      *      7.  SQL-ERRCHK                                           *\n' \
                 + '      *      8.  FILE-ERRCHK                                          *\n' \
                 + '      *      9.  ERROR-PRINT                                          *\n' \
                 + '      *---------------------------------------------------------------*\n'
        templine = templine + '           EXEC SQL INCLUDE PUBMODUL END-EXEC.\n' \
                + '           EXEC SQL INCLUDE PROMODUL END-EXEC.\n'
        self.cobolFile.writelines(templine)

    def closefile(self):
        self.cobolFile.close()

