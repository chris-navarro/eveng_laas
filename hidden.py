
platform = input("Enter the Platform to use(e.i. eos,nxos,iosl3,iosl2): ")

if platform == "eos":
    secret = '{"username":"arista","password":"eve","html5":"-1"}'

elif platform == "nxos":
    secret = '{"username":"nxos","password":"eve","html5":"-1"}'

elif platform == "iosl3":
    secret = '{"username":"iosl3","password":"eve","html5":"-1"}'

elif platform == "iosl2":
    secret = '{"username":"iosl2","password":"eve","html5":"-1"}'