from flask import Flask

app = Flask(__name__)

#プレイヤーデータ保存用
player = {}
enemy_data = {}

enemy_types = {
    "slime": 30,
    "goblin": 60,
    "dragon": 150
}

@app.route("/create/<name>")
def create(name):
    player["name"] = name
    player["hp"] = 100
    player["level"] = 1
    player["exp"] = 0
    return f"{name} を作成しました！HPは１００です"

@app.route("/status")
def status():
    if not player:
        return "まだプレイヤーが作られていません"
    return f"{player['name']} のHPは {player['hp']}です"

import random

@app.route("/battle/<enemy>")
def battle(enemy):
    global enemy_data

    if not player:
        return "まだプレイヤーが作られていません"
    
    #敵がまだ存在しないなら作る
    if enemy not in enemy_data:
        hp = enemy_types.get(enemy, 50)
        enemy_data[enemy] = {"hp": hp}

    #プレイヤーの攻撃
    player_damage = random.randint(10, 20)
    enemy_data[enemy]["hp"] -= player_damage
    
    if enemy_data[enemy]["hp"] <= 0:
        del enemy_data[enemy]

        player["exp"] += 20

        if player["exp"] >= 100:
            player["level"] += 1
            player["exp"] = 0
            player["hp"] += 20
            return f"{enemy} を倒した！レベルアップ！現在Lv{player['level']}"
    
        return f"{enemy} を倒した！経験値 +20 (現在 {player['exp']})"
    
    #敵の攻撃
    enemy_damage = random.randint(5, 15)
    player["hp"] -= enemy_damage

    if player["hp"] <= 0:
        return f"{enemy} にやられた… ゲームオーバー"
    
    return (
        f"{enemy} に {player_damage} ダメージを与えた！"
        f"{enemy} の残り体力は {enemy_data[enemy]['hp']}。\n"
        f"{enemy} の攻撃！ {enemy_damage} ダメージを受けた！"
        f"あなたの残りHPは {player['hp']}。"
    )

if __name__ == "__main__":
    app.run(debug=True)