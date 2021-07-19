# Start date 24/05/2021
# Convert4-5 python script
# Version 0.3 / Dated 27/05/2021 / bad coding by Michael Schipp
# Version 0.4 / Dated 06/06/2021 / added net add dns and net add syslog


import sys, getopt
#set global veriable
current_ver = '0.4'
CUE = "nv"
inputfile = ''
outputfile = 'output.txt'

def main(argv):   
   if not argv:     #check if no arg are entered
      print ('convert425.py -i <inputfile> -o <outputfile> -c')
      print ('')
      print ('Usage:')
      print ('Input file must be specificed by using -i')
      print ('If -o is not specified then dafault of output.txt is used')
      print ('Optional -c will use cl set instead of the default of nv set')
      sys.exit()    # no arg, bugging out of here
   global inputfile,outputfile,CUE  #use gloabal veriable
   try:
      opts, args = getopt.getopt(argv,"hi:o:c",["ifile=","ofile="])
   except getopt.GetoptError:
      print ('convert425.py -i <inputfile> -o <outputfile> -c')
      print ('')
      print ('Usage:')
      print ('If -o is not specified then dafault of output.txt is used')
      print ('-c will use cl set, default is to use nv set')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('convert425.py -i <inputfile> -o <outputfile> -c')
         print ('')
         print ('Usage:')
         print ('If -o is not specified then dafault of output.txt is used')
         print ('-c will use cl set, default is to use nv set')
         
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
      elif opt == '-c':
         CUE = "cl"         
  
if __name__ == "__main__":
   main(sys.argv[1:])
line_output = []
line_str = ""
temp_list = []
write_line = True
input_file = open(inputfile,'r')            # open the file for raeading only
in_data = input_file.readlines()            # read the file into a list
ouput_file = open(outputfile,'w')           # open the file for writting to 

title = '#Converted from 4.x to 4.4/5\n'    # add comment to file to say what created this file
ouput_file.write(title)

for line_data in in_data:
    line_str = line_data
    if line_str.startswith('net add bgp'):
       line_str = line_str.replace('net add bgp', CUE +' set router bgp')
    elif line_str.startswith('net add ospf'):
       line_str = line_str.replace('net add ospf', CUE +' set router ospf')
    elif line_str.startswith('net add hostname'):
       line_str = line_str.replace('net add hostname', CUE +' set platform hostname')
    elif line_str.startswith('net add syslog'): #look for syslog entry
       line_str = line_str.replace('net add syslog host',CUE + ' set service syslog')
       line_str = line_str.replace('port ','')
    elif (line_str.startswith('net add dns') and line_str.find('vrf') != -1): #look for dns with a vrf entry
       temp_list = line_str.split() #temp list to hold each word
       line_str = line_str.replace('vrf','')
       line_str = line_str.replace(temp_list[-1],'') #temp_list index -1 is the last word aka vrf name
       line_str = line_str.replace('net add dns nameserver', CUE +' set service dns vrf '+ temp_list[-1] +' server')
    elif line_str.startswith('net add dns'): # no vrf specified for dns entry
       line_str = line_str.replace('net add dns nameserver', CUE +' set service dns server')
    elif line_str.startswith('net add bond'):
       line_str = line_str.replace('net add bond', CUE +' set interface')
       line_str = line_str.replace('bond slaves', 'bond member') 
    elif line_str.startswith('net add bridge bridge ports'):
       line_str = line_str.replace('net add bridge bridge ports ', '')   
       line_str = line_str.replace('\n', '')
       temp_list = line_str.split(",")
       for word in temp_list:
           line_str = CUE + ' set interface ' + word + ' bridge domain br_default\n'
           line_output.extend(line_str)
           write_line = False
    elif line_str.startswith('net add '):
       line_str = line_str.replace('net add ', CUE +' set ')  
    if write_line:
       line_output.extend(line_str)
       #print (line_str)
    else:
       write_line = True
    
for i in line_output:                       # go thouw line by line of the input file
    ouput_file.write(i)                     # write new output file
    #print(i)                               # dump it on the screen too
input_file.close()                          # close the input file
ouput_file.close()                          # close the output file

print ('Convert NCLU to CUE script - version '+current_ver)
print('Using output type',CUE)
print ('Output file is "', outputfile)
