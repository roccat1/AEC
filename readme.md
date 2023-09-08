# AEC
- Afers Exteriors Capitalitzats : https://github.com/roccat1/AEC
- Download: https://github.com/roccat1/AEC/releases/

![game_view_v0 4](https://github.com/roccat1/AEC/assets/58339860/b0f4b05a-e18f-4aa0-9db8-038d8df9fd87)

# Funcionament

Tens una poblacio, un ets tu i no consumeixes res, els altres consumeixen recursos/s. Per tal de generar recursos basics (wood, food, stone) has de millorar els edificis i posar persones a treballar-hi

# Versions
- v0.0.X - Alpha
- v0.X   - Beta
- dX     - Unbalanced release
- vX     - Balanced release
- vX_d   - In development
______________________________________
- vX.x.x - base change
- vx.X.x - New mechanics/expansion/major change
- vx.x.X - minor changes/bug fix
______________________________________
change version.json, foto amb downmenu!!!!!!!

# To do (Not released)
## NOW
- [ ] balance
- [ ] Repassar menus
- [ ] Cost adding sells at internal market
- [x] info menu text
- [x] Save file (pickle, game i models)
- [x] Tots menus tanquen en tornar a clickar
- [x] Girar +- internal market
- [x] Font en els fitxers del joc
- [x] Calcular delta en pausa
## Futur
- [ ] Si canvia funcionament edifici o algo a la info!!!!!
- [ ] prestecs
- [ ] edificis refinadors
- [ ] Traduccions
    - [ ] Accents
- [ ] Log file
- [ ] Menu pausa amb config
    - [x] config.json
- [ ] llistes d'edificis no generadors, materials generats, ...
## Detalls
- [ ] produccio/edifici/segon en info
- [ ] Repassar menus

# Chuleta github
git status

git fetch  //comprovar agafar de remot
git checkout
git pull

git add .
git commit <-m msg>
git push

https://bluuweb.github.io/tutorial-github/

# Culeta pickle
with open('save.pkl', 'rb') as f:
    game = pickle.load(f)

with open('save.pkl','wb') as f:
    pickle.dump(game, f)
