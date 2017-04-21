import re
from urllib2 import urlopen

#Clase pokemon para almacenar el numero del Pokemon introducido, nombre y la tabla de efectividad de ataques contra el
class Pokemon:
    def __init__(self, number, url, name, table):
        self.pokedex_no = number
        self.url_serebii = url
        self.poke_name = name
        self.weak_table = table





#Funcion que valida, primero, si el dato introducido es un numero y no una letra, y en caso de serlo hace una segunda validacion para ver si es un numero entre el 1 y el 802
def validPokemon():
    print "\nIntroduce el numero del Pokemon en la Pokedex Nacional:"
    no_poke = raw_input("> ")

    try:
        no_poke = int(no_poke)
        if no_poke > 802:
            print "ERROR\nNo existe un Pokemon con ese numero, intenta de nuevo."
        elif no_poke < 0:
            print "ERROR\nNo existen Pokemon negativos, intenta de nuevo."
        else:
            return no_poke
    except ValueError:
        print "ERROR\nNo puede introducirse ningun dato que no sea un numero entero"



#funcion que crea la URL de consulta en la pagina de serebii
def urlMaker(numberPokemon):
    url_serebii = "http://www.serebii.net/pokedex-sm/"

    if numberPokemon <= 9:
        newNumberPokemon = "00" + str(numberPokemon)
        url_serebii = url_serebii + newNumberPokemon + ".shtml"
        return url_serebii
    elif  numberPokemon <= 99:
        newNumberPokemon = "0" + str(numberPokemon)
        url_serebii = url_serebii + newNumberPokemon + ".shtml"
        return url_serebii
    else:
        url_serebii = url_serebii + str(numberPokemon) + ".shtml"
        return url_serebii



#Funcion que sirve para sacar el nombre del Pokemon
def namePokemon(urlPoke):
    try: #se asegura de poder abrir la pagina, si no manda un mensaje de error y termina el programa
        poke_page = urlopen(urlPoke)
        print "Pokemon encontrado"
    except:
        print "No se pudo abrir la pagina"
    page_line = poke_page.readlines() #Es recomendable utilizar readlines() cuando se habla de archivos muy grandes, se puede mover y leer mejor un archivo

    #esta parte del codigo saca el nombre del Pokemon
    for line in range (0,10):#Se leen solo las primeras 10 lines de codigo porque el nombre del pokemon lo sacamos en la parte de la etiqueta <title> y esa etiqueta siempre es una de las primeras
        if re.match("<title>", page_line[line]): #si se encuentra la linea que tiene <title>
            nombre_pkmn = re.match("<title>(\w+\S?\s?\w+\.?)\s", page_line[line])
            name_pokemon = nombre_pkmn.group(1)
    return name_pokemon



#Esta funcion extrae la informacion de los puntos de efectividad y los pone en un arreglo, ademas lleva un contador de los tipos de ataques superefectivos
def pokeWeakPoints(urlPoke):
    try: #se asegura de poder abrir la pagina, si no manda un mensaje de error y termina el programa
        poke_page = urlopen(urlPoke)
        print "Empezando a capturar datos"
    except:
        print "No se pudo abrir la pagina"
    page_line = poke_page.readlines() #Es recomendable utilizar readlines() cuando se habla de archivos muy grandes, se puede mover y leer mejor un archivo

    #esta parte sirve para sacar la linea donde se encuentra la tabla de debilidades
    damage_taken_line = 0 #contador de lineas para saber en que linea del archivo se encuenta la parte de los danos
    for line in page_line:
        if re.search(".Damage Taken", line):
            break #una vez encontrada la linea corta el ciclo for para no seguir haciendo trabajo que no es necesario
        damage_taken_line +=  1

    #esta parte de la funcion declara una lista vacia y la va llenando con los datos leidos en la pagina se Serebii
    #a su vez lleva una cuenta de cuantos tipos de ataques son superefectivos contra el Pokemon
    weak_points_array = []
    for line_damage in range (damage_taken_line, damage_taken_line + 100):
        if re.search(">\*", page_line[line_damage]):
            weak_points = re.search(">\*(\d.?\d?\d?)<", page_line[line_damage])
            weak_points_array.append(float(weak_points.group(1)))


    return weak_points_array



