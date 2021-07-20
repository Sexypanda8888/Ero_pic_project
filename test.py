import os 
dat_file = open('a.png', "rb") 
dat_file.seek(-2,2)
a=dat_file.read(2)
print(a[2])