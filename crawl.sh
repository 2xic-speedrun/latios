#python3 -m latios.links.FeedbackFromFile --file ./feedback/good.txt --is-good true
#python3 -m latios.links.FeedbackFromFile --file ./feedback/bad.txt

while true; do
    python3 -m latios.links.extractor.Service;
    python3 -m latios.links.ranker.Service;
#    python3 -m latios.ranker.Train
    echo "Done epoch"
    sleep 128;
done
