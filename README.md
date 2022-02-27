# Script Timer v4

This is a simple script timer class. 
It is used to time various sections of code, with minimal additional code
It has use cases such as :
* Testing which section of code is taking more time, in order to optimise time complexity 
* Logging time taken by total script and its subsections
* Keeping track of which subsection is running at the moment, within the script (for cases where scripts take minutes or more)

## Features
* Time different sections (and their subsections) of code with minimal code
* Infinite subsection levels possible
* Customisable logging
* Live log
* Starting next section automatically stops previous section
* Automatic adjustment of time unit i.e. whether it should be showed in seconds, minutes.... upto days unit

## Usage

This is a object oriented approach. This allows multiple timers to be made in the same script
First, we have to import the script and create a script timer object

```
import ScriptTimer as st
timer = st.Timer()
```

This object will be used for all timing purposes

## Script timer object functions :

### 0. Constructor( verbose = 0)

* verbose : has different levels of logging while starting/ending a subsection. It can take the following values :
    * 0 : No logging while start() or end() are called (DEFAULT)
    * 1 : Print only section names when their respective start()/end() are called
    * 2 : Print section names with time the section started
    * 3 : Print section name, its start date and start time 

### 1. start( section = '0', label = 'Start'):
This function starts the script timer/any subsection of the script

#### Arguments :
* section : Single string containing numbers seperated by fullstop.
            Represents the section of code being tested
* label   : Name given to the section of the code. Useful in case of many/complicated sections
            If no label is given, then a default label of '-No Label-' is given

#### Examples  : 
```
# 1. start overall script timer (optional)
timer.start()

# 2. Typical command to start a particular section
timer.start('1', 'Data Cleaning')

# 3. starting a new section automatically stops the previous running section 
# (in this case, section 1 (Data Cleaning) is ended automatically before starting section 2 ( Data Preprocessing))
timer.start('2', 'Data Preporcessing')
```

### 2. end( section = '0', label = 'Start'):
Ends a particular subsection, or even the entire timer
#### Arguments
* section : Single string containing numbers seperated by fullstop.
            Represents the section of code being tested

#### Examples  : 
```
# 1. Typical command to start and end a particular section of code
timer.start('1', 'Data Cleaning')
#
# your code
#
timer.end('1')


# 2. end whole timer
timer.end()
```

### 3. show( level = 1000, verbose = 0 ):
This function is used to print the various subsections and their respective time taken

#### Arguments
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

### 4. reset()
resets the whole timer

### 5. get_table()
Returns pandas dataframe representing all subsections with various attributes (described in show())

### 6. save( filename = 'Timer_logs' )
saves the timer pandas dataframe into a csv file with user-given filename in the python pwd path
 

## Example 

### Code :
```
import ScriptTimer
import time

# Initialising object with high verbose level
st = ScriptTimer.Timer(verbose = 2)

# Starting timer without any section will start the overall timer
# This is not necessary at all, but shown here for reference purposes
st.start()
time.sleep(1)

# Starting a particular section
st.start('1', 'Data Fetching')
time.sleep(1)

# Starting next section will automatically stop previous section
st.start('2', 'Data Augmentation')
time.sleep(1)

# Starting a subsection
st.start('2.1', 'Data Cleaning')
time.sleep(1)

# restarting the same section
st.start('2.1', 'Data Cleaning')
time.sleep(1)

st.start('2.2', 'Data Preprocessing')
time.sleep(1)

# Ending a section will end all its subsections as well
st.end('2')
time.sleep(1)

# Creating a subsection without creating it's parent section possible.
# For eg. Here, section 3 had not been created, but 3.1 is being started
st.start('3.1', 'Hypothesis Testing')
time.sleep(1)

# Ending the whole timer
st.end()

# Showing the logs of timer object
st.show()

# Showing logs of only top-level sections
print('\nShowing logs of only top-level sections)
st.show(level = 1)

# Showing logs at a high verbose level
print('\nShowing logs at a high verbose level)
st.show(verbose = 3)
```
### Output :
```
Started : 1	 Data Fetching	 at 16:57:00
Ended   : 1	 Data Fetching	 at 16:57:01
Started : 2	 Data Augmentation	 at 16:57:01
Started : 2.1	 Data Cleaning	 at 16:57:02
Started : 2.1	 Data Cleaning	 at 16:57:03
Ended   : 2.1	 Data Cleaning	 at 16:57:04
Started : 2.2	 Data Preprocessing	 at 16:57:04
Ended   : 2.2	 Data Preprocessing	 at 16:57:05
Started : 3	 -No Label-	 at 16:57:06
Started : 3.1	 Hypothesis Testing	 at 16:57:06
Ended   : 3.1	 Hypothesis Testing	 at 16:57:07
                      Label   Time_Taken
Section
0             Entire Script  8.0252 Secs
1             Data Fetching  1.0017 Secs
2         Data Augmentation  4.0147 Secs
2.1           Data Cleaning  1.0051 Secs
2.2      Data Preprocessing  1.0038 Secs
3                -No Label-  1.0031 Secs
3.1      Hypothesis Testing  1.0029 Secs

Showing logs of only top-level sections
                     Label   Time_Taken
Section
0            Entire Script  8.0252 Secs
1            Data Fetching  1.0017 Secs
2        Data Augmentation  4.0147 Secs
3               -No Label-  1.0031 Secs

Showing logs at a high verbose level
                      Label   Time_Taken  Chronology  Start_Date Start_Time    End_Date  End_Time
Section
0             Entire Script  8.0252 Secs         1.0  18-09-2021   16:56:59  18-09-2021  16:57:07
1             Data Fetching  1.0017 Secs         2.0  18-09-2021   16:57:00  18-09-2021  16:57:01
2         Data Augmentation  4.0147 Secs         3.0  18-09-2021   16:57:01  18-09-2021  16:57:05
2.1           Data Cleaning  1.0051 Secs         4.0  18-09-2021   16:57:03  18-09-2021  16:57:04
2.2      Data Preprocessing  1.0038 Secs         5.0  18-09-2021   16:57:04  18-09-2021  16:57:05
3                -No Label-  1.0031 Secs         6.0  18-09-2021   16:57:06  18-09-2021  16:57:07
3.1      Hypothesis Testing  1.0029 Secs         7.0  18-09-2021   16:57:06  18-09-2021  16:57:07
```