import time
import pandas as pd

class Node:
    def __init__(self, nid, label, full_id, set_time = True):
        self.full_id = full_id 
        self.nid = nid
        self.label = label
        if(set_time):
            self.start = time.time()
        else:
            self.start = pd.NA
        self.end = pd.NA
        self.child = {}

class Timer:
    
    
    # Constructor
    def __init__(self, verbose = 0, seq = False):
        """
        Description : 
            Constructor of the object
        
        Parameters : 
            verbose : has different levels of logging while starting/ending a subsection. It can take the following values :
                0 : No logging while start() or end() are called (DEFAULT)
                1 : Print only section names when their respective start()/end() are called
                2 : Print section names with time the section started
                3 : Print section name, its start date and start time 
        
        Example :
            from ScriptTimer import Timer
            st = Timer(verbose = 2)        
        """
        self.tree = Node(0, 'Entire Script', '0', False)
        self.seq = seq
        self.latest_section = ''
        self.incomplete_end = False
        self.raw_data = []
        self.table = pd.DataFrame()
        self.changed = False
        self.started = False
        self.verbose = verbose
    
    
    # Interface Functions
    def start(self, section = '0', label = 'Start'):
        """
        Description : 
            This function starts the script timer/any subsection of the script

        Arguments :
            * section : Single string containing numbers seperated by fullstop.
                        Represents the section of code being tested
            * label   : Name given to the section of the code. Useful in case of many/complicated sections
                        If no label is given, then a default label of '-No Label-' is given

        Examples : 
            from ScriptTimer import Timer
            st = Timer(verbose = 2)     
            # 1. start overall script timer (optional)
            timer.start()

            # 2. Typical command to start a particular section
            timer.start('1', 'Data Cleaning')

            # 3. starting a new section automatically stops the previous running section 
            # (in this case, section 1 (Data Cleaning) is ended automatically before starting section 2 ( Data Preprocessing))
            timer.start('2', 'Data Preporcessing')
        """

        seclist = self.__listview(section)
            
        if(pd.isna(self.tree.start)):
            self.tree.start = time.time()
        
        if(section == '0'):
            return
            
        if(self.latest_section != '' and self.incomplete_end and section.startswith(self.latest_section) == False and section != self.latest_section):
            self.end(self.latest_section)
        
        self.__insert_node(self.tree, seclist, label)
        self.latest_section = section
        self.incomplete_end = True
        self.changed = True
        if(self.started == False):
            self.started = True
    
    
    def end(self, section = '0'):
        """
        Description : 
            Ends a particular subsection, or even the entire timer
        Arguments : 
            * section : Single string containing numbers seperated by fullstop.
                        Represents the section of code being tested

        Examples : 
            from ScriptTimer import Timer
            timer = Timer(verbose = 2)  
            # 1. Typical command to start and end a particular section of code
            timer.start('1', 'Data Cleaning')
            #
            # your code
            # ending section 1
            timer.end('1')

            # 2. end whole timer
            timer.end()
        """

        if(section == '0'):
            if(pd.isna(self.tree.start)):
                print('Timer has not been started yet!')
                return
            if(self.incomplete_end):
                self.tree.end = self.__insert_node_endtime(self.tree, self.__listview(self.latest_section))
            else:
                self.tree.end = time.time()
            
        else:
            if(self.latest_section.startswith(section)):
                self.__insert_node_endtime(self.tree, self.__listview(self.latest_section))
            else:
                self.__insert_node_endtime(self.tree, self.__listview(section))
        self.incomplete_end = False
        self.changed = True
            

    
    def show(self, level = 1000, verbose = 0):
        """
        Description : 
            This function is used to print the various subsections and their respective time taken

        Arguments : 
            * level   : The inner levels of sections upto which time-taken must be shown
            * verbose : Levels of output to be shown. It can take the values of :
                * 0 :   
                    * Label : label of the section
                    * Time_Taken : time taken by the section
                    * And All above columns
                * 1 :   
                    * Chronology : order in which the sections were run in the script
                    * And All above columns
                * 2 :   
                    * Start_Time
                    * End_Time
                    * And All above columns
                * 3 :   
                    * Start_Date
                    * End_Date
                    * And All above columns
                * 4 :   
                    * Raw_Time : time taken by section in Epoch format
                    * Raw_Start: start time of section in Epoch format
                    * Raw_End  : end time of section in Epoch format
                    * And All above columns

        Example : 
            from ScriptTimer import Timer
            import time
            timer = Timer(verbose = 2)  
            timer.start('1', 'Data Cleaning')
            time.sleep(2)
            timer.end('1') 
            timer.show(verbose = 2)

        """
        reveal = {
            0 : ['Label', 'Time_Taken'],
            1 : ['Label', 'Time_Taken', 'Chronology'],
            2 : ['Label', 'Time_Taken', 'Chronology', 'Start_Time', 'End_Time'],
            3 : ['Label', 'Time_Taken', 'Chronology', 'Start_Date', 'Start_Time', 'End_Date', 'End_Time'],
            4 : ['Label', 'Time_Taken', 'Chronology', 'Start_Date', 'Start_Time', 'End_Date', 'End_Time', 'Raw_Time',  'Raw_Start', 'Raw_End'],
        }
        
        if(self.started == False):
            print('Timer has not started yet!')
            return
        
        if(self.changed or len(self.table) == 0):
            self.__create_table()
            
        print(self.table[self.table.Level <= level][reveal[verbose]]) 
        self.changed = False
        
    
    def reset(self, seq = False):
        """
        Description :
            Resets the timer object
        
        Arguments : NONE

        Example : 
            from ScriptTimer import Timer
            import time
            timer = Timer(verbose = 2)  
            timer.start('1', 'Data Cleaning')
            time.sleep(2)
            timer.end('1') 
            timer.show(verbose = 2)
            timer.reset()
        """
        self.__init__(seq)
    
    def get_table(self):
        """
        Description :
            Returns a table containing details of sections, time taken etc
        
        Arguments : NONE

        Example : 
            from ScriptTimer import Timer
            import pandas as pd
            import time
            timer = Timer(verbose = 2)  
            timer.start('1', 'Data Cleaning')
            time.sleep(2)
            timer.end('1') 
            timer.show(verbose = 2)
            
            # df will contain the pandas dataframe
            df = timer.get_table()
        """
        return self.table
    
    def save(self, filename = 'Timer_Logs'):
        """
        Description :
            Saves the timer dataframe into a csv file in the present working directory
            The dataframe contains information about sections, time taken, chronology etc
            If you want the csv in another directory, enter filename relative to pwd 
            or just use get_table() and obtain the dataframe. You can do whatever then
        
        Arguments : 
            * filename : name of csv file. Default file name is 'Timer_Logs'

        Example : 
            from ScriptTimer import Timer
            import time
            timer = Timer(verbose = 2)  
            timer.start('1', 'Data Cleaning')
            time.sleep(2)
            timer.end('1') 
            timer.show(verbose = 2)
            timer.save()
            # notice a csv file in your pwd
        """
        self.table.to_csv( filename + '.csv')
    
    # Background Functions
    def __insert_node(self, root, seclist, label):
        nid = seclist[0]
        if(nid<= 0):
            print('Section no.s can only start with 1! (did not start this section)')
            return
        if(len(seclist) == 1):
            if nid not in root.child.keys():
                root.child[nid] = Node(nid, label, self.__get_full_id(root.full_id, nid))
                self.__print_logs(root.child[nid])
                return
            else:
                root.child[nid].start = time.time()
                root.child[nid].child = {}
                self.__print_logs(root.child[nid])
        else:
            if(nid not in root.child.keys()):
                root.child[nid] = Node(nid, '-No Label-', self.__get_full_id(root.full_id, nid))
                self.__print_logs(root.child[nid])
            self.__insert_node(root.child[nid], seclist[1:], label)
    
    
    def __insert_node_endtime(self, root, seclist):
        nid = seclist[0]
        if(nid<= 0):
            print('There is no such section -_-')
            return 0
        if(len(seclist) == 1):
            if(nid not in root.child.keys()):
                print('There is no such section -_-')
                return 0
            root.child[nid].end = time.time()
            root.end = root.child[nid].end
            
            self.__print_logs(root.child[nid], start = False)
            
            return root.end
        else:
            if(nid not in root.child.keys()):
                print('There is no such section!!')
                return
            end = self.__insert_node_endtime(root.child[nid], seclist[1:])
            if(end!=0):
                root.end = end   
                return end
  
    def __create_table(self):
        self.raw_data = []
        self.__get_rows(self.tree)
        temp = pd.DataFrame(columns = ['Section', 'Label', 'Raw_Start', 'Raw_End', 'Level'], data = self.raw_data)
        
        temp['Chronology'] = temp.Raw_Start.rank()
        temp['Raw_Time'] = temp.Raw_End - temp.Raw_Start
        temp['Time_Taken'] = temp.Raw_Time.apply(lambda x : self.__get_time_units(x))
        temp['Start_Date'] = temp.Raw_Start.apply(lambda x : self.__get_date(x))
        temp['Start_Time'] = temp.Raw_Start.apply(lambda x : self.__get_time(x))
        temp['End_Date'] = temp.Raw_End.apply(lambda x : self.__get_date(x))
        temp['End_Time'] = temp.Raw_End.apply(lambda x : self.__get_time(x))
        temp['Time_Taken'] = temp.apply(lambda x : 'Still Running' if pd.isna(x['Raw_End']) else x['Time_Taken'], axis = 1)
        
        temp.set_index('Section', inplace = True)
        
        self.table = temp
    
    def __get_rows(self, root):
        rtime = self.__get_time_units(root.end - root.start)
        self.raw_data.append([root.full_id, root.label, root.start, root.end, len(self.__listview(root.full_id))])
        if(root.child == {}):
            return
        else:
            keys = list(root.child.keys())
            keys.sort()
            for i in keys:
                self.__get_rows(root.child[i])

    
    def __get_time_units(self, n):
        if(n < 60):
            return str(round(n, 4))+ (' Sec' if(n == 1) else ' Secs')
        n1 = n/60
        if(n1 < 60):
            return str(round(n1, 4))+ (' Min' if n1 == 1 else ' Mins')
        n2 = n1/60
        if(n2 < 24):
            return str(round(n2, 4))+ (' Hr' if n2 == 1 else ' Hrs')
        n3 = n2/24
        return str(round(n3, 4))+ (' Day' if n3 == 1 else ' Days')
    
    
    def __get_full_id(self, prev_id, nid):
        if(prev_id == '0'):
            return str(nid)
        return prev_id + '.' + str(nid)
    
    
    def __listview(self, section):
        return [int(i) for i in section.split('.')]
    
    def __get_date(self, epoch):
        if(pd.isna(epoch)):
            return pd.NA
        temp = time.localtime(epoch)
        return '{:02d}-{:02d}-{:02d}'.format(temp.tm_mday, temp.tm_mon, temp.tm_year)
        
    def __get_time(self, epoch):
        if(pd.isna(epoch)):
            return pd.NA
        temp = time.localtime(epoch)
        return '{:02d}:{:02d}:{:02d}'.format(temp.tm_hour, temp.tm_min, temp.tm_sec)
        
    def __print_logs(self, node, start = True):
        if(self.verbose == 0):
            return
        
        prefix = 'Started : ' if start else 'Ended   : '
        pt = node.start if start else node.end
        if(self.verbose == 1):
            print(prefix + node.full_id + ' ' +  node.label)
        elif(self.verbose == 2):
            print(prefix + node.full_id + '\t ' +  node.label + '\t at ' + self.__get_time(pt))
        else:
            print(prefix + node.full_id + '\t ' +  node.label + '\t at ' + self.__get_date(pt) + ' ' + self.__get_time(pt))
        