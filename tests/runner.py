from ScriptTimer import Timer
import time

# Initialising object with high verbose level
st = Timer(verbose = 2)

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

# Starting a subsection without a label is possible
st.start('2.1')
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
st.show(level = 1)

# Showing logs at maximum verbose level
st.show(verbose = 3)

