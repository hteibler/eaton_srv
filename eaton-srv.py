#!/usr/bin/python3

# http://192.168.0.90:9999/actor?actor=345046&set=off
# http://192.168.0.95:9999/list?
# http://192.168.0.90:9999/set?set=floor&kg=off

#       192.168.0.90:9999/floor?kg=on&og=off


from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sys
import traceback

from xComfortAPI import xComfortAPI

shcurl = 'http://192.168.0.81'  # url to eaton smart home controller
username="" # username
password="" # password

# get this list from http://192.168.0.95:9999/list?
# build your groups and floors
a="""[
{
id: "xCo:2000747_u0",
name: "Schuppen ",
type: "",
zone: "hz_1",
floor: "",
group: "",
room: ""
},
{
id: "xCo:2102697_u0",
name: "Lichtband-Wohnraum ",
type: "",
zone: "hz_1",
floor: "",
group: "",
room: ""
},
{
id: "xCo:2106574_u0",
name: "KG Dusche ",
type: "",
zone: "hz_1",
floor: "",
group: "",
room: ""
},
{
id: "xCo:2568738_u0",
name: "Stecker-Aktor1 ",
type: "",
zone: "hz_1",
floor: "",
group: "",
room: ""
},
{
id: "xCo:2902174_u0",
name: "KellerMitte ",
type: "",
zone: "hz_1",
floor: "",
group: "",
room: ""
},
{
id: "xCo:2902177_u0",
name: "Wohnraum Schreibtisch ",
type: "",
zone: "hz_1",
floor: "",
group: "",
room: ""
},
{
id: "xCo:3135024_u0",
name: "Gï¿½stezimmer ",
type: "",
zone: "hz_1",
floor: "",
group: "",
room: ""
},
{
id: "xCo:333447_u0",
name: "Haustï¿½r ",
type: "",
zone: "hz_1",
floor: "",
group: "",
room: ""
},
{
id: "xCo:345046_u0",
name: "KG Ausgang ",
type: "",
zone: "hz_1",
floor: "",
group: "",
room: ""
},
{
id: "xCo:347908_u0",
name: "Licht Kï¿½che ",
type: "",
zone: "hz_1",
floor: "",
group: "",
room: ""
},
{
id: "xCo:4081332_u0",
name: "KellerStiege ",
type: "",
zone: "hz_1",
floor: "",
group: "",
room: ""
},
{
id: "xCo:5707679_u0",
name: "Vorraum (Aktor)",
type: "",
zone: "hz_1",
floor: "",
group: "",
room: ""
},
{
id: "xCo:5776305_u0",
name: "KG WC-Techik (Actuator)",
type: "",
zone: "hz_1",
floor: "",
group: "",
room: ""
},
{
id: "xCo:5778534_u0",
name: "Esstisch (Aktor)",
type: "",
zone: "hz_1",
floor: "",
group: "",
room: ""
},
{
id: "xCo:6151364_u0",
name: "Tisch-Wohnraumneu (Aktor)",
type: "",
zone: "hz_1",
floor: "",
group: "",
room: ""
},
{
id: "xCo:6151404_u0",
name: "Ofen LiRe (Aktor)",
type: "",
zone: "hz_1",
floor: "",
group: "",
room: ""
},
{
id: "xCo:6151493_u0",
name: "Ofen Mitte (Aktor)",
type: "",
zone: "hz_1",
floor: "",
group: "",
room: ""
},
{
id: "xCo:8012833_u0",
name: "Coutch-Wohnraumneu (Aktor)",
type: "",
zone: "hz_1",
floor: "",
group: "",
room: ""
},
{
id: "xCo:7981102_u0",
name: "jal_EG_WEST ",
type: "",
zone: "hz_1",
floor: "",
group: "",
room: ""
},
{
id: "xCo:8000123_u0",
name: "jal_eg_links ",
type: "",
zone: "hz_1",
floor: "",
group: "",
room: ""
},
{
id: "xCo:534822_u0",
name: "Raumcontroller ",
type: "",
zone: "hz_1",
floor: "",
group: "",
room: ""
},
{
id: "xCo:534822_w",
name: "Raumcontroller (adjustment)",
type: "",
zone: "hz_1",
floor: "",
group: "",
room: ""
},
{
id: "xCo:334048_u0",
name: "OG WZ Ost ",
type: "",
zone: "hz_2",
floor: "",
group: "",
room: ""
},
{
id: "xCo:334052_u0",
name: "OG Küche Ost ",
type: "",
zone: "hz_2",
floor: "",
group: "",
room: ""
},
{
id: "xCo:337015_u0",
name: "OG WZ Tür ",
type: "",
zone: "hz_2",
floor: "",
group: "",
room: ""
},
{
id: "xCo:5687813_u0",
name: "Eltern SZ ",
type: "",
zone: "hz_2",
floor: "",
group: "",
room: ""
},
{
id: "xCo:5695494_u0",
name: "Kinder West ",
type: "",
zone: "hz_2",
floor: "",
group: "",
room: ""
},
{
id: "xCo:7705203_u0",
name: "Kinder Süd ",
type: "",
zone: "hz_2",
floor: "",
group: "",
room: ""
},
{
id: "xCo:7705216_u0",
name: "Kinder Tür ",
type: "",
zone: "hz_2",
floor: "",
group: "",
room: ""
},
{
id: "xCo:7981001_u0",
name: "OG_WZ-SÜD-OST ",
type: "",
zone: "hz_2",
floor: "",
group: "",
room: ""
},
{
id: "xCo:7981027_u0",
name: "jal_OG-WEST ",
type: "",
zone: "hz_2",
floor: "",
group: "",
room: ""
}
]
"""

