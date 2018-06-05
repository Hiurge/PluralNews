import re

txt='Niezalezna.pl - 3 dni temu '

#re1='(Niezalezna\\.pl)'	# Fully Qualified Domain Name 1

rg = re.compile(txt,re.IGNORECASE|re.DOTALL)
m = rg.search(txt)
if m:
    fqdn1=m.group(1)
    print ("("+fqdn1+")"+"\n")