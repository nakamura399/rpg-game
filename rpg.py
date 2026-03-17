import json

import random

from enemies import enemy_data, enemy_table

def save_game(player, player_x, player_y):

    save_data = {
        "player": player,
        "x": player_x,
        "y": player_y
    }
    
    with open("save.json", "w") as f:
        json.dump(save_data, f)

    print("データをセーブしました！")

def load_game():

    with open("save.json", "r") as f:
        save_data = json.load(f)

    return save_data

def draw_map(player_x, player_y):

    for y in range(len(map_data)):

        row = ""

        for x in range(len(map_data[y])):

            if x == player_x and y == player_y:
                row += "P "

            else:
                row += map_data[y][x] + " "

        print(row)

def make_status_bar(current_hp, max_hp):

    bar_length = 10
    ratio = current_hp / max_hp
    filled = int(bar_length * ratio)

    bar = "▮" * filled + "▯" * (bar_length - filled)

    return bar

def create_enemy(player_level):

    level = min(player_level, max(enemy_table.keys()))
    enemy_list = enemy_table[level]
    enemy_type =random.choice(enemy_list)

    enemy_level = random.randint(1, player_level + 1)

    data = enemy_data[enemy_type]

    enemy_hp = data["hp"] + enemy_level
    enemy_attack = data["attack"] + enemy_level
    enemy_crit_rate = data["crit"]

    return {
        "type": enemy_type, 
        "level": enemy_level,
        "max_hp": enemy_hp,
        "hp": enemy_hp,
        "attack": enemy_attack,
        "crit_rate": enemy_crit_rate
    }

def create_boss(player_level):

    boss = {
        "type": "魔王",
        "level": player_level + 3,
        "max_hp": 40 + player_level * 5,
        "hp": 40 + player_level * 5,
        "attack": 8 + player_level * 2,
        "crit_rate": 0.2
    }

    return boss

def battle(player, enemy):
    
    enemy_stunned = False

    while enemy["hp"] > 0 and player["hp"] > 0:
        print(f"\n{enemy['type']}")
        print(f"HP {make_status_bar(enemy["hp"], enemy["max_hp"])}  {enemy['hp']}/{enemy['max_hp']}")

        print("あなた")
        print(f"HP {make_status_bar(player["hp"], player["max_hp"])}  {player['hp']}/{player['max_hp']}")
        print(f"MP {make_status_bar(player["mp"], player["max_mp"])}  {player['mp']}/{player['max_mp']}")
        print()
        print("1. 攻撃する")
        print("2. ファイアボール（MP2)")
        print("3. サンダーストライク(MP3)")
        action = input("どうする？（１～３を選んでEnter）")
        print()

        if action == "1":

            if random.random() < 0.1 + enemy["level"] * 0.01:
                print("攻撃が回避された！")
                
            else:
                damage = 3 + player["level"]
                crit_rate = 0.1 + player["level"] * 0.1
                if random.random() < crit_rate:
                    damage *= 2 + player["level"] * 0.1
                    damage = int(damage)
                    print("会心の一撃！")

                enemy["hp"] -= damage
                print(f"{damage}のダメージを与えた！")
            
        elif action == "2":

            if player["mp"] >= 2:
                player["mp"] -= 2
                damage = 6 + player["level"] * 2
                enemy["hp"] -= damage
                print("ファイアボール！")
                print(f"{damage}のダメージ！")
        
            else:
                print("MPが足りない！")

        elif action == "3":

            if player["mp"] >= 3:
                    player["mp"] -= 3
                    damage = random.randint(4, 10) + player["level"]
                    enemy["hp"] -= damage
                    print("サンダーストライク！")
                    print(f"{damage}のダメージ！")

                    if random.random() < 0.3:
                        print(f"{enemy["type"]}をスタンさせた！")
                        enemy_stunned = True
                    else:
                        enemy_stunned = False
            else:
                print("MPが足りない！")
                enemy_stunned = False

        else:
            print("行動できなかった！")

        if enemy["hp"] > 0:

            if enemy_stunned:
                print(f"{enemy["type"]}は行動できない！")
                enemy_stunned = False
            else:
                if random.random() < 0.1 + player["level"] * 0.01:
                    print("攻撃を回避した！")

                else:
                    if enemy["type"] == "魔王" and random.random() < 0.25:
                        print("魔王のダークブレイク！")
                        enemy_damage = enemy["attack"] * 2
                    else:
                        enemy_damage =  enemy["attack"]

                    if random.random() < enemy["crit_rate"]:
                        enemy_damage *= 1.5
                        enemy_damage = int(enemy_damage)
                        print("敵の改心必殺！")

                    player["hp"] -= enemy_damage
                    print(f"{enemy_damage}のダメージを受けた！")

    if enemy["hp"] <= 0:

        print()
        print(f"{enemy["type"]}を倒した！")

        if enemy["type"] == "魔王":
            gold = random.randint(20, 40)
        else:
            gold = random.randint(3, 8)

        player["gold"] += gold
        print(f"{gold}GOLD手に入れた！")

        if enemy["type"] == "魔王":
            gained_exp = enemy["level"] * 3

        else:
            gained_exp = enemy["level"] + 2

        player["exp"] += gained_exp
        print(f"経験値を{gained_exp}ゲット！")

        if player["exp"] >= player["level"] * 3:

            player["level"] += 1
            player["exp"] = 0
            player["max_hp"] += 5
            player["max_mp"] += 3
            player["hp"] = player["max_hp"]
            player["mp"] = player["max_mp"]
            print("レベルアップ！")
            print("最大HPが５増えた！")
            print("最大MPが３増えた！")
            print("HP、MPが全回復した！")
        
    return player["hp"], player["mp"], player["exp"], player["level"], player["max_hp"], player["max_mp"]