actors=json.loads(a)

def do_actor(pa):
    global my_house
    params = {x[0] : x[1] for x in [x.split("=") for x in pa[0:].split("&") ]}
    actor = params["actor"]
    #print("actor",actor,actor[0:2])
    if actor[0:3] != "xCo":
        actor = f'xCo:{params["actor"]}_u0'
    state = params["set"]
    result=my_house.switch('hz_1', actor, state)
    if result == [{}]:
        my_house._get_session_id()
        #print(my_house)
        result=my_house.switch('hz_1', actor, state)

    print(15*" ",'hz_1', actor, "S:"+state+" res:",result["status"])
    #self.wfile.write(json.dumps(result).encode('utf-8'))
    #                self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    return(result)

def do_list():
    global my_house
    try:
        result=my_house.get_zone_devices()
    except Exception as e:
        my_house._get_session_id()
        result=my_house.get_zone_devices()

    #self.wfile.write(json.dumps(result[0]).encode('utf-8'))
    #                for zone in result:
    #                    for dev in zone["devices"]:
    #                        print('"',dev["id"],'"  ',dev["id"]," ",dev["name"],sep="")#,dev["value"])

    actors=[]
    for zone in result:
        zoneId=zone["zoneId"]
        for dev in zone["devices"]:
            actor={}
            actor["id"]=dev["id"]
            actor["name"]=dev["name"]
            actor["type"]=""
            actor["zone"]=zoneId
            actor["floor"]=""
            actor["group"]=""
            actor["room"]=""
            actors.append(actor)

    return(actors)

    #return(result[0])

def do_set(pa):
    result=[]
    params = {x[0] : x[1] for x in [x.split("=") for x in pa[0:].split("&") ]}
    for f in params:
        floor = f.upper()
        set = params[f]
        for a in actors:
            if a["floor"] == floor:
                do_pa = "actor="+a["id"]+"&set="+set
                r= do_actor(do_pa)
                result.append(r)

    return result

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        global my_house
        self._set_response()
#        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))
        p=self.path
        try:
            if p.find("?") == -1:
                print("furz")
                return False
            pa = p.split("?")[1]
            uu = p.split("?")[0][1:]

            if uu == "actor":  ret= do_actor(pa)
            if uu == "list":   ret= do_list()
            if uu == "set":  ret= do_set(pa)

            if uu == "scene":
                params = {x[0] : x[1] for x in [x.split("=") for x in pa[0:].split("&") ]}
                scene = f'xCo:{params["scene"]}_u0'
                state = params["set"]
                result=my_house.switch('hz_1', actor, state)
                print(15*" ",'hz_1', actor, "S:"+state+" res:",result["status"])
                self.wfile.write(json.dumps(result).encode('utf-8'))
#                self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

            if uu == "err": x = 1/0

            self.wfile.write(json.dumps(ret).encode('utf-8'))


        except Exception as e:
            print("GET:",type(e))
            print("GET:",e.args)
            #traceback.print_exc()
            result={}
            result["status"]="error"
            result["error"]=str(e)
            if str(e)== "Zone":
                my_house = xComfortAPI(shcurl, username, password, verbose=False)

            print(15*" ","ERROR:",result)
            self.wfile.write(json.dumps(result).encode('utf-8'))

            pass


    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        #logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
        #        str(self.path), str(self.headers), post_data.decode('utf-8'))

        print (post_data.decode('utf-8'),"*****")

        #self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

    def log_message(self, format, *args):
        return


def run(server_class=HTTPServer, handler_class=S, port=9999):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd... at ',port)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print("main:",e)
    httpd.server_close()
    print('Stopping httpd...')

if __name__ == '__main__':
    from sys import argv

    my_house = xComfortAPI(shcurl, username, password, verbose=False)
    #my_house._get_session_id()

    #print (actors)

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
