from bcolors import bcolors


"""
Check if a list of IPv4 addresses is valid

excluded addresses (invalid):

loopback:                   127.0.0.0 - 127.255.255.255
multicast:                  224.0.0.0 - 239.255.255.255
broadcast:                  255.255.255.255
link-local:                 169.254.0.0 - 169.254.255.255
reserved for future use:    240.0.0.0 - 255.255.255.254

0.0.0.0 <- non-routable meta-address used to designate an invalid,
           unknwon or non-applicable target

0.0.0.0 – 0.255.255.255 <- only valid as sourse address (scope: software)

---------------------------------------------------------
proper unicast addresses:          1.0.0.0 - 223.255.255.255
"""

while True:
    
    #Prompting for IPv4 address
    ip_addr = input('Enter IPv4 address: ')

    #Splitting the address to octets
    octets = ip_addr.split('.')

    #Checking the octets:
    if(len(octets) != 4):
        print(f'{bcolors.FAIL}Invalid IPv4 address (invalid number of octets).{bcolors.ENDC}')
    elif (1 <= int(octets[0]) <= 223) == False:
        print(f'{bcolors.FAIL}Invalid IPv4 address (not a proper unicast).{bcolors.ENDC}')
    elif (0 <= int(octets[1]) <= 255 and 0 <= int(octets[2]) <= 255 and 0 <= int(octets[3]) <= 255) == False:
        print(f'{bcolors.FAIL}Invalid IPv4 address.{bcolors.ENDC}')
    elif int(octets[0]) == 127:
        print(f'{bcolors.FAIL}Invalid IPv4 address (loopback).{bcolors.ENDC}')
    elif int(octets[0]) == 169 and int(octets[1]) == 254:
        print(f'{bcolors.FAIL}Invalid IPv4 address (link-local).{bcolors.ENDC}')
    else:
        break

#Valid subnet mask's octect values
masks = [255, 254, 252, 248, 240, 224, 192, 128, 0]

while True:

    #Prompting for IPv4 subnet mask
    subnet_mask = input('Enter a subnet mask: ')

    #Splitting the subnet mask to octets
    mask_octets = subnet_mask.split('.')

    #Checking the octets
    if(len(mask_octets) != 4):
        print(f'{bcolors.FAIL}Invalid IPv4 mask (invalid number of octets).{bcolors.ENDC}')
    elif(int(mask_octets[0]) in masks and int(mask_octets[1]) in masks and int(mask_octets[2]) in masks and int(mask_octets[3]) in masks and (int(mask_octets[0]) >= int(mask_octets[1]) >= int(mask_octets[2]) >= int(mask_octets[3]))) == False:
        print(f'{bcolors.FAIL}Invalid IPv4 mask (invalid values in octets).{bcolors.ENDC}')
    else:
        break


#Converting the mask to binary
mask_octets_binary = []

for octet in mask_octets:
    #converting octet to binary, first to int conversion is needed
    #binary number in python starts with '0b', whitch we do not need
    bin_octet = bin(int(octet)).lstrip('0b')
    #zfill method is used to optain 8 bits <- e.g if octet is '0', zfill(8) method makes it '00000000'
    mask_octets_binary.append(bin_octet.zfill(8))

bin_mask = ''.join(mask_octets_binary)

#Couting zeros and ones in the mask
num_of_zeros = bin_mask.count('0')
num_of_ones = 32 - num_of_zeros

#Calculating number of avaiable hosts
#This can't be negative value (/32 mask)
num_of_hosts = abs(2 ** num_of_zeros - 2)

#Wildcard mask
wildcard_octets = []

for octet in mask_octets:
    w_octet = 255 - int(octet)
    wildcard_octets.append(str(w_octet))

wildcard_mask = '.'.join(wildcard_octets)

#Converting IPv4 address to binary string
ip_octets_binary = []

for octet in octets:
    bin_octet = bin(int(octet)).lstrip('0b')
    ip_octets_binary.append(bin_octet.zfill(8))

bin_ip = ''.join(ip_octets_binary)

#Network address binary
bin_network_addr = bin_ip[:num_of_ones] + '0' * num_of_zeros

#Broadcast address binary
bin_broadcast_adr = bin_ip[:num_of_ones] + '1' * num_of_zeros

#Converting to decimal

network_address_octets = []
broadcast_address_octets = []

#(0, 32, 8) <- octets starting with: 0, 8, 16, 24 bits
for bit in range(0, 32, 8):
    #Network address octetes
    net_addr_octet = bin_network_addr[bit: bit + 8]
    network_address_octets.append(net_addr_octet)
    #Broadcast address octets
    broad_addr_octet = bin_broadcast_adr[bit: bit + 8]
    broadcast_address_octets.append(broad_addr_octet)

dec_net_addr_octets = []
dec_broad_addr_octets = []

for octet in network_address_octets:
    #Convertion of the octet to decimal
    dec_net_addr_octets.append(str(int(octet, 2)))  # '2' is the base

for octet in broadcast_address_octets:
    #Convertion of the octet to decimal
    dec_broad_addr_octets.append(str(int(octet, 2)))

network_address = '.'.join(dec_net_addr_octets)
broadcast_address = '.'.join(dec_broad_addr_octets)

print(f"""{bcolors.OKBLUE}RESULT:{bcolors.ENDC}
Network address:                {network_address}
Broadcast address:              {broadcast_address}
Number of hosts in the subnet:  {num_of_hosts}
Wildcard mask:                  {wildcard_mask}""")
