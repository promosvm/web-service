docker exec -it <name_conteiner> bash                                 #войитй в контейнре
docker ps                                                             #все запущенные контейнеры
docker compose volume  loc/cont                                       #связь контейнра с машиной
workdir в dockerfile                                                  #рабочая дерртиктория 
docker exec -it flask_hello_flask_1 python train_model.py             #запуск скприта в контейнере

curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"flower":"1,2,3,4"}' \
  http://localhost:5000/iris_post