map_data = [
    ["□","□","宝","□","□"],
    ["□","□","村","□","□"],
    ["□","□","□","□","□"],
    ["□","□","□","□","□"],
    ["□","□","□","□","□"]
 ]

def play_rpg():

    print()
    print("1. ニューゲーム")
    print("2. 続きから")

    start = input("選んでください: ")

    if start == "1":

        player_x = 2
        player_y = 2

        player = {
            "hp": 30,
            "max_hp": 30,
            "mp" : 5,
            "max_mp": 5,
            "exp": 0,
            "level": 1,
            "gold": 0,
            "potion": 0
        }

    elif start == "2":

        try:
            save_data = load_game()

            player = save_data["player"]
            player_x = save_data["x"]
            player_y = save_data["y"]
            print("セーブデータを読み込みました！")
        except:
            print("セーブデータがありません。ニューゲームを開始します。")
            start = "1"

    print()
    print("～冒険の始まり～")

    while player["hp"] > 0:
        print()
        draw_map(player_x, player_y)

        print()
        print("１:上 ２:下 ３:左 ４:右")
        move = input("どこへ行く？(１～４を選んでEnter) ").lower()

        if move == "1":
            player_y -= 1

        elif move == "2":
            player_y += 1

        elif move == "3":
            player_x -= 1

        elif move == "4":
            player_x += 1

        player_x = max(0, min(player_x, 4))
        player_y = max(0, min(player_y, 4))

        tile = map_data[player_y][player_x]

        if tile == "宝":
            print("宝箱を見つけた！")
            input("Enterで開ける。")

            gold = random.randint(5, 15)
            player["gold"] += gold

            print(f"{gold}GOLD手に入れた！")

            map_data[player_y][player_x] = "□"

        print(f"\nLv:{player['level']} "
              f"HP:{player['hp']}/{player['max_hp']} "
              f"MP:{player['mp']}/{player['max_mp']} "
              f"EXP:{player['exp']}/{player['level'] * 3} "
              f"GOLD:{player['gold']} "
              f"POTION:{player['potion']}"
              )  
        print("1.探索する")
        print("2.ショップに行く")
        print("3.宿屋で休む（セーブ）")
        print("4.ボスに挑む")
        print("5.冒険をやめる")


        choice = input("どうする？（１～５を選んでEnter）")

        if choice == "1":
                       
            enemy = create_enemy(player["level"])

            print(f"\n{enemy["type"]}が現れた！")

            battle(player, enemy)

        elif choice == "2":

            print("\nショップへようこそ！")
            print("1.ポーションを買う (10G)")
            print("2.戻る")

            shop = input("何をする？(１～２を選んでEnter) ")

            if shop == "1":

                if player["gold"] >= 10:
                    player["gold"] -= 10
                    player["potion"] += 1
                    print("ポーションを買った！")
                    print(f"GOLD:{player['gold']}")
                    print(f"POTION:{player['potion']}")

                else:
                    print("ゴールドが足りない！")
    
        elif choice == "3":
            print("\nしっかり休んだ。HP.MPが全回復した。")
            player["hp"] = player["max_hp"]
            player["mp"] = player["max_mp"]

            save_game(player, player_x, player_y)

        elif choice == "4":

            boss = create_boss(player["level"])
            print("\n魔王が現れた！")

            battle(player, boss)

        elif choice == "5":
            print("\n村に帰った。冒険終了！")
            return
        
        else :
            print("\n１～５を選んでね。")

    print("HPが０になった…ゲームオーバー。")

play_rpg()