#!/bin/bash
# rsyncs the folders containing original exercises into this one 
for folder in Matematiques-Grau-Multimedia/exercicis Matematiques-Bio/exercicis ORcourse/exercises
do
echo "############### rsyncing $folder ####################"
rsync -Pchav --stats ../$folder/ exercises 
done