#Esta funcion sirve para sacar que tipos de ataque son efectivos contra un Pokemon
def superEfectiveAttacks(weakTable):
    super_efective_types = []
    for i in range(len(weakTable)):
        if weakTable[i] >= 2:
            if i == 0:
                super_efective_types.append("Normal")
            elif i == 1:
                super_efective_types.append("Fire")
            elif i == 2:
                super_efective_types.append("Water")
            elif i == 3:
                super_efective_types.append("Electric")
            elif i == 4:
                super_efective_types.append("Grass")
            elif i == 5:
                super_efective_types.append("Ice")
            elif i == 6:
                super_efective_types.append("Fight")
            elif i == 7:
                super_efective_types.append("Poison")
            elif i == 8:
                super_efective_types.append("Ground")
            elif i == 9:
                super_efective_types.append("Flying")
            elif i == 10:
                super_efective_types.append("Pyschic")
            elif i == 11:
                super_efective_types.append("Bug")
            elif i == 12:
                super_efective_types.append("Rock")
            elif i == 13:
                super_efective_types.append("Ghost")
            elif i == 14:
                super_efective_types.append("Dragon")
            elif i == 15:
                super_efective_types.append("Dark")
            elif i == 16:
                super_efective_types.append("Steel")
            elif i == 17:
                super_efective_types.append("Fairy")

    return super_efective_types



#En esta funcion se hace la suma de todas las tablas de debilidades del equipo Pokemon
def counterTotalWeek(list_of_pokemons):
    total_party_weak = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(len(list_of_pokemons)):
        total_party_weak = [e1 + e2 for e1, e2 in zip(total_party_weak,list_of_pokemons[i].weak_table)]

    return total_party_weak



#fucion donde se hace la suma de los puntos de debilidad (entre otras cosas)
def howWeak (dataPoke):
    total_weak = sum(dataPoke)
    return total_weak

#En esta funcion se imprime una tabla con la suma total de las debilidades de la party
def totalPrint (data_team):
    print "La tabla total de debilidades queda de la siguiente forma:"
    print "\tNormal:\t\t%.2f" % data_team[0]
    print "\tFire:\t\t%.2f" % data_team[1]
    print "\tWater:\t\t%.2f" % data_team[2]
    print "\tElectric:\t%.2f" % data_team[3]
    print "\tGrass:\t\t%.2f" % data_team[4]
    print "\tIce:\t\t%.2f" % data_team[5]
    print "\tFight:\t\t%.2f" % data_team[6]
    print "\tPoison:\t\t%.2f" % data_team[7]
    print "\tGround:\t\t%.2f" % data_team[8]
    print "\tFlying:\t\t%.2f" % data_team[9]
    print "\tPsychic:\t%.2f" % data_team[10]
    print "\tBug:\t\t%.2f" % data_team[11]
    print "\tRock:\t\t%.2f" % data_team[12]
    print "\tGhost:\t\t%.2f" % data_team[13]
    print "\tDragon:\t\t%.2f" % data_team[14]
    print "\tDark:\t\t%.2f" % data_team[15]
    print "\tSteel:\t\t%.2f" % data_team[16]
    print "\tFairy:\t\t%.2f" % data_team[17]



#Seccion principal del programa


team_list = []
counterteam = 0
team_continue = True

print "Analisis debilidades Pokemon"

while team_continue == True:
    data_number = validPokemon()
    data_url = urlMaker(data_number)
    data_name = namePokemon(data_url)
    data_weak_table = pokeWeakPoints(data_url)
    team_list.append(Pokemon(data_number, data_url, data_name, data_weak_table))
    counterteam += 1
    if counterteam < 6:
        print "Continuar? (S/N)"
        continuar = raw_input("> ")
        if continuar == 'n':
            team_continue = False
    else:
        break

for i in range(len(team_list)):
    super_efective = superEfectiveAttacks(team_list[i].weak_table)
    print "El Pokemon No. %s, %s es debil contra los ataques: " % (team_list[i].pokedex_no, team_list[i].poke_name)
    for j in range(len(super_efective)):
        print super_efective[j]


all_weak_list = counterTotalWeek(team_list)
totalPrint(all_weak_list)
