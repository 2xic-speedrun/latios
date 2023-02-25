
while true; do
    python3 -m latios.links.extractor.Service;
    python3 -m latios.links.ranker.Service;
    sleep 10;
done
