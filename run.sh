docker rm -f normo-money

docker run -d  \
    --log-driver=json-file --log-opt max-size=10m --log-opt max-file=3 \
    --net=host \
    --name normo-money \
    -v /home/norman/aucobo/dockermanager:/dockermanager:Z \
    --restart=unless-stopped \
    normo/money:0.0.1


docker logs -f normo-